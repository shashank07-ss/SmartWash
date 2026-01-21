from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "smartwash_secret_key"

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------
# DATABASE INITIALIZATION
# -------------------------------
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service TEXT,
            quantity INTEGER,
            total_price REAL,
            status TEXT DEFAULT 'Pending',
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Create default admin
    cursor.execute("SELECT * FROM users WHERE role='admin'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, ("Admin", "admin@smartwash.com", "admin123", "admin"))

    conn.commit()
    conn.close()

init_db()

# -------------------------------
# AUTH ROUTES
# -------------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["name"] = user["name"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already exists", "danger")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------------------
# USER DASHBOARD
# -------------------------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session or session.get("role") != "user":
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        service = request.form["service"]
        quantity = int(request.form["quantity"])

        pricing = {
            "Wash": 50,
            "Dry": 32,
            "Iron": 20
        }

        total_price = pricing.get(service, 0) * quantity

        conn.execute("""
            INSERT INTO orders (user_id, service, quantity, total_price, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            service,
            quantity,
            total_price,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()

    orders = conn.execute("""
        SELECT * FROM orders WHERE user_id=?
        ORDER BY created_at DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    # 🔹 PAYMENT ENABLED ONLY IF ANY ORDER IS COMPLETED
    payment_allowed = any(order["status"] == "Completed" for order in orders)

    return render_template(
        "dashboard.html",
        orders=orders,
        name=session["name"],
        payment_allowed=payment_allowed
    )

# -------------------------------
# ADMIN DASHBOARD
# -------------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        order_id = request.form["order_id"]
        status = request.form["status"]

        conn.execute(
            "UPDATE orders SET status=? WHERE id=?",
            (status, order_id)
        )
        conn.commit()

    orders = conn.execute("""
        SELECT orders.*, users.name 
        FROM orders 
        JOIN users ON orders.user_id = users.id
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()
    return render_template("admin.html", orders=orders)

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=False)

