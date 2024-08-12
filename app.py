from flask import Flask, render_template
from fin_database import engine
from sqlalchemy import create_engine, text

app = Flask(__name__, template_folder="templates")

def load_customer_info():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM user"))

        client_data = [row._mapping for row in result.all()]

        return client_data
    
def load_customer_specific_info(id):
    
    with engine.connect() as conn:
        customer = conn.execute(text("SELECT * FROM user WHERE id = :val"), {"val": id})
        
        # customer = conn.execute(text("SELECT * FROM user WHERE id = :val"), val=id)
        
        rows= customer.all()

        rows_dict = [row._mapping for row in rows]

        if len(rows)==0:
            return None
        else:
            return rows_dict[0]

@app.route("/")
def index():
    info = load_customer_info()
    return render_template("index.html", jobs=info)

@app.route("/customer/<id>")
def load_info_by_id(id):
    
    customer = load_customer_specific_info(id)

    return render_template("jobitem.html", user=customer)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
