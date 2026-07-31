from .llm import LLMProvider
from .models import (
    AIMessage,
    AnalysisRequest,
    AnalysisResponse
)
from .prompts import PromptLibrary


class Analyzer:
    """
    Builds prompts and sends repository analysis
    requests to the configured LLM.
    """

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def analyze(
    self,
    request: AnalysisRequest
) -> str:
        """
        Analyze the repository and return the LLM response.
        """

        candidate_files = (
            "\n".join(request.candidate_files)
            if request.candidate_files
            else "None"
        )

        reviewed_files = (
            "\n\n".join(
                f"### {path}\n{content}"
                for path, content in request.reviewed_files.items()
            )
            if request.reviewed_files
            else "None"
        )

        prompt = PromptLibrary.ANALYZE_REPOSITORY.format(
            repository=request.repository,
            issue=request.issue,
            workspace=request.workspace,
            candidate_files=candidate_files,
            reviewed_files=reviewed_files
        )

        messages = [
            AIMessage(
                role="system",
                content=PromptLibrary.SYSTEM
            ),
            AIMessage(
                role="user",
                content=prompt
            )
        ]

        return self.llm.generate(messages)