from .replace import replace_code


def replace_multiple_files(
    repo_name,
    edits,
    commit_message,
    branch="main"
):
    """
    Apply multiple code replacements across multiple files.
    """

    results = []

    for edit in edits:

        result = replace_code(
            repo_name=repo_name,
            file_path=edit["file_path"],
            old_code=edit["old_code"],
            new_code=edit["new_code"],
            commit_message=commit_message,
            branch=branch
        )

        results.append(result)

    return {
        "success": True,
        "branch": branch,
        "files_updated": len(results),
        "results": results
    }