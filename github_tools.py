import requests
import base64
from config import HEADERS, USERNAME

from github_client import GitHubClient

client = GitHubClient()


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


import base64

def read_readme(repo_name):
    """
    Return the README content of a repository.
    """

    data = client.get(f"/repos/{USERNAME}/{repo_name}/readme")

    readme_content = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    return readme_content


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


def list_issues(repo_name):
    """
    Return all issues of a repository.
    """

    issues = client.get(f"/repos/{USERNAME}/{repo_name}/issues")

    issue_list = []

    for issue in issues:

        # Skip Pull Requests
        if "pull_request" in issue:
            continue

        issue_list.append({
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "author": issue["user"]["login"],
            "created_at": issue["created_at"]
        })

    return issue_list


def create_issue(repo_name, title, body):
    """
    Create a GitHub issue.
    """

    data = {
        "title": title,
        "body": body
    }

    issue = client.post(
        f"/repos/{USERNAME}/{repo_name}/issues",
        data
    )

    return {
        "number": issue["number"],
        "title": issue["title"],
        "url": issue["html_url"]
    }

def list_files(repo_name):
    """
    Return all files and folders in the root directory.
    """

    items = client.get(
        f"/repos/{USERNAME}/{repo_name}/contents"
    )

    files = []

    for item in items:
        files.append({
            "name": item["name"],
            "type": item["type"],
            "path": item["path"]
        })

    return files

import base64

def read_file(repo_name, file_path):
    """
    Read the contents of a file from a repository.
    """

    data = client.get(
        f"/repos/{USERNAME}/{repo_name}/contents/{file_path}"
    )

    content = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    return content

def repository_tree(repo_name):
    """
    Return every file and folder in the repository.
    """

    tree = client.get(
        f"/repos/{USERNAME}/{repo_name}/git/trees/main?recursive=1"
    )

    items = []

    for item in tree["tree"]:
        items.append({
            "path": item["path"],
            "type": item["type"]
        })

    return items

def search_code(repo_name, keyword):
    """
    Search for a keyword in all text files of a repository.
    """

    tree = repository_tree(repo_name)

    matches = []

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        try:

            data = client.get(
                f"/repos/{USERNAME}/{repo_name}/contents/{path}"
            )

            if data.get("encoding") != "base64":
                continue

            content = base64.b64decode(
                data["content"]
            ).decode("utf-8", errors="ignore")

            if keyword.lower() in content.lower():

                matches.append({
                    "file": path
                })

        except Exception:
            continue

    return matches

def get_file_history(repo_name, file_path):
    """
    Return commit history for a specific file.
    """

    commits = client.get(
        f"/repos/{USERNAME}/{repo_name}/commits?path={file_path}"
    )

    history = []

    for commit in commits:

        history.append({
            "sha": commit["sha"][:7],
            "author": commit["commit"]["author"]["name"],
            "date": commit["commit"]["author"]["date"],
            "message": commit["commit"]["message"]
        })

    return history

def create_branch(repo_name, branch_name):
    """
    Create a new branch from the default branch.
    """

    repo = client.get(
        f"/repos/{USERNAME}/{repo_name}"
    )

    default_branch = repo["default_branch"]

    branch = client.get(
        f"/repos/{USERNAME}/{repo_name}/git/ref/heads/{default_branch}"
    )

    latest_sha = branch["object"]["sha"]

    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": latest_sha
    }

    result = client.post(
        f"/repos/{USERNAME}/{repo_name}/git/refs",
        data
    )

    return {
        "branch": result["ref"],
        "sha": result["object"]["sha"]
    }

def create_pull_request(repo_name, title, body, head, base="main"):
    """
    Create a pull request.
    """

    repo = client.get(
        f"/repos/{USERNAME}/{repo_name}"
    )

    base = repo["default_branch"]

    data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }

    result = client.post(
        f"/repos/{USERNAME}/{repo_name}/pulls",
        data
    )

    return {
        "number": result["number"],
        "title": result["title"],
        "url": result["html_url"],
        "state": result["state"]
    }

import base64

def write_file(repo_name, file_path, new_content, commit_message):
    """
    Update a file in a GitHub repository.
    """

    file = client.get(
        f"/repos/{USERNAME}/{repo_name}/contents/{file_path}"
    )

    sha = file["sha"]

    encoded = base64.b64encode(
        new_content.encode("utf-8")
    ).decode("utf-8")

    data = {
        "message": commit_message,
        "content": encoded,
        "sha": sha
    }

    result = client.put(
        f"/repos/{USERNAME}/{repo_name}/contents/{file_path}",
        data
    )

    return {
        "commit": result["commit"]["sha"][:7],
        "url": result["commit"]["html_url"]
    }
