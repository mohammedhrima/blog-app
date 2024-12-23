from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'users.db'

def get_db():
    """Create or open a connection to the SQLite database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
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

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
  return render_template("signup.html")

@app.route("/home",methods=["GET"])
def home():
  return render_template("home.html")

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

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                flash("Username already exists!", "error")
                return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

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
        if request.is_json:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
        else:
            username = request.form["username"]
            password = request.form["password"]

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if not user or not check_password_hash(user["password"], password):
                if request.is_json:
                    return jsonify({"error": "Invalid username or password"}), 401
                flash("Invalid username or password!", "error")
                return redirect(url_for("login"))

        user_data = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }

        if request.is_json:
            return jsonify(user_data), 200

        flash("Login successful!", "success")
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/users", methods=["GET"])
def get_all_users():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email FROM users')
        users = cursor.fetchall()

    users_list = [{"id": user["id"], "username": user["username"], "email": user["email"]} for user in users]
    return jsonify(users_list)

news_articles = [
    {
        "title": "Breaking: Market Hits All-Time High",
        "content": "The stock market reached an unprecedented high today...",
        "author": "Jane Doe",
        "date": "2024-12-23"
    },
    {
        "title": "Tech Trends to Watch in 2025",
        "content": "As we approach 2025, here are the top tech trends to keep an eye on...",
        "author": "John Smith",
        "date": "2024-12-22"
    },
    {
        "title": "World Cup Highlights",
        "content": "The World Cup delivered thrilling moments this week, with underdogs stealing the spotlight...",
        "author": "Alex Johnson",
        "date": "2024-12-21"
    }
]
@app.route("/news")
def get_news():
    return jsonify(news_articles)


if __name__ == "__main__":
    app.run(debug=True)
