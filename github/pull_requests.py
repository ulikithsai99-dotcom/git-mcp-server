import base64

from github_client import client
from config import USERNAME

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


def create_pull_request(repo_name, title, body, head, base=None):
    """
    Create a pull request.
    """

    if base is None:
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


def write_file(repo_name, file_path, new_content, commit_message, branch=None):
    """Update a file in a GitHub repository."""

    if branch is None:
        repo = client.get(f"/repos/{USERNAME}/{repo_name}")
        branch = repo["default_branch"]

    file = client.get(
        f"/repos/{USERNAME}/{repo_name}/contents/{file_path}",
        params={"ref": branch}
    )

    sha = file["sha"]

    encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")

    data = {
        "message": commit_message,
        "content": encoded,
        "sha": sha,
        "branch": branch,
    }

    result = client.put(f"/repos/{USERNAME}/{repo_name}/contents/{file_path}", data)

    return {"commit": result["commit"]["sha"][:7], "url": result["commit"]["html_url"]}