"""Collect GitHub statistics with a handful of API calls."""

from __future__ import annotations

import json
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone

from .http import gh_graphql, gh_rest

PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    login name createdAt
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST, ISSUE, REPOSITORY]) { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestReviewContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}
"""

YEARS_QUERY = "query($login: String!) { user(login: $login) { contributionsCollection { contributionYears } } }"

REPOS_QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        stargazerCount
      }
    }
  }
}
"""


def _year_calendar_query(years: list[int]) -> str:
    parts = []
    for y in years:
        parts.append(
            f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") '
            "{ contributionCalendar { weeks { contributionDays { date contributionCount } } } }"
        )
    return "query($login: String!) { user(login: $login) { " + " ".join(parts) + " } }"


def fetch_profile(login: str) -> dict:
    return gh_graphql(PROFILE_QUERY, login=login)["user"]


def fetch_repos(login: str) -> tuple[int, list[dict]]:
    repos: list[dict] = []
    cursor, total = None, 0
    while True:
        data = gh_graphql(REPOS_QUERY, login=login, cursor=cursor)["user"]["repositories"]
        total = data["totalCount"]
        repos.extend(data["nodes"])
        if not data["pageInfo"]["hasNextPage"]:
            return total, repos
        cursor = data["pageInfo"]["endCursor"]


def fetch_all_days(login: str) -> dict[str, int]:
    """Daily contribution counts across every contribution year."""
    years = gh_graphql(YEARS_QUERY, login=login)["user"]["contributionsCollection"]["contributionYears"]
    days: dict[str, int] = {}
    if not years:
        return days
    data = gh_graphql(_year_calendar_query(sorted(years)), login=login)["user"]
    for coll in data.values():
        for week in coll["contributionCalendar"]["weeks"]:
            for d in week["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
    return days


def compute_streaks(days: dict[str, int], today: date) -> dict:
    ordered = sorted((date.fromisoformat(k), v) for k, v in days.items() if date.fromisoformat(k) <= today)
    total = sum(v for _, v in ordered)
    first = next((d for d, v in ordered if v > 0), today)

    longest = (0, None, None)
    run_len, run_start = 0, None
    for d, v in ordered:
        if v > 0:
            if run_len == 0:
                run_start = d
            run_len += 1
            if run_len > longest[0]:
                longest = (run_len, run_start, d)
        else:
            run_len = 0

    lookup = dict(ordered)
    cursor = today if lookup.get(today, 0) > 0 else today - timedelta(days=1)
    cur_end = cursor
    current = 0
    while lookup.get(cursor, 0) > 0:
        current += 1
        cursor -= timedelta(days=1)
    cur_start = cursor + timedelta(days=1)

    return {
        "total": total,
        "first": first,
        "today": today,
        "current": current,
        "current_range": (cur_start, cur_end) if current else None,
        "longest": longest[0],
        "longest_range": (longest[1], longest[2]) if longest[0] else None,
    }


def fetch_recent_commits(login: str, max_commits: int = 1000) -> list[dict]:
    """Most recent project commits authored by this account (excludes profile meta-repos)."""
    q = f"author:{login} -repo:{login}/{login} -repo:{login}/.github"
    import urllib.parse

    def page(n: int) -> dict:
        encoded = urllib.parse.urlencode({"q": q, "sort": "author-date", "order": "desc", "per_page": 100, "page": n})
        return gh_rest(f"search/commits?{encoded}")

    first = page(1)
    items = list(first.get("items", []))
    total = min(int(first.get("total_count", len(items))), max_commits)
    last_page = (total + 99) // 100
    if last_page > 1:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for res in pool.map(page, range(2, last_page + 1)):
                items.extend(res.get("items", []))
    return items


def compute_commit_clock(commits: list[dict]) -> dict:
    """Hour/weekday histogram in the author's local time."""
    hours = [0] * 24
    weekdays = [0] * 7
    for item in commits:
        stamp = datetime.fromisoformat(item["commit"]["author"]["date"].replace("Z", "+00:00"))
        hours[stamp.hour] += 1
        weekdays[stamp.weekday()] += 1
    return {"hours": hours, "weekdays": weekdays, "sample": len(commits)}


def fetch_repo_languages(full_names: list[str]) -> dict[str, list[dict]]:
    """Language byte breakdown for the given repos, 50 per aliased GraphQL query."""
    result: dict[str, list[dict]] = {}
    for i in range(0, len(full_names), 50):
        chunk = full_names[i : i + 50]
        parts = []
        for j, full in enumerate(chunk):
            owner, name = full.split("/", 1)
            parts.append(
                f'r{j}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) '
                "{ languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }"
            )
        data = gh_graphql("query { " + " ".join(parts) + " }", allow_partial=True)
        for j, full in enumerate(chunk):
            repo = data.get(f"r{j}")
            if repo:
                result[full] = repo["languages"]["edges"]
    return result


def compute_languages(commits: list[dict], repo_langs: dict[str, list[dict]], exclude: set[str], top: int = 8) -> list[dict]:
    """Languages weighted by commit count across repositories."""
    per_repo = Counter(item["repository"]["full_name"] for item in commits)
    scores: Counter[str] = Counter()
    colors: dict[str, str] = {}
    for repo, n_commits in per_repo.items():
        edges = [e for e in repo_langs.get(repo, []) if e["node"]["name"].lower() not in exclude]
        repo_total = sum(e["size"] for e in edges)
        if not repo_total:
            continue
        for e in edges:
            name = e["node"]["name"]
            scores[name] += n_commits * e["size"] / repo_total
            colors[name] = e["node"]["color"] or "#8b949e"
    total = sum(scores.values()) or 1
    langs = [{"name": n, "size": s, "pct": s * 100 / total, "color": colors[n]} for n, s in scores.most_common(top)]
    rest = total - sum(l["size"] for l in langs)
    if len(scores) > top and rest > 0:
        langs.append({"name": "Other", "size": rest, "pct": rest * 100 / total, "color": "#4b5563"})
    return langs


def _exp_cdf(x: float) -> float:
    return 1 - 2 ** (-x)


def _lognorm_cdf(x: float) -> float:
    return x / (1 + x)


def compute_rank(*, commits: int, prs: int, issues: int, reviews: int, stars: int, followers: int) -> dict:
    weights = {"commits": 2, "prs": 3, "issues": 1, "reviews": 1, "stars": 4, "followers": 1}
    score = (
        weights["commits"] * _exp_cdf(commits / 250)
        + weights["prs"] * _exp_cdf(prs / 50)
        + weights["issues"] * _exp_cdf(issues / 25)
        + weights["reviews"] * _exp_cdf(reviews / 2)
        + weights["stars"] * _lognorm_cdf(stars / 50)
        + weights["followers"] * _lognorm_cdf(followers / 10)
    ) / sum(weights.values())
    percentile = (1 - score) * 100
    for threshold, level in ((1, "S"), (12.5, "A+"), (25, "A"), (37.5, "A-"), (50, "B+"), (62.5, "B"), (75, "B-"), (87.5, "C+")):
        if percentile <= threshold:
            return {"level": level, "percentile": percentile}
    return {"level": "C", "percentile": percentile}


TROPHY_TIERS = ("SSS", "SS", "S", "AAA", "AA", "A", "B", "C")
TROPHY_THRESHOLDS = {
    "Contributions": (20000, 10000, 5000, 2500, 1000, 500, 100, 1),
    "Stars": (2000, 700, 200, 100, 50, 30, 10, 1),
    "Followers": (1000, 400, 200, 100, 50, 20, 10, 1),
    "Repositories": (200, 150, 100, 70, 50, 30, 10, 1),
    "Pull Requests": (1000, 500, 200, 100, 50, 20, 10, 1),
    "Issues": (1000, 500, 200, 100, 50, 20, 10, 1),
    "Reviews": (300, 150, 70, 45, 20, 8, 3, 1),
    "Experience": (15, 10, 8, 6, 4, 3, 2, 1),
}


def trophy_tier(category: str, value: float) -> str | None:
    for tier, threshold in zip(TROPHY_TIERS, TROPHY_THRESHOLDS[category]):
        if value >= threshold:
            return tier
    return None


def collect(login: str) -> dict:
    today = datetime.now(timezone.utc).date()
    exclude = {x.strip().lower() for x in os.environ.get("LANG_EXCLUDE", "").split(",") if x.strip()}

    with ThreadPoolExecutor(max_workers=4) as pool:
        f_profile = pool.submit(fetch_profile, login)
        f_days = pool.submit(fetch_all_days, login)
        f_repos = pool.submit(fetch_repos, login)
        f_commits = pool.submit(fetch_recent_commits, login)
        profile, days, commits = f_profile.result(), f_days.result(), f_commits.result()
        repo_langs = fetch_repo_languages(sorted({c["repository"]["full_name"] for c in commits}))
        repo_total, repo_nodes = f_repos.result()
    cc = profile["contributionsCollection"]
    stars = sum(r["stargazerCount"] for r in repo_nodes)

    recent = [
        (d["date"], d["contributionCount"])
        for w in cc["contributionCalendar"]["weeks"]
        for d in w["contributionDays"]
        if date.fromisoformat(d["date"]) <= today
    ]

    stats = {
        "login": profile["login"],
        "name": profile["name"] or profile["login"],
        "stars": stars,
        "contrib_year": cc["contributionCalendar"]["totalContributions"],
        "commits_year": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "reviews_year": cc["totalPullRequestReviewContributions"],
        "prs": profile["pullRequests"]["totalCount"],
        "issues": profile["issues"]["totalCount"],
        "contributed_to": profile["repositoriesContributedTo"]["totalCount"],
        "followers": profile["followers"]["totalCount"],
        "repos": repo_total,
        "years": (today - datetime.fromisoformat(profile["createdAt"].replace("Z", "+00:00")).date()).days / 365.25,
    }
    stats["rank"] = compute_rank(
        commits=stats["commits_year"],
        prs=stats["prs"],
        issues=stats["issues"],
        reviews=stats["reviews_year"],
        stars=stats["stars"],
        followers=stats["followers"],
    )
    streak = compute_streaks(days, today)
    stats["contrib_all"] = streak["total"]

    return {
        "stats": stats,
        "streak": streak,
        "recent_days": recent,
        "languages": compute_languages(commits, repo_langs, exclude),
        "clock": compute_commit_clock(commits),
    }
