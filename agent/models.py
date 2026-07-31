from dataclasses import dataclass, field
from typing import Any


@dataclass
class FileCandidate:
    """
    A file that may contain the root cause of the issue.
    """

    path: str
    reason: str


@dataclass
class ProposedChange:
    """
    A single code modification proposed by the AI.
    """

    file_path: str
    old_code: str
    new_code: str
    reason: str = ""


@dataclass
class RepairPlan:
    """
    Shared state passed through the complete workflow.
    """

    repository: str
    issue: str

    # Repository context
    workspace: dict = field(default_factory=dict)

    # Planner
    candidate_files: list[FileCandidate] = field(default_factory=list)

    # Reviewer
    reviewed_files: dict[str, str] = field(default_factory=dict)

    # Intelligence
    summary: str = ""
    proposed_changes: list[ProposedChange] = field(default_factory=list)

    # Fixer
    fix_results: list[Any] = field(default_factory=list)

    # Pull Request
    pull_request: Any = None

    # Workflow state
    completed: bool = False