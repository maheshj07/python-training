from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# ========== DATABASE MODELS ==========
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(200))
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    address = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Placed')
    user = db.relationship('User')
    product = db.relationship('Product')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========== ROUTES ==========
@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        password = request.form['password']
        user = User.query.filter_by(mobile=mobile).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid Mobile or Password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        address = request.form['address']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(mobile=mobile).first():
            flash('Mobile already exists', 'warning')
            return redirect(url_for('register'))
        
        new_user = User(name=name, mobile=mobile, address=address, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered Successfully! Please Login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Product.query
    if search:
        query = query.filter(Product.name.like(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
    
    products = query.all()
    categories = db.session.query(Product.category).distinct()
    return render_template('products.html', products=products, categories=categories)

@app.route('/order/<int:product_id>', methods=['POST'])
@login_required
def place_order(product_id):
    qty = int(request.form['quantity'])
    order = Order(user_id=current_user.id, product_id=product_id, quantity=qty, address=current_user.address)
    db.session.add(order)
    db.session.commit()
    flash('Order Placed Successfully!', 'success')
    return redirect(url_for('orders'))

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/ai_chat', methods=['GET', 'POST'])
@login_required
def ai_chat():

    reply = ""

    if request.method == "POST":

        question = request.form.get("question")

        products = Product.query.all()

        product_text = "\n".join(
            [f"{p.name}, Price ₹{p.price}, Category {p.category}, Stock {p.stock}" for p in products]
        )

        prompt = f"""
You are an AI shopping assistant.

Available products:

{product_text}

Customer Question:
{question}
"""

        try:
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message.content

        except Exception as e:
            reply = str(e)

    return render_template("ai_chat.html", reply=reply)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ========== FIRST RUN SETUP ==========
with app.app_context():
    db.create_all()
    # Sample Products add 
    if Product.query.count() == 0:
        sample = [
            Product(name='iPhone 15', category='Mobile', price=79999, stock=10, description='Latest Apple Phone'),
            Product(name='Samsung TV 55"', category='TV', price=55000, stock=5, description='4K Smart TV'),            Product(name='iPhone 15', category='Mobile', price=79999, stock=10, description='Latest Apple Phone'),
            Product(name='Samsung Galaxy S24', category='Mobile', price=74999, stock=12, description='Samsung flagship smartphone'),
            Product(name='OnePlus 12', category='Mobile', price=64999, stock=15, description='Premium Android smartphone'),
            Product(name='Xiaomi Redmi Note 13 Pro', category='Mobile', price=26999, stock=20, description='5G smartphone with AMOLED display'),
            Product(name='Realme Narzo 70', category='Mobile', price=18999, stock=18, description='Budget gaming smartphone'),
        ]
        db.session.add_all(sample)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)   
