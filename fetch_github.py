import os
import sqlite3
import requests
from dotenv import load_dotenv
from collections import Counter   

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Check if token exists
if not GITHUB_TOKEN:
    raise SystemExit(
        "ERROR: GITHUB_TOKEN not found. Add it to your .env file."
    )

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ===============================
# Database Connection
# ===============================
conn = sqlite3.connect("developers.db")   # <-- Correct database name
cursor = conn.cursor()

skills = [
    "Python",
    "Flask",
    "Machine Learning",
    "Data Science",
    "React",
    "Java",
    "JavaScript",
    "Node.js",
    "FastAPI",
    "TensorFlow"
]


def search_users(skill):
    url = "https://api.github.com/search/users"
    params = {"q": skill, "per_page": 20}

    response = requests.get(url, headers=headers, params=params)

    print(f"Searching {skill} | Status:", response.status_code)

    if response.status_code != 200:
        print("GitHub API Error:", response.json())
        return []

    return response.json()["items"]


def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()

    print(f"Could not fetch {username}")
    return None

from collections import Counter


def get_primary_language(username):

    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(
        url,
        headers=headers,
        params={"per_page": 100}
    )

    if response.status_code != 200:
        return "Unknown"

    repos = response.json()

    languages = []

    for repo in repos:

        language = repo.get("language")

        if language:
            languages.append(language)

    if not languages:
        return "Unknown"

    counter = Counter(languages)

    return counter.most_common(1)[0][0]

def save_developer(data, skill):
    username = data["login"]
    language = get_primary_language(username)

    cursor.execute(
        "SELECT skills FROM developers WHERE username=?",
        (username,)
    )

    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO developers(
                username,
                name,
                bio,
                skills,
                interests,
                location,
                followers,
                following,
                public_repos,
                avatar,
                github_url,
                language
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            username,
            data.get("name"),
            data.get("bio"),
            skill,
            "",
            data.get("location"),
            data.get("followers"),
            data.get("following"),
            data.get("public_repos"),
            data.get("avatar_url"),
            data.get("html_url"),
            language
        ))

    else:
        existing_skills = row[0] or ""

        skill_list = [
            s.strip()
            for s in existing_skills.split(",")
            if s.strip()
        ]

        if skill not in skill_list:
            skill_list.append(skill)

        merged_skills = ", ".join(skill_list)

        cursor.execute("""
            UPDATE developers
            SET
                name=?,
                bio=?,
                skills=?,
                location=?,
                followers=?,
                following=?,
                public_repos=?,
                avatar=?,
                github_url=?,
                language=?
            WHERE username=?
        """, (
            data.get("name"),
            data.get("bio"),
            merged_skills,
            data.get("location"),
            data.get("followers"),
            data.get("following"),
            data.get("public_repos"),
            data.get("avatar_url"),
            data.get("html_url"),
            language,
            username
        ))

    conn.commit()


# ===============================
# Start Scraping
# ===============================

for skill in skills:
    print(f"\nSearching Developers for: {skill}")

    users = search_users(skill)

    for user in users:
        details = get_user_details(user["login"])

        if details:
            save_developer(details, skill)
            print("Saved:", details["login"])

conn.close()

print("\nDatabase Updated Successfully!")