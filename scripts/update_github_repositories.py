import json
import os
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


START_MARKER = "<!-- repositories:start -->"
END_MARKER = "<!-- repositories:end -->"
README_PATH = Path(__file__).resolve().parents[1] / "README.md"


def fetch_repositories(owner, token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "JamesTamayo-Imben-portfolio",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repositories = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/users/{quote(owner, safe='')}/repos"
            f"?type=owner&sort=updated&direction=desc&per_page=100&page={page}"
        )
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=30) as response:
                page_repositories = json.load(response)
        except (HTTPError, URLError) as error:
            raise RuntimeError(f"Unable to fetch GitHub repositories: {error}") from error

        if not isinstance(page_repositories, list) or not all(
            isinstance(repository, dict) for repository in page_repositories
        ):
            raise ValueError("GitHub repository API returned an unexpected response")
        repositories.extend(page_repositories)
        if len(page_repositories) < 100:
            break
        page += 1

    return [repository for repository in repositories if repository.get("private") is False]


def markdown_cell(value):
    text = str(value or "").replace("\\", "\\\\")
    text = text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")
    text = text.replace("<", "&lt;").replace(">", "&gt;").strip()
    return text or "—"


def repository_table(repositories):
    rows = [
        "### All public repositories (refreshed daily)",
        "",
        "| Repository | Description | Language | Stars | Last updated |",
        "| --- | --- | --- | ---: | --- |",
    ]

    repositories = sorted(
        repositories,
        key=lambda repository: datetime.fromisoformat(
            repository["updated_at"].replace("Z", "+00:00")
        ),
        reverse=True,
    )
    for repository in repositories:
        name = markdown_cell(repository["name"])
        url = repository["html_url"]
        updated = datetime.fromisoformat(
            repository["updated_at"].replace("Z", "+00:00")
        ).date().isoformat()
        rows.append(
            "| "
            + f"[{name}]({url}) | "
            + markdown_cell(repository.get("description"))
            + " | "
            + markdown_cell(repository.get("language"))
            + " | "
            + str(repository.get("stargazers_count", 0))
            + " | "
            + updated
            + " |"
        )

    if not repositories:
        rows.append("| _No public repositories found._ |  |  |  |  |")

    return "\n".join(rows)


def update_readme(repositories, readme_path=README_PATH):
    readme = readme_path.read_text(encoding="utf-8")
    if readme.count(START_MARKER) != 1 or readme.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one repository-index marker pair")

    start = readme.index(START_MARKER) + len(START_MARKER)
    end = readme.index(END_MARKER)
    if end < start:
        raise ValueError("README repository-index markers are out of order")

    updated = readme[:start] + "\n\n" + repository_table(repositories) + "\n\n" + readme[end:]
    if updated != readme:
        readme_path.write_text(updated, encoding="utf-8")


def main():
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
    if not owner:
        raise ValueError("GITHUB_REPOSITORY_OWNER is required")

    repositories = fetch_repositories(owner, os.environ.get("GITHUB_TOKEN"))
    update_readme(repositories)
    stars_total = sum(repository.get("stargazers_count", 0) for repository in repositories)
    print(f"repository_count={len(repositories)}")
    print(f"stars_total={stars_total}")


if __name__ == "__main__":
    main()
