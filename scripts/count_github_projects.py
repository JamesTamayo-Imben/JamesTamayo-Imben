import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


def main():
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
    if not owner:
        raise ValueError("GITHUB_REPOSITORY_OWNER is required")

    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "JamesTamayo-Imben-portfolio",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repos = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/users/{quote(owner, safe='')}/repos"
            f"?type=owner&per_page=100&page={page}"
        )
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=30) as response:
                page_repos = json.load(response)
        except (HTTPError, URLError) as error:
            raise RuntimeError(f"Unable to fetch GitHub repositories: {error}") from error

        if not isinstance(page_repos, list):
            raise ValueError("GitHub repository API returned an unexpected response")
        repos.extend(page_repos)
        if len(page_repos) < 100:
            break
        page += 1

    project_count = sum(
        1 for repo in repos
        if isinstance(repo, dict)
        and repo.get("fork") is False
        and repo.get("archived") is False
    )
    print(project_count)


if __name__ == "__main__":
    main()
