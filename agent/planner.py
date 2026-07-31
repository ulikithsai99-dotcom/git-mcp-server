from .models import RepairPlan, FileCandidate


class Planner:
    """
    Responsible for locating the files that are most likely
    related to a user's issue.
    """

    def __init__(self, tools):
        self.tools = tools

    def locate_files(self, plan: RepairPlan)-> RepairPlan:

        workspace = plan.workspace

        architecture = workspace.get("architecture", {})

        repo_map = workspace.get("repository_map", {})

        dependency_graph = workspace.get("dependency_graph", {})

        keywords = self.extract_keywords(
            plan.issue
        )

        # Search symbols

        for keyword in keywords:

            try:

                result = self.tools.find_symbol(
                    plan.repository,
                    keyword
                )

            except Exception:
                continue

            files = result.get("files", [])

            for file in files:

                self.add_candidate(
                    plan,
                    file,
                    f"Matched symbol '{keyword}'"
                )

        # Entry points

        for file in architecture.get(
            "entry_points",
            []
        ):

            self.add_candidate(
                plan,
                file,
                "Application entry point"
            )

        # Controllers

        for file in architecture.get(
            "controllers",
            []
        ):

            self.add_candidate(
                plan,
                file,
                "Controller"
            )

        # Services

        for file in architecture.get(
            "services",
            []
        ):

            self.add_candidate(
                plan,
                file,
                "Service"
            )

        # Models

        for file in architecture.get(
            "models",
            []
        ):

            self.add_candidate(
                plan,
                file,
                "Model"
            )

        # Dependency graph

        for file in dependency_graph:

            if file not in [c.path for c in plan.candidate_files]:

                if any(
                    keyword.lower() in file.lower()
                    for keyword in keywords
                ):

                    self.add_candidate(
                        plan,
                        file,
                        "Filename matches issue"
                    )

        return plan

    def extract_keywords(
        self,
        issue: str
    ) -> list[str]:

        words = issue.lower().split()

        ignored = {
            "the",
            "is",
            "a",
            "an",
            "to",
            "of",
            "in",
            "on",
            "for",
            "fix",
            "bug",
            "issue",
            "error",
            "problem"
        }

        return [
            word
            for word in words
            if word not in ignored
        ]

    def add_candidate(
        self,
        plan:RepairPlan,
        path: str,
        reason: str
    ):

        for candidate in plan.candidate_files:

            if candidate.path == path:
                return

        plan.candidate_files.append(

            FileCandidate(
                path=path,
                reason=reason
            )

        )