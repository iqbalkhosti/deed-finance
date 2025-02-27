from flask import Flask, render_template
from fin_database import engine
from sqlalchemy import create_engine, text

app = Flask(__name__, template_folder="templates")

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
    
@app.route("/client_login")
def client_signup():
    
    return render_template("signup.html")




if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5001, debug=True)

