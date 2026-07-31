from .models import RepairPlan


class Fixer:
    """
    Responsible for applying the proposed code changes
    to the repository.
    """

    def __init__(self, tools):
        self.tools = tools

    def apply(self, plan: RepairPlan):
        """
        Apply every proposed change.
        """

        if not plan.proposed_changes:
            print("No proposed changes found.")
            return plan

        results = []

        for change in plan.proposed_changes:

            try:

                result = self.tools.replace_code(
                    repo_name=plan.repository,
                    file_path=change.file_path,
                    old_code=change.old_code,
                    new_code=change.new_code,
                    commit_message=f"Fix: {plan.issue}"
                )

                results.append(result)

            except Exception as e:

                results.append({
                    "success": False,
                    "file": change.file_path,
                    "error": str(e)
                })

        plan.fix_results = results
        return plan