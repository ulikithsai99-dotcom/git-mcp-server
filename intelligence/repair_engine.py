from agent.models import (
    RepairPlan,
    ProposedChange
)

from .models import AnalysisRequest
from .analyzer import Analyzer
from .parser import ResponseParser


class RepairEngine:
    """
    Coordinates the complete intelligence pipeline.

    RepairPlan
        ↓
    AnalysisRequest
        ↓
    Analyzer
        ↓
    LLM
        ↓
    ResponseParser
        ↓
    AnalysisResponse
        ↓
    ProposedChange
        ↓
    Updated RepairPlan
    """

    def __init__(
        self,
        analyzer: Analyzer
    ):
        self.analyzer = analyzer
        self.parser = ResponseParser()

    def repair(
        self,
        plan: RepairPlan
    ) -> RepairPlan:
        """
        Analyze the repository and populate the repair
        plan with proposed code changes.
        """

        request = AnalysisRequest(
            repository=plan.repository,
            issue=plan.issue,
            workspace=plan.workspace,
            candidate_files=[
                candidate.path
                for candidate in plan.candidate_files
            ],
            reviewed_files=plan.reviewed_files
        )

        raw_response = self.analyzer.analyze(request)

        analysis = self.parser.parse(raw_response)

        plan.summary = analysis.summary
        plan.proposed_changes.clear()

        for change in analysis.proposed_changes:

            plan.proposed_changes.append(
                ProposedChange(
                    file_path=change["file_path"],
                    old_code=change["old_code"],
                    new_code=change["new_code"],
                    reason=change.get(
                        "reason",
                        ""
                    )
                )
            )

        return plan