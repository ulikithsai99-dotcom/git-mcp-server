from abc import ABC, abstractmethod

from .models import AIMessage


class LLMProvider(ABC):
    """
    Base interface for all Large Language Model providers.

    Implementations may include:
    - OpenAI
    - Claude
    - Gemini
    - Ollama
    - Groq
    - DeepSeek
    """

    @abstractmethod
    def generate(
        self,
        messages: list[AIMessage]
    ) -> str:
        """
        Send the conversation to the LLM and return
        the raw text response.

        The response is expected to be a JSON string,
        which will later be parsed by ResponseParser.
        """
        raise NotImplementedError