from flask import Flask, render_template
from fin_database import engine
from sqlalchemy import create_engine, text

app = Flask(__name__, template_folder="templates")

def load_customer_info():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM user"))

        client_data = [row._mapping for row in result.all()]

        return client_data

@app.route("/")
def index():
    info = load_customer_info()
    return render_template("index.html", jobs=info)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
