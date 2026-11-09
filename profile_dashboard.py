#!/usr/bin/env python3
"""Build self-hosted GitHub profile cards and refresh the README activity table.

Dependencies: Python standard library only.
Environment:
  GH_USER       GitHub login (defaults to 2b-adrix)
  GH_TOKEN      GitHub token for REST + GraphQL access
  OUTPUT_DIR    SVG output directory (defaults to ./out)
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path
from typing import Any

USER = os.environ.get("GH_USER", "2b-adrix")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
OUT = Path(os.environ.get("OUTPUT_DIR", "out"))
API = "https://api.github.com"

BG = "#0b1020"
PANEL = "#111a2e"
PANEL_2 = "#17233b"
BORDER = "#263653"
TEXT = "#e7eefb"
MUTED = "#8ea1bd"
CYAN = "#44d7e8"
BLUE = "#6ea8fe"
PURPLE = "#b69cff"
GREEN = "#59d499"
ORANGE = "#ffbd69"
PINK = "#f28ab2"


def api_json(url: str, payload: dict[str, Any] | None = None, *, attempts: int = 3) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "2b-adrix-profile-dashboard",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    if payload is not None:
        headers["Content-Type"] = "application/json"
    last_error: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=35) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:900]
            if exc.code in (429, 500, 502, 503, 504) and attempt < attempts - 1:
                last_error = RuntimeError(f"GitHub API HTTP {exc.code}: {detail}")
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"GitHub API HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < attempts - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"GitHub API request failed: {last_error}")


def rest(path: str) -> Any:
    return api_json(f"{API}/{path.lstrip('/')}")


def graphql(query: str, variables: dict[str, Any]) -> Any:
    result = api_json("https://api.github.com/graphql", {"query": query, "variables": variables})
    if result.get("errors"):
        raise RuntimeError("GitHub GraphQL error: " + json.dumps(result["errors"])[:900])
    data = result.get("data") or {}
    if not data.get("user"):
        raise RuntimeError(f"GitHub GraphQL did not return user @{USER}; check PROFILE_TOKEN permissions.")
    return data["user"]


def fetch_profile() -> dict[str, Any]:
    user = rest(f"users/{urllib.parse.quote(USER)}")
    if not isinstance(user, dict) or user.get("login", "").lower() != USER.lower():
        raise RuntimeError(f"Could not retrieve GitHub profile for @{USER}.")
    return user


def fetch_repositories() -> list[dict[str, Any]]:
    repositories: list[dict[str, Any]] = []
    for page in range(1, 11):
        batch = rest(
            f"users/{urllib.parse.quote(USER)}/repos?type=owner&sort=updated&per_page=100&page={page}"
        )
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected response while fetching repositories.")
        repositories.extend(
            item for item in batch
            if not item.get("private", False) and not item.get("fork", False)
        )
        if len(batch) < 100:
            break
    return repositories


def fetch_contributions(start: datetime, end: datetime) -> dict[str, Any]:
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalPullRequestReviewContributions
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
    user = graphql(query, variables)
    return user["contributionsCollection"]


def fetch_one_language_repo(full_name: str) -> dict[str, int]:
    encoded = urllib.parse.quote(full_name, safe="/")
    response = rest(f"repos/{encoded}/languages")
    return response if isinstance(response, dict) else {}


def fetch_languages(repositories: list[dict[str, Any]]) -> Counter[str]:
    totals: Counter[str] = Counter()
    names = [r["full_name"] for r in repositories if r.get("full_name")]
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_one_language_repo, name): name for name in names}
        for future in as_completed(futures):
            name = futures[future]
            try:
                totals.update({k: int(v) for k, v in future.result().items()})
            except Exception as exc:  # one repository's language endpoint must not block the dashboard
                print(f"Warning: skipped language data for {name}: {exc}", file=sys.stderr)
    return totals


def fetch_commit_sample(start: datetime, max_pages: int = 4) -> list[dict[str, Any]]:
    """Sample up to 400 recent public commits authored by this account."""
    query = f"author:{USER} author-date:>={start.date().isoformat()}"

    def get_page(page: int) -> list[dict[str, Any]]:
        encoded = urllib.parse.urlencode({
            "q": query, "sort": "author-date", "order": "desc", "per_page": 100, "page": page
        })
        data = rest(f"search/commits?{encoded}")
        return data.get("items", []) if isinstance(data, dict) else []

    items: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(get_page, p) for p in range(1, max_pages + 1)]
        for future in as_completed(futures):
            try:
                items.extend(future.result())
            except Exception as exc:
                print(f"Warning: commit sample request failed: {exc}", file=sys.stderr)
    # Search pages can arrive in any order; keep one copy of each SHA and sort newest first.
    unique: dict[str, dict[str, Any]] = {}
    for item in items:
        sha = item.get("sha")
        if sha:
            unique[sha] = item
    return sorted(
        unique.values(),
        key=lambda x: (x.get("commit", {}).get("author", {}).get("date") or ""),
        reverse=True,
    )


def fetch_public_events() -> list[dict[str, Any]]:
    events = rest(f"users/{urllib.parse.quote(USER)}/events/public?per_page=100")
    return events if isinstance(events, list) else []


def flatten_days(collection: dict[str, Any]) -> list[dict[str, Any]]:
    days: list[dict[str, Any]] = []
    for week in collection.get("contributionCalendar", {}).get("weeks", []):
        days.extend(week.get("contributionDays", []))
    return sorted(days, key=lambda x: x.get("date", ""))


def streak_values(days: list[dict[str, Any]]) -> tuple[int, int, int, int]:
    ordered = [(date.fromisoformat(d["date"]), int(d.get("contributionCount", 0))) for d in days if d.get("date")]
    if not ordered:
        return 0, 0, 0, 0
    today = date.today()
    # GitHub may not yet have a contribution count for the current day.
    current_scan = list(ordered)
    if current_scan[-1][0] == today and current_scan[-1][1] == 0:
        current_scan.pop()
    current = 0
    for _, count in reversed(current_scan):
        if count > 0:
            current += 1
        else:
            break
    best = run = active = total = 0
    for _, count in ordered:
        total += count
        if count:
            run += 1
            active += 1
            best = max(best, run)
        else:
            run = 0
    return current, best, active, total


def svg_header(width: int, height: int, title: str, subtitle: str = "") -> list[str]:
    bits = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
        '<defs><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#44d7e8"/><stop offset=".55" stop-color="#6ea8fe"/><stop offset="1" stop-color="#b69cff"/></linearGradient></defs>',
        f'<rect width="{width}" height="{height}" rx="16" fill="{BG}"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="15" fill="none" stroke="{BORDER}"/>',
        '<rect x="1" y="1" width="100%" height="4" rx="2" fill="url(#accent)"/>',
        '<circle cx="24" cy="25" r="5" fill="#ff6b6b"/><circle cx="42" cy="25" r="5" fill="#ffbd69"/><circle cx="60" cy="25" r="5" fill="#59d499"/>',
        f'<text x="82" y="30" fill="{MUTED}" font-family="JetBrains Mono,Consolas,monospace" font-size="12">{escape(title)}</text>',
    ]
    if subtitle:
        bits.append(f'<text x="{width-22}" y="30" fill="{MUTED}" text-anchor="end" font-family="JetBrains Mono,Consolas,monospace" font-size="10">{escape(subtitle)}</text>')
    return bits


def text(x: float, y: float, value: Any, *, size: int = 13, color: str = TEXT, weight: str = "400", anchor: str = "start") -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" font-family="JetBrains Mono,Consolas,monospace" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')


def rect(x: float, y: float, w: float, h: float, fill: str = PANEL_2, radius: int = 10, opacity: float = 1) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{radius}" fill="{fill}" opacity="{opacity:.2f}"/>'


def save_svg(filename: str, parts: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / filename).write_text("\n".join(parts + ["</svg>"]) + "\n", encoding="utf-8")


def card_stats(profile: dict[str, Any], repos: list[dict[str, Any]], cc: dict[str, Any]) -> None:
    calendar = cc.get("contributionCalendar", {})
    values = [
        ("PUBLIC REPOSITORIES", len(repos), CYAN),
        ("STARS ON OWNED REPOS", sum(int(r.get("stargazers_count", 0)) for r in repos), PURPLE),
        ("FORKS ON OWNED REPOS", sum(int(r.get("forks_count", 0)) for r in repos), GREEN),
        ("FOLLOWERS", int(profile.get("followers", 0)), ORANGE),
        ("CONTRIBUTIONS / YEAR", int(calendar.get("totalContributions", 0)), CYAN),
        ("COMMITS / YEAR", int(cc.get("totalCommitContributions", 0)), GREEN),
        ("PULL REQUESTS / YEAR", int(cc.get("totalPullRequestContributions", 0)), PURPLE),
        ("ISSUES / YEAR", int(cc.get("totalIssueContributions", 0)), ORANGE),
    ]
    out = svg_header(1000, 310, f"GITHUB STATS / @{USER}", "PUBLIC ACCOUNT DATA")
    for index, (label, value, color) in enumerate(values):
        col, row = index % 4, index // 4
        x, y = 20 + col * 245, 54 + row * 119
        out += [rect(x, y, 225, 98), rect(x + 14, y + 15, 4, 66, color, 2),
                text(x + 30, y + 48, f"{value:,}", size=25, weight="700"),
                text(x + 30, y + 73, label, size=9, color=MUTED, weight="600")]
    out.append(text(974, 292, "Updated by GitHub Actions", size=9, color=MUTED, anchor="end"))
    save_svg("stats.svg", out)


def card_streak(days: list[dict[str, Any]], cc: dict[str, Any]) -> None:
    current, best, active, total = streak_values(days)
    values = [("CURRENT STREAK", current, CYAN), ("LONGEST STREAK", best, PURPLE),
              ("ACTIVE DAYS", active, GREEN), ("CONTRIBUTIONS", total, ORANGE)]
    out = svg_header(1000, 220, f"CONTRIBUTION STREAK / @{USER}")
    for i, (name, value, color) in enumerate(values):
        x = 20 + i * 245
        out += [rect(x, 65, 225, 110), text(x + 18, 116, f"{value:,}", size=34, color=color, weight="700"),
                text(x + 18, 145, name, size=10, color=MUTED, weight="600")]
    out.append(text(974, 202, "Based on GitHub contribution calendar", size=9, color=MUTED, anchor="end"))
    save_svg("streak.svg", out)


def card_languages(languages: Counter[str]) -> None:
    palette = [CYAN, BLUE, PURPLE, GREEN, ORANGE, PINK, "#d0a8ff", "#9bd1ff"]
    top = languages.most_common(8)
    total = sum(languages.values()) or 1
    out = svg_header(1000, 330, "LANGUAGES / OWNED PUBLIC REPOSITORIES")
    if not top:
        out.append(text(28, 110, "No language data returned by GitHub.", size=14, color=MUTED))
    for i, (name, amount) in enumerate(top):
        y = 78 + i * 28
        share = amount / total
        out += [text(28, y, name, size=12, weight="600"), rect(225, y - 12, 650, 12, PANEL_2, 6),
                rect(225, y - 12, 650 * share, 12, palette[i % len(palette)], 6),
                text(970, y, f"{share * 100:.1f}%", size=11, color=MUTED, anchor="end")]
    out.append(text(28, 310, "Distribution by language bytes across public, non-fork repositories.", size=9, color=MUTED))
    save_svg("languages.svg", out)


def card_clock(commits: list[dict[str, Any]]) -> None:
    hours: Counter[int] = Counter()
    for item in commits:
        stamp = (item.get("commit", {}).get("author", {}) or {}).get("date")
        if not stamp:
            continue
        try:
            hours[datetime.fromisoformat(stamp.replace("Z", "+00:00")).hour] += 1
        except ValueError:
            continue
    peak = max(hours.values(), default=1)
    out = svg_header(1000, 320, "COMMIT CLOCK / UTC", f"SAMPLE: {len(commits)} COMMITS")
    x0, y0, width = 28, 72, 944
    out.append(rect(x0, y0, width, 170, PANEL, 12))
    slot = width / 24
    for hour in range(24):
        value = hours.get(hour, 0)
        bh = max(2, value / peak * 112) if value else 2
        x = x0 + hour * slot + 7
        y = y0 + 136 - bh
        color = CYAN if value else BORDER
        out.append(rect(x, y, slot - 13, bh, color, 4, .95 if value else .65))
        if hour % 2 == 0:
            out.append(text(x + (slot - 13) / 2, 263, f"{hour:02d}", size=9, color=MUTED, anchor="middle"))
    out.append(text(28, 300, "Commit timestamps grouped by UTC hour; this is a sample, not a full lifetime measure.", size=9, color=MUTED))
    save_svg("commit-clock.svg", out)


def card_contributions(days: list[dict[str, Any]]) -> None:
    cutoff = date.today() - timedelta(days=89)
    recent = [d for d in days if d.get("date") and date.fromisoformat(d["date"]) >= cutoff]
    peak = max((int(d.get("contributionCount", 0)) for d in recent), default=0) or 1
    out = svg_header(1200, 300, "CONTRIBUTIONS / LAST 90 DAYS")
    x0, y0, width, height = 32, 66, 1136, 165
    out.append(rect(x0, y0, width, height, PANEL, 12))
    slot = width / max(1, len(recent))
    for i, day in enumerate(recent):
        count = int(day.get("contributionCount", 0))
        bh = max(2, count / peak * 125) if count else 2
        x = x0 + i * slot + .8
        y = y0 + 140 - bh
        color = CYAN if count else BORDER
        title = escape(f"{day.get('date', '')}: {count} contributions")
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{max(1, slot-1.5):.2f}" height="{bh:.2f}" rx="2" fill="{color}"><title>{title}</title></rect>')
    if recent:
        out += [text(x0, 258, recent[0]["date"], size=10, color=MUTED),
                text(x0 + width, 258, recent[-1]["date"], size=10, color=MUTED, anchor="end")]
    total = sum(int(d.get("contributionCount", 0)) for d in recent)
    out.append(text(600, 283, f"{total:,} contributions in the displayed period", size=11, color=CYAN, anchor="middle"))
    save_svg("contributions.svg", out)


def custom_tier(value: float, thresholds: tuple[int, ...]) -> str:
    for tier, threshold in zip(("S", "A", "B", "C", "D", "E"), thresholds):
        if value >= threshold:
            return tier
    return "—"


def card_trophies(profile: dict[str, Any], repos: list[dict[str, Any]], cc: dict[str, Any], account_years: float) -> None:
    contrib = int(cc.get("contributionCalendar", {}).get("totalContributions", 0))
    stars = sum(int(r.get("stargazers_count", 0)) for r in repos)
    values = [
        ("Contributions", contrib, (5000, 2500, 1000, 500, 100, 1)),
        ("Stars", stars, (100, 50, 25, 10, 5, 1)),
        ("Followers", int(profile.get("followers", 0)), (100, 50, 25, 10, 5, 1)),
        ("Repositories", len(repos), (50, 25, 10, 5, 3, 1)),
        ("Pull requests", int(cc.get("totalPullRequestContributions", 0)), (100, 50, 25, 10, 5, 1)),
        ("Issues", int(cc.get("totalIssueContributions", 0)), (100, 50, 25, 10, 5, 1)),
        ("Reviews", int(cc.get("totalPullRequestReviewContributions", 0)), (100, 50, 25, 10, 5, 1)),
        ("Years", account_years, (8, 6, 4, 3, 2, 1)),
    ]
    tier_colors = {"S": ORANGE, "A": CYAN, "B": PURPLE, "C": GREEN, "D": BLUE, "E": MUTED, "—": BORDER}
    tier_progress = {"S": 1.0, "A": 0.83, "B": 0.66, "C": 0.50, "D": 0.33, "E": 0.16, "—": 0.0}
    out = svg_header(1200, 220, "GITHUB MILESTONES / CUSTOM TIERS", "COMMUNITY + CONTRIBUTION SIGNALS")
    col = 145
    for i, (name, value, thresholds) in enumerate(values):
        x = 20 + i * col
        tier = custom_tier(value, thresholds)
        color = tier_colors[tier]
        out += [rect(x, 62, 132, 108, PANEL_2),
                f'<circle cx="{x+66}" cy="104" r="26" fill="none" stroke="{BORDER}" stroke-width="7"/>',
                f'<circle cx="{x+66}" cy="104" r="26" fill="none" stroke="{color}" stroke-width="7" stroke-dasharray="{163 * tier_progress[tier]:.1f} 180" transform="rotate(-90 {x+66} 104)"/>',
                text(x + 66, 112, tier, size=21, color=color, weight="700", anchor="middle"),
                text(x + 66, 148, name, size=10, color=MUTED, weight="600", anchor="middle")]
        shown = f"{value:.1f}" if isinstance(value, float) else f"{value:,}"
        out.append(text(x + 66, 190, shown, size=11, color=TEXT, anchor="middle"))
    out.append(text(1180, 210, "Custom profile milestones — not GitHub-issued achievements.", size=8, color=MUTED, anchor="end"))
    save_svg("trophies.svg", out)


def activity_row(event: dict[str, Any]) -> tuple[str, str, str] | None:
    try:
        when = datetime.fromisoformat(event.get("created_at", "").replace("Z", "+00:00")).strftime("%b %d")
    except ValueError:
        when = "Recent"
    repo = (event.get("repo") or {}).get("name", "")
    payload = event.get("payload") or {}
    kind = event.get("type", "")
    if kind == "PushEvent":
        branch = (payload.get("ref") or "").replace("refs/heads/", "")
        count = payload.get("size") or len(payload.get("commits", []))
        icon, action = "⬆️", f"Pushed {count or 'updates'} commit(s) to `{branch or 'branch'}`"
    elif kind == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        icon, action = "🔀", f"{str(payload.get('action', 'updated')).capitalize()} PR #{pr.get('number', '?')}: {pr.get('title', 'Pull request')}"
    elif kind == "IssuesEvent":
        issue = payload.get("issue", {})
        icon, action = "🐛", f"{str(payload.get('action', 'updated')).capitalize()} issue #{issue.get('number', '?')}: {issue.get('title', 'Issue')}"
    elif kind == "ReleaseEvent":
        icon, action = "🚀", f"Published release `{(payload.get('release') or {}).get('tag_name', '')}`"
    elif kind == "CreateEvent":
        icon, action = "✨", f"Created {payload.get('ref_type', 'repository')} `{payload.get('ref') or repo}`"
    elif kind == "WatchEvent":
        icon, action = "⭐", "Starred a repository"
    elif kind == "ForkEvent":
        icon, action = "🍴", "Forked a repository"
    else:
        return None
    link = f"[{repo}](https://github.com/{repo})" if repo else "GitHub"
    safe_action = action.replace("|", "\\|").replace("\n", " ").replace("\r", " ")
    return when, icon, f"{safe_action} in {link}"


def refresh_readme_activity(events: list[dict[str, Any]]) -> None:
    start_marker, end_marker = "<!--START_SECTION:activity-->", "<!--END_SECTION:activity-->"
    readme_path = Path("README.md")
    if not readme_path.exists():
        raise RuntimeError("README.md was not found in the repository root.")
    content = readme_path.read_text(encoding="utf-8")
    if start_marker not in content or end_marker not in content:
        raise RuntimeError("README.md is missing activity section markers.")
    rows: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for event in events:
        row = activity_row(event)
        if row and row not in seen:
            rows.append(row)
            seen.add(row)
        if len(rows) >= 8:
            break
    table = ["| When | | What |", "| :-- | :-: | :-- |"]
    if rows:
        table.extend(f"| `{when}` | {icon} | {what} |" for when, icon, what in rows)
    else:
        table.append("| `No recent event` | ◌ | No recent public activity was returned by GitHub. |")
    before, remainder = content.split(start_marker, 1)
    _, after = remainder.split(end_marker, 1)
    readme_path.write_text(before + start_marker + "\n" + "\n".join(table) + "\n" + end_marker + after, encoding="utf-8")


def main() -> None:
    if not TOKEN:
        raise RuntimeError("GH_TOKEN is not set. Configure PROFILE_TOKEN in repository Actions secrets or use GITHUB_TOKEN.")
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=365)
    profile = fetch_profile()
    repos = fetch_repositories()
    contributions = fetch_contributions(start, now)
    days = flatten_days(contributions)
    languages = fetch_languages(repos)
    commits = fetch_commit_sample(now - timedelta(days=180))
    try:
        events = fetch_public_events()
    except Exception as exc:
        print(f"Warning: recent activity unavailable: {exc}", file=sys.stderr)
        events = []
    created = profile.get("created_at")
    account_years = 0.0
    if created:
        account_years = max(0.0, (now.date() - datetime.fromisoformat(created.replace("Z", "+00:00")).date()).days / 365.25)
    card_stats(profile, repos, contributions)
    card_streak(days, contributions)
    card_languages(languages)
    card_clock(commits)
    card_contributions(days)
    card_trophies(profile, repos, contributions, account_years)
    refresh_readme_activity(events)
    print(f"Dashboard generated for @{USER}.")
    print(f"Repositories included: {len(repos)} public owned, non-fork repositories.")
    print(f"Commit-clock sample: {len(commits)} public commits.")
    print(f"SVG cards written to: {OUT.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
