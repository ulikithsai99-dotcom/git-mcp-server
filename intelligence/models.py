from dataclasses import dataclass, field
from typing import List


@dataclass
class AIMessage:
    role: str
    content: str


@dataclass
class AnalysisRequest:
    """
    Information required for repository analysis.
    """

    repository: str
    issue: str

    workspace: dict

    candidate_files: List[str]

    reviewed_files: dict


@dataclass
class AnalysisResponse:
    """
    Structured analysis returned by the parser.
    """

    summary: str

    root_cause: str

    affected_files: List[str] = field(default_factory=list)

    proposed_changes: List[dict] = field(default_factory=list)