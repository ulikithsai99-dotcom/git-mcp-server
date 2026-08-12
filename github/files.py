from github_client import client
from config import USERNAME
import base64

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


def read_file(
    repo_name,
    file_path,
    branch=None
):
    """
    Read the contents of a file from a GitHub repository.
    """

    if branch is None:
        repo = client.get(
            f"/repos/{USERNAME}/{repo_name}"
        )

        branch = repo["default_branch"]

    data = client.get(
        f"/repos/{USERNAME}/{repo_name}/contents/{file_path}",
        params={
            "ref": branch
        }
    )

    content = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    return content


def repository_tree(repo_name):
    """
    Return every file and folder in the repository.
    """

    repo = client.get(
        f"/repos/{USERNAME}/{repo_name}"
    )

    default_branch = repo["default_branch"]

    tree = client.get(
        f"/repos/{USERNAME}/{repo_name}/git/trees/{default_branch}?recursive=1"
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