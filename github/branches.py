
from github_client import client
from config import USERNAME


def list_branches(repo_name):
    """
    Return all branches of a repository.
    """

    branches = client.get(f"/repos/{USERNAME}/{repo_name}/branches")

    branch_list = []

    for branch in branches:
        branch_list.append({
            "name": branch["name"],
            "sha": branch["commit"]["sha"][:7]
        })

    return branch_list
