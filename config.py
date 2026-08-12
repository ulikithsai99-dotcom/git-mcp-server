import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

USERNAME = os.getenv(
    "GITHUB_USERNAME",
    "ulikithsai99-dotcom"
)

if not TOKEN:
    raise RuntimeError(
        "GITHUB_TOKEN environment variable is not set."
    )

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}