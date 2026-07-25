import os
import csv
from io import StringIO
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response
from dotenv import load_dotenv
from google import genai
from similarity import recommend_by_skills
from repository_api import recommend_repositories
from skill_gap import skill_gap_analysis
from insights import generate_insights, expertise_level
from roadmap import generate_roadmap
from career import recommend_careers
from analytics import get_dashboard_data
from youtube_api import recommend_channels, search_videos

# ==========================================
# Flask App Configuration
# ==========================================

app = Flask(__name__)
app.secret_key = "NeuralNexus@123"

load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6IVmC-OxXTvbpBF6r_HVCsCokSML-G10WnQmNBFtcT3HA"))


# ==========================================
# Home Page & Base Routes
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/developer")
def developers():
    matched_devs = [
        {
            "name": "Sarah Chen",
            "match_score": "98%",
            "skills": ["Python", "Flask", "React", "Docker"],
            "missing_skills": ["AWS"],
            "github_url": "https://github.com/sarahchen"
        },
        {
            "name": "Alex Rivera",
            "match_score": "92%",
            "skills": ["Python", "Django", "PostgreSQL", "Tailwind"],
            "missing_skills": ["GraphQL"],
            "github_url": "https://github.com/arivera"
        },
        {
            "name": "Michael Zhang",
            "match_score": "88%",
            "skills": ["Python", "Machine Learning", "PyTorch", "Pandas"],
            "missing_skills": ["Kubernetes"],
            "github_url": "https://github.com/mzhang"
        }
    ]

    dashboard_stats = {
        "top_skills": ["Python", "Flask", "React", "Docker", "PostgreSQL"],
        "avg_compatibility": 93,
        "top_languages": [
            ("Python", "100%"),
            ("Flask", "66%"),
            ("React", "33%"),
            ("Docker", "33%")
        ]
    }

    # Save initial default data to session
    session['matched_developers'] = matched_devs
    session['dashboard_data'] = dashboard_stats

    return render_template("developer.html", developers=matched_devs, dashboard=dashboard_stats)


# ==========================================
# Chat API Endpoints
# ==========================================

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower()

    dashboard = get_dashboard_data()
    total_devs = dashboard.get("developers", 0)
    top_languages = dashboard.get("top_languages", [])
    top_skills = dashboard.get("top_skills", [])

    if "developer" in user_message or "profile" in user_message or "count" in user_message:
        reply = f"We currently have **{total_devs} developer profiles** matching your search criteria."
    elif "language" in user_message or "tech" in user_message:
        if top_languages:
            top_lang = top_languages[0][0]
            reply = f"The most prevalent language in your match set is **{top_lang}**."
        else:
            reply = "No top language data is currently loaded."
    elif "skill" in user_message or "missing" in user_message:
        reply = f"We are tracking **{len(top_skills)} key skills** across candidate profiles."
    else:
        reply = f"I'm analyzing your current pool of {total_devs} developers. Ask me about top languages, matched skills, or candidate stats!"

    return jsonify({"reply": reply})


@app.route("/api/chat/ai", methods=["POST"])
def ai_chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please enter a message."}), 400

    dashboard = get_dashboard_data()

    system_context = f"""
    You are Network Assistant AI, an expert recruiter bot.
    Answer the user's questions concisely using the following live data:
    - Total Developers Processed: {dashboard.get('developers', 0)}
    - Top Languages: {dashboard.get('top_languages', [])}
    - Top Skills: {dashboard.get('top_skills', [])}
    - Average Compatibility: {dashboard.get('avg_compatibility', 'High Match')}
    """

    prompt = f"{system_context}\n\nUser Question: {user_message}\nAnswer:"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        print("AI Error:", e)
        return jsonify({"reply": "Sorry, I had trouble processing that request with AI."}), 500

# ==========================================
# Recommendation System
# ==========================================

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    if request.method == "POST":
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

        # Calculate all recommendation data
        developer_list = recommend_by_skills(skills_list, limit=30)
        repository_list = recommend_repositories(skills_list)
        missing_skills = skill_gap_analysis(skills_list, developer_list)
        roadmap = generate_roadmap(skills_list)
        career_list = recommend_careers(skills_list)
        dashboard_data = get_dashboard_data()

        if len(developer_list) == 0:
            flash("No matching developers found. Try different skills.", "warning")

        # Save data to session for persistence & CSV export
        session["searched_skills"] = skills_list
        session["raw_skills_string"] = skills
        session["matched_developers"] = developer_list
        session["repository_list"] = repository_list
        session["missing_skills"] = missing_skills
        session["roadmap"] = roadmap
        session["career_list"] = career_list
        session["dashboard_data"] = dashboard_data

        return render_template(
            "results.html",
            developers=developer_list,
            repositories=repository_list,
            missing_skills=missing_skills,
            roadmap=roadmap,
            careers=career_list,
            searched_skills=skills,
            dashboard=dashboard_data
        )

    # --- GET REQUEST (Clicking "Back to Results" from Analytics) ---
    # Check if we already have search results stored in session
    if "matched_developers" in session:
        return render_template(
            "results.html",
            developers=session.get("matched_developers", []),
            repositories=session.get("repository_list", []),
            missing_skills=session.get("missing_skills", []),
            roadmap=session.get("roadmap", []),
            careers=session.get("career_list", []),
            searched_skills=session.get("raw_skills_string", ""),
            dashboard=session.get("dashboard_data", {})
        )

    # If no search history exists in session at all, redirect to search form
    flash("Please select your skills to see recommendations.", "warning")
    return redirect(url_for("developers"))


@app.route("/youtube")
def youtube():
    # Fallback to default skills if none exist in session
    skills = session.get("searched_skills") or ["Python", "Web Development"]

    channels = recommend_channels(skills)
    videos = search_videos(skills)

    return render_template(
        "youtube.html",
        channels=channels,
        videos=videos,
        searched_skills=", ".join(skills)
    )


@app.route("/analytics")
def analytics():
    dashboard = get_dashboard_data()
    return render_template("analytics.html", dashboard=dashboard)


@app.route("/profile/<username>")
def profile(username):
    import sqlite3

    conn = sqlite3.connect("developers.db")
    conn.row_factory = sqlite3.Row
    cursor_sqlite = conn.cursor()

    cursor_sqlite.execute(
        "SELECT * FROM developers WHERE username=?",
        (username,)
    )

    developer = cursor_sqlite.fetchone()
    conn.close()

    if developer is None:
        return "Developer not found"

    developer = dict(developer)
    developer["insights"] = generate_insights(developer)
    developer["expertise"] = expertise_level(developer)

    return render_template("profile.html", developer=developer)

# ==========================================
# Export Complete CSV Report
# ==========================================

@app.route('/export/report')
def export_report():
    output = StringIO()
    writer = csv.writer(output)

    # 1. Fetch search results stored in session
    developers_list = session.get('matched_developers', [])
    dashboard_data = session.get('dashboard_data', {})

    # ----------------------------------------------------
    # 1. ANALYTICS OVERVIEW SECTION
    # ----------------------------------------------------
    writer.writerow(["=== ANALYTICS OVERVIEW ==="])
    writer.writerow(["Metric", "Value"])
    
    top_skills_count = len(dashboard_data.get('top_skills', []))
    avg_compat = dashboard_data.get('avg_compatibility', 'High Match')
    
    writer.writerow(["Top Skills Tracked", top_skills_count])
    writer.writerow(["Average Compatibility", f"{avg_compat}%" if isinstance(avg_compat, (int, float)) else avg_compat])
    
    if dashboard_data.get('top_languages'):
        writer.writerow([])
        writer.writerow(["Language/Skill", "Share / Count"])
        for lang, count in dashboard_data['top_languages']:
            writer.writerow([lang, count])

    writer.writerow([])  # Blank line separator

    # ----------------------------------------------------
    # 2. MATCHED DEVELOPERS SECTION
    # ----------------------------------------------------
    writer.writerow(["=== MATCHED DEVELOPERS ==="])
    writer.writerow(["Name", "Match Percentage", "Top Skills", "Missing Skills", "Profile Link"])

    for dev in developers_list:
        if isinstance(dev, dict):
            name = dev.get('name', dev.get('username', 'N/A'))
            match = dev.get('match_score', dev.get('compatibility', dev.get('score', 'N/A')))
            skills_raw = dev.get('skills', [])
            skills = " | ".join(skills_raw) if isinstance(skills_raw, list) else str(skills_raw)
            missing_raw = dev.get('missing_skills', [])
            missing = " | ".join(missing_raw) if isinstance(missing_raw, list) else str(missing_raw)
            link = dev.get('github_url', dev.get('profile_url', dev.get('html_url', 'N/A')))
        else:
            name = getattr(dev, 'name', getattr(dev, 'username', 'N/A'))
            match = getattr(dev, 'match_score', getattr(dev, 'compatibility', getattr(dev, 'score', 'N/A')))
            skills_raw = getattr(dev, 'skills', [])
            skills = " | ".join(skills_raw) if isinstance(skills_raw, list) else str(skills_raw)
            missing_raw = getattr(dev, 'missing_skills', [])
            missing = " | ".join(missing_raw) if isinstance(missing_raw, list) else str(missing_raw)
            link = getattr(dev, 'github_url', getattr(dev, 'profile_url', 'N/A'))

        writer.writerow([name, match, skills, missing or "None", link])

    # ----------------------------------------------------
    # 3. DOWNLOAD RESPONSE
    # ----------------------------------------------------
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=network_builder_overall_report.csv"}
    )
from flask import jsonify

@app.route("/bookmark", methods=["POST"])
def bookmark_candidate():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Please log in to bookmark developers."}), 401

    data = request.get_json()
    username = data.get("name")
    github_url = data.get("github_url")

    # Insert into database table
    cursor.execute("""
        INSERT INTO saved_developers (user_id, developer_name, github_url)
        VALUES (%s, %s, %s)
    """, (session["user_id"], username, github_url))
    db.commit()

    return jsonify({"status": "success", "message": f"{username} bookmarked!"})
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
    app.run(debug=True)