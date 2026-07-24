CAREERS = {

    "Backend Developer": [
        "python",
        "flask",
        "sql",
        "git",
        "rest api",
        "docker",
        "aws"
    ],

    "AI/ML Engineer": [
        "python",
        "machine learning",
        "tensorflow",
        "pandas",
        "numpy",
        "deep learning"
    ],

    "Data Scientist": [
        "python",
        "pandas",
        "numpy",
        "sql",
        "statistics",
        "matplotlib"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "typescript"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "python",
        "flask",
        "sql",
        "git",
        "docker"
    ],

    "Android Developer": [
        "java",
        "kotlin",
        "android",
        "firebase",
        "xml"
    ]
}


def recommend_careers(user_skills):

    user_skills = {
        skill.lower().strip()
        for skill in user_skills
    }

    recommendations = []

    for career, required_skills in CAREERS.items():

        matched = user_skills.intersection(
            set(required_skills)
        )

        score = int(
            len(matched) / len(required_skills) * 100
        )

        recommendations.append({

            "career": career,

            "score": score,

            "matched": list(matched),

            "missing": [
                skill
                for skill in required_skills
                if skill not in matched
            ]

        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:3]