from .planner import Planner
from .reviewer import Reviewer
from .fixer import Fixer
from .pr_generator import PullRequestGenerator
from .models import (
    RepairPlan,
    FileCandidate
)
from intelligence.mock_provider import MockProvider
from intelligence.analyzer import Analyzer
from intelligence.repair_engine import RepairEngine

class SoftwareEngineerWorkflow:
    """
    Orchestrates the complete software engineering workflow.
    """

    def __init__(self, tools):
        """
        tools is an object exposing your GitHub MCP functions.
        """

        self.tools = tools

        self.planner = Planner(tools)
        self.reviewer = Reviewer(tools)
        self.fixer = Fixer(tools)
        self.pr_generator = PullRequestGenerator(tools)
        self.repair_engine = RepairEngine(
            Analyzer(MockProvider())
        )

    def start(
        self,
        repo_name: str,
        issue: str
    ) -> RepairPlan:
        """
        Create a new repair plan and load repository context.
        """

        plan = RepairPlan(
            repository=repo_name,
            issue=issue
        )

        self.load_workspace(plan)

        return plan

    def execute(
        self,
        repo_name: str,
        issue: str
    ) -> RepairPlan:
        """
        Execute the repository analysis workflow.

        Current pipeline:

        Start
            ↓
        Load Workspace
            ↓
        Planner
            ↓
        Reviewer
            ↓
        Return RepairPlan

        Future pipeline:

        Planner
            ↓
        Reviewer
            ↓
        Intelligence Engine
            ↓
        Fixer
            ↓
        Pull Request Generator
        """

        plan = self.start(
            repo_name=repo_name,
            issue=issue
        )

        # Locate candidate files
        self.planner.locate_files(plan)

        # Review candidate files
        self.reviewer.review(plan)

        # AI analysis
        plan = self.repair_engine.repair(plan)

        plan = self.fixer.apply(plan)

        plan.pull_request = self.pr_generator.generate(plan)

        plan.completed = True

        return plan

    def load_workspace(
        self,
        plan: RepairPlan
    ):
        """
        Load repository metadata into the repair plan.
        """

        print("Loading workspace...")

        plan.workspace = self.tools.workspace_context(
            plan.repository
        )

    def add_candidate_file(
        self,
        plan: RepairPlan,
        file_path: str,
        reason: str
    ):
        """
        Manually add a candidate file.
        """

        candidate = FileCandidate(
            path=file_path,
            reason=reason
        )

        plan.candidate_files.append(candidate)

    def finish(
        self,
        plan: RepairPlan,
        summary: str
    ):
        """
        Mark the workflow as completed.
        """

        plan.summary = summary
        plan.completed = True

        return plan