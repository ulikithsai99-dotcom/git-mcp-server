import re

from .files import repository_tree, read_file


SYMBOL_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".php",
    ".rb"
)


def find_symbol(repo_name, symbol):
    """
    Locate function/class/variable definitions and references.
    """

    tree = repository_tree(repo_name)

    results = []

    patterns = [
        rf"\bdef\s+{re.escape(symbol)}\b",
        rf"\bclass\s+{re.escape(symbol)}\b",
        rf"\bfunction\s+{re.escape(symbol)}\b",
        rf"\bconst\s+{re.escape(symbol)}\b",
        rf"\blet\s+{re.escape(symbol)}\b",
        rf"\bvar\s+{re.escape(symbol)}\b",
        rf"\b{re.escape(symbol)}\s*=",
        rf"\b{re.escape(symbol)}\("
    ]

    compiled = [re.compile(p) for p in patterns]

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        if not path.endswith(SYMBOL_EXTENSIONS):
            continue

        try:

            content = read_file(repo_name, path)

            if not isinstance(content, str):
                continue

            matches = []

            for line_no, line in enumerate(content.splitlines(), start=1):

                for pattern in compiled:

                    if pattern.search(line):

                        matches.append({
                            "line": line_no,
                            "code": line.strip()
                        })

                        break

            if matches:

                results.append({
                    "file": path,
                    "matches": matches
                })

        except Exception:
            continue

    return {
        "symbol": symbol,
        "files": results,
        "total_files": len(results)
    }