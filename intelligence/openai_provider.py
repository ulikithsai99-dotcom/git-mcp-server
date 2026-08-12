import os

from openai import OpenAI

from .llm import LLMProvider
from .models import AIMessage


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of the LLMProvider interface.
    """

    def __init__(
        self,
        model: str | None = None
    ):
        api_key = os.getenv("OPENAI_API_KEY")

        if model is None:
            model = os.getenv(
        "OPENAI_MODEL",
        "gpt-5"
    )

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = model

    def generate(
        self,
        messages: list[AIMessage]
    ) -> str:

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ],
        )

        return response.output_text