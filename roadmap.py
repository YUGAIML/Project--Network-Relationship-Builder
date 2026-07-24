ROADMAP = {

    "python": [
        "Python",
        "Object Oriented Programming",
        "Data Structures",
        "SQL",
        "Git & GitHub",
        "Flask",
        "REST API",
        "Docker",
        "AWS",
        "Kubernetes"
    ],

    "flask": [
        "HTML",
        "CSS",
        "JavaScript",
        "Python",
        "Flask",
        "SQL",
        "REST API",
        "JWT Authentication",
        "Docker",
        "AWS"
    ],

    "machine learning": [
        "Python",
        "NumPy",
        "Pandas",
        "Matplotlib",
        "Scikit-Learn",
        "TensorFlow",
        "Deep Learning",
        "MLOps",
        "Docker",
        "AWS"
    ],

    "java": [
        "Java",
        "OOP",
        "Collections",
        "Spring Boot",
        "Hibernate",
        "REST API",
        "Docker",
        "AWS"
    ],

    "react": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Redux",
        "Node.js",
        "MongoDB",
        "Docker"
    ]
}


def generate_roadmap(user_skills):

    roadmap = []

    added = set()

    for skill in user_skills:

        skill = skill.lower().strip()

        if skill in ROADMAP:

            for topic in ROADMAP[skill]:

                if topic not in added:

                    roadmap.append(topic)

                    added.add(topic)

    return roadmap