from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # customer | shopkeeper
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    unit = db.Column(db.String(20), nullable=False, default='pcs')
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(30), default='Placed')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product')
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()
    if not Category.query.first():
        for c in ['Groceries', 'Dairy', 'Vegetables', 'Snacks', 'Beverages', 'Household']:
            db.session.add(Category(name=c))
        db.session.commit()
    if not Product.query.first():
        cats = {c.name: c for c in Category.query.all()}
        sample = [
            ('Rice 5kg', 'Groceries', 'bag', 450, 25, 'Premium daily use rice'),
            ('Milk 1L', 'Dairy', 'pack', 60, 50, 'Fresh milk'),
            ('Potato 1kg', 'Vegetables', 'kg', 35, 80, 'Fresh potatoes'),
            ('Tea 250g', 'Groceries', 'pack', 120, 30, 'Strong tea blend'),
            ('Soap', 'Household', 'bar', 35, 100, 'Bath soap'),
        ]
        for name, cat, unit, price, stock, desc in sample:
            db.session.add(Product(name=name, category=cats[cat], unit=unit, price=price, stock=stock, description=desc))
        db.session.commit()

@app.context_processor
def inject_user():
    return dict(current_user=User.query.get(session['user_id']) if session.get('user_id') else None)

def login_required():
    if not session.get('user_id'):
        flash('Please login first.', 'warning')
        return False
    return True

@app.route('/')
def home():
    products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_orders = Order.query.count()
    return render_template('home.html', products=products, total_products=total_products, total_categories=total_categories, total_orders=total_orders)

@app.route('/products')
def products():
    q = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    query = Product.query
    if q:
        query = query.filter(or_(Product.name.ilike(f'%{q}%'), Product.description.ilike(f'%{q}%')))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    products = query.order_by(Product.name.asc()).all()
    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template('products.html', products=products, categories=categories)

@app.route('/order', methods=['GET', 'POST'])
def order_page():
    if not login_required():
        return redirect(url_for('login'))
    products = Product.query.order_by(Product.name.asc()).all()
    if request.method == 'POST':
        product_id = request.form.get('product_id', type=int)
        qty = request.form.get('qty', type=int, default=1)
        product = Product.query.get_or_404(product_id)
        if qty <= 0 or qty > product.stock:
            flash('Invalid quantity.', 'danger')
            return redirect(url_for('order_page'))
        order = Order(user_id=session['user_id'], total=product.price * qty)
        db.session.add(order)
        db.session.flush()
        db.session.add(OrderItem(order_id=order.id, product_id=product.id, qty=qty, price=product.price))
        product.stock -= qty
        db.session.commit()
        flash('Order placed successfully.', 'success')
        return redirect(url_for('orders'))
    return render_template('order.html', products=products)

@app.route('/orders')
def orders():
    if not login_required():
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        phone = request.form.get('phone', '').strip() or None
        password = request.form['password']
        role = request.form['role']
        if role not in ['customer', 'shopkeeper']:
            flash('Invalid role.', 'danger')
            return redirect(url_for('register'))
        existing = User.query.filter_by(email=email).first()
        if existing or (phone and User.query.filter_by(phone=phone).first()):
            flash('User already exists.', 'warning')
            return redirect(url_for('register'))
        user = User(name=name, email=email, phone=phone, password_hash=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    products = Product.query.filter(Product.name.ilike(f'%{q}%')).limit(8).all() if q else []
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'stock': p.stock} for p in products])

if __name__ == '__main__':
    app.run(debug=True)