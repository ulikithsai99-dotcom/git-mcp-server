from github_client import client
from config import USERNAME


def list_commits(repo_name):
    """
    Return the latest commits of a repository.
    """

    commits = client.get(f"/repos/{USERNAME}/{repo_name}/commits")

    commit_list = []

    for commit in commits:
        commit_list.append({
            "sha": commit["sha"][:7],
            "author": commit["commit"]["author"]["name"],
            "date": commit["commit"]["author"]["date"],
            "message": commit["commit"]["message"].split("\n")[0]
        })

    return commit_list