import os
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Read the GitHub token
token = os.getenv("GITHUB_TOKEN")

if not token:
    print("❌ GitHub token not found!")
    exit()

# Request headers
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# Call the GitHub API
response = requests.get(
    "https://api.github.com/user/repos",
    headers=headers
)

if response.status_code == 200:
    repos = response.json()

    print("\n📂 Your Repositories\n")

    for i, repo in enumerate(repos, start=1):
        print(f"{i}. {repo['name']}")
        print(f"   ⭐ Stars : {repo['stargazers_count']}")
        print(f"   🌐 Visibility : {repo['visibility']}")
        print(f"   🔗 URL : {repo['html_url']}")
        print()

else:
    print(response.status_code)
    print(response.text)