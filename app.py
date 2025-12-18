"""
Deed Leisure - Subscription Points Planner
A web app that helps users understand how to use credit card points to cover subscriptions.
"""
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Client, CreditCard, Subscription, SpendingCategory, CardBonus, UserCard, UserSubscription
from forms import SignupForm, LoginForm

# App setup
app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "my very secret key"

# Database setup
engine = create_engine("sqlite:///clients.db", echo=False)
Session = sessionmaker(bind=engine)

# Extensions
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    with Session() as session:
        return session.get(Client, int(user_id))


# =============================================================================
# Public Routes
# =============================================================================

@app.route("/")
def index():
    """Landing page."""
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        with Session() as session:
            # Check if email already exists
            existing = session.query(Client).filter_by(email=form.email.data).first()
            if existing:
                flash("Email already registered. Please log in.", "warning")
                return redirect(url_for("login"))
            
            new_client = Client(
                first_name=form.first_name.data,
                email=form.email.data,
                password=hashed_password,
                surname=form.surname.data,
            )
            session.add(new_client)
            session.commit()
            
            # Log in the new user
            session.refresh(new_client)
            login_user(new_client)

        flash("Account created successfully! Welcome to Deed.", "success")
        return redirect(url_for("dashboard"))
    
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    form = LoginForm()
    if form.validate_on_submit():
        with Session() as session:
            client = session.query(Client).filter_by(email=form.email.data).first()

            if client and bcrypt.check_password_hash(client.password, form.password.data):
                login_user(client)
                flash("Welcome back!", "success")
                next_page = request.args.get("next")
                return redirect(next_page if next_page else url_for("dashboard"))

            if not client:
                flash("Email not found. Please sign up.", "danger")
            else:
                flash("Incorrect password. Please try again.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# =============================================================================
# Dashboard Routes (Protected)
# =============================================================================

@app.route("/dashboard")
@login_required
def dashboard():
    """Main dashboard showing points overview and subscriptions."""
    with Session() as session:
        # Get user's cards with points
        user_cards = session.query(UserCard).filter_by(client_id=current_user.id).all()
        total_points = sum(uc.current_points for uc in user_cards)
        
        # Get user's subscriptions
        user_subs = session.query(UserSubscription).filter_by(
            client_id=current_user.id, 
            is_active=True
        ).all()
        
        total_monthly_cost = sum(
            us.subscription.monthly_cost_cad for us in user_subs
        )
        
        # Calculate points needed (rough estimate: $1 = 100 points for most cards)
        points_per_dollar = 100  # Average conversion
        points_needed = int(total_monthly_cost * points_per_dollar)
        
        # Calculate coverage percentage
        coverage_percent = min(100, int((total_points / max(points_needed, 1)) * 100))
        
        return render_template(
            "dashboard.html",
            user_cards=user_cards,
            user_subs=user_subs,
            total_points=total_points,
            total_monthly_cost=total_monthly_cost,
            points_needed=points_needed,
            coverage_percent=coverage_percent
        )


@app.route("/my-cards")
@login_required
def my_cards():
    """View and manage user's credit cards."""
    with Session() as session:
        # Get all available credit cards
        all_cards = session.query(CreditCard).filter_by(is_active=True).all()
        
        # Get user's cards
        user_cards = session.query(UserCard).filter_by(client_id=current_user.id).all()
        user_card_ids = [uc.credit_card_id for uc in user_cards]
        
        return render_template(
            "my_cards.html",
            all_cards=all_cards,
            user_cards=user_cards,
            user_card_ids=user_card_ids
        )


@app.route("/add-card/<int:card_id>", methods=["POST"])
@login_required
def add_card(card_id):
    """Add a credit card to user's wallet."""
    with Session() as session:
        # Check if already added
        existing = session.query(UserCard).filter_by(
            client_id=current_user.id,
            credit_card_id=card_id
        ).first()
        
        if existing:
            flash("You already have this card!", "warning")
            return redirect(url_for("my_cards"))
        
        # Add the card
        new_user_card = UserCard(
            client_id=current_user.id,
            credit_card_id=card_id,
            current_points=0
        )
        session.add(new_user_card)
        session.commit()
        
        # Get card name for flash message
        card = session.get(CreditCard, card_id)
        flash(f"Added {card.name} to your wallet!", "success")
    
    return redirect(url_for("my_cards"))


@app.route("/remove-card/<int:user_card_id>", methods=["POST"])
@login_required
def remove_card(user_card_id):
    """Remove a credit card from user's wallet."""
    with Session() as session:
        user_card = session.query(UserCard).filter_by(
            id=user_card_id,
            client_id=current_user.id
        ).first()
        
        if user_card:
            card_name = user_card.credit_card.name
            session.delete(user_card)
            session.commit()
            flash(f"Removed {card_name} from your wallet.", "info")
        else:
            flash("Card not found.", "danger")
    
    return redirect(url_for("my_cards"))


@app.route("/update-points/<int:user_card_id>", methods=["POST"])
@login_required
def update_points(user_card_id):
    """Update points balance for a user's card."""
    points = request.form.get("points", 0, type=int)
    
    with Session() as session:
        user_card = session.query(UserCard).filter_by(
            id=user_card_id,
            client_id=current_user.id
        ).first()
        
        if user_card:
            user_card.current_points = max(0, points)
            session.commit()
            flash("Points balance updated!", "success")
        else:
            flash("Card not found.", "danger")
    
    return redirect(url_for("my_cards"))


@app.route("/my-subscriptions")
@login_required
def my_subscriptions():
    """View and manage subscriptions to track."""
    with Session() as session:
        # Get all available subscriptions
        all_subs = session.query(Subscription).filter_by(is_active=True).all()
        
        # Get user's subscriptions
        user_subs = session.query(UserSubscription).filter_by(client_id=current_user.id).all()
        user_sub_ids = [us.subscription_id for us in user_subs]
        
        return render_template(
            "my_subscriptions.html",
            all_subs=all_subs,
            user_subs=user_subs,
            user_sub_ids=user_sub_ids
        )


@app.route("/add-subscription/<int:sub_id>", methods=["POST"])
@login_required
def add_subscription(sub_id):
    """Add a subscription to track."""
    with Session() as session:
        existing = session.query(UserSubscription).filter_by(
            client_id=current_user.id,
            subscription_id=sub_id
        ).first()
        
        if existing:
            flash("You're already tracking this subscription!", "warning")
            return redirect(url_for("my_subscriptions"))
        
        new_user_sub = UserSubscription(
            client_id=current_user.id,
            subscription_id=sub_id
        )
        session.add(new_user_sub)
        session.commit()
        
        sub = session.get(Subscription, sub_id)
        flash(f"Now tracking {sub.name}!", "success")
    
    return redirect(url_for("my_subscriptions"))


@app.route("/remove-subscription/<int:user_sub_id>", methods=["POST"])
@login_required
def remove_subscription(user_sub_id):
    """Remove a subscription from tracking."""
    with Session() as session:
        user_sub = session.query(UserSubscription).filter_by(
            id=user_sub_id,
            client_id=current_user.id
        ).first()
        
        if user_sub:
            sub_name = user_sub.subscription.name
            session.delete(user_sub)
            session.commit()
            flash(f"Stopped tracking {sub_name}.", "info")
        else:
            flash("Subscription not found.", "danger")
    
    return redirect(url_for("my_subscriptions"))


@app.route("/advisor")
@login_required
def advisor():
    """Smart spending advisor page."""
    with Session() as session:
        # Get user's cards
        user_cards = session.query(UserCard).filter_by(client_id=current_user.id).all()
        
        # Get spending categories
        categories = session.query(SpendingCategory).all()
        
        # Get user's subscriptions
        user_subs = session.query(UserSubscription).filter_by(
            client_id=current_user.id,
            is_active=True
        ).all()
        
        return render_template(
            "advisor.html",
            user_cards=user_cards,
            categories=categories,
            user_subs=user_subs
        )


@app.route("/calculate-points", methods=["POST"])
@login_required
def calculate_points():
    """Calculate points earned based on spending inputs."""
    data = request.get_json()
    spending = data.get("spending", {})  # {category_id: amount}
    
    with Session() as session:
        user_cards = session.query(UserCard).filter_by(client_id=current_user.id).all()
        
        results = []
        total_points = 0
        
        for category_id, amount in spending.items():
            if amount <= 0:
                continue
                
            category = session.get(SpendingCategory, int(category_id))
            if not category:
                continue
            
            best_card = None
            best_rate = 0
            best_points = 0
            
            for user_card in user_cards:
                card = user_card.credit_card
                
                # Check for bonus rate in this category
                bonus = session.query(CardBonus).filter_by(
                    credit_card_id=card.id,
                    category_id=int(category_id)
                ).first()
                
                rate = bonus.earn_rate if bonus else card.base_earn_rate
                points = int(amount * rate)
                
                if rate > best_rate:
                    best_rate = rate
                    best_card = card
                    best_points = points
            
            if best_card:
                results.append({
                    "category": category.name,
                    "amount": amount,
                    "card": best_card.name,
                    "rate": best_rate,
                    "points": best_points
                })
                total_points += best_points
        
        # Get subscriptions user can cover
        user_subs = session.query(UserSubscription).filter_by(
            client_id=current_user.id,
            is_active=True
        ).all()
        
        coverage = []
        points_remaining = total_points
        for us in user_subs:
            sub = us.subscription
            points_needed = int(sub.monthly_cost_cad * 100)  # rough estimate
            can_cover = points_remaining >= points_needed
            coverage.append({
                "name": sub.name,
                "cost": sub.monthly_cost_cad,
                "points_needed": points_needed,
                "can_cover": can_cover
            })
            if can_cover:
                points_remaining -= points_needed
        
        return jsonify({
            "results": results,
            "total_points": total_points,
            "coverage": coverage
        })


# =============================================================================
# Run App
# =============================================================================

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
