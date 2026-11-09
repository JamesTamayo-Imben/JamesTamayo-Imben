# GitHub project-count automation

The `Generate contribution snake` workflow refreshes the portfolio's project count and contribution graphic. It runs every 12 hours, on pushes to `main`, or when manually started.

## One-time setup

1. Push this repository, including `.github/workflows/snake.yml`, to the `main` branch.
2. In GitHub, open **Settings → Actions → General** and make sure Actions are enabled.
3. Under **Workflow permissions**, allow read and write access to repository contents. The workflow needs `contents: write` to update the generated SVGs on `main` and publish the contribution graphic to the `output` branch.
4. If `main` has branch protection rules, allow the `github-actions[bot]` workflow to push, or the generated count commit will be rejected.

No personal access token or extra repository secret is required. GitHub provides the workflow's `GITHUB_TOKEN`.

## What is counted

The workflow queries the repository owner's public GitHub repositories and counts repositories that are not forks and are not archived. The number is used in the portrait and Featured Projects SVGs. This is the account's repository count, not just the projects featured in the portfolio.

When the count changes, the workflow regenerates `assets/ascii-portrait.svg`, `assets/achievements.svg`, and `assets/full-readme.svg`, then commits those files to `main`. If nothing changed, it makes no count-update commit. It also publishes the contribution snake to the `output` branch.

## Run or check it

- To update now, open **Actions → Generate contribution snake → Run workflow** and select `main`.
- To check the result, open the run and review its steps. A successful count step prints the current number; the commit step reports whether any SVGs needed updating.
- To check the count locally, run:

  ```sh
  GITHUB_REPOSITORY_OWNER=JamesTamayo-Imben python3 scripts/count_github_projects.py
  ```

The local count script requires Python 3 and internet access to the GitHub API.
