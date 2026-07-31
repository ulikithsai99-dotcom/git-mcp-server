import json

from .models import AnalysisResponse


class ResponseParser:
    """
    Parses the JSON returned by the LLM into
    AnalysisResponse objects.
    """

    def parse(
        self,
        response: str
    ) -> AnalysisResponse:

        try:

            data = json.loads(response)

        except json.JSONDecodeError as e:

            raise ValueError(
                f"Invalid JSON returned by LLM: {e}"
            )

        return AnalysisResponse(

            summary=data.get(
                "summary",
                ""
            ),

            root_cause=data.get(
                "root_cause",
                ""
            ),

            affected_files=data.get(
                "affected_files",
                []
            ),

            proposed_changes=data.get(
                "proposed_changes",
                []
            )
        )