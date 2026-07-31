import re

from .files import repository_tree, read_file


IMPORT_PATTERNS = [

    re.compile(r'^\s*import\s+([a-zA-Z0-9_\.]+)', re.MULTILINE),

    re.compile(r'^\s*from\s+([a-zA-Z0-9_\.]+)\s+import', re.MULTILINE),

    re.compile(r'require\([\'"](.+?)[\'"]\)', re.MULTILINE),

    re.compile(r'import\s+.*?from\s+[\'"](.+?)[\'"]', re.MULTILINE)

]


SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx"
)


def dependency_graph(repo_name):

    tree = repository_tree(repo_name)

    graph = {}

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        if not path.endswith(SUPPORTED_EXTENSIONS):
            continue

        try:

            content = read_file(repo_name, path)

        except Exception:

            continue

        imports = []

        for pattern in IMPORT_PATTERNS:

            imports.extend(pattern.findall(content))

        imports = sorted(set(imports))

        graph[path] = imports

    return graph