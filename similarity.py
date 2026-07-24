# ==========================================================
# Neural Nexus
# AI Recommendation Engine
# similarity.py (Part 1)
# ==========================================================

import sqlite3
import difflib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================================
# Skill Normalization Dictionary
# ==========================================================

SKILL_ALIASES = {

    "py":"python",
    "pyhton":"python",
    "python3":"python",

    "js":"javascript",
    "node":"node.js",
    "nodejs":"node.js",

    "reactjs":"react",
    "react.js":"react",

    "ml":"machine learning",
    "ai":"artificial intelligence",

    "tensorflow":"tensorflow",
    "tensor flow":"tensorflow",

    "opencv-python":"opencv",

    "postgres":"postgresql",
    "mongo":"mongodb",

    "express":"express.js",
    "expressjs":"express.js",

    "scikit":"scikit-learn",
    "sklearn":"scikit-learn"

}

# ==========================================================
# Related Skills
# ==========================================================

RELATED_SKILLS = {

    "python":[
        "flask",
        "django",
        "fastapi",
        "numpy",
        "pandas",
        "opencv",
        "tensorflow",
        "pytorch",
        "scikit-learn"
    ],

    "machine learning":[
        "python",
        "tensorflow",
        "pytorch",
        "opencv",
        "numpy",
        "pandas",
        "scikit-learn"
    ],

    "flask":[
        "python",
        "fastapi",
        "django",
        "sqlalchemy"
    ],

    "react":[
        "javascript",
        "html",
        "css",
        "redux"
    ],

    "javascript":[
        "react",
        "node.js",
        "express.js",
        "typescript"
    ],

    "node.js":[
        "express.js",
        "mongodb",
        "javascript"
    ],

    "data science":[
        "python",
        "machine learning",
        "pandas",
        "numpy",
        "matplotlib"
    ],

    "deep learning":[
        "tensorflow",
        "pytorch",
        "keras",
        "python"
    ],

    "docker":[
        "kubernetes",
        "linux",
        "aws"
    ]

}

# ==========================================================
# Normalize User Skills
# ==========================================================

def normalize_skills(skill_list):

    normalized = []

    for skill in skill_list:

        skill = skill.strip().lower()

        if skill in SKILL_ALIASES:

            skill = SKILL_ALIASES[skill]

        normalized.append(skill)

    return list(set(normalized))

# ==========================================================
# Auto Correct Skills
# ==========================================================

def correct_skill(skill):

    skill = skill.lower()

    vocabulary = list(SKILL_ALIASES.values())

    vocabulary.extend(

        RELATED_SKILLS.keys()

    )

    match = difflib.get_close_matches(

        skill,

        vocabulary,

        n=1,

        cutoff=0.75

    )

    if match:

        return match[0]

    return skill

# ==========================================================
# Expand Skills using AI
# ==========================================================

def expand_skills(skill_list):

    expanded = []

    for skill in skill_list:

        skill = correct_skill(skill)

        expanded.append(skill)

        if skill in RELATED_SKILLS:

            expanded.extend(

                RELATED_SKILLS[skill]

            )

    return list(set(expanded))

# ==========================================================
# AI Recommendation Engine
# ==========================================================

def recommend_by_skills(skills, limit=30):

    # ----------------------------------------------
    # Convert String to List
    # ----------------------------------------------

    if isinstance(skills, str):

        skills = [

            skill.strip()

            for skill in skills.split(",")

            if skill.strip()

        ]

    # ----------------------------------------------
    # Normalize Skills
    # ----------------------------------------------

    skills = normalize_skills(skills)

    expanded_skills = expand_skills(skills)

    # ----------------------------------------------
    # Read Database
    # ----------------------------------------------

    conn = sqlite3.connect("developers.db")

    df = pd.read_sql_query(

        "SELECT * FROM developers",

        conn

    )

    conn.close()

    if df.empty:

        print("No developers found.")

        return []

    # ----------------------------------------------
    # Fill Missing Values
    # ----------------------------------------------

    columns = [

        "skills",

        "bio",

        "language",

        "location"

    ]

    for column in columns:

        df[column] = df[column].fillna("")

    df["followers"] = df["followers"].fillna(0)

    df["public_repos"] = df["public_repos"].fillna(0)

    # ----------------------------------------------
    # Developer Profile
    # ----------------------------------------------

    df["profile"] = (

        df["skills"] + " " +

        df["bio"] + " " +

        df["language"] + " " +

        df["location"]

    )

    # ----------------------------------------------
    # TF-IDF Similarity
    # ----------------------------------------------

    vectorizer = TfidfVectorizer(

        stop_words="english"

    )

    tfidf_matrix = vectorizer.fit_transform(

        df["profile"]

    )

    user_profile = " ".join(expanded_skills)

    user_vector = vectorizer.transform(

        [user_profile]

    )

    tfidf_scores = cosine_similarity(

        user_vector,

        tfidf_matrix

    ).flatten()

    df["tfidf"] = tfidf_scores

    # ----------------------------------------------
    # AI Skill Matching
    # ----------------------------------------------

    exact_scores = []

    related_scores = []

    matched_skills = []

    missing_skills = []

    language_scores = []

    # ----------------------------------------------

    for _, developer in df.iterrows():

        developer_skills = [

            skill.strip().lower()

            for skill in developer["skills"].split(",")

            if skill.strip()

        ]

        developer_languages = [

            language.strip().lower()

            for language in developer["language"].split(",")

            if language.strip()

        ]

        exact_match = 0

        related_match = 0

        matched = []

        missing = []

        language_match = 0

        # ------------------------------------------
        # Exact Skill Matching
        # ------------------------------------------

        for skill in skills:

            if skill in developer_skills:

                exact_match += 1

                matched.append(skill)

            else:

                missing.append(skill)

        # ------------------------------------------
        # Related Skill Matching
        # ------------------------------------------

        for skill in expanded_skills:

            if skill in developer_skills:

                related_match += 1

        # ------------------------------------------
        # Programming Language Match
        # ------------------------------------------

        for skill in skills:

            if skill in developer_languages:

                language_match += 1

        # ------------------------------------------

        if len(skills):

            exact_match /= len(skills)

            language_match /= len(skills)

        if len(expanded_skills):

            related_match /= len(expanded_skills)

        exact_scores.append(exact_match)

        related_scores.append(related_match)

        language_scores.append(language_match)

        matched_skills.append(", ".join(matched))

        missing_skills.append(", ".join(missing))

    # ==========================================================
    # Additional Scoring
    # ==========================================================

    df["exact_score"] = exact_scores
    df["related_score"] = related_scores
    df["language_score"] = language_scores
    df["matched_skills"] = matched_skills
    df["missing_skills"] = missing_skills

    # ----------------------------------------------
    # Normalize Followers
    # ----------------------------------------------

    max_followers = max(df["followers"].max(), 1)

    df["followers_score"] = (
        df["followers"] / max_followers
    )

    # ----------------------------------------------
    # Normalize Public Repositories
    # ----------------------------------------------

    max_repos = max(df["public_repos"].max(), 1)

    df["repo_score"] = (
        df["public_repos"] / max_repos
    )

    # ==========================================================
    # AI Weighted Recommendation Score
    # ==========================================================

    df["similarity"] = (

        0.40 * df["exact_score"] +

        0.20 * df["related_score"] +

        0.15 * df["tfidf"] +

        0.10 * df["followers_score"] +

        0.10 * df["repo_score"] +

        0.05 * df["language_score"]

    )

    # ==========================================================
    # Confidence Score
    # ==========================================================

    df["confidence"] = (
        df["similarity"] * 100
    ).clip(0,100)

    # ==========================================================
    # Sort Developers
    # ==========================================================

    recommendations = (

        df.sort_values(

            by="similarity",

            ascending=False

        )

        .head(limit)

    )

    # ==========================================================
    # Prepare Final Results
    # ==========================================================

    results = []

    for _, developer in recommendations.iterrows():

        results.append({

            "username": developer["username"],

            "name": developer["name"] or developer["username"],

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
            ),

            "confidence": round(
                developer["confidence"],
                2
            ),

            "matched_skills": developer["matched_skills"],

            "missing_skills": developer["missing_skills"]

        })

    return results


# ==========================================================
# Featured Developers
# ==========================================================

def get_featured_developers(limit=5):

    conn = sqlite3.connect("developers.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM developers

        ORDER BY

            followers DESC,

            public_repos DESC

        LIMIT ?

    """,

    (limit,))

    developers = cursor.fetchall()

    conn.close()

    return [

        dict(row)

        for row in developers

    ]
