"""CLI: python -m readme_bot {activity,github,views,static,all}"""

from __future__ import annotations

import os
import re
import sys
import time
import urllib.request
from pathlib import Path

from . import cards
from .svg import write

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
OUT = Path(os.environ.get("README_BOT_OUT") or ROOT / "out")
LOGIN = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "2b-adrix"


def replace_section(name: str, content: str) -> None:
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(rf"(<!--START_SECTION:{name}-->).*?(<!--END_SECTION:{name}-->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"README is missing the {name} section markers")
    new = pattern.sub(lambda m: f"{m.group(1)}\n{content.strip()}\n{m.group(2)}", text)
    if new != text:
        README.write_text(new, encoding="utf-8", newline="\n")
        print(f"  updated README section '{name}'")
    else:
        print(f"  README section '{name}' unchanged")


def cmd_activity() -> None:
    from . import activity

    ignored = {f"{LOGIN}/{LOGIN}"} | {r.strip() for r in os.environ.get("ACTIVITY_IGNORED_REPOS", "").split(",") if r.strip()}
    replace_section("activity", activity.collect(LOGIN, ignored))


def cmd_github() -> None:
    from . import github

    data = github.collect(LOGIN)
    write(OUT / "stats.svg", cards.stats_card(data["stats"]))
    write(OUT / "streak.svg", cards.streak_card(data["streak"]))
    write(OUT / "languages.svg", cards.languages_card(data["languages"], data["clock"]["sample"]))
    write(OUT / "commit-clock.svg", cards.clock_card(data["clock"]))
    write(OUT / "contributions.svg", cards.contributions_card(data["recent_days"]))
    write(OUT / "trophies.svg", cards.trophies_card(data["stats"]))
    write(OUT / "snake.svg", cards.snake_card(data["weeks"]))


def cmd_views() -> None:
    """Read the komarev counter without incrementing it."""
    from .http import USER_AGENT

    req = urllib.request.Request(f"https://komarev.com/ghpvc/?username={LOGIN}&style=flat", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        svg = resp.read().decode("utf-8")
    numbers = re.findall(r">([\d,]+)<", svg)
    if not numbers:
        raise SystemExit("couldn't find a view count in komarev's response")
    write(OUT / "views.svg", cards.views_badge(int(numbers[-1].replace(",", ""))))


def cmd_static() -> None:
    from . import static

    static.build(ROOT)


COMMANDS = {"activity": cmd_activity, "github": cmd_github, "views": cmd_views, "static": cmd_static}


def main(argv: list[str]) -> int:
    names = argv or ["activity", "github", "views"]
    if names == ["all"]:
        names = ["activity", "github", "views"]
    unknown = [n for n in names if n not in COMMANDS]
    if unknown:
        print(f"unknown command(s): {', '.join(unknown)}; choose from {', '.join(COMMANDS)}", file=sys.stderr)
        return 2
    for name in names:
        started = time.perf_counter()
        print(f"▶ {name}")
        COMMANDS[name]()
        print(f"✔ {name} in {time.perf_counter() - started:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
