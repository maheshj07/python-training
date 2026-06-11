from flask import Flask, render_template

app = Flask(__name__)

shop = {
    "name": "Mahesh Super Store",
    "address": "Bus Stop, Hingoli, Maharashtra",
    "contact": "9307199102",
    "email": "jabademahesh2006@gmail.com"
}

products = [
    {
        "id": 1,
        "name": "Rice",
        "price": 60,
        "stock": 120,
        "expiry": "15-01-2027",
        "details": "Premium Basmati Rice"
    },
    {
        "id": 2,
        "name": "Sugar",
        "price": 45,
        "stock": 80,
        "expiry": "10-12-2026",
        "details": "Refined White Sugar"
    },
    {
        "id": 3,
        "name": "Milk",
        "price": 30,
        "stock": 50,
        "expiry": "12-07-2026",
        "details": "Fresh Dairy Milk"
    }
]

@app.route("/")
def home():
    return render_template("home.html", shop=shop)

@app.route("/products")
def index():
    return render_template("index.html", shop=shop, products=products)

@app.route("/product/<int:id>")
def product(id):
    item = next((p for p in products if p["id"] == id), None)
    return render_template("product.html", shop=shop, product=item)

if __name__ == "__main__":
    app.run(debug=True)