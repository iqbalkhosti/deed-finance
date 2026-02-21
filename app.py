"""
Deed Finance - Subscription Points Planner
A web app that helps users understand how to use credit card points to cover subscriptions.
"""

from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, session as flask_session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
import traceback
import os

from models import Base, Client, CreditCard, Subscription, SpendingCategory, CardBonus, UserCard, UserSubscription
from forms import SignupForm, LoginForm, VerificationForm, EditProfileForm, ChangePasswordForm
from email_utils import generate_verification_code, get_code_expiry, send_verification_email, mail

# App setup
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-key")

# Email configuration
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@deed.com")

# Initialize Flask-Mail
try:
    mail.init_app(app)
except Exception as e:
    print(f"Warning: Could not initialize Flask-Mail: {e}")

# Database setup - handle Vercel serverless environment
is_vercel = os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV")
if is_vercel:
    db_path = "/tmp/clients.db"
    os.makedirs("/tmp", exist_ok=True)
else:
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clients.db")

database_url = os.environ.get("DATABASE_URL", f"sqlite:///{db_path}")
engine = create_engine(database_url, echo=False, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

# Initialize database tables
try:
    Base.metadata.create_all(engine)
    print(f"Database initialized at: {db_path}")
except Exception as e:
    print(f"Warning: Could not initialize database tables: {e}")

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
        user = session.get(Client, int(user_id))
        if user:
            session.expunge(user)
        return user


# =============================================================================
# Public Routes
# =============================================================================

@app.route("/")
def index():
    """Landing page."""
    return render_template("index.html")


@app.route("/health")
def health():
    """Health check endpoint for debugging."""
    try:
        with Session() as session:
            from sqlalchemy import text
            session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return jsonify({
        "status": "ok",
        "database": db_path,
        "vercel": bool(is_vercel),
        "db_status": db_status
    }), 200


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """User registration with email verification."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Generate verification code
        verification_code = generate_verification_code()
        code_expiry = get_code_expiry()
        
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
                is_verified=False,
                verification_code=verification_code,
                code_expires_at=code_expiry,
            )
            session.add(new_client)
            session.commit()
            
            # Get the user ID before session closes
            new_client_id = new_client.id
        
        # Send verification email
        send_verification_email(form.email.data, verification_code, form.first_name.data)
        
        # Store user ID in flask session for verification page
        flask_session['pending_verification_user_id'] = new_client_id
        
        flash("Account created! Please check your email for the verification code.", "success")
        return redirect(url_for("verify_email"))
    
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
                # Check if email is verified
                if not client.is_verified:
                    flask_session['pending_verification_user_id'] = client.id
                    flash("Please verify your email before logging in.", "warning")
                    return redirect(url_for("verify_email"))
                
                # Detach user from session so Flask-Login can use it
                session.expunge(client)
                login_user(client)
                flash("Welcome back!", "success")
                next_page = request.args.get("next")
                return redirect(next_page if next_page else url_for("dashboard"))

            if not client:
                flash("Email not found. Please sign up.", "danger")
            else:
                flash("Incorrect password. Please try again.", "danger")

    return render_template("login.html", form=form)


@app.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    """Email verification page."""
    user_id = flask_session.get('pending_verification_user_id')
    if not user_id:
        flash("No pending verification. Please sign up or log in.", "warning")
        return redirect(url_for("login"))
    
    form = VerificationForm()
    email = None
    
    with Session() as session:
        user = session.get(Client, user_id)
        if not user:
            flash("User not found. Please sign up again.", "danger")
            return redirect(url_for("signup"))
        
        if user.is_verified:
            flask_session.pop('pending_verification_user_id', None)
            flash("Email already verified. Please log in.", "info")
            return redirect(url_for("login"))
        
        email = user.email
        
        if form.validate_on_submit():
            if user.verification_code == form.code.data:
                if user.code_expires_at and datetime.utcnow() > user.code_expires_at:
                    flash("Verification code has expired. Please request a new one.", "warning")
                else:
                    user.is_verified = True
                    user.verification_code = None
                    user.code_expires_at = None
                    session.commit()
                    
                    flask_session.pop('pending_verification_user_id', None)
                    verified_user_id = user.id
                    
                    # Log in user in a new session
                    with Session() as login_session:
                        verified_user = login_session.get(Client, verified_user_id)
                        login_session.expunge(verified_user)
                        login_user(verified_user)
                    
                    flash("Email verified successfully! Welcome to Deed.", "success")
                    return redirect(url_for("dashboard"))
            else:
                flash("Invalid verification code. Please try again.", "danger")
    
    return render_template("verify_email.html", form=form, email=email)


@app.route("/resend-verification")
def resend_verification():
    """Resend verification code."""
    user_id = flask_session.get('pending_verification_user_id')
    if not user_id:
        flash("No pending verification.", "warning")
        return redirect(url_for("login"))
    
    with Session() as session:
        user = session.get(Client, user_id)
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("signup"))
        
        if user.is_verified:
            flash("Email already verified.", "info")
            return redirect(url_for("login"))
        
        new_code = generate_verification_code()
        user.verification_code = new_code
        user.code_expires_at = get_code_expiry()
        session.commit()
        
        send_verification_email(user.email, new_code, user.first_name)
        
        flash("A new verification code has been sent to your email.", "success")
    
    return redirect(url_for("verify_email"))


@app.route("/logout")
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile settings."""
    form = EditProfileForm()
    
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.surname.data = current_user.surname
        
    if form.validate_on_submit():
        with Session() as session:
            client = session.get(Client, current_user.id)
            if client:
                client.first_name = form.first_name.data
                client.surname = form.surname.data
                session.commit()
                flash("Profile updated successfully!", "success")
                return redirect(url_for("profile"))
    
    return render_template("profile.html", form=form)


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user password."""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        with Session() as session:
            client = session.get(Client, current_user.id)
            if client and bcrypt.check_password_hash(client.password, form.current_password.data):
                hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                client.password = hashed_password
                session.commit()
                flash("Password changed successfully!", "success")
                return redirect(url_for("profile"))
            else:
                flash("Incorrect current password.", "danger")
    
    return render_template("change_password.html", form=form)

# =============================================================================
# Dashboard Routes (Protected)
# =============================================================================

@app.route("/dashboard")
@login_required
def dashboard():
    """Main dashboard showing points overview and subscriptions."""
    user_id = current_user.id
    
    with Session() as session:
        # Eagerly load relationships to avoid DetachedInstanceError in templates
        user_cards = session.query(UserCard).options(
            joinedload(UserCard.credit_card)
        ).filter_by(client_id=user_id).all()
        
        user_subs = session.query(UserSubscription).options(
            joinedload(UserSubscription.subscription)
        ).filter_by(client_id=user_id, is_active=True).all()
        
        # Calculate totals
        total_points = sum(uc.current_points for uc in user_cards)
        total_monthly_cost = sum(us.subscription.monthly_cost_cad for us in user_subs)
        
        # Calculate points needed (rough estimate: $1 = 100 points for most cards)
        points_per_dollar = 100
        points_needed = int(total_monthly_cost * points_per_dollar)
        
        # Calculate coverage percentage
        coverage_percent = min(100, int((total_points / max(points_needed, 1)) * 100))
        
        # Detach all objects so they can be used in templates after session closes
        for uc in user_cards:
            session.expunge(uc)
        for us in user_subs:
            session.expunge(us)
        
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
    user_id = current_user.id
    
    with Session() as session:
        # Eagerly load credit_card relationship
        all_cards = session.query(CreditCard).filter_by(is_active=True).all()
        
        user_cards = session.query(UserCard).options(
            joinedload(UserCard.credit_card)
        ).filter_by(client_id=user_id).all()
        user_card_ids = [uc.credit_card_id for uc in user_cards]
        
        # Detach all objects for use in templates
        for card in all_cards:
            session.expunge(card)
        for uc in user_cards:
            session.expunge(uc)
        
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
    user_id = current_user.id
    
    with Session() as session:
        existing = session.query(UserCard).filter_by(
            client_id=user_id,
            credit_card_id=card_id
        ).first()
        
        if existing:
            flash("You already have this card!", "warning")
            return redirect(url_for("my_cards"))
        
        new_user_card = UserCard(
            client_id=user_id,
            credit_card_id=card_id,
            current_points=0
        )
        session.add(new_user_card)
        session.commit()
        
        card = session.get(CreditCard, card_id)
        if card:
            flash(f"Added {card.name} to your wallet!", "success")
        else:
            flash("Card added to wallet!", "success")
    
    return redirect(url_for("my_cards"))


@app.route("/remove-card/<int:user_card_id>", methods=["POST"])
@login_required
def remove_card(user_card_id):
    """Remove a credit card from user's wallet."""
    user_id = current_user.id
    
    with Session() as session:
        user_card = session.query(UserCard).options(
            joinedload(UserCard.credit_card)
        ).filter_by(
            id=user_card_id,
            client_id=user_id
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
    user_id = current_user.id
    
    with Session() as session:
        user_card = session.query(UserCard).filter_by(
            id=user_card_id,
            client_id=user_id
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
    user_id = current_user.id
    
    with Session() as session:
        all_subs = session.query(Subscription).filter_by(is_active=True).all()
        
        user_subs = session.query(UserSubscription).options(
            joinedload(UserSubscription.subscription)
        ).filter_by(client_id=user_id).all()
        user_sub_ids = [us.subscription_id for us in user_subs]
        
        # Detach all objects for use in templates
        for sub in all_subs:
            session.expunge(sub)
        for us in user_subs:
            session.expunge(us)
        
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
    user_id = current_user.id
    
    with Session() as session:
        existing = session.query(UserSubscription).filter_by(
            client_id=user_id,
            subscription_id=sub_id
        ).first()
        
        if existing:
            flash("You're already tracking this subscription!", "warning")
            return redirect(url_for("my_subscriptions"))
        
        new_user_sub = UserSubscription(
            client_id=user_id,
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
    user_id = current_user.id
    
    with Session() as session:
        user_sub = session.query(UserSubscription).options(
            joinedload(UserSubscription.subscription)
        ).filter_by(
            id=user_sub_id,
            client_id=user_id
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
    user_id = current_user.id
    
    with Session() as session:
        user_cards = session.query(UserCard).options(
            joinedload(UserCard.credit_card)
        ).filter_by(client_id=user_id).all()
        
        categories = session.query(SpendingCategory).all()
        
        user_subs = session.query(UserSubscription).options(
            joinedload(UserSubscription.subscription)
        ).filter_by(client_id=user_id, is_active=True).all()
        
        # Detach all objects for use in templates
        for uc in user_cards:
            session.expunge(uc)
        for cat in categories:
            session.expunge(cat)
        for us in user_subs:
            session.expunge(us)
        
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
    
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
        
    spending = data.get("spending", {})
    user_id = current_user.id
    
    with Session() as session:
        user_cards = session.query(UserCard).options(
            joinedload(UserCard.credit_card)
        ).filter_by(client_id=user_id).all()
        
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
        user_subs = session.query(UserSubscription).options(
            joinedload(UserSubscription.subscription)
        ).filter_by(client_id=user_id, is_active=True).all()
        
        coverage = []
        points_remaining = total_points
        for us in user_subs:
            sub = us.subscription
            points_needed = int(sub.monthly_cost_cad * 100)
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
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions."""
    if request.path.startswith('/api/') or request.is_json:
        return jsonify({
            "error": "Unhandled exception",
            "type": type(e).__name__,
            "message": str(e),
        }), 500
    flash(f"An error occurred: {str(e)}", "danger")
    return redirect(url_for("index"))


# =============================================================================
# Run App
# =============================================================================

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
