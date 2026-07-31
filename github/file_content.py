from github_client import client

def read_file_by_owner(owner: str, repo: str, path: str, branch: str = "main"):
    """
    Read the contents of a file from a GitHub repository.
    """

    try:
        url = f"/repos/{owner}/{repo}/contents/{path}"

        response = client.get(
            url,
            params={"ref": branch}
        )

        data = response.json()

        if "content" not in data:
            return {
                "success": False,
                "message": "File not found."
            }

        import base64

        content = base64.b64decode(
            data["content"]
        ).decode("utf-8")

        return {
            "success": True,
            "path": path,
            "size": data["size"],
            "content": content
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }