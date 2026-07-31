import requests
from config import HEADERS


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def get(self, endpoint, params=None):
        """
        Send a GET request to the GitHub API.
        """

        url = f"{self.BASE_URL}{endpoint}"

        response = requests.get(
            url,
            headers=HEADERS,
            params=params
        )

        if response.status_code == 200:
            return response.json()

        raise Exception(
            f"GitHub API Error {response.status_code}: {response.text}"
        )

    def post(self, endpoint, data):
        """
        Send a POST request to the GitHub API.
        """

        url = f"{self.BASE_URL}{endpoint}"

        response = requests.post(url, headers=HEADERS, json=data)

        if response.status_code in [200, 201]:
            return response.json()

        raise Exception(
            f"GitHub API Error {response.status_code}: {response.text}"
        )
    
    def put(self, endpoint, data, params=None):
        """
        Send a PUT request to the GitHub API.
        """

        url = f"{self.BASE_URL}{endpoint}"

        response = requests.put(
    url,
    headers=HEADERS,
    json=data,
    params=params
)

        if response.status_code not in [200, 201]:
            raise Exception(
                f"GitHub API Error {response.status_code}: {response.text}"
            )

        return response.json()

# Create a reusable GitHub client instance
client = GitHubClient()    