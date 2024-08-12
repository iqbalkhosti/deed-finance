
@app.route("/customer/<id>")
def load_info_by_id(id):
    
    customer = load_customer_specific_info(id)

    return render_template("jobitem.html", user=customer)