import os
import sqlite3
import random
import datetime
import smtplib
import traceback
from flask import Flask, render_template, request, jsonify, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "defaultsecret")

# ---------------- Database Setup ----------------
if not os.path.exists('project.db'):
    import init_db
def get_db_conn():
    conn = sqlite3.connect("project.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- Email OTP ----------------
#EMAIL_USER = os.getenv("EMAIL_USER", "youremail@example.com")
#EMAIL_PASS = os.getenv("EMAIL_PASS", "yourpassword")
#
#def send_email(to, subject, content):
#    msg = MIMEText(content)
#    msg["Subject"] = subject
#    msg["From"] = EMAIL_USER
#    msg["To"] = to
#
#    with smtplib.SMTP("smtp.gmail.com", 587) as server:
#        server.starttls()
#        server.login(EMAIL_USER, EMAIL_PASS)
#        server.sendmail(msg["From"], [msg["To"]], msg.as_string())
#
# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup_method', methods=["POST"])
def signup_method():
    data = request.get_json()  # ✅ read JSON
    username = data.get("username")
    full_name = data.get("full_name")
    email = data.get("email")
    password = generate_password_hash(data.get("password"))
    phone = data.get("phone")

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return jsonify({"message": "Email already registered"}), 400

    try:
        cursor.execute(
            "INSERT INTO users (username, full_name, email, password, phone) VALUES (?, ?, ?, ?, ?)",
            (username, full_name, email, password, phone)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Registration successful"}), 200
    except Exception as e:
        traceback.print_exc()
        conn.close()
        return jsonify({"message": "Registration failed"}), 500


@app.route('/login_method', methods=["POST"])
def login_method():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]

        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/home_login")
def home_login():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("home.html", user=session["user_id"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- Static Pages ----------------
@app.route('/appointments')
def appointment():
    return render_template("appointment.html")

@app.route('/careers')
def careers(): return render_template("careers.html")

@app.route('/discussion')
def discussion(): 
    if "user_id" not in session:
        return redirect("/login")
    
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM discussions WHERE user_email = ?", (session["email"],))
    subs = cursor.fetchall()
    conn.close()
    return render_template("discussion.html")

@app.route('/contact')
def contact(): 
    #conn = get_db_conn()
    #cursor = conn.cursor()
    #cursor.execute("SELECT * #FROM contact_messages #WHERE user_email = ?", #(session["email"],))
    #subs = cursor.fetchall()
    #conn.close()
    return render_template("contact.html")

@app.route('/insurance')
def insurance(): 
    return render_template("insurance.html")

@app.route('/subscription')
def subscription():
    if "user_id" not in session:
        return redirect("/login")
    
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscriptions WHERE user_email = ?", (session["email"],))
    subs = cursor.fetchall()
    conn.close()
    return render_template("subscription.html")

#------user section --------


@app.context_processor
def inject_user():
    if "user_id" in session:
        return dict(user={
            "id": session["user_id"],
            "username": session.get("username"),
            "email": session.get("email")
        })
    return dict(user=None)

#----------user section rendering in pages ------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug = True)
