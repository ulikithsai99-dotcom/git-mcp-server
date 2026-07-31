from .files import read_file


def review_file(
    repo_name: str,
    file_path: str
):
    """
    Read a single file for detailed review.
    """

    content = read_file(repo_name, file_path)

    if not isinstance(content, str):
        return {
            "success": False,
            "error": "Unable to read file."
        }

    return {
        "success": True,
        "file": file_path,
        "size": len(content),
        "content": content
    }