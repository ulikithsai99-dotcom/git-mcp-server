from github_client import client
from config import USERNAME

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
