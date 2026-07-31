import re

from .models import RepairPlan


class PullRequestGenerator:
    """
    Generates pull request metadata from a RepairPlan.
    """

    def __init__(self, tools):
        self.tools = tools

    def generate(self, plan: RepairPlan) -> dict:

        branch = self.generate_branch_name(plan.issue)

        commit = f"Fix: {plan.issue}"

        title = f"Fix: {plan.issue}"

        body = self.generate_body(plan)

        return {

            "branch": branch,

            "commit_message": commit,

            "title": title,

            "body": body

        }

    def generate_branch_name(self, issue: str) -> str:

        cleaned = issue.lower()

        cleaned = re.sub(
            r"[^a-z0-9]+",
            "-",
            cleaned
        )

        cleaned = cleaned.strip("-")

        return f"fix/{cleaned}"

    def generate_body(self, plan: RepairPlan) -> str:

        body = []

        body.append("## Summary")
        body.append("")
        body.append(plan.summary or plan.issue)
        body.append("")
        body.append("## Files Reviewed")

        for file in plan.reviewed_files:

            body.append(f"- {file}")

        if plan.proposed_changes:

            body.append("")
            body.append("## Proposed Changes")

            for change in plan.proposed_changes:

                body.append(
                    f"- {change.file_path}"
                )

        return "\n".join(body)