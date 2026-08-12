import os

from intelligence.models import AIMessage
from intelligence.openai_provider import OpenAIProvider


def test_openai_provider():
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set. Skipping OpenAI provider test.")
        return

    provider = OpenAIProvider()

    messages = [
        AIMessage(
            role="system",
            content="You are a helpful assistant."
        ),
        AIMessage(
            role="user",
            content="Reply with exactly: Hello from OpenAI!"
        )
    ]

    response = provider.generate(messages)

    assert response
    print("OpenAI provider test passed.")


if __name__ == "__main__":
    test_openai_provider()