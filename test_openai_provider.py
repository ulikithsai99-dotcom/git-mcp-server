from intelligence.models import AIMessage
from intelligence.openai_provider import OpenAIProvider

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

print(response)