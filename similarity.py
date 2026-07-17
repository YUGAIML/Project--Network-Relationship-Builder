import sqlite3
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_by_skills(skills, limit=30):

    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]

    conn = sqlite3.connect("developers.db")

    df = pd.read_sql_query(
        "SELECT * FROM developers",
        conn
    )

    conn.close()

    if df.empty:
        print("No developers found in database.")
        return []

    # Fill missing values
    df["skills"] = df["skills"].fillna("")
    df["bio"] = df["bio"].fillna("")
    df["language"] = df["language"].fillna("")
    df["location"] = df["location"].fillna("")
    df["followers"] = df["followers"].fillna(0)
    df["public_repos"] = df["public_repos"].fillna(0)

    # Developer profile
    df["profile"] = (
        df["skills"] + " " +
        df["bio"] + " " +
        df["language"] + " " +
        df["location"]
    )

    # TF-IDF Similarity
    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(df["profile"])

    user_profile = " ".join(skills)

    user_vector = vectorizer.transform([user_profile])

    tfidf_scores = cosine_similarity(
        user_vector,
        tfidf_matrix
    ).flatten()

    # Skill Matching Score
    skill_scores = []

    for developer_skills in df["skills"]:

        dev_skill_list = [
            s.strip().lower()
            for s in developer_skills.split(",")
            if s.strip()
        ]

        matches = 0

        for skill in skills:
            if skill.lower() in dev_skill_list:
                matches += 1

        if len(skills) > 0:
            score = matches / len(skills)
        else:
            score = 0

        skill_scores.append(score)

    df["tfidf"] = tfidf_scores
    df["skill_score"] = skill_scores

    # Normalize followers
    max_followers = max(df["followers"].max(), 1)
    df["followers_score"] = df["followers"] / max_followers

    # Normalize repositories
    max_repos = max(df["public_repos"].max(), 1)
    df["repo_score"] = df["public_repos"] / max_repos

    # Final weighted score
    df["similarity"] = (
        0.60 * df["skill_score"] +
        0.25 * df["tfidf"] +
        0.10 * df["followers_score"] +
        0.05 * df["repo_score"]
    )

    recommendations = (
        df.sort_values(
            by="similarity",
            ascending=False
        )
        .head(limit)
    )

    print("\n==============================")
    print("User Skills :", skills)
    print("Maximum Score :", recommendations.iloc[0]["similarity"])
    print("==============================\n")

    results = []

    for _, developer in recommendations.iterrows():

        results.append({

            "username": developer["username"],

            "name": developer["name"] if developer["name"] else developer["username"],

            "bio": developer["bio"],

            "skills": developer["skills"],

            "language": developer["language"],

            "location": developer["location"],

            "followers": int(developer["followers"]),

            "public_repos": int(developer["public_repos"]),

            "avatar": developer["avatar"],

            "profile": developer["github_url"],

            "similarity": round(
                developer["similarity"] * 100,
                2
            )
        })

    return results


def get_featured_developers(limit=5):

    conn = sqlite3.connect("developers.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM developers
        ORDER BY followers DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]