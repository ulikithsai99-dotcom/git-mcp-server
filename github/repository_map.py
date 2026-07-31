import os

from .files import repository_tree


FRAMEWORK_FILES = {
    "package.json": "Node.js",
    "requirements.txt": "Python",
    "pyproject.toml": "Python",
    "manage.py": "Django",
    "next.config.js": "Next.js",
    "next.config.mjs": "Next.js",
    "vite.config.js": "Vite",
    "vite.config.ts": "Vite",
    "angular.json": "Angular",
    "pom.xml": "Spring Boot / Maven",
    "build.gradle": "Spring Boot / Gradle",
    "Cargo.toml": "Rust",
    "composer.json": "PHP",
    "go.mod": "Go",
    "Gemfile": "Ruby"
}


ENTRY_FILES = [
    "main.py",
    "app.py",
    "server.py",
    "index.js",
    "server.js",
    "app.js",
    "main.js",
    "main.ts",
    "index.ts",
    "Program.cs"
]


def repository_map(repo_name):
    """
    Build a quick overview of a repository.
    """

    tree = repository_tree(repo_name)

    framework = None
    entry_points = []
    env_files = []
    docker_files = []
    github_actions = []
    package_files = []
    languages = set()

    folders = set()

    for item in tree:

        path = item["path"]

        if item["type"] == "tree":
            folders.add(path)
            continue

        filename = os.path.basename(path)

        if filename in FRAMEWORK_FILES:
            framework = FRAMEWORK_FILES[filename]

        if filename in ENTRY_FILES:
            entry_points.append(path)

        if filename.startswith(".env"):
            env_files.append(path)

        if filename == "Dockerfile":
            docker_files.append(path)

        if path.startswith(".github/workflows/"):
            github_actions.append(path)

        if filename in FRAMEWORK_FILES:
            package_files.append(path)

        ext = os.path.splitext(path)[1]

        if ext:
            languages.add(ext)

    return {
        "framework": framework,
        "entry_points": entry_points,
        "environment_files": env_files,
        "docker_files": docker_files,
        "github_actions": github_actions,
        "package_files": package_files,
        "languages": sorted(languages),
        "folders": sorted(folders)
    }