import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def recommend_repositories(skills):

    query = " ".join(skills)

    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        print("GitHub API Error:", response.status_code)
        return []

    data = response.json()

    repositories = []

    for repo in data.get("items", []):

        repositories.append({

            "name": repo["name"],

            "owner": repo["owner"]["login"],

            "description": repo["description"],

            "language": repo["language"],

            "stars": repo["stargazers_count"],

            "forks": repo["forks_count"],

            "url": repo["html_url"]

        })

    return repositories
if __name__ == "__main__":

    repos = recommend_repositories(
        ["Python", "Flask"]
    )

    for repo in repos:

        print(repo["name"], "-", repo["stars"])