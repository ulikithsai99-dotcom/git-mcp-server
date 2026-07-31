from .files import read_file
from .pull_requests import write_file


def replace_code(
    repo_name: str,
    file_path: str,
    old_code: str,
    new_code: str,
    commit_message: str
):
    """
    Replace a code snippet inside a file and commit the change.
    """

    content = read_file(repo_name, file_path)

    if not isinstance(content, str):
        return {
            "success": False,
            "error": "Unable to read file."
        }

    if old_code not in content:
        return {
            "success": False,
            "error": "Original code snippet not found."
        }

    updated = content.replace(
        old_code,
        new_code,
        1
    )

    result = write_file(
        repo_name,
        file_path,
        updated,
        commit_message
    )

    return {
        "success": True,
        "file": file_path,
        "commit": result
    }