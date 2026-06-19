from flask import Flask, render_template, request
from database import *

app = Flask(__name__)

create_tables()
insert_sample_data()

@app.route("/")
def home():
    return render_template(
        "home.html",
        products=get_products(),
        low_stock=low_stock_products(),
        suppliers=get_suppliers()
    )

@app.route("/products")
def products():
    return render_template(
        "index.html",
        products=get_products()
    )

@app.route("/search")
def search():

    query = request.args.get("query","")

    products = []

    if query:
        products = search_product(query)

    return render_template(
        "search.html",
        products=products,
        query=query
    )

@app.route("/filter")
def filter_page():

    category = request.args.get("category")

    if category:
        products = filter_products(category)
    else:
        products = get_products()

    return render_template(
        "filter.html",
        products=products
    )

if __name__ == "__main__":
    app.run(debug=True)