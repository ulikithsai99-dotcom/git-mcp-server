from github_client import client
from config import USERNAME
import base64

def list_repositories():
    """
    Return all repositories of the authenticated user.
    """

    repos = client.get("/user/repos")

    repositories = []

    for repo in repos:
        repositories.append({
            "name": repo["name"],
            "visibility": repo["visibility"],
            "stars": repo["stargazers_count"]
        })

    return repositories


def get_repository(repo_name):
    """
    Return details of a repository.
    """

    repo = client.get(f"/repos/{USERNAME}/{repo_name}")

    return {
        "name": repo["name"],
        "description": repo["description"],
        "visibility": repo["visibility"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "watchers": repo["watchers_count"],
        "url": repo["html_url"]
    }


def read_readme(repo_name):
    """
    Return the README content of a repository.
    """

    data = client.get(f"/repos/{USERNAME}/{repo_name}/readme")

    readme_content = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    return readme_content
