import json
import re

from .files import repository_tree, read_file


FRAMEWORKS = {
    "express": "Express",
    "react": "React",
    "next": "Next.js",
    "vue": "Vue",
    "nestjs": "NestJS",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "spring-boot": "Spring Boot",
    "mongoose": "MongoDB",
    "sequelize": "Sequelize",
    "typeorm": "TypeORM"
}


AUTH_PACKAGES = {
    "jsonwebtoken": "JWT",
    "passport": "Passport",
    "firebase-admin": "Firebase",
    "next-auth": "NextAuth",
    "bcrypt": "Bcrypt"
}


DATABASE_PACKAGES = {
    "mongoose": "MongoDB",
    "mysql2": "MySQL",
    "pg": "PostgreSQL",
    "sqlite3": "SQLite",
    "prisma": "Prisma",
    "typeorm": "TypeORM"
}


def repository_analyzer(repo_name):

    tree = repository_tree(repo_name)

    result = {
        "framework": None,
        "database": None,
        "authentication": [],
        "entry_points": [],
        "routes": [],
        "controllers": [],
        "models": [],
        "services": [],
        "environment_variables": [],
        "github_actions": [],
        "docker": [],
        "languages": set()
    }

    # --------------------------
    # First Pass
    # --------------------------

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        ext = path.split(".")[-1]

        result["languages"].add(ext)

        if path.endswith("package.json"):

            try:

                package = json.loads(
                    read_file(repo_name, path)
                )

                deps = {}

                deps.update(
                    package.get("dependencies", {})
                )

                deps.update(
                    package.get("devDependencies", {})
                )

                for dep in deps:

                    dep_lower = dep.lower()

                    if dep_lower in FRAMEWORKS:
                        result["framework"] = FRAMEWORKS[dep_lower]

                    if dep_lower in DATABASE_PACKAGES:
                        result["database"] = DATABASE_PACKAGES[dep_lower]

                    if dep_lower in AUTH_PACKAGES:
                        result["authentication"].append(
                            AUTH_PACKAGES[dep_lower]
                        )

            except Exception:
                pass

        filename = path.split("/")[-1]

        if filename in (
            "server.js",
            "index.js",
            "app.js",
            "main.py",
            "app.py",
            "server.py"
        ):
            result["entry_points"].append(path)

        if ".github/workflows/" in path:
            result["github_actions"].append(path)

        if filename.startswith(".env"):
            result["environment_variables"].append(path)

        if filename == "Dockerfile":
            result["docker"].append(path)

        lower = path.lower()

        if "/controller" in lower or "/controllers/" in lower:
            result["controllers"].append(path)

        if "/service" in lower or "/services/" in lower:
            result["services"].append(path)

        if "/model" in lower or "/models/" in lower:
            result["models"].append(path)

    # --------------------------
    # Second Pass
    # Read important files
    # --------------------------

    ROUTE_PATTERN = re.compile(
        r"""(?:app|router)\.(?:get|post|put|delete|patch|use)\(\s*['"]([^'"]+)"""
    )

    ENV_PATTERN = re.compile(
        r"process\.env\.([A-Za-z0-9_]+)"
    )

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        if not (
            path.endswith(".js")
            or path.endswith(".ts")
            or path.endswith(".py")
        ):
            continue

        try:

            content = read_file(repo_name, path)

        except Exception:
            continue

        if not isinstance(content, str):
            continue

        for route in ROUTE_PATTERN.findall(content):

            if route not in result["routes"]:
                result["routes"].append(route)

        for env in ENV_PATTERN.findall(content):

            if env not in result["environment_variables"]:
                result["environment_variables"].append(env)

    result["authentication"] = sorted(
        set(result["authentication"])
    )

    result["languages"] = sorted(
        result["languages"]
    )

    return result