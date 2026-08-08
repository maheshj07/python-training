from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_sqlalchemy import (
    SQLAlchemy
)

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import (
    secure_filename
)

from groq import (
    Groq
)

from dotenv import (
    load_dotenv
)

from datetime import (
    datetime
)

import os


# ------------------------
# LOAD ENVIRONMENT
# ------------------------

load_dotenv()


# ------------------------
# CREATE FLASK APP
# ------------------------

app = Flask(
    __name__
)


# ------------------------
# APP CONFIGURATION
# ------------------------

app.config[
    "SECRET_KEY"
] = os.getenv(
    "SECRET_KEY",
    "inventory_secret_key"
)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///database.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False


# ------------------------
# UPLOAD FOLDER
# ------------------------

app.config[
    "UPLOAD_FOLDER"
] = os.path.join(

    app.root_path,

    "static",

    "uploads"

)

os.makedirs(

    app.config[
        "UPLOAD_FOLDER"
    ],

    exist_ok=True

)


# ------------------------
# DATABASE
# ------------------------

db = SQLAlchemy(
    app
)


# ------------------------
# LOGIN MANAGER
# ------------------------

login_manager = LoginManager(
    app
)

login_manager.login_view = (
    "login"
)


# ------------------------
# GROQ CLIENT
# ------------------------

groq_client = Groq(

    api_key=os.getenv(
        "GROQ_API_KEY"
    )

)
# ------------------------
# USER MODEL
# ------------------------
class User(
    UserMixin,
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    mobile = db.Column(
        db.String(15)
    )

    address = db.Column(
        db.String(300)
    )

    pincode = db.Column(
        db.String(10)
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    profile_pic = db.Column(
        db.String(200),
        default="default.png"
    )
    is_admin = db.Column(
        db.Boolean,
          default=False
    )
    # User Orders

    orders = db.relationship(
        "Order",
        backref="user",
        lazy=True
    )



# ------------------------
# PRODUCT MODEL
# ------------------------

class Product(
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(50)
    )

    price = db.Column(
        db.Float
    )

    stock = db.Column(
        db.Integer
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(200),
        default="product.png"
    )


# ------------------------
# ORDER MODEL
# ------------------------

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    product_name = db.Column(db.String(200))

    price = db.Column(db.Float)

    quantity = db.Column(db.Integer)

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ------------------------
# USER LOADER
# ------------------------

@login_manager.user_loader
def load_user(
    user_id
):

    return User.query.get(
        int(user_id)
    )
# ------------------------
# PRODUCT SEEDER
# ------------------------

def seed_products():

    # Prevent Duplicate Entries

    if Product.query.count() > 0:
        return
    products = [

        # -----------------
        # MOBILES
        # -----------------

      Product(
            name="iPhone 15",
            category="Mobile",
            price=79999,
            stock=10,
            description="Latest Apple smartphone."
        ),
       Product(name="iPhone 15", category="Mobile", price=79999, stock=10,
            description="Latest Apple smartphone."),

    Product(name="Samsung Galaxy S25", category="Mobile", price=85999, stock=12,
            description="Premium Samsung flagship phone."),

    Product(name="OnePlus 13", category="Mobile", price=69999, stock=15,
            description="Fast and smooth Android smartphone."),

    Product(name="Realme Narzo 70", category="Mobile", price=18999, stock=18,
            description="Budget gaming smartphone."),

    Product(name="Redmi Note 14 Pro", category="Mobile", price=24999, stock=20,
            description="High-performance Redmi smartphone."),

    Product(name="Vivo V40", category="Mobile", price=32999, stock=14,
            description="Stylish camera-focused smartphone."),

    Product(name="Oppo Reno 12", category="Mobile", price=34999, stock=13,
            description="Premium design with AI camera."),

    Product(name="Google Pixel 9", category="Mobile", price=79999, stock=8,
            description="Pure Android experience."),

    Product(name="Motorola Edge 50", category="Mobile", price=29999, stock=16,
            description="Powerful performance and display."),

    Product(name="Nothing Phone 3", category="Mobile", price=42999, stock=11,
            description="Unique transparent design smartphone."),

    Product(name="MacBook Air M4", category="Laptop", price=114999, stock=8,
            description="Apple M4 powered lightweight laptop."),

    Product(name="MacBook Pro 14", category="Laptop", price=189999, stock=5,
            description="Professional Apple laptop."),

    Product(name="Dell XPS 13", category="Laptop", price=129999, stock=7,
            description="Premium ultrabook laptop."),

    Product(name="HP Pavilion 15", category="Laptop", price=69999, stock=12,
            description="Everyday productivity laptop."),

    Product(name="Lenovo IdeaPad Slim 5", category="Laptop", price=64999, stock=15,
            description="Slim and lightweight laptop."),

    Product(name="ASUS ROG Strix G16", category="Laptop", price=149999, stock=6,
            description="Gaming laptop with RTX graphics."),

    Product(name="Acer Aspire 7", category="Laptop", price=59999, stock=10,
            description="Powerful multitasking laptop."),

    Product(name="MSI Katana 15", category="Laptop", price=109999, stock=7,
            description="Gaming performance laptop."),

    Product(name="Samsung Galaxy Book4", category="Laptop", price=89999, stock=9,
            description="Premium Samsung laptop."),

    Product(name="LG Gram 16", category="Laptop", price=139999, stock=5,
            description="Ultra-light business laptop."),

    Product(name="Sony Bravia 55", category="TV", price=74999, stock=8,
            description="4K Smart Android TV."),

    Product(name="Samsung Crystal UHD 50", category="TV", price=52999, stock=10,
            description="Crystal clear UHD display."),

    Product(name="LG OLED C4", category="TV", price=129999, stock=4,
            description="Premium OLED smart television."),

    Product(name="Mi X Series 55", category="TV", price=46999, stock=14,
            description="Affordable 4K smart TV."),

    Product(name="TCL QLED 65", category="TV", price=69999, stock=6,
            description="Large screen QLED television."),

    Product(name="Boat Airdopes 181", category="Accessories", price=1499, stock=30,
            description="Wireless Bluetooth earbuds."),

    Product(name="Apple AirPods Pro", category="Accessories", price=24999, stock=10,
            description="Premium noise cancelling earbuds."),

    Product(name="Samsung Galaxy Buds 3", category="Accessories", price=9999, stock=15,
            description="Comfortable wireless earbuds."),

    Product(name="JBL Tune 760NC", category="Accessories", price=6999, stock=20,
            description="Wireless noise cancelling headphones."),

    Product(name="Sony WH-1000XM5", category="Accessories", price=29999, stock=5,
            description="Industry-leading ANC headphones."),

    Product(name="Logitech MX Master 3S", category="Accessories", price=8999, stock=12,
            description="Advanced wireless mouse."),

    Product(name="Logitech K380", category="Accessories", price=3499, stock=18,
            description="Compact Bluetooth keyboard."),

    Product(name="Boat Stone 1200", category="Accessories", price=3999, stock=22,
            description="Portable Bluetooth speaker."),

    Product(name="JBL Flip 6", category="Accessories", price=9999, stock=11,
            description="Premium portable speaker."),

    Product(name="Samsung T7 SSD 1TB", category="Accessories", price=8999, stock=13,
            description="Portable high-speed SSD."),

    Product(name="Apple Watch Series 10", category="Wearable", price=49999, stock=7,
            description="Advanced smartwatch from Apple."),

    Product(name="Samsung Galaxy Watch 7", category="Wearable", price=29999, stock=9,
            description="Feature-rich Android smartwatch."),

    Product(name="Noise ColorFit Pro 6", category="Wearable", price=3999, stock=25,
            description="Affordable fitness smartwatch."),

    Product(name="Fire-Boltt Ninja", category="Wearable", price=2499, stock=30,
            description="Budget smartwatch."),

    Product(name="Fitbit Charge 6", category="Wearable", price=14999, stock=10,
            description="Advanced fitness tracker."),

    Product(name="Canon EOS R10", category="Camera", price=89999, stock=5,
            description="Mirrorless camera for creators."),

    Product(name="Sony Alpha A6700", category="Camera", price=139999, stock=4,
            description="Professional mirrorless camera."),

    Product(name="Nikon Z50", category="Camera", price=79999, stock=6,
            description="Compact mirrorless camera."),

    Product(name="GoPro Hero 13", category="Camera", price=44999, stock=8,
            description="Action camera for adventures."),

    Product(name="DJI Osmo Pocket 3", category="Camera", price=54999, stock=7,
            description="Portable vlogging camera."),

    Product(name="PlayStation 5", category="Gaming", price=54990, stock=8,
            description="Next generation gaming console."),

    Product(name="Xbox Series X", category="Gaming", price=52999, stock=6,
            description="Powerful Microsoft gaming console."),

    Product(name="Nintendo Switch OLED", category="Gaming", price=34999, stock=9,
            description="Portable gaming console."),

    Product(name="ASUS ROG Ally", category="Gaming", price=69999, stock=5,
            description="Handheld gaming device."),

    Product(name="Steam Deck OLED", category="Gaming", price=59999, stock=5,
            description="Portable PC gaming console."),


        Product(
            name="Realme Narzo 70",
            category="Mobile",
            price=18999,
            stock=18,
            description="Budget gaming smartphone."
        ),

        Product(
            name="OnePlus Nord 5",
            category="Mobile",
            price=32999,
            stock=12,
            description="Premium mid-range phone."
        ),

        Product(
            name="Google Pixel 10",
            category="Mobile",
            price=74999,
            stock=6,
            description="Google AI smartphone."
        ),

        # -----------------
        # LAPTOPS
        # -----------------

        Product(
            name="MacBook Air M4",
            category="Laptop",
            price=109999,
            stock=5,
            description="Apple laptop with M4 chip."
        ),

        Product(
            name="Dell Inspiron 15",
            category="Laptop",
            price=65999,
            stock=9,
            description="Best for office work."
        ),

        Product(
            name="HP Pavilion",
            category="Laptop",
            price=72999,
            stock=7,
            description="Powerful performance laptop."
        ),

        Product(
            name="Lenovo IdeaPad 5",
            category="Laptop",
            price=58999,
            stock=10,
            description="Slim and lightweight."
        ),

        Product(
            name="Acer Nitro V",
            category="Laptop",
            price=76999,
            stock=6,
            description="Gaming laptop."
        ),

        # -----------------
        # SMART WATCHES
        # -----------------

        Product(
            name="Apple Watch SE",
            category="Smart Watch",
            price=29999,
            stock=7,
            description="Apple smartwatch."
        ),
        Product(
    name="Apple Watch Series 10",
    category="Smart Watch",
    price=49999,
    stock=8,
    description="Premium Apple smartwatch with health tracking."
),

Product(
    name="Samsung Galaxy Watch 7",
    category="Smart Watch",
    price=29999,
    stock=10,
    description="Advanced Android smartwatch."
),

Product(
    name="Samsung Galaxy Watch Ultra",
    category="Smart Watch",
    price=59999,
    stock=5,
    description="Rugged smartwatch for outdoor adventures."
),

Product(
    name="Noise ColorFit Pro 6",
    category="Smart Watch",
    price=3999,
    stock=25,
    description="Affordable smartwatch with fitness features."
),

Product(
    name="Fire-Boltt Ninja Call Pro",
    category="Smart Watch",
    price=2499,
    stock=30,
    description="Bluetooth calling smartwatch."
),

Product(
    name="Boat Wave Sigma",
    category="Smart Watch",
    price=2199,
    stock=35,
    description="Stylish smartwatch with long battery life."
),

Product(
    name="Amazfit GTR 4",
    category="Smart Watch",
    price=16999,
    stock=12,
    description="Premium fitness and health smartwatch."
),

Product(
    name="Fitbit Charge 6",
    category="Smart Watch",
    price=14999,
    stock=15,
    description="Advanced fitness tracker smartwatch."
),

Product(
    name="Garmin Forerunner 265",
    category="Smart Watch",
    price=42999,
    stock=6,
    description="Professional GPS smartwatch for athletes."
),

Product(
    name="Huawei Watch GT 5",
    category="Smart Watch",
    price=18999,
    stock=10,
    description="Elegant smartwatch with long battery backup."
),

Product(
    name="Realme Watch S2",
    category="Smart Watch",
    price=4999,
    stock=20,
    description="Feature-rich smartwatch for daily use."
),

Product(
    name="OnePlus Watch 3",
    category="Smart Watch",
    price=24999,
    stock=8,
    description="Premium smartwatch with AMOLED display."
),

Product(
    name="Xiaomi Watch 2 Pro",
    category="Smart Watch",
    price=22999,
    stock=9,
    description="Wear OS powered smartwatch."
),

Product(
    name="Fastrack Revoltt FS1",
    category="Smart Watch",
    price=1999,
    stock=40,
    description="Budget smartwatch with Bluetooth calling."
),

Product(
    name="Titan Smart 3",
    category="Smart Watch",
    price=4995,
    stock=18,
    description="Stylish smartwatch from Titan."
),

        Product(
            name="Samsung Galaxy Watch 8",
            category="Smart Watch",
            price=32999,
            stock=6,
            description="Premium smartwatch."
        ),

        Product(
            name="Noise ColorFit Pro",
            category="Smart Watch",
            price=4999,
            stock=20,
            description="Affordable smartwatch."
        ),

        Product(
            name="Fire-Boltt Ninja",
            category="Smart Watch",
            price=2999,
            stock=25,
            description="Bluetooth calling watch."
        ),

        # -----------------
        # HEADPHONES
        # -----------------

        Product(
            name="Boat Rockerz 550",
            category="Headphones",
            price=2499,
            stock=25,
            description="Wireless headphones."
        ),

        Product(
            name="Sony WH-1000XM5",
            category="Headphones",
            price=29999,
            stock=10,
            description="Noise cancelling headphones."
        ),

        Product(
            name="JBL Tune 760NC",
            category="Headphones",
            price=6999,
            stock=14,
            description="Wireless ANC headphones."
        ),
        Product(
    name="Sony WH-1000XM5",
    category="Headphones",
    price=29999,
    stock=8,
    description="Premium wireless noise cancelling headphones."
),

Product(
    name="Sony WH-CH720N",
    category="Headphones",
    price=9999,
    stock=15,
    description="Lightweight wireless ANC headphones."
),

Product(
    name="Apple AirPods Max",
    category="Headphones",
    price=59999,
    stock=5,
    description="Apple premium over-ear headphones."
),

Product(
    name="Beats Studio Pro",
    category="Headphones",
    price=34999,
    stock=7,
    description="Wireless headphones with active noise cancellation."
),

Product(
    name="JBL Live 770NC",
    category="Headphones",
    price=12999,
    stock=12,
    description="Smart noise cancelling wireless headphones."
),

Product(
    name="JBL Tune 720BT",
    category="Headphones",
    price=5999,
    stock=18,
    description="Wireless headphones with long battery life."
),

Product(
    name="Boat Nirvana 751 ANC",
    category="Headphones",
    price=3999,
    stock=20,
    description="Affordable ANC wireless headphones."
),

Product(
    name="Boat Rockerz 550",
    category="Headphones",
    price=2499,
    stock=25,
    description="Bluetooth headphones with deep bass."
),

Product(
    name="Skullcandy Hesh ANC",
    category="Headphones",
    price=10999,
    stock=10,
    description="Wireless ANC headphones with premium sound."
),

Product(
    name="Sennheiser Accentum",
    category="Headphones",
    price=14999,
    stock=8,
    description="High-quality wireless headphones."
),

Product(
    name="Sennheiser HD 450BT",
    category="Headphones",
    price=11999,
    stock=9,
    description="Wireless headphones with active noise cancellation."
),

Product(
    name="Bose QuietComfort",
    category="Headphones",
    price=32999,
    stock=6,
    description="World-class noise cancelling headphones."
),

Product(
    name="Bose QuietComfort Ultra",
    category="Headphones",
    price=44999,
    stock=4,
    description="Premium immersive audio headphones."
),

Product(
    name="Marshall Major V",
    category="Headphones",
    price=13999,
    stock=11,
    description="Stylish wireless headphones with iconic sound."
),

Product(
    name="Anker Soundcore Life Q30",
    category="Headphones",
    price=7999,
    stock=14,
    description="Budget-friendly ANC headphones."
),

        # -----------------
        # ACCESSORIES
        # -----------------

        Product(
            name="Apple AirPods Pro",
            category="Accessories",
            price=24999,
            stock=10,
            description="Premium wireless earbuds."
        ),

        Product(
            name="Logitech MX Master 3",
            category="Accessories",
            price=8999,
            stock=12,
            description="Wireless mouse."
        ),

        Product(
            name="Amazon Echo Dot",
            category="Accessories",
            price=4999,
            stock=15,
            description="Alexa smart speaker."
        ),

        Product(
            name="Anker Power Bank",
            category="Accessories",
            price=2499,
            stock=18,
            description="Fast charging power bank."
        ),

        Product(
            name="SanDisk SSD 1TB",
            category="Accessories",
            price=11999,
            stock=8,
            description="Portable SSD."
        ),

        # -----------------
        # TV & GAMING
        # -----------------

        Product(
            name='LG Smart TV 55"',
            category="TV",
            price=55999,
            stock=4,
            description="55-inch 4K Smart TV."
        ),

        Product(
            name="Sony Bravia 65",
            category="TV",
            price=89999,
            stock=3,
            description="65-inch Smart TV."
        ),

        Product(
            name="Sony PlayStation 6",
            category="Gaming",
            price=69999,
            stock=5,
            description="Gaming console."
        ),

        Product(
            name="Nintendo Switch 2",
            category="Gaming",
            price=45999,
            stock=5,
            description="Portable gaming console."
        ),
        Product(
    name="PlayStation 5 Slim",
    category="Gaming",
    price=54990,
    stock=8,
    description="Next-generation Sony gaming console."
),

Product(
    name="PlayStation 5 Pro",
    category="Gaming",
    price=69990,
    stock=4,
    description="High-performance PlayStation console."
),

Product(
    name="Xbox Series X",
    category="Gaming",
    price=52999,
    stock=6,
    description="Powerful Microsoft gaming console."
),

Product(
    name="Xbox Series S",
    category="Gaming",
    price=34999,
    stock=10,
    description="Compact digital gaming console."
),

Product(
    name="Nintendo Switch OLED",
    category="Gaming",
    price=34999,
    stock=8,
    description="Portable OLED gaming console."
),

Product(
    name="Nintendo Switch Lite",
    category="Gaming",
    price=19999,
    stock=12,
    description="Compact handheld gaming console."
),

Product(
    name="ASUS ROG Ally X",
    category="Gaming",
    price=79999,
    stock=5,
    description="Windows-powered handheld gaming device."
),

Product(
    name="Steam Deck OLED",
    category="Gaming",
    price=59999,
    stock=6,
    description="Portable PC gaming console."
),

Product(
    name="Lenovo Legion Go",
    category="Gaming",
    price=74999,
    stock=4,
    description="Large-screen handheld gaming device."
),

Product(
    name="Sony PlayStation Portal",
    category="Gaming",
    price=24999,
    stock=7,
    description="Remote Play handheld for PS5."
),

Product(
    name="Logitech G Cloud",
    category="Gaming",
    price=29999,
    stock=5,
    description="Cloud gaming handheld console."
),

Product(
    name="Sony DualSense Controller",
    category="Gaming",
    price=5999,
    stock=20,
    description="Wireless controller for PlayStation 5."
),

Product(
    name="Xbox Wireless Controller",
    category="Gaming",
    price=5499,
    stock=18,
    description="Official Xbox wireless controller."
),

Product(
    name="Razer Kishi V2",
    category="Gaming",
    price=8999,
    stock=10,
    description="Mobile gaming controller."
),

Product(
    name="HyperX Cloud III",
    category="Gaming",
    price=9999,
    stock=12,
    description="Gaming headset with immersive sound."
),
    ]

    db.session.add_all(
        products
    )

    db.session.commit()

    print(
        "Products Seeded Successfully!"
    )
    # ------------------------
# HOME
# ------------------------
@app.route("/")
def home():

    products = Product.query.limit(8).all()

    total_products = Product.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()

    low_stock_products = Product.query.filter(
        Product.stock < 5
    ).all()

    recent_orders = Order.query.order_by(
        Order.id.desc()
    ).limit(5).all()

    return render_template(
        "home.html",
        products=products,
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        low_stock=len(low_stock_products),
        low_stock_products=low_stock_products,
        recent_orders=recent_orders
    )
# ------------------------
# DASHBOARD
# ------------------------
@app.route("/dashboard")
@login_required
def dashboard():

    total_products = Product.query.count()

    total_users = User.query.count()

    total_orders = Order.query.count()

    low_stock = Product.query.filter(
        Product.stock < 5
    ).count()

    recent_orders = Order.query.order_by(
        Order.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        low_stock=low_stock,
        recent_orders=recent_orders
    )


# ------------------------
# REGISTER
# ------------------------

@app.route(
    "/register",
    methods=[
        "GET",
        "POST"
    ]
)
def register():

    if request.method == "POST":

        email = request.form[
            "email"
        ]

        existing_user = \
            User.query.filter_by(
                email=email
            ).first()

        if existing_user:

            flash(
                "Email already registered!",
                "danger"
            )

            return redirect(
                url_for(
                    "register"
                )
            )

        if request.form[
            "password"
        ] != request.form[
            "confirm_password"
        ]:

            flash(
                "Passwords do not match!",
                "danger"
            )

            return redirect(
                url_for(
                    "register"
                )
            )

        user = User(

            name=request.form[
                "name"
            ],

            email=email,

            mobile=request.form[
                "mobile"
            ],

            address=request.form[
                "address"
            ],

            pincode=request.form[
                "pincode"
            ],

            password=
            generate_password_hash(

                request.form[
                    "password"
                ]

            )
        )

        db.session.add(
            user
        )

        db.session.commit()

        flash(
            "Registration Successful!",
            "success"
        )

        return redirect(
            url_for(
                "login"
            )
        )

    return render_template(
        "register.html"
    )


# ------------------------
# LOGIN
# ------------------------

@app.route(
    "/login",
    methods=[
        "GET",
        "POST"
    ]
)
def login():

    if request.method == "POST":

        user = User.query.filter_by(

            email=request.form[
                "email"
            ]

        ).first()

        if user and \
            check_password_hash(

                user.password,

                request.form[
                    "password"
                ]

        ):

            login_user(
                user
            )

            flash(
                "Welcome Back!",
                "success"
            )

            return redirect(
                url_for(
                    "dashboard"
                )
            )

        flash(
            "Invalid Email or Password!",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ------------------------
# LOGOUT
# ------------------------

@app.route(
    "/logout"
)
@login_required
def logout():

    logout_user()

    flash(
        "Logged Out Successfully!",
        "info"
    )

    return redirect(
        url_for(
            "home"
        )
    )
# ------------------------
# PRODUCTS
# ------------------------
from sqlalchemy import or_

@app.route("/products")
def products():

    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "")

    query = Product.query

    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.category.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )

    pagination = query.order_by(Product.id.desc()).paginate(
        page=page,
        per_page=9,
        error_out=False
    )

    return render_template(
        "products.html",
        products=pagination.items,
        pagination=pagination,
        search=search
    )


# ------------------------
# PLACE ORDER
# ------------------------

@app.route(
    "/place_order/<int:product_id>"
)
@login_required
def place_order(
    product_id
):

    product = \
        Product.query.get_or_404(
            product_id
        )

    # Check Stock

    if product.stock <= 0:

        flash(
            "Product is Out of Stock!",
            "danger"
        )

        return redirect(
            url_for(
                "products"
            )
        )

    # Create Order

    order = Order(

        product_name=
        product.name,

        price=
        product.price,

        quantity=1,

        user_id=
        current_user.id

    )

    # Reduce Stock

    product.stock -= 1

    db.session.add(
        order
    )

    db.session.commit()

    flash(
        "Order Placed Successfully!",
        "success"
    )

    return redirect(
        url_for(
            "orders"
        )
    )


# ------------------------
# ORDERS
# ------------------------
@app.route("/order/<int:product_id>", methods=["GET", "POST"])
@login_required
def order(product_id):

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":

        quantity = int(request.form["quantity"])

        if quantity > product.stock:
            flash("Insufficient Stock!", "danger")
            return redirect(
                url_for("order", product_id=product.id)
            )

        new_order = Order(
            user_id=current_user.id,
            product_name=product.name,
            price=product.price,
            quantity=quantity,
            status="Pending"
        )

        db.session.add(new_order)

        product.stock -= quantity

        db.session.commit()

        flash("Order Placed Successfully!", "success")

        return redirect(url_for("orders"))

    return render_template(
        "order.html",
        product=product
    )
@app.route("/orders")
@login_required
def orders():

    user_orders = Order.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "orders.html",
        orders=user_orders,
        total_orders=len(user_orders),
        pending_orders=len(
            [o for o in user_orders if o.status == "Pending"]
        ),
        completed_orders=len(
            [o for o in user_orders if o.status == "Completed"]
        )
    )
@app.route("/cancel_order/<int:order_id>")
@login_required
def cancel_order(order_id):

    order = Order.query.get_or_404(order_id)
    order.status = "Cancelled"

    db.session.commit()

    flash("Order Cancelled Successfully!", "success")
    return redirect(url_for("orders"))
# ------------------------
# PROFILE
# ------------------------
@app.route("/profile")
@login_required
def profile():

    total_products = Product.query.count()

    total_orders = Order.query.filter_by(
        user_id=current_user.id
    ).count()

    total_sales = db.session.query(
        db.func.sum(Order.price * Order.quantity)
    ).filter(
        Order.user_id == current_user.id
    ).scalar() or 0

    return render_template(
        "profile.html",
        total_products=total_products,
        total_orders=total_orders,
        total_sales=total_sales
    )
@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def profile_edit():

    if request.method == "POST":

        current_user.name = request.form["name"]
        current_user.email = request.form["email"]
        current_user.mobile = request.form["mobile"]
        current_user.address = request.form["address"]
        current_user.pincode = request.form["pincode"]

        password = request.form.get("password")

        if password:
            current_user.password = generate_password_hash(password)

        # Profile Photo Upload
        file = request.files.get("profile_pic")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            current_user.profile_pic = filename

        db.session.commit()

        flash("Profile Updated Successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("profile_edit.html")



# ------------------------
# AI CHAT
# ------------------------

@app.route(
    "/ai_chat",
    methods=[
        "GET",
        "POST"
    ]
)
@login_required
def ai_chat():

    question = ""
    answer = ""

    if request.method == "POST":

        question = request.form[
            "question"
        ]

        try:

            response = \
                groq_client.chat.completions.create(

                    model=
                    "llama-3.3-70b-versatile",

                    messages=[

                        {
                            "role":
                            "system",

                            "content":

                            """
                            You are an AI Product
                            Assistant for an
                            Electronic Inventory
                            System.

                            Help users with:

                            - Product Recommendations
                            - Product Comparisons
                            - Technical Specifications
                            - Buying Suggestions
                            - Electronics Questions
                            """
                        },

                        {
                            "role":
                            "user",

                            "content":
                            question
                        }

                    ]

                )

            answer = \
                response.choices[
                    0
                ].message.content

        except Exception as e:

            answer = \
                f"Error: {e}"

    return render_template(

        "ai_chat.html",

        question=
        question,

        answer=
        answer

    )
from sqlalchemy import or_

@app.route("/search")
def search():

    query = request.args.get("q", "")

    products = Product.query.filter(

        or_(

            Product.name.ilike(f"%{query}%"),

            Product.category.ilike(f"%{query}%"),

            Product.description.ilike(f"%{query}%")

        )

    ).all()

    return render_template(

        "search.html",

        products=products,

        query=query

    )
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admin")
@login_required
def admin_panel():

    if not current_user.is_admin:
        flash("Access Denied!", "danger")
        return redirect(url_for("dashboard"))

    total_products = Product.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()

    low_stock_products = Product.query.filter(
        Product.stock < 5
    ).all()

    total_sales = 0

    orders = Order.query.all()

    for order in orders:
        total_sales += order.price * order.quantity

    recent_orders = Order.query.order_by(
        Order.id.desc()
    ).limit(10).all()

    return render_template(
        "admin.html",
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        low_stock_products=low_stock_products,
        total_sales=total_sales,
        recent_orders=recent_orders
    )
@app.route("/admin/products")
@login_required
def admin_products():

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    products = Product.query.all()

    return render_template(
        "admin_products.html",
        products=products
    )
@app.route("/admin/users")
@login_required
def admin_users():

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    users = User.query.all()

    return render_template(
        "admin_users.html",
        users=users
    )
@app.route("/admin/orders")
@login_required
def admin_orders():

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    orders = Order.query.order_by(
        Order.id.desc()
    ).all()

    return render_template(
        "admin_orders.html",
        orders=orders
    )
@app.route("/admin/delete_product/<int:id>")
@login_required
def delete_product(id):

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    flash(
        "Product Deleted Successfully",
        "success"
    )

    return redirect(
        url_for("admin_products")
    )
@app.route("/admin/order_status/<int:id>/<status>")
@login_required
def order_status(id, status):

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    order = Order.query.get_or_404(id)

    order.status = status

    db.session.commit()

    flash(
        "Order Status Updated",
        "success"
    )

    return redirect(
        url_for("admin_orders")
    )
@app.route("/admin/add_product", methods=["GET", "POST"])
@login_required
def add_product():

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        product = Product(
            name=request.form["name"],
            category=request.form["category"],
            price=float(request.form["price"]),
            stock=int(request.form["stock"]),
            description=request.form["description"]
        )

        db.session.add(product)
        db.session.commit()

        flash("Product Added Successfully", "success")

        return redirect(url_for("admin_products"))

    return render_template("add_product.html")
@app.route("/admin/edit_product/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        product.name = request.form["name"]
        product.category = request.form["category"]
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])
        product.description = request.form["description"]

        db.session.commit()

        flash(
            "Product Updated Successfully",
            "success"
        )

        return redirect(
            url_for("admin_products")
        )

    return render_template(
        "edit_product.html",
        product=product
    )
@app.route("/admin/delete_user/<int:id>")
@login_required
def delete_user(id):

    if not current_user.is_admin:
        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(id)

    if user.is_admin:
        flash("Admin Account Cannot Be Deleted", "danger")
        return redirect(url_for("admin_users"))

    db.session.delete(user)
    db.session.commit()

    flash("User Deleted Successfully", "success")

    return redirect(url_for("admin_users"))
# ------------------------
# USER LOADER
# ------------------------

@login_manager.user_loader
def load_user(
    user_id
):

    return User.query.get(
        int(user_id)
    )
def create_admin():

    admin = User.query.filter_by(
        email="admin@gmail.com"
    ).first()

    if not admin:

        admin = User(
            name="Administrator",
            email="admin@gmail.com",
            mobile="9999999999",
            address="Admin Office",
            pincode="000000",
            password=generate_password_hash("admin123"),
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin Created Successfully!")

    else:

        admin.is_admin = True
        db.session.commit()

with app.app_context():

    db.create_all()

    seed_products()

    create_admin()


# ------------------------
# RUN APPLICATION
# ------------------------

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )