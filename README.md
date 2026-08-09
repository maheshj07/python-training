# 📦 Electronic Inventory System

A modern web-based **Electronic Inventory System** developed using **Python Flask, Bootstrap, SQLite, HTML, CSS, and JavaScript**.

The system is designed to manage electronic products, inventory, customers, orders, complaints, and administrative activities through an easy-to-use web interface.

---

## 🚀 Project Overview

The **Electronic Inventory System** helps an electronics shop manage its products and customer orders digitally.

The system provides separate functionality for **customers/users** and **administrators**.

Customers can browse products, search for products, place orders, manage their profile, view orders, submit complaints, and interact with an AI Product Assistant.

Administrators can manage products, users, and orders through the admin panel.

---

## ✨ Features

### 👤 User Features

* User Registration
* User Login & Logout
* User Dashboard
* Profile Management
* Profile Photo Upload
* View Electronic Products
* Product Search
* Product Categories
* Product Details
* Place Orders
* View Order History
* Cancel Orders
* Submit Complaints
* AI Product Assistant

### 🛠️ Admin Features

* Admin Login
* Admin Dashboard
* Manage Products
* Add Products
* Delete Products
* Manage Users
* View Customer Orders
* Update Order Status
* Inventory Management

### 🎨 UI Features

* Modern Responsive Design
* Bootstrap 5.3.3
* Glassmorphism UI
* Premium Liquid Navbar
* Responsive Product Cards
* Font Awesome Icons
* Mobile-Friendly Layout
* Attractive Gradient Sections
* Dark/Light UI support where implemented

---

## 🤖 AI Product Assistant

The project includes an **AI Product Assistant** powered by the **Groq API**.

It can help users with questions related to electronic products and provide product-related recommendations.

The AI functionality uses the:

**Model:** `llama-3.3-70b-versatile`

> An API key must be configured in the environment before using the AI assistant.

---

## 🧰 Technologies Used

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| Python           | Backend Programming       |
| Flask            | Web Framework             |
| Flask-SQLAlchemy | Database ORM              |
| Flask-Login      | User Authentication       |
| SQLite           | Database                  |
| HTML5            | Web Page Structure        |
| CSS3             | Styling                   |
| Bootstrap 5.3.3  | Responsive UI             |
| JavaScript       | Client-Side Functionality |
| Font Awesome     | Icons                     |
| Groq API         | AI Product Assistant      |
| Jinja2           | Flask Templates           |

---

## 📁 Project Structure

```text
Electronic-Inventory-System/
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   ├── images/
│   │   ├── mj.jpeg
│   │   └── ...
│   │
│   └── uploads/
│       └── ...
│
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── products.html
    ├── search.html
    ├── order.html
    ├── orders.html
    ├── profile.html
    ├── profile_edit.html
    ├── ai_chat.html
    ├── complaint.html
    ├── about.html
    │
    └── admin/
        ├── admin.html
        ├── products.html
        ├── users.html
        └── orders.html
```

> The exact folder structure may vary depending on the latest version of the project.

---

## 🗄️ Database

The project uses **SQLite** as its database.

The main database file is:

```text
database.db
```

### Main Database Models

#### User

Stores customer and administrator information.

Fields include:

* ID
* Name
* Email
* Mobile
* Address
* Pincode
* Password
* Profile Picture
* Admin Status

#### Product

Stores electronic product information.

Fields include:

* ID
* Product Name
* Category
* Price
* Stock
* Description
* Product Image

#### Order

Stores customer order information.

Fields include:

* ID
* User ID
* Product Name
* Price
* Quantity
* Status
* Order Date

---

## 📦 Product Categories

The inventory can contain products from categories such as:

* 📱 Mobiles
* 💻 Laptops
* ⌚ Smart Watches
* 🎧 Headphones
* 🔌 Accessories
* 📺 Televisions
* 🎮 Gaming

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/electronic-inventory-system.git
```

### 2. Open the Project Folder

```bash
cd electronic-inventory-system
```

### 3. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install the main dependencies:

```bash
pip install flask flask-sqlalchemy flask-login groq
```

### 5. Configure Environment Variables

Create a `.env` file if your project uses environment variables.

Example:

```text
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_groq_api_key
```

**Do not upload your real API key to GitHub.**

---

## ▶️ Run the Project

Start the Flask application:

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000/
```

Open the address in your web browser.

---

## 🔐 Admin Access

The system supports an administrator account through the `is_admin` field in the User model.

Administrators can access the admin panel and perform tasks such as:

* Product management
* User management
* Order management
* Inventory management
* Order status updates

> Configure your administrator account according to the authentication logic implemented in `app.py`.

---

## 🔍 Main Routes

| Route                 | Description          |
| --------------------- | -------------------- |
| `/`                   | Home Page            |
| `/dashboard`          | User Dashboard       |
| `/register`           | User Registration    |
| `/login`              | User Login           |
| `/logout`             | Logout               |
| `/products`           | Product Listing      |
| `/order/<product_id>` | Order Page           |
| `/orders`             | User Orders          |
| `/profile`            | User Profile         |
| `/profile/edit`       | Edit Profile         |
| `/ai_chat`            | AI Product Assistant |
| `/admin`              | Admin Dashboard      |

---

## 🧪 Testing

The system can be tested using the following areas:

### Authentication Testing

* Registration
* Login
* Logout
* Invalid login
* Duplicate email

### Product Testing

* Product listing
* Product search
* Product categories
* Product details
* Product stock

### Order Testing

* Place order
* View order
* Cancel order
* Order status

### Admin Testing

* Add product
* Delete product
* View users
* View orders
* Update order status

### UI Testing

* Desktop responsiveness
* Mobile responsiveness
* Navigation
* Buttons
* Forms
* Product cards

---

## 🔒 Security

The project includes authentication and authorization features.

Important security practices:

* Password authentication
* Login protection
* Admin authorization
* Unique user email
* Environment variables for API keys
* `.gitignore` for sensitive files

Example `.gitignore`:

```text
venv/
__pycache__/
.env
*.pyc
database.db
```

> If you want the SQLite database included in your GitHub repository, remove `database.db` from `.gitignore`.

---

## 📸 Screenshots

You can add project screenshots here.

Example:

```markdown
## 🏠 Home Page

![Home Page](static/images/home.png)

## 📦 Products Page

![Products Page](static/images/products.png)

## 👤 Dashboard

![Dashboard](static/images/dashboard.png)

## 🛠️ Admin Panel

![Admin Panel](static/images/admin.png)
```

---

## 📈 Future Scope

The system can be improved in the future by adding:

* Online Payment Gateway
* Email Notifications
* SMS Notifications
* Advanced Inventory Reports
* Sales Analytics
* Low Stock Notifications
* Product Reviews and Ratings
* Wishlist
* Shopping Cart
* Invoice Generation
* PDF Reports
* Advanced AI Recommendations
* Cloud Database
* Deployment on a production server
* Mobile Application

---

## 🎯 Advantages

* Easy inventory management
* Reduces manual work
* Saves time
* Centralized product information
* Easy order management
* Customer-friendly interface
* Admin management system
* Searchable electronic products
* AI-based product assistance
* Responsive web design
* SQLite database for simple deployment

---

## 👨‍💻 Developer

**Mahesh Jabade**

### Project

**Electronic Inventory System**

### Technology

**Python Flask + SQLite + Bootstrap**

---

## 📄 License

This project is developed for **educational and academic purposes**.

You may modify and improve the project according to your requirements.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

```
```
