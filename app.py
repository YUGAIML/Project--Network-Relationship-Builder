from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from similarity import recommend_by_skills
from dotenv import load_dotenv
import os

# ==========================================
# Flask App Configuration
# ==========================================

app = Flask(__name__)
app.secret_key = "NeuralNexus@123"

load_dotenv()

# ==========================================
# MySQL Database Connection
# ==========================================

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="network_relationship"
    )

    cursor = db.cursor(dictionary=True)
    print("✅ MySQL Connected Successfully")

except mysql.connector.Error as err:
    print("❌ Database Connection Error:", err)

# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# Developer Page
# ==========================================

@app.route("/developer")
def developers():
    return render_template("developer.html")


# ==========================================
# Register
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        if cursor.fetchone():
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        cursor.execute("""
            INSERT INTO users(fullname,email,password)
            VALUES(%s,%s,%s)
        """, (fullname, email, password))

        db.commit()

        flash("Registration Successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ==========================================
# Login
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"].strip()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email=%s
            AND password=%s
        """, (email, password))

        user = cursor.fetchone()

        if user:

            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]

            flash("Login Successful!", "success")

            return redirect(url_for("developers"))

        flash("Invalid Email or Password!", "danger")

    return render_template("login.html")


# ==========================================
# Recommendation System
# ==========================================

@app.route("/recommend", methods=["POST"])
def recommend():

    skills = request.form.get("skills", "").strip()

    print("=" * 60)
    print("Received Skills :", skills)

    if not skills:
        flash("Please enter at least one skill.", "warning")
        return redirect(url_for("developers"))

    skills_list = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    print("Skill List :", skills_list)

    developer_list = recommend_by_skills(
        skills_list,
        limit=30
    )

    print("Recommendations Found :", len(developer_list))
    print("=" * 60)

    if len(developer_list) == 0:
        flash(
            "No matching developers found. Try different skills.",
            "warning"
        )

    return render_template(
        "results.html",
        developers=developer_list,
        searched_skills=skills
    )


# ==========================================
# Logout
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("home"))


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )