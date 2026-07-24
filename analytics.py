import sqlite3
from collections import Counter


def get_dashboard_data():

    # Connect Database
    conn = sqlite3.connect("developers.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM developers")

    developers = cursor.fetchall()

    total_developers = len(developers)

    language_counter = Counter()
    skill_counter = Counter()

    # Read Every Developer
    for developer in developers:

        # ----------------------------
        # Programming Language
        # ----------------------------
        language = developer["language"]

        if language and str(language).strip():

            language_counter[str(language).strip()] += 1

        # ----------------------------
        # Skills
        # ----------------------------
        skills = developer["skills"]

        if skills and str(skills).strip():

            skill_list = [

                skill.strip()

                for skill in str(skills).split(",")

                if skill.strip()

            ]

            skill_counter.update(skill_list)

    # ----------------------------
    # Debug (Check Terminal)
    # ----------------------------

    print("=" * 50)
    print("Developers :", total_developers)
    print("Top Skills :", skill_counter.most_common(10))
    print("Top Languages :", language_counter.most_common(10))
    print("=" * 50)

    conn.close()

    # ----------------------------
    # Return Dashboard Data
    # ----------------------------

    return {

        # Summary Cards
        "total_developers": total_developers,
        "total_languages": len(language_counter),
        "total_skills": len(skill_counter),

        # Tables
        "top_languages": language_counter.most_common(10),
        "top_skills": skill_counter.most_common(10),

        # Bar Chart
        "skill_labels": [
            skill
            for skill, count in skill_counter.most_common(8)
        ],

        "skill_values": [
            count
            for skill, count in skill_counter.most_common(8)
        ],

        # Pie Chart
        "language_labels": [
            language
            for language, count in language_counter.most_common(5)
        ],

        "language_values": [
            count
            for language, count in language_counter.most_common(5)
        ]

    }


# ---------------------------------------
# Run File Directly (Testing Only)
# ---------------------------------------

if __name__ == "__main__":

    dashboard = get_dashboard_data()

    print("\nReturned Data:\n")

    for key, value in dashboard.items():

        print(f"{key} : {value}")