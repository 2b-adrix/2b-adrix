#!/usr/bin/env python3
"""Generate self-hosted SVG cards and recent activity for @2b-adrix."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path
from typing import Any

USER = os.environ.get("GH_USER", "2b-adrix")
TOKEN = os.environ.get("GH_TOKEN", "")
OUT = Path(os.environ.get("OUTPUT_DIR", "output"))
API = "https://api.github.com"
BG, PANEL, BORDER = "#0d1117", "#161b22", "#30363d"
TEXT, MUTED = "#e6edf3", "#8b949e"
CYAN, GREEN, BLUE, PURPLE, ORANGE = "#22d3ee", "#3fb950", "#58a6ff", "#bc8cff", "#f0883e"


def api_json(url: str, payload: dict[str, Any] | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "2b-adrix-profile-dashboard",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload is not None else None
    if payload is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"GitHub API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"GitHub API connection failed: {exc.reason}") from exc


def rest(path: str) -> Any:
    return api_json(API + path)


def get_repositories() -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    for page in range(1, 11):
        batch = rest(
            f"/users/{urllib.parse.quote(USER)}/repos"
            f"?type=owner&sort=updated&per_page=100&page={page}"
        )
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected GitHub repositories response.")
        repos.extend(
            repo for repo in batch
            if not repo.get("private", False) and not repo.get("fork", False)
        )
        if len(batch) < 100:
            break
    return repos


def get_contributions(start: datetime, end: datetime) -> dict[str, Any]:
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          contributionCalendar {
            totalContributions
            weeks { contributionDays { contributionCount date weekday } }
          }
        }
      }
    }
    """
    variables = {
        "login": USER,
        "from": start.isoformat().replace("+00:00", "Z"),
        "to": end.isoformat().replace("+00:00", "Z"),
    }
    result = api_json("https://api.github.com/graphql", {"query": query, "variables": variables})
    if result.get("errors"):
        raise RuntimeError("GitHub GraphQL: " + json.dumps(result["errors"])[:900])
    user = result.get("data", {}).get("user")
    if not user:
        raise RuntimeError("Could not read the contribution calendar for " + USER)
    return user["contributionsCollection"]


def get_languages(repos: list[dict[str, Any]]) -> Counter[str]:
    totals: Counter[str] = Counter()
    for repo in repos:
        full_name = repo.get("full_name")
        if not full_name:
            continue
        try:
            values = rest(f"/repos/{urllib.parse.quote(full_name, safe='/')}/languages")
            if isinstance(values, dict):
                totals.update({name: int(size) for name, size in values.items()})
        except RuntimeError as exc:
            print(f"Warning: language data skipped for {full_name}: {exc}", file=sys.stderr)
    return totals


def get_commit_hours(repos: list[dict[str, Any]], since: datetime) -> Counter[int]:
    """Sample commit timestamps from the 15 most recently pushed public repositories."""
    counts: Counter[int] = Counter()
    candidates = []
    for repo in repos:
        pushed = repo.get("pushed_at")
        if not pushed:
            continue
        try:
            pushed_at = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
        except ValueError:
            continue
        if pushed_at >= since:
            candidates.append(repo)

    for repo in candidates[:15]:
        name = urllib.parse.quote(repo["full_name"], safe="/")
        url = (
            f"{API}/repos/{name}/commits?author={urllib.parse.quote(USER)}"
            f"&since={urllib.parse.quote(since.isoformat())}&per_page=100"
        )
        try:
            commits = api_json(url)
            for commit in commits if isinstance(commits, list) else []:
                stamp = (
                    commit.get("commit", {}).get("author", {}).get("date")
                    or commit.get("commit", {}).get("committer", {}).get("date")
                )
                if stamp:
                    counts[datetime.fromisoformat(stamp.replace("Z", "+00:00")).hour] += 1
        except (RuntimeError, ValueError, KeyError) as exc:
            print(f"Warning: commit sample skipped for {repo['full_name']}: {exc}", file=sys.stderr)
    return counts


def get_events() -> list[dict[str, Any]]:
    events = rest(f"/users/{urllib.parse.quote(USER)}/events/public?per_page=100")
    return events if isinstance(events, list) else []


def header(width: int, height: int, title: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<rect width="{width}" height="{height}" rx="16" fill="{BG}"/>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="15" fill="none" stroke="{BORDER}"/>
<circle cx="24" cy="25" r="5" fill="{GREEN}"/>
<text x="40" y="30" fill="{MUTED}" font-family="Consolas,monospace" font-size="12">{escape(title)}</text>
"""


def label(x: float, y: float, value: str, size: int = 13, color: str = TEXT,
          weight: str = "400", anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" '
        f'font-family="Consolas,monospace" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'
    )


def box(x: float, y: float, width: float, height: float, color: str,
        radius: int = 9, opacity: float = 1) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{radius}" fill="{color}" opacity="{opacity:.2f}"/>'
    )


def save(name: str, content: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content + "</svg>\n", encoding="utf-8")


def flatten_days(collection: dict[str, Any]) -> list[dict[str, Any]]:
    days = []
    weeks = collection.get("contributionCalendar", {}).get("weeks", [])
    for week in weeks:
        days.extend(week.get("contributionDays", []))
    return sorted(days, key=lambda item: item.get("date", ""))


def streak_numbers(days: list[dict[str, Any]]) -> tuple[int, int, int]:
    counts = [int(day.get("contributionCount", 0)) for day in days]
    best = run = active = 0
    for count in counts:
        if count:
            run += 1
            active += 1
            best = max(best, run)
        else:
            run = 0

    current = 0
    scan = list(days)
    if scan and scan[-1].get("date") == date.today().isoformat() and not int(scan[-1].get("contributionCount", 0)):
        scan.pop()
    for day in reversed(scan):
        if int(day.get("contributionCount", 0)):
            current += 1
        else:
            break
    return current, best, active


def make_stats(user: dict[str, Any], repos: list[dict[str, Any]], collection: dict[str, Any]) -> None:
    calendar = collection["contributionCalendar"]
    values = [
        ("PUBLIC REPOSITORIES", len(repos), CYAN),
        ("STARS RECEIVED", sum(int(repo.get("stargazers_count", 0)) for repo in repos), PURPLE),
        ("FORKS RECEIVED", sum(int(repo.get("forks_count", 0)) for repo in repos), GREEN),
        ("FOLLOWERS", int(user.get("followers", 0)), ORANGE),
        ("CONTRIBUTIONS / YEAR", int(calendar.get("totalContributions", 0)), CYAN),
        ("COMMITS / YEAR", int(collection.get("totalCommitContributions", 0)), GREEN),
        ("PULL REQUESTS", int(collection.get("totalPullRequestContributions", 0)), PURPLE),
        ("ISSUE CONTRIBUTIONS", int(collection.get("totalIssueContributions", 0)), ORANGE),
    ]
    out = [header(920, 330, f"ACCOUNT STATS / {USER}")]
    for i, (name, value, color) in enumerate(values):
        col, row = i % 4, i // 4
        x, y = 20 + col * 225, 58 + row * 132
        out += [box(x, y, 208, 112, PANEL), box(x + 15, y + 17, 4, 72, color, 2),
                label(x + 32, y + 43, f"{value:,}", 27, TEXT, "700"),
                label(x + 32, y + 70, name, 10, MUTED, "600"),
                label(x + 32, y + 92, "LIVE API DATA", 9, color)]
    out.append(label(895, 313, "github.com/2b-adrix", 10, MUTED, anchor="end"))
    save("stats.svg", "".join(out))


def make_streak(days: list[dict[str, Any]], collection: dict[str, Any]) -> None:
    current, best, active = streak_numbers(days)
    total = int(collection.get("contributionCalendar", {}).get("totalContributions", 0))
    metrics = [
        ("CURRENT STREAK", f"{current} days", CYAN),
        ("LONGEST STREAK", f"{best} days", PURPLE),
        ("ACTIVE DAYS", f"{active} days", GREEN),
        ("CONTRIBUTIONS", f"{total:,}", ORANGE),
    ]
    out = [header(920, 205, f"CONTRIBUTION STREAK / {USER}")]
    for i, (name, value, color) in enumerate(metrics):
        x = 20 + i * 225
        out += [box(x, 62, 208, 105, PANEL), label(x+18, 106, value, 25, color, "700"),
                label(x+18, 136, name, 10, MUTED, "600")]
    out.append(label(895, 188, "Based on GitHub contribution calendar", 9, MUTED, anchor="end"))
    save("streak.svg", "".join(out))


def make_languages(languages: Counter[str]) -> None:
    colors = [CYAN, BLUE, PURPLE, GREEN, ORANGE, "#f778ba", "#d2a8ff"]
    top = languages.most_common(7)
    total = sum(languages.values()) or 1
    out = [header(920, 310, "LANGUAGES / OWNED PUBLIC REPOSITORIES")]
    if not top:
        out.append(label(28, 100, "No language data was returned by GitHub.", 14, MUTED))
    for i, (name, value) in enumerate(top):
        y = 80 + i * 30
        share = value / total
        out += [label(28, y, name, 13, TEXT, "600"), box(210, y-13, 570, 13, PANEL, 6),
                box(210, y-13, 570*share, 13, colors[i % len(colors)], 6),
                label(890, y, f"{share*100:.1f}%", 12, MUTED, anchor="end")]
    out.append(label(28, 290, "Language byte counts aggregated through GitHub's repository languages API.", 9, MUTED))
    save("languages.svg", "".join(out))


def make_commit_clock(hours: Counter[int]) -> None:
    maximum = max(hours.values(), default=1)
    out = [header(920, 310, "COMMIT CLOCK / UTC")]
    x0, y0, width = 35, 75, 850
    out.append(box(x0, y0, width, 165, PANEL, 10))
    slot = width / 24
    for hour in range(24):
        value = hours.get(hour, 0)
        bar_height = max(2, (value / maximum) * 112) if value else 2
        x = x0 + hour * slot + 7
        y = y0 + 128 - bar_height
        out.append(box(x, y, slot-13, bar_height, CYAN if value else BORDER, 4, .95 if value else .55))
        if hour % 2 == 0:
            out.append(label(x+(slot-13)/2, 263, f"{hour:02d}", 9, MUTED, anchor="middle"))
    out.append(label(35, 292, f"{sum(hours.values())} commits sampled across up to 15 recently pushed public repositories", 9, MUTED))
    out.append(label(885, 55, "24-HOUR DISTRIBUTION", 9, CYAN, anchor="end"))
    save("commit-clock.svg", "".join(out))


def make_contributions(days: list[dict[str, Any]]) -> None:
    recent = days[-90:]
    max_count = max((int(day.get("contributionCount", 0)) for day in recent), default=1) or 1
    out = [header(1000, 250, "CONTRIBUTIONS / LAST 90 DAYS")]
    x0, y0, width = 28, 75, 944
    out.append(box(x0, y0, width, 115, PANEL, 10))
    slot = width / max(len(recent), 1)
    for i, day in enumerate(recent):
        count = int(day.get("contributionCount", 0))
        bar_height = max(2, count / max_count * 84) if count else 2
        x = x0 + i * slot + 1
        y = y0 + 94 - bar_height
        color = CYAN if count else BORDER
        title = escape(f"{day.get('date', '')}: {count} contributions")
        out.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{max(1, slot-2):.2f}" '
            f'height="{bar_height:.2f}" rx="2" fill="{color}"><title>{title}</title></rect>'
        )
    if recent:
        out += [label(x0, 218, recent[0].get("date", ""), 10, MUTED),
                label(x0+width, 218, recent[-1].get("date", ""), 10, MUTED, anchor="end")]
    total = sum(int(day.get("contributionCount", 0)) for day in recent)
    out.append(label(500, 238, f"{total:,} contributions in the displayed period", 10, CYAN, anchor="middle"))
    save("contributions.svg", "".join(out))


def make_milestones(user: dict[str, Any], repos: list[dict[str, Any]]) -> None:
    values = [
        ("PUBLIC REPOSITORIES", len(repos)),
        ("STARS ON OWNED REPOS", sum(int(r.get("stargazers_count", 0)) for r in repos)),
        ("FORKS ON OWNED REPOS", sum(int(r.get("forks_count", 0)) for r in repos)),
        ("FOLLOWERS", int(user.get("followers", 0))),
    ]
    out = [header(1000, 170, "ACCOUNT MILESTONES / PUBLIC DATA")]
    for i, (name, value) in enumerate(values):
        x = 25 + i * 245
        out += [box(x, 62, 225, 75, PANEL), label(x+15, 99, f"{value:,}", 22, CYAN if i % 2 == 0 else PURPLE, "700"),
                label(x+15, 122, name, 9, MUTED, "600")]
    save("milestones.svg", "".join(out))


def activity_row(event: dict[str, Any]) -> tuple[str, str, str] | None:
    try:
        when = datetime.fromisoformat(event.get("created_at", "").replace("Z", "+00:00")).strftime("%b %d")
    except ValueError:
        when = "Recent"
    repo = event.get("repo", {}).get("name", "")
    data = event.get("payload", {}) or {}
    kind = event.get("type", "")
    if kind == "PushEvent":
        branch = (data.get("ref") or "").replace("refs/heads/", "")
        count = data.get("size") or len(data.get("commits", []))
        icon, action = "⬆️", f"Pushed {count or 'updates'} commit(s) to `{branch or 'branch'}`"
    elif kind == "PullRequestEvent":
        pr = data.get("pull_request", {})
        icon = "🔀"
        action = f"{data.get('action', 'updated').capitalize()} PR #{pr.get('number', '?')}: {pr.get('title', 'Pull request')}"
    elif kind == "IssuesEvent":
        issue = data.get("issue", {})
        icon = "🐛"
        action = f"{data.get('action', 'updated').capitalize()} issue #{issue.get('number', '?')}: {issue.get('title', 'Issue')}"
    elif kind == "IssueCommentEvent":
        icon = "💬"
        action = f"Commented on issue / PR #{data.get('issue', {}).get('number', '?')}"
    elif kind == "CreateEvent":
        icon = "✨"
        action = f"Created {data.get('ref_type', 'repository')} `{data.get('ref') or repo}`"
    elif kind == "ReleaseEvent":
        icon = "🚀"
        action = f"Published release `{data.get('release', {}).get('tag_name', '')}`"
    elif kind == "WatchEvent":
        icon, action = "⭐", "Starred a repository"
    elif kind == "ForkEvent":
        icon, action = "🍴", "Forked a repository"
    elif kind == "DeleteEvent":
        icon = "🗑️"
        action = f"Deleted {data.get('ref_type', 'reference')} `{data.get('ref', '')}`"
    else:
        return None
    link = f"[{repo}](https://github.com/{repo})" if repo else "GitHub"
    action = action.replace("|", "\\|").replace("\n", " ").replace("\r", " ")
    return when, icon, f"{action} in {link}"


def refresh_activity(events: list[dict[str, Any]]) -> None:
    start, end = "<!--START_SECTION:activity-->", "<!--END_SECTION:activity-->"
    path = Path("README.md")
    readme = path.read_text(encoding="utf-8")
    if start not in readme or end not in readme:
        raise RuntimeError("README.md activity markers are missing.")
    rows, seen = [], set()
    for event in events:
        row = activity_row(event)
        if row and row not in seen:
            rows.append(row)
            seen.add(row)
        if len(rows) == 8:
            break
    table = ["| When | | What |", "| :-- | :-: | :-- |"]
    if rows:
        table += [f"| `{when}` | {icon} | {what} |" for when, icon, what in rows]
    else:
        table.append("| `No recent event` | ◌ | No public activity was returned by GitHub's recent events API. |")
    before, rest_text = readme.split(start, 1)
    _, after = rest_text.split(end, 1)
    path.write_text(before + start + "\n" + "\n".join(table) + "\n" + end + after, encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=365)
    user = rest(f"/users/{urllib.parse.quote(USER)}")
    repos = get_repositories()
    collection = get_contributions(since, now)
    days = flatten_days(collection)
    languages = get_languages(repos)
    hours = get_commit_hours(repos, since)
    events = get_events()

    OUT.mkdir(parents=True, exist_ok=True)
    make_stats(user, repos, collection)
    make_streak(days, collection)
    make_languages(languages)
    make_commit_clock(hours)
    make_contributions(days)
    make_milestones(user, repos)
    refresh_activity(events)

    print(f"Generated profile dashboard for @{USER}")
    print(f"Included {len(repos)} owned public non-fork repositories.")
    print(f"Wrote SVG cards to {OUT.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
