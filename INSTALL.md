# Install the @2b-adrix GitHub dashboard

This package is designed for the profile repository `2b-adrix/2b-adrix`.

## Package layout

- `README.md` — terminal-style account dashboard.
- `.github/workflows/update-profile-dashboard.yml` — scheduled/manual refresh workflow.
- `scripts/profile_dashboard.py` — Python standard-library generator for SVG metrics and recent public activity.
- `assets/static/header.svg` — local dashboard header.
- `assets/static/badges/` — local social/contact badges.

The generator publishes `stats.svg`, `streak.svg`, `languages.svg`, `commit-clock.svg`, `contributions.svg`, and `milestones.svg` to the `output` branch.

## Installation

1. Download and extract this package.
2. Copy the package contents into the root of your existing `2b-adrix/2b-adrix` repository. Merge the `.github` directory; **do not delete your existing `.github/workflows/snake.yml`**.
3. Keep your existing banner file `1774850926972.png` if you want to preserve it elsewhere. The new README uses the included vector header instead.
4. Commit and push the files to `main`.
5. Open **Settings → Actions → General → Workflow permissions** in your profile repository.
6. Select **Read and write permissions**, then save.
7. Open **Actions → Update Profile Dashboard → Run workflow**.

The workflow refreshes automatically every 12 hours. The first run creates the `output` branch and publishes the cards.

## Tokens and privacy

No extra secret is needed for public repository statistics and public activity. The workflow uses the repository's `GITHUB_TOKEN`.

You can optionally configure a `PROFILE_TOKEN` repository secret for broader authenticated access. Never paste tokens into source files or the README. This generator uses public activity events; private events are not exposed.

## What the generated cards mean

- `stats.svg`: public non-fork repository count, stars/forks on those repositories, followers, and contribution totals from GitHub's contribution calendar.
- `streak.svg`: active-day and streak calculations from the contribution calendar.
- `languages.svg`: language bytes aggregated from owned public non-fork repositories.
- `commit-clock.svg`: UTC commit-hour histogram sampled from up to 15 recently pushed public repositories (up to 100 commits per repository). This is a sample, not a complete lifetime distribution.
- `contributions.svg`: daily contribution counts for the last 90 days.
- `milestones.svg`: public account/repository totals, not official GitHub achievement badges.
- Activity table: latest events returned by GitHub's public events API.

The contribution calendar and activity feed are different datasets. GitHub may delay contribution processing, and the public events endpoint has a limited history. Generated statistic cards do not depend on public third-party statistics-card services.
