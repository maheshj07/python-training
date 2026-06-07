from flask import Flask

app = Flask(__name__)

Products = [
    {"p.name": "laptop", "price": 10000, "quantity": 10},
    {"p.name": "mouse", "price": 2000, "quantity": 8},
    {"p.name": "keyboard", "price": 500, "quantity": 11},
    {"p.name": "speaker", "price": 800, "quantity": 8}
]

@app.route('/')
def home():
    html = "<h1>Shop Inventory Portal</h1>"

    for product in Products:
        html += f"<li>{product['p.name']} - {product['price']} - quantity: {product['quantity']}</li>"

    return html

if __name__ == "__main__":
    app.run(debug=True)