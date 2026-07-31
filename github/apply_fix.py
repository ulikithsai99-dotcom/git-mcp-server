from .review_file import review_file
from .replace import replace_code


def apply_fix(
    repo_name: str,
    file_path: str,
    old_code: str,
    new_code: str,
    commit_message: str
):
    """
    Review a file and apply a code fix.
    """

    review = review_file(repo_name, file_path)

    if not review["success"]:
        return review

    result = replace_code(
        repo_name,
        file_path,
        old_code,
        new_code,
        commit_message
    )

    return {
        "success": result["success"],
        "review": {
            "file": review["file"],
            "size": review["size"]
        },
        "commit": result.get("commit"),
        "file": file_path
    }