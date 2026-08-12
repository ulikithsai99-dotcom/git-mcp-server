from intelligence.mock_provider import MockProvider
from intelligence.analyzer import Analyzer
from intelligence.repair_engine import RepairEngine

from agent.models import RepairPlan, FileCandidate


def test_repair_engine():
    plan = RepairPlan(
        repository="demo-repo",
        issue="Fix greeting"
    )

    plan.workspace = {
        "repository": "demo-repo"
    }

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

    assert plan.summary
    assert len(plan.proposed_changes) > 0

    change = plan.proposed_changes[0]

    assert change.file_path == "src/example.py"
    assert change.old_code == "print('Hello')"
    assert change.new_code == "print('Hello World')"

    print("Repair engine test passed.")


if __name__ == "__main__":
    test_repair_engine()