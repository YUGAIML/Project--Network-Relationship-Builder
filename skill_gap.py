from collections import Counter


def skill_gap_analysis(user_skills, developers):

    user_skills = [skill.lower().strip() for skill in user_skills]

    skill_counter = Counter()

    for developer in developers:

        skills = developer.get("skills")

        if not skills:
            continue

        developer_skills = [
            skill.lower().strip()
            for skill in skills.split(",")
        ]

        skill_counter.update(developer_skills)

    missing_skills = []

    for skill, count in skill_counter.most_common():

        if skill not in user_skills:

            missing_skills.append({

                "skill": skill,

                "count": count

            })

    return missing_skills[:10]