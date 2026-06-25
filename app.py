from flask import Flask, render_template, request, redirect, session
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = "secretkey"

init_db()

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()

    low_stock = conn.execute("SELECT * FROM products WHERE stock <= 5").fetchall()

    return render_template("index.html", products=products, low_stock=low_stock)

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # ✅ Fixed credentials (hardcoded login)
        if username == "mahesh" and password == "2006":
            session["user"] = username
            return redirect("/")
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# PRODUCTS PAGE
@app.route("/products")
def products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    return render_template("products.html", products=products)

# SEARCH
@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        conn = get_db()
        results = conn.execute("SELECT * FROM products WHERE name LIKE ?",
                               ('%' + keyword + '%',)).fetchall()

    return render_template("search.html", results=results)

# FILTER (LOW STOCK / HIGH STOCK)
@app.route("/filter/<type>")
def filter(type):
    conn = get_db()

    if type == "low":
        products = conn.execute("SELECT * FROM products WHERE stock <= 5").fetchall()
    else:
        products = conn.execute("SELECT * FROM products WHERE stock > 5").fetchall()

    return render_template("filter.html", products=products, type=type)

if __name__ == "__main__":
    app.run(debug=True)