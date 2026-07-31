import json

from .llm import LLMProvider
from .models import AIMessage


class MockProvider(LLMProvider):
    """
    Mock LLM provider used for testing the
    complete workflow without calling a real LLM.
    """

    def generate(
        self,
        messages: list[AIMessage]
    ) -> str:

        response = {
            "summary": "Mock analysis completed.",

            "root_cause": (
                "This is a simulated response from the "
                "MockProvider."
            ),

            "affected_files": [
                "src/example.py"
            ],

            "proposed_changes": [
                {
                    "file_path": "src/example.py",

                    "old_code": "print('Hello')",

                    "new_code": "print('Hello World')",

                    "reason": (
                        "Demonstration change generated "
                        "by MockProvider."
                    )
                }
            ]
        }

        return json.dumps(response, indent=4)