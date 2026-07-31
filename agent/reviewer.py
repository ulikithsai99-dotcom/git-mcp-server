from .models import RepairPlan


class Reviewer:
    """
    Responsible for reviewing the candidate files
    selected by the planner.
    """

    def __init__(self, tools):
        self.tools = tools

    def review(
        self,
        plan: RepairPlan
    ) -> RepairPlan:
        """
        Read all candidate files and store their contents.
        """

        for candidate in plan.candidate_files:

            try:

                result = self.tools.review_file(
                    plan.repository,
                    candidate.path
                )

            except Exception:
                continue

            if not result.get("success"):
                continue

            plan.reviewed_files[candidate.path] = result["content"]

        return plan