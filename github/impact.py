import re

from .files import repository_tree, read_file


def impact_analysis(repo_name: str, symbol: str):
    """
    Find where a function, class, variable or filename is used.
    """

    tree = repository_tree(repo_name)

    results = []

    pattern = re.compile(rf"\b{re.escape(symbol)}\b")

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        try:
            content = read_file(repo_name, path)

            if not isinstance(content, str):
                continue

            matches = []

            for number, line in enumerate(content.splitlines(), start=1):

                if pattern.search(line):

                    matches.append({
                        "line": number,
                        "code": line.strip()
                    })

            if matches:

                results.append({
                    "file": path,
                    "matches": matches
                })

        except Exception:
            pass

    return {
        "symbol": symbol,
        "references": results,
        "total_files": len(results)
    }