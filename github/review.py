import os

from .files import repository_tree, read_file


# Directories to ignore
SKIP_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".next",
    ".idea",
    ".vscode",
}


# File extensions worth reading
READ_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".md",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
    ".sql",
    ".html",
    ".css",
}


# Important filenames
IMPORTANT_FILES = {
    "Dockerfile",
    "requirements.txt",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "README",
    "README.md",
    ".gitignore",
    "pyproject.toml",
}


# Read limits
MAX_FILES = 50
MAX_FILE_SIZE = 50000


# Priority files (read first)
PRIORITY_FILES = [
    "README.md",
    "README",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "server.js",
    "app.py",
]


def should_read(path):
    """
    Decide whether a file should be included in the repository review.
    """

    parts = path.split("/")

    if any(part in SKIP_DIRS for part in parts):
        return False

    filename = os.path.basename(path)

    if filename in IMPORTANT_FILES:
        return True

    _, ext = os.path.splitext(filename)

    return ext.lower() in READ_EXTENSIONS


def repository_review_context(repo_name):
    """
    Collect important repository files and return
    a complete context for ChatGPT code review.
    """

    tree = repository_tree(repo_name)

    # Prioritize important files first
    tree.sort(
        key=lambda item: (
            os.path.basename(item["path"]) not in PRIORITY_FILES,
            item["path"]
        )
    )

    result = {
        "repository": repo_name,

        "summary": {
            "files_read": [],
            "files_skipped": [],
            "total_files_read": 0,
            "total_files_skipped": 0,
        },

        "tree": tree,

        "files": {}
    }

    count = 0

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        if not should_read(path):
            result["summary"]["files_skipped"].append({
                "path": path,
                "reason": "Unsupported file type or skipped directory"
            })
            continue

        if count >= MAX_FILES:
            result["summary"]["files_skipped"].append({
                "path": path,
                "reason": "Maximum file limit reached"
            })
            continue

        try:

            content = read_file(repo_name, path)

            if not isinstance(content, str):
                result["files"][path] = content
                continue

            if len(content) > MAX_FILE_SIZE:
                result["summary"]["files_skipped"].append({
                    "path": path,
                    "reason": "File too large"
                })
                continue

            result["files"][path] = content

            result["summary"]["files_read"].append({
                "path": path,
                "size": len(content)
            })

            count += 1

        except Exception as e:

            result["files"][path] = {
                "error": str(e)
            }

    result["summary"]["total_files_read"] = len(
        result["summary"]["files_read"]
    )

    result["summary"]["total_files_skipped"] = len(
        result["summary"]["files_skipped"]
    )

    return result