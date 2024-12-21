from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database setup
DATABASE = 'users.db'

def get_db():
    """Create or open a connection to the SQLite database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def init_db():
    """Initialize the database and create the users table if it doesn't exist"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

# Initialize database
init_db()

@app.route("/")
def index():
  return render_template("signup.html")

@app.route("/home")
def func():
  return render_template("users.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("signup"))

        # Check if the username already exists
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                flash("Username already exists!", "error")
                return redirect(url_for("signup"))

        # Hash the password before storing
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Insert the new user into the database
        with get_db() as conn:
            conn.execute('''
                INSERT INTO users (username, email, password) 
                VALUES (?, ?, ?)
            ''', (username, email, hashed_password))
            conn.commit()

        flash("Signup successful!", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Fetch the user from the database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if not user or not check_password_hash(user["password"], password):
                flash("Invalid username or password!", "error")
                return redirect(url_for("login"))

        flash("Login successful!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/users", methods=["GET"])
def get_all_users():
    # Fetch all users from the database
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email FROM users')
        users = cursor.fetchall()

    # Convert to a list of dictionaries for JSON response
    users_list = [{"id": user["id"], "username": user["username"], "email": user["email"]} for user in users]
    return jsonify(users_list)

if __name__ == "__main__":
    app.run(debug=True)
