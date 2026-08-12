import os

from github.repositories import list_repositories


def test_list_repositories():
    if not os.getenv("GITHUB_TOKEN"):
        print("GITHUB_TOKEN not set. Skipping repository test.")
        return

    repositories = list_repositories()

    assert isinstance(repositories, list)

    print(f"Repository test passed. Found {len(repositories)} repositories.")


if __name__ == "__main__":
    test_list_repositories()