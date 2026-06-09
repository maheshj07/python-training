from flask import Flask, render_template, request, redirect

app = Flask(__name__)

products = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_product():

    product = {
        "name": request.form['name'],
        "price": request.form['price'],
        "quantity": request.form['quantity'],
        "expiry": request.form['expiry']
    }

    products.append(product)

    return redirect('/products')

@app.route('/products')
def products_page():
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)