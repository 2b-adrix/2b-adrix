"""Renderers that turn collected GitHub data into terminal-window SVG cards."""

from __future__ import annotations

import math
from datetime import date

from .svg import CHROME_H, MONO, TERM_THEME, THEME, card, delay, esc, fmt_int, fmt_short, panel

T = TERM_THEME


def _fmt_day(d: date, with_year: bool = True) -> str:
    return f"{d:%b} {d.day}, {d.year}" if with_year else f"{d:%b} {d.day}"


def _fmt_range(r: tuple[date, date] | None, today: date) -> str:
    if not r:
        return "—"
    start, end = r
    same_year = start.year == end.year == today.year
    left = _fmt_day(start, start.year != end.year)
    right = "Today" if end == today else _fmt_day(end, not same_year)
    return left if start == end else f"{left} – {right}"


# ---------------------------------------------------------------- stats ----

def stats_card(s: dict) -> str:
    w, h = 500, 240
    rows = [
        ("stars_earned", fmt_int(s["stars"])),
        ("contributions_1y", fmt_int(s["contrib_year"])),
        ("contributions_all", fmt_int(s["contrib_all"])),
        ("pull_requests", fmt_int(s["prs"])),
        ("issues", fmt_int(s["issues"])),
        ("contributed_to", fmt_int(s["contributed_to"])),
        ("repositories", fmt_int(s["repos"])),
        ("followers", fmt_int(s["followers"])),
    ]
    body = [
        f'<text x="24" y="30" class="mono" font-size="13"><tspan class="accent">$</tspan> gh stats '
        f'<tspan class="muted">--user</tspan> {esc(s["login"])}</text>'
    ]
    for i, (k, v) in enumerate(rows):
        y = 58 + i * 19
        body.append(
            f'<g class="fade" {delay(0.1 + i * 0.06)}>'
            f'<text x="24" y="{y}" class="mono muted" font-size="12.5">{k}</text>'
            f'<text x="160" y="{y}" class="mono dim" font-size="12.5">{"·" * 11}</text>'
            f'<text x="290" y="{y}" class="mono" font-size="12.5" font-weight="600" text-anchor="end">{v}</text>'
            f"</g>"
        )

    r = 48
    circ = 2 * math.pi * r
    progress = max(0.04, min(1.0, (100 - s["rank"]["percentile"]) / 100))
    offset = circ * (1 - progress)
    cx, cy = 400, 108
    css = f"@keyframes ring {{ from {{ stroke-dashoffset: {circ:.2f}; }} }} .ring {{ animation: ring 1.4s cubic-bezier(.2,.8,.2,1) both; }}"
    body.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{T["grid"]}" stroke-width="8"/>'
        f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#accentGrad)" stroke-width="8" '
        f'stroke-linecap="round" stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}" transform="rotate(-90 {cx} {cy})"/>'
        f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" font-size="30" font-weight="700" class="fade" {delay(0.6)}>{esc(s["rank"]["level"])}</text>'
        f'<text x="{cx}" y="{cy + r + 30}" text-anchor="middle" class="mono muted" font-size="11">top {max(s["rank"]["percentile"], 0.1):.1f}%</text>'
    )
    return card(w, h, "~/github/stats.yaml", "\n".join(body), extra_css=css, right_label=s["name"])


# --------------------------------------------------------------- streak ----

def streak_card(st: dict) -> str:
    w, h = 500, 240
    today = st["today"]
    cols = [83, 250, 417]
    body = [
        f'<line x1="166" y1="36" x2="166" y2="168" stroke="{T["border"]}"/>',
        f'<line x1="334" y1="36" x2="334" y2="168" stroke="{T["border"]}"/>',
        f'<g class="fade" {delay(0.1)}>'
        f'<text x="{cols[0]}" y="92" text-anchor="middle" font-size="28" font-weight="700">{fmt_short(st["total"])}</text>'
        f'<text x="{cols[0]}" y="122" text-anchor="middle" font-size="13" class="muted">Total Contributions</text>'
        f'<text x="{cols[0]}" y="146" text-anchor="middle" font-size="11" class="mono dim">since {esc(_fmt_day(st["first"]))}</text>'
        f"</g>",
        f'<circle cx="{cols[1]}" cy="80" r="40" fill="none" stroke="url(#accentGrad)" stroke-width="5"/>'
        f'<g class="fade" {delay(0.3)}>'
        f'<text x="{cols[1]}" y="90" text-anchor="middle" font-size="28" font-weight="700">{st["current"]}</text>'
        f'<text x="{cols[1]}" y="146" text-anchor="middle" font-size="13" font-weight="600" class="accent">Current Streak</text>'
        f'<text x="{cols[1]}" y="166" text-anchor="middle" font-size="11" class="mono dim">{esc(_fmt_range(st["current_range"], today))}</text>'
        f"</g>",
        f'<g class="fade" {delay(0.5)}>'
        f'<text x="{cols[2]}" y="92" text-anchor="middle" font-size="28" font-weight="700">{st["longest"]}</text>'
        f'<text x="{cols[2]}" y="122" text-anchor="middle" font-size="13" class="muted">Longest Streak</text>'
        f'<text x="{cols[2]}" y="146" text-anchor="middle" font-size="11" class="mono dim">{esc(_fmt_range(st["longest_range"], today))}</text>'
        f"</g>",
        '<text x="250" y="194" text-anchor="middle" font-size="11" class="mono dim">days with ≥1 contribution · UTC</text>',
    ]
    return card(w, h, "~/github/streak.log", "\n".join(body), right_label="since day one")


# ------------------------------------------------------------ languages ----

def languages_card(langs: list[dict], sample: int) -> str:
    w, h = 500, 240
    x0, bar_w = 24, 452
    body = [f'<clipPath id="barClip"><rect x="{x0}" y="22" width="{bar_w}" height="10" rx="5"/></clipPath>']
    cursor = float(x0)
    segs = []
    for lang in langs:
        seg = bar_w * lang["pct"] / 100
        segs.append(f'<rect x="{cursor:.2f}" y="22" width="{max(seg, 0):.2f}" height="10" fill="{lang["color"]}"/>')
        cursor += seg
    body.append(f'<g clip-path="url(#barClip)"><g class="grow">{"".join(segs)}</g></g>')

    per_col = math.ceil(len(langs) / 2) or 1
    for i, lang in enumerate(langs):
        col, row = divmod(i, per_col)
        x = x0 + col * 236
        y = 66 + row * 26
        body.append(
            f'<g class="fade" {delay(0.2 + i * 0.06)}>'
            f'<circle cx="{x + 5}" cy="{y - 4}" r="5" fill="{lang["color"]}"/>'
            f'<text x="{x + 18}" y="{y}" font-size="13">{esc(lang["name"])}</text>'
            f'<text x="{x + 210}" y="{y}" font-size="12" class="mono muted" text-anchor="end">{lang["pct"]:.1f}%</text>'
            f"</g>"
        )
    body.append(f'<text x="24" y="194" font-size="11" class="mono dim">weighted by last {fmt_int(sample)} project commits</text>')
    return card(w, h, "~/github/languages.json", "\n".join(body), right_label="top languages")


# ---------------------------------------------------------------- clock ----

PERIODS = (
    ("Night", range(0, 6), "#a78bfa"),
    ("Morning", range(6, 12), "#fbbf24"),
    ("Daytime", range(12, 18), "#34d399"),
    ("Evening", range(18, 24), "#22d3ee"),
)


def clock_card(clock: dict) -> str:
    w, h = 500, 240
    hours, weekdays, sample = clock["hours"], clock["weekdays"], max(clock["sample"], 1)
    period_totals = {name: sum(hours[i] for i in rng) for name, rng, _ in PERIODS}
    top_period = max(period_totals, key=period_totals.get)
    top_day = ("Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays", "Sundays")[weekdays.index(max(weekdays))]
    color_of = {i: c for _, rng, c in PERIODS for i in rng}

    body = [
        f'<text x="24" y="30" font-size="13"><tspan class="muted">mostly a</tspan> '
        f'<tspan font-weight="700" class="accent">{top_period.lower()}</tspan> '
        f'<tspan class="muted">coder ·</tspan> <tspan font-weight="700" class="accent2">{top_day}</tspan></text>'
    ]
    cx0, base, max_h, step = 24, 164, 100, 11.5
    peak = max(hours) or 1
    body.append(f'<line x1="{cx0}" y1="{base + 0.5}" x2="{cx0 + 24 * step}" y2="{base + 0.5}" stroke="{T["border"]}"/>')
    for i, v in enumerate(hours):
        bh = max(2, max_h * v / peak)
        body.append(
            f'<rect class="rise" {delay(i * 0.025)} x="{cx0 + i * step + 1.5:.1f}" y="{base - bh:.1f}" width="8" height="{bh:.1f}" rx="2" fill="{color_of[i]}" opacity="{0.45 + 0.55 * v / peak:.2f}"/>'
        )
    for hr in (0, 6, 12, 18, 23):
        body.append(f'<text x="{cx0 + hr * step + 5.5:.1f}" y="{base + 16}" font-size="10" class="mono dim" text-anchor="middle">{hr:02d}h</text>')

    wx, peak_d = 330, max(weekdays) or 1
    for i, (label, v) in enumerate(zip(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), weekdays)):
        y = 58 + i * 17
        bw = 90 * v / peak_d
        body.append(
            f'<text x="{wx}" y="{y + 8}" font-size="10.5" class="mono muted">{label}</text>'
            f'<rect x="{wx + 32}" y="{y}" width="90" height="9" rx="4.5" fill="{T["grid"]}"/>'
            f'<rect class="grow" {delay(0.3 + i * 0.05)} x="{wx + 32}" y="{y}" width="{max(bw, 3):.1f}" height="9" rx="4.5" fill="url(#accentGrad)"/>'
            f'<text x="{wx + 146}" y="{y + 8}" font-size="10" class="mono dim" text-anchor="end">{v * 100 / sample:.0f}%</text>'
        )
    body.append(f'<text x="24" y="194" font-size="11" class="mono dim">author-local time · last {fmt_int(clock["sample"])} commits</text>')
    return card(w, h, "~/github/commit-clock.sh", "\n".join(body), right_label="when I ship")


# -------------------------------------------------------- contributions ----

def contributions_card(days: list[tuple[str, int]], span: int = 90) -> str:
    w, h = 1000, 300
    pts = days[-span:]
    total = sum(v for _, v in pts)
    peak = max((v for _, v in pts), default=0)
    left, right, top, bottom = 56, 976, 34, 214
    y_max = max(4, math.ceil(peak / 4) * 4)
    step = (right - left) / max(len(pts) - 1, 1)

    def xy(i: int, v: int) -> tuple[float, float]:
        return left + i * step, bottom - (bottom - top) * v / y_max

    body = []
    for k in range(5):
        y = bottom - (bottom - top) * k / 4
        body.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{T["grid"]}" stroke-dasharray="{"0" if k == 0 else "3 5"}"/>')
        body.append(f'<text x="{left - 10}" y="{y + 4:.1f}" font-size="10.5" class="mono dim" text-anchor="end">{fmt_short(y_max * k / 4)}</text>')
    for i in range(0, len(pts), 14):
        x, _ = xy(i, 0)
        d = date.fromisoformat(pts[i][0])
        body.append(f'<text x="{x:.1f}" y="{bottom + 22}" font-size="10.5" class="mono dim" text-anchor="middle">{d:%b} {d.day}</text>')

    coords = [xy(i, v) for i, (_, v) in enumerate(pts)]
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in coords) if coords else "M0,0"
    area = f"{line} L{coords[-1][0]:.1f},{bottom} L{coords[0][0]:.1f},{bottom} Z" if coords else ""
    css = (
        "@keyframes draw { from { stroke-dashoffset: 1; } } "
        ".draw { stroke-dasharray: 1; stroke-dashoffset: 0; animation: draw 2.2s ease-out both; }"
    )
    body.append(
        f'<defs><linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{T["accent"]}" stop-opacity=".35"/><stop offset="1" stop-color="{T["accent"]}" stop-opacity="0"/>'
        f"</linearGradient></defs>"
        f'<path class="fade" {delay(0.8)} d="{area}" fill="url(#areaGrad)"/>'
        f'<path class="draw" pathLength="1" d="{line}" fill="none" stroke="url(#accentGrad)" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>'
    )
    if pts and peak:
        i_peak = max(range(len(pts)), key=lambda i: pts[i][1])
        px, py = coords[i_peak]
        anchor = "end" if px > right - 80 else "start"
        dx = -10 if anchor == "end" else 10
        body.append(
            f'<g class="fade" {delay(1.8)}><circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{T["bg"]}" stroke="{T["accent2"]}" stroke-width="2"/>'
            f'<text x="{px + dx:.1f}" y="{py + 4:.1f}" font-size="11" class="mono accent2" text-anchor="{anchor}">peak {peak}</text></g>'
        )
    body.append(
        f'<text x="{left}" y="20" font-size="12" class="mono"><tspan class="accent">$</tspan> git log --since="{span} days ago" '
        f'<tspan class="muted">| wc -l</tspan>  <tspan font-weight="700">{fmt_int(total)}</tspan> <tspan class="muted">contributions</tspan></text>'
    )
    return card(w, h, "~/github/contributions.graph", "\n".join(body), extra_css=css, right_label=f"last {span} days")


# ------------------------------------------------------------- trophies ----

TIER_COLORS = {"S": "#fbbf24", "A": "#22d3ee", "B": "#a78bfa", "C": "#8b949e"}


def _cup(cx: float, y: float, color: str, tier: str | None) -> str:
    fill = color if tier else T["grid"]
    stroke = color if tier else T["dim"]
    label = esc(tier or "—")
    return (
        f'<path d="M{cx - 12},{y + 6} h-6 a6,6 0 0 0 0,12 h7 M{cx + 12},{y + 6} h6 a6,6 0 0 1 0,12 h-7" fill="none" stroke="{stroke}" stroke-width="3"/>'
        f'<path d="M{cx - 20},{y} H{cx + 20} V{y + 14} Q{cx + 20},{y + 34} {cx},{y + 36} Q{cx - 20},{y + 34} {cx - 20},{y + 14} Z" fill="{fill}"/>'
        f'<rect x="{cx - 3}" y="{y + 35}" width="6" height="8" fill="{stroke}"/>'
        f'<rect x="{cx - 14}" y="{y + 43}" width="28" height="6" rx="2" fill="{stroke}"/>'
        f'<text x="{cx}" y="{y + 22}" text-anchor="middle" font-size="{13 if len(label) < 3 else 11}" font-weight="800" fill="{T["bg"]}" style="fill:{T["bg"]}">{label}</text>'
    )


def trophies_card(s: dict) -> str:
    items = [
        ("Contributions", s["contrib_all"], fmt_short(s["contrib_all"])),
        ("Stars", s["stars"], fmt_short(s["stars"])),
        ("Followers", s["followers"], fmt_short(s["followers"])),
        ("Repositories", s["repos"], fmt_short(s["repos"])),
        ("Pull Requests", s["prs"], fmt_short(s["prs"])),
        ("Issues", s["issues"], fmt_short(s["issues"])),
        ("Reviews", s["reviews_year"], fmt_short(s["reviews_year"])),
        ("Experience", s["years"], f"{s['years']:.1f} yrs"),
    ]
    from .github import trophy_tier

    w, h = 1000, 196
    col = (w - 32) / len(items)
    body = []
    for i, (name, value, shown) in enumerate(items):
        tier = trophy_tier(name, value)
        color = TIER_COLORS[tier[0]] if tier else T["dim"]
        cx = 16 + col * i + col / 2
        body.append(
            f'<g class="fade" {delay(0.08 * i)}>'
            f'<rect x="{cx - col / 2 + 6:.1f}" y="16" width="{col - 12:.1f}" height="128" rx="10" fill="{T["chrome"]}" stroke="{T["border"]}"/>'
            f"{_cup(cx, 30, color, tier)}"
            f'<text x="{cx:.1f}" y="106" text-anchor="middle" font-size="12.5" font-weight="600">{esc(name)}</text>'
            f'<text x="{cx:.1f}" y="126" text-anchor="middle" font-size="11.5" class="mono muted">{esc(shown)}</text>'
            f"</g>"
        )
    return card(w, h, "~/github/trophies", "\n".join(body), right_label="SSS › SS › S › AAA › AA › A › B › C")


# --------------------------------------------------------------- views ----

def views_badge(count: int) -> str:
    """Pill-shaped Profile-views badge matching the 30px Material badges."""
    label, value = "VIEWS", fmt_int(count)
    left = 34 + len(label) * 7.6 + 10
    right = len(value) * 8.6 + 24
    w, h = round(left + right), 30
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Profile views: {value}">
<title>Profile views: {value}</title>
<defs><clipPath id="vc"><rect width="{w}" height="{h}" rx="15"/></clipPath></defs>
<g clip-path="url(#vc)">
  <rect width="{w}" height="{h}" fill="{THEME['surface']}"/>
  <rect x="{left:.1f}" width="{right:.1f}" height="{h}" fill="{THEME['chrome']}"/>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="15" fill="none" stroke="{THEME['border']}"/>
<g transform="translate(11 7)" fill="none" stroke="{THEME['mint']}" stroke-width="1.6">
  <path d="M1 8s2.8-5 7-5 7 5 7 5-2.8 5-7 5-7-5-7-5z"/><circle cx="8" cy="8" r="2.2" fill="{THEME['mint']}"/>
</g>
<text x="34" y="19" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1" fill="{THEME['muted']}" style="white-space:pre">{label}</text>
<text x="{left + right / 2:.1f}" y="19.5" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="800" fill="{THEME['mint']}">{value}</text>
</svg>
"""


def placeholder_card(w: int, h: int, title: str, message: str) -> str:
    body = f'<text x="{w / 2}" y="{(h - CHROME_H) / 2 + 4}" text-anchor="middle" font-size="13" class="mono muted">{esc(message)}</text>'
    return card(w, h, title, body)


# ----------------------------------------------------------------- snake ----

SNAKE_LEVELS = ("#161c28", "#134e32", "#1d7a4c", "#29b469", "#3ddc84")
SNAKE_SEGMENTS = (
    (THEME["mint"], 13, 4.0, 1.00),   # glowing Android Mint head
    ("#2dd4bf", 12, 3.5, 0.92),       # teal
    (THEME["sky"], 11, 3.5, 0.82),    # electric sky
    (THEME["kotlin"], 10, 3.0, 0.72), # Kotlin violet
    (THEME["coral"], 9, 3.0, 0.60),   # coral tail
)


def _snake_level(count: int, q: tuple[int, int, int]) -> int:
    if count <= 0:
        return 0
    if count <= q[0]:
        return 1
    if count <= q[1]:
        return 2
    if count <= q[2]:
        return 3
    return 4


def _build_snake_path(active: list[tuple[int, int]], cols: int) -> list[tuple[int, int]]:
    """Build a continuous 1-step orthogonal grid path visiting every active cell."""
    if not active:
        return [(c, 3) for c in range(-1, cols + 1)]
    remaining = set(active)
    path: list[tuple[int, int]] = [(-1, 0), (0, 0)]
    cur = (0, 0)
    remaining.discard(cur)

    while remaining:
        nxt = min(
            remaining,
            key=lambda p: (abs(p[0] - cur[0]) + abs(p[1] - cur[1])) * 3 + (0 if p[0] >= cur[0] else 2) + abs(p[1] - cur[1]) * 0.1,
        )
        c, r = cur
        tc, tr = nxt
        while c != tc:
            c += 1 if tc > c else -1
            path.append((c, r))
            remaining.discard((c, r))
        while r != tr:
            r += 1 if tr > r else -1
            path.append((c, r))
            remaining.discard((c, r))
        cur = nxt

    c, r = cur
    while c < cols:
        c += 1
        path.append((c, r))
    return path


def snake_card(weeks: list[list[tuple[str, int]]]) -> str:
    """Custom animated Material HUD contribution snake matching @2b-adrix's profile."""
    w, h = 1000, 250
    weeks = weeks[-53:]
    cols = max(1, len(weeks))
    cell, step = 13, 17
    gx, gy = 62, 28
    grid_w = cols * step - 4

    counts = [cnt for col in weeks for _, cnt in col if cnt > 0]
    counts_sorted = sorted(counts)
    if counts_sorted:
        n_c = len(counts_sorted)
        q = (
            counts_sorted[min(n_c - 1, n_c // 4)],
            counts_sorted[min(n_c - 1, n_c // 2)],
            counts_sorted[min(n_c - 1, (3 * n_c) // 4)],
        )
    else:
        q = (1, 3, 6)

    grid: dict[tuple[int, int], tuple[str, int, int]] = {}
    active: list[tuple[int, int]] = []
    total = 0
    for c, col in enumerate(weeks):
        for r, (d_str, cnt) in enumerate(col[:7]):
            lvl = _snake_level(cnt, q)
            grid[(c, r)] = (d_str, cnt, lvl)
            total += cnt
            if cnt > 0:
                active.append((c, r))

    path = _build_snake_path(active, cols)
    n_steps = max(1, len(path) - 1)
    dur = max(14.0, min(26.0, round(n_steps * 0.055, 1)))

    # Map each active cell to the first step index where the snake head visits it
    eat_step: dict[tuple[int, int], int] = {}
    for idx, pos in enumerate(path):
        if pos in grid and grid[pos][1] > 0 and pos not in eat_step:
            eat_step[pos] = idx

    css_parts = [f".snk {{ animation: none {dur:.1f}s linear infinite; }}"]
    # Snake segment animations (emit keyframes only at start, end, and direction turns)
    for seg_i, (_, size, _, _) in enumerate(SNAKE_SEGMENTS):
        offset_px = (cell - size) / 2
        seq = [
            path[i - seg_i] if i >= seg_i else (-1 - (seg_i - i), path[0][1])
            for i in range(n_steps + 1)
        ]
        frames = []
        for i, (pc, pr) in enumerate(seq):
            if i == 0 or i == n_steps:
                keep = True
            else:
                d_prev = (pc - seq[i - 1][0], pr - seq[i - 1][1])
                d_next = (seq[i + 1][0] - pc, seq[i + 1][1] - pr)
                keep = d_prev != d_next
            if keep:
                pct = i * 100 / n_steps
                tx = gx + pc * step + offset_px
                ty = gy + pr * step + offset_px
                frames.append(f"{pct:.2f}%{{transform:translate({tx:.1f}px,{ty:.1f}px)}}")
        css_parts.append(f"@keyframes s{seg_i}{{{''.join(frames)}}}.s{seg_i}{{animation-name:s{seg_i};}}")

    # Eaten cell animations
    eaten_fill = "#12161f"
    for idx, (pos, step_i) in enumerate(eat_step.items()):
        orig = SNAKE_LEVELS[grid[pos][2]]
        p1 = max(0.0, step_i * 100 / n_steps - 0.15)
        p2 = min(94.5, step_i * 100 / n_steps + 0.05)
        css_parts.append(
            f"@keyframes e{idx}{{0%,{p1:.2f}%{{fill:{orig}}}{p2:.2f}%,96%{{fill:{eaten_fill}}}100%{{fill:{orig}}}}}"
            f".e{idx}{{animation:e{idx} {dur:.1f}s linear infinite;}}"
        )
    eat_cls = {pos: f"e{idx}" for idx, pos in enumerate(eat_step)}

    # Progress bar synced with snake
    css_parts.append(
        f"@keyframes snkBar{{0%{{transform:scaleX(0)}}92%,97%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}"
        f".snkBar{{animation:snkBar {dur:.1f}s linear infinite;transform-box:fill-box;transform-origin:left center;}}"
    )

    body = []
    # Month labels across top of grid
    last_month = ""
    for c, col in enumerate(weeks):
        if not col:
            continue
        m = date.fromisoformat(col[0][0]).strftime("%b")
        if m != last_month and (c == 0 or c < cols - 2):
            body.append(f'<text x="{gx + c * step}" y="18" class="mono dim" font-size="9.5">{m}</text>')
            last_month = m

    # Weekday labels on left
    for r, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        body.append(f'<text x="{gx - 10}" y="{gy + r * step + 10}" text-anchor="end" class="mono dim" font-size="9.5">{label}</text>')

    # Matrix cells wrapped in clipPath so snake enters/exits cleanly at grid edges
    grid_clip = f'<clipPath id="snkGrid"><rect x="{gx - 2}" y="{gy - 2}" width="{grid_w + 4}" height="{7 * step}" rx="4"/></clipPath>'
    cells = []
    for (c, r), (d_str, cnt, lvl) in grid.items():
        x, y = gx + c * step, gy + r * step
        fill = SNAKE_LEVELS[lvl]
        cls = f' class="{eat_cls[(c, r)]}"' if (c, r) in eat_cls else ""
        stroke = f' stroke="#1f2737" stroke-width="0.8"' if lvl == 0 else ""
        tip = esc(f"{d_str}: {cnt} contribution{'s' if cnt != 1 else ''}")
        cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{fill}"{cls}{stroke}><title>{tip}</title></rect>')

    snake_rects = []
    for seg_i, (color, size, rad, op) in reversed(list(enumerate(SNAKE_SEGMENTS))):
        snake_rects.append(f'<rect class="snk s{seg_i}" width="{size}" height="{size}" rx="{rad}" fill="{color}" opacity="{op:.2f}"/>')

    body.append(grid_clip)
    body.append(f'<g clip-path="url(#snkGrid)">{"".join(cells)}{"".join(snake_rects)}</g>')

    # Synced progress track + footer metadata + legend
    py = gy + 7 * step + 12
    body.append(
        f'<rect x="{gx}" y="{py}" width="{grid_w}" height="4" rx="2" fill="{THEME["surface"]}"/>'
        f'<rect class="snkBar" x="{gx}" y="{py}" width="{grid_w}" height="4" rx="2" fill="url(#brandGrad)"/>'
    )
    ly = py + 23
    body.append(
        f'<text x="{gx}" y="{ly}" class="mono muted" font-size="10.5">'
        f'<tspan fill="{THEME["mint"]}" font-weight="700">{fmt_int(total)}</tspan> contributions · {len(active)} active days</text>'
    )
    lx = gx + grid_w - 126
    body.append(f'<text x="{lx - 8}" y="{ly}" text-anchor="end" class="mono dim" font-size="9.5">Less</text>')
    for i, col_hex in enumerate(SNAKE_LEVELS):
        body.append(f'<rect x="{lx + i * 16}" y="{ly - 9.5}" width="11" height="11" rx="2.5" fill="{col_hex}"/>')
    body.append(f'<text x="{lx + 84}" y="{ly}" class="mono dim" font-size="9.5">More</text>')

    return panel(
        w,
        h,
        "MATRIX // CONTRIBUTION SNAKE",
        "\n".join(body),
        extra_css="".join(css_parts),
        tag=f"LIVE {cols}W",
        accent=THEME["mint"],
    )
