from flask import Flask, render_template, flash, redirect, url_for, request
from fin_database import Session, engine,Client


from sqlalchemy import create_engine, text
from flask_bcrypt import Bcrypt
from forms import SignupForm, LoginForm




app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = "my very secret key"
bcrypt = Bcrypt(app)

def load_customer_info():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Client"))

        client_data = [row._mapping for row in result.all()]

        print(client_data)

        return client_data
    
def load_customer_specific_info(id):
    
    with engine.connect() as conn:
        customer = conn.execute(text("SELECT * FROM Client  WHERE id = :val"), {"val": id})
        
        # customer = conn.execute(text("SELECT * FROM user WHERE id = :val"), val=id)
        
        rows= customer.all()

        if rows:
            return rows[0]._mapping

        else:
            return None



@app.route("/")
def index():
    info = load_customer_info()
    return render_template("index.html", jobs=info)

@app.route("/customer/<id>")
def load_info_by_id(id):
    
    customer = load_customer_specific_info(id)
    
    if not customer:
        return "Not Found" , 404
    
    return render_template("jobitem.html", user=customer)
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        with Session(bind=engine) as session:
            new_client = Client(
                first_name=form.first_name.data,
                
                email=form.email.data,
                password=hashed_password,
                surname=form.surname.data,
            )
            session.add(new_client)
            session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('index'))
    
    return render_template("signup.html", form=form)
   

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with Session(bind=engine) as session:
            client = session.query(Client).filter_by(email=form.email.data).first()

        # Case 1: user exists AND password matches
        if client and bcrypt.check_password_hash(client.password, form.password.data):
            flash("Login successful!", "success")
            return redirect(url_for('index'))

        # Case 2: email not found
        if not client:
            flash("Email not found. Please sign up.", "danger")
        # Case 3: password wrong
        else:
            flash("Incorrect password. Please try again.", "danger")

    elif request.method == "POST":
        # debug helper
        app.logger.debug("Login form errors: %s", form.errors)
        flash(f"Form errors: {form.errors}", "warning")

    return render_template("login.html", form=form)




if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5001, debug=True)

