def generate_insights(developer):

    skills = developer.get("skills", "").lower()

    followers = developer.get("followers", 0) or 0
    repos = developer.get("public_repos", 0) or 0

    insights = []

    # AI / ML
    if any(skill in skills for skill in [
        "machine learning",
        "tensorflow",
        "pytorch",
        "deep learning",
        "data science"
    ]):
        insights.append("🤖 AI / Machine Learning Specialist")

    # Backend
    if any(skill in skills for skill in [
        "python",
        "flask",
        "fastapi",
        "django"
    ]):
        insights.append("⚙️ Backend Developer")

    # Frontend
    if any(skill in skills for skill in [
        "react",
        "javascript",
        "html",
        "css"
    ]):
        insights.append("🎨 Frontend Developer")

    # DevOps
    if any(skill in skills for skill in [
        "docker",
        "kubernetes",
        "aws"
    ]):
        insights.append("☁️ Cloud / DevOps Engineer")

    # Popularity
    if followers > 1000:
        insights.append("⭐ Popular Open Source Contributor")

    # Activity
    if repos > 50:
        insights.append("🔥 Highly Active GitHub Developer")

    if len(insights) == 0:
        insights.append("💻 Software Developer")

    return insights


def expertise_level(developer):

    followers = developer.get("followers", 0) or 0
    repos = developer.get("public_repos", 0) or 0

    score = followers + repos

    if score >= 1200:
        return "Expert"

    elif score >= 400:
        return "Advanced"

    elif score >= 100:
        return "Intermediate"

    return "Beginner"