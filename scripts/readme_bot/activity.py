"""Recent public activity, rendered as a Markdown table."""

from __future__ import annotations

from datetime import datetime

from .http import gh_rest

MAX_LINES = 8


def _repo(name: str) -> str:
    return f"[{name}](https://github.com/{name})"


def _describe(ev: dict) -> tuple[str, str] | None:
    t, p, repo = ev["type"], ev.get("payload") or {}, ev["repo"]["name"]
    if t == "PushEvent":
        branch = p.get("ref", "").removeprefix("refs/heads/")
        return "⬆️", f"Pushed to `{branch or 'main'}` in {_repo(repo)}"
    if t == "PullRequestEvent":
        pr = p.get("pull_request") or {}
        num = pr.get("number") or p.get("number")
        url = pr.get("html_url") or (f"https://github.com/{repo}/pull/{num}" if num else f"https://github.com/{repo}/pulls")
        action = p.get("action")
        if action == "closed" and pr.get("merged"):
            return "🎉", f"Merged PR [#{num}]({url}) in {_repo(repo)}"
        if action in ("opened", "reopened", "closed"):
            icon = {"opened": "🔀", "reopened": "🔀", "closed": "❌"}[action]
            return icon, f"{action.capitalize()} PR [#{num}]({url}) in {_repo(repo)}"
        return None
    if t == "IssuesEvent" and p.get("action") in ("opened", "closed", "reopened"):
        issue = p.get("issue") or {}
        num = issue.get("number")
        url = issue.get("html_url") or (f"https://github.com/{repo}/issues/{num}" if num else f"https://github.com/{repo}/issues")
        icon = "✔️" if p["action"] == "closed" else "❗"
        return icon, f"{p['action'].capitalize()} issue [#{num}]({url}) in {_repo(repo)}"
    if t == "PullRequestReviewEvent":
        pr = p.get("pull_request") or {}
        num = pr.get("number")
        url = pr.get("html_url") or (f"https://github.com/{repo}/pull/{num}" if num else f"https://github.com/{repo}/pulls")
        return "👀", f"Reviewed PR [#{num or '?'}]({url}) in {_repo(repo)}"
    if t == "ReleaseEvent" and p.get("action") == "published":
        rel = p.get("release") or {}
        tag = rel.get("tag_name") or "release"
        url = rel.get("html_url") or f"https://github.com/{repo}/releases"
        return "🚀", f"Released [{tag}]({url}) in {_repo(repo)}"
    if t == "CreateEvent" and p.get("ref_type") == "repository":
        return "📦", f"Created repository {_repo(repo)}"
    if t == "PublicEvent":
        return "🌍", f"Open-sourced {_repo(repo)}"
    return None


def collect(login: str, ignored: set[str]) -> str:
    events: list[dict] = []
    for page in (1, 2, 3):
        batch = gh_rest(f"users/{login}/events/public?per_page=100&page={page}")
        events.extend(batch)
        if len(batch) < 100:
            break
    events.sort(key=lambda e: e["created_at"], reverse=True)
    rows: list[tuple[str, str, str]] = []
    pushed: set[str] = set()
    for ev in events:
        name = (ev.get("repo") or {}).get("name")
        if not name or name in ignored:
            continue
        if ev["type"] == "PushEvent":
            if name in pushed:
                continue
            pushed.add(name)
        described = _describe(ev)
        if not described:
            continue
        icon, text = described
        when = datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00"))
        rows.append((f"`{when:%b %d}`", icon, text))
        if len(rows) >= MAX_LINES:
            break

    if not rows:
        return "_No recent public activity — probably building something offline._"
    lines = ["| When | | What |", "| :-- | :-: | :-- |"]
    lines += [f"| {w} | {i} | {t} |" for w, i, t in rows]
    return "\n".join(lines)
