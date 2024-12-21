from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {}

@app.route("/")
def index():
  return render_template("signup.html")


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

    if username in users:
      flash("Username already exists!", "error")
      return redirect(url_for("signup"))

    # Hash the password before storing (use pbkdf2:sha256)
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    # Save user data (here using a dictionary)
    users[username] = {"email": email, "password": hashed_password}

    flash("Signup successful!", "success")
    return redirect(url_for("login"))

  return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    user = users.get(username)
    if not user or not check_password_hash(user["password"], password):
      flash("Invalid username or password!", "error")
      return redirect(url_for("login"))

    flash("Login successful!", "success")
    return redirect(url_for("index"))

  return render_template("login.html")


if __name__ == "__main__":
  app.run(debug=True)
