from intelligence.mock_provider import MockProvider
from intelligence.analyzer import Analyzer
from intelligence.repair_engine import RepairEngine

from agent.models import RepairPlan, FileCandidate


plan = RepairPlan(
    repository="demo-repo",
    issue="Fix greeting"
)

plan.workspace = "Mock workspace"

plan.candidate_files.append(
    FileCandidate(
        path="src/example.py",
        reason="Contains greeting"
    )
)

plan.reviewed_files = {
    "src/example.py": "print('Hello')"
}

engine = RepairEngine(
    Analyzer(
        MockProvider()
    )
)

plan = engine.repair(plan)

print("\nSummary:")
print(plan.summary)

print("\nProposed Changes:")
for change in plan.proposed_changes:
    print(change)