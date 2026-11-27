"""Renderers turning collected GitHub metrics into crisp monochrome obsidian SVG cards."""

from __future__ import annotations

import math
from datetime import date

from .svg import HEADER_H, MONO, THEME, delay, esc, fmt_int, fmt_short, panel

T = THEME


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
    """2x4 Metric Grid + Horizontal Rank Progress Bar."""
    w, h = 500, 266
    tiles = [
        ("STARS", fmt_int(s["stars"]), T["amber"]),
        ("CONTRIB (1Y)", fmt_int(s["contrib_year"]), T["accent"]),
        ("ALL-TIME", fmt_int(s["contrib_all"]), T["sky"]),
        ("REPOSITORIES", fmt_int(s["repos"]), T["violet"]),
        ("PULL REQS", fmt_int(s["prs"]), T["muted"]),
        ("ISSUES", fmt_int(s["issues"]), T["muted"]),
        ("REVIEWS", fmt_int(s["reviews_year"]), T["muted"]),
        ("FOLLOWERS", fmt_int(s["followers"]), T["muted"]),
    ]
    body = []
    bw, bh, gx, gy = 109, 66, 10, 10
    for idx, (label, val, color) in enumerate(tiles):
        col, row = idx % 4, idx // 4
        x = 17 + col * (bw + gx)
        y = 14 + row * (bh + gy)
        body.append(
            f'<g class="fade" {delay(0.05 * idx)}>'
            f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<rect x="{x + 12}" y="{y + 11}" width="16" height="2.5" rx="1.25" fill="{color}"/>'
            f'<text x="{x + 12}" y="{y + 39}" font-size="20.5" font-weight="800">{val}</text>'
            f'<text x="{x + 12}" y="{y + 55}" class="mono dim" font-size="9">{label}</text>'
            f'</g>'
        )

    pct = max(0.5, min(99.9, 100 - s["rank"]["percentile"]))
    bar_x, bar_y, bar_w = 17, 168, 466
    body.append(
        f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="42" rx="10" fill="{T["chrome"]}" stroke="{T["border"]}"/>'
        f'<text x="{bar_x + 14}" y="{bar_y + 17}" class="mono muted" font-size="10">GITHUB RATING · GRADE <tspan fill="{T["accent"]}" font-weight="700">{esc(s["rank"]["level"])}</tspan></text>'
        f'<text x="{bar_x + bar_w - 14}" y="{bar_y + 17}" text-anchor="end" class="mono sky" font-size="10">TOP {max(s["rank"]["percentile"], 0.1):.1f}%</text>'
        f'<rect x="{bar_x + 14}" y="{bar_y + 26}" width="{bar_w - 28}" height="6" rx="3" fill="{T["grid"]}"/>'
        f'<rect class="grow" x="{bar_x + 14}" y="{bar_y + 26}" width="{max(16, (bar_w - 28) * pct / 100):.1f}" height="6" rx="3" fill="url(#accentLine)"/>'
    )
    return panel(w, h, "GITHUB OVERVIEW", "\n".join(body), tag=f"@{s['login']}", accent=T["accent"])


# --------------------------------------------------------------- streak ----

def streak_card(st: dict) -> str:
    """Three clean Material streak cards."""
    w, h = 500, 266
    today = st["today"]
    boxes = [
        ("TOTAL", fmt_short(st["total"]), f"since {_fmt_day(st['first'])}", T["sky"]),
        ("CURRENT", str(st["current"]), _fmt_range(st["current_range"], today), T["accent"]),
        ("LONGEST", str(st["longest"]), _fmt_range(st["longest_range"], today), T["amber"]),
    ]
    body = []
    bw = 148
    for i, (label, val, sub, color) in enumerate(boxes):
        x = 17 + i * (bw + 11)
        is_mid = i == 1
        stroke = color if is_mid else T["border"]
        body.append(
            f'<g class="fade" {delay(0.1 * i)}>'
            f'<rect x="{x}" y="16" width="{bw}" height="156" rx="12" fill="{T["surface"]}" stroke="{stroke}" stroke-width="{1.4 if is_mid else 1}"/>'
            f'<text x="{x + bw / 2:.1f}" y="44" text-anchor="middle" class="mono" font-size="10" fill="{color}" letter-spacing="1">{label}</text>'
            f'<text x="{x + bw / 2:.1f}" y="100" text-anchor="middle" font-size="36" font-weight="800">{esc(val)}</text>'
            f'<text x="{x + bw / 2:.1f}" y="124" text-anchor="middle" class="mono muted" font-size="10.5">days</text>'
            f'<text x="{x + bw / 2:.1f}" y="150" text-anchor="middle" class="mono dim" font-size="9.5">{esc(sub)}</text>'
            f'</g>'
        )
    body.append(
        f'<rect x="17" y="186" width="466" height="24" rx="8" fill="{T["chrome"]}" stroke="{T["border"]}"/>'
        f'<text x="250" y="202" text-anchor="middle" class="mono dim" font-size="10">UTC CONTRIBUTION STREAK · ≥1 EVENT / DAY</text>'
    )
    return panel(w, h, "CONTRIBUTION STREAK", "\n".join(body), tag="DAILY SYNC", accent=T["accent"])


# ------------------------------------------------------------ languages ----

def languages_card(langs: list[dict], sample: int) -> str:
    """Horizontal ranked progress bars per language."""
    w, h = 500, 266
    body = []
    shown = langs[:6]
    max_pct = max((l["pct"] for l in shown), default=100.0) or 1.0
    for i, lang in enumerate(shown):
        y = 18 + i * 31
        bw = 240 * (lang["pct"] / max_pct)
        body.append(
            f'<g class="fade" {delay(0.07 * i)}>'
            f'<circle cx="24" cy="{y + 9}" r="4.5" fill="{lang["color"]}"/>'
            f'<text x="38" y="{y + 13}" font-size="12.5" font-weight="600">{esc(lang["name"])}</text>'
            f'<rect x="168" y="{y + 4}" width="240" height="9" rx="4.5" fill="{T["grid"]}"/>'
            f'<rect class="grow" x="168" y="{y + 4}" width="{max(6, bw):.1f}" height="9" rx="4.5" fill="{lang["color"]}"><title>{esc(lang["name"])}: {lang["pct"]:.1f}%</title></rect>'
            f'<text x="480" y="{y + 13}" text-anchor="end" class="mono muted" font-size="11.5">{lang["pct"]:.1f}%</text>'
            f'</g>'
        )
    body.append(
        f'<text x="18" y="212" class="mono dim" font-size="10">WEIGHTED BY LAST {fmt_int(sample)} COMMITS</text>'
    )
    return panel(w, h, "LANGUAGE MIX", "\n".join(body), tag="COMMIT-WEIGHTED", accent=T["sky"])


# ---------------------------------------------------------------- clock ----

PERIODS = (
    ("LATE NIGHT", range(0, 6), T["violet"]),
    ("MORNING", range(6, 12), T["amber"]),
    ("DAYTIME", range(12, 18), T["accent"]),
    ("EVENING", range(18, 24), T["sky"]),
)


def clock_card(clock: dict) -> str:
    """4 Day-Part KPI tiles over a 24h histogram."""
    w, h = 500, 266
    hours, weekdays, sample = clock["hours"], clock["weekdays"], max(clock["sample"], 1)
    period_totals = {name: sum(hours[i] for i in rng) for name, rng, _ in PERIODS}
    top_period = max(period_totals, key=period_totals.get)
    top_day = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[weekdays.index(max(weekdays))]
    color_of = {i: c for _, rng, c in PERIODS for i in rng}

    body = []
    pw = 109
    for idx, (name, _, color) in enumerate(PERIODS):
        x = 17 + idx * (pw + 10)
        tot = period_totals[name]
        pct = tot * 100 / sample
        active = name == top_period
        body.append(
            f'<g class="fade" {delay(0.07 * idx)}>'
            f'<rect x="{x}" y="14" width="{pw}" height="56" rx="10" fill="{T["surface"]}" stroke="{color if active else T["border"]}"/>'
            f'<text x="{x + 12}" y="32" class="mono" font-size="9" fill="{color}">{name}</text>'
            f'<text x="{x + 12}" y="55" font-size="18" font-weight="800">{pct:.0f}%</text>'
            f'<text x="{x + pw - 10}" y="55" text-anchor="end" class="mono dim" font-size="10">{tot}</text>'
            f'</g>'
        )

    x0, base, max_h, slot = 20, 176, 76, 19.2
    peak = max(hours) or 1
    body.append(f'<rect x="17" y="82" width="466" height="114" rx="10" fill="{T["chrome"]}" stroke="{T["border"]}"/>')
    for i, v in enumerate(hours):
        bh = max(3, max_h * v / peak)
        x = x0 + i * slot + 3
        body.append(
            f'<rect class="rise" {delay(i * 0.02)} x="{x:.1f}" y="{base - bh:.1f}" width="12" height="{bh:.1f}" rx="2.5" fill="{color_of[i]}" opacity="{0.38 + 0.62 * v / peak:.2f}"><title>{i:02d}:00 — {v} commits</title></rect>'
        )
    for hr in (0, 6, 12, 18, 23):
        body.append(f'<text x="{x0 + hr * slot + 9:.1f}" y="191" font-size="9.5" class="mono dim" text-anchor="middle">{hr:02d}h</text>')

    body.append(
        f'<text x="18" y="213" class="mono muted" font-size="10">PEAK DAY: <tspan fill="{T["accent"]}" font-weight="700">{top_day.upper()}</tspan> · SAMPLE {fmt_int(clock["sample"])} COMMITS</text>'
    )
    return panel(w, h, "COMMIT CADENCE", "\n".join(body), tag="LOCAL TIME", accent=T["accent"])


# -------------------------------------------------------- contributions ----

def contributions_card(days: list[tuple[str, int]], span: int = 90) -> str:
    w, h = 1000, 296
    pts = days[-span:]
    total = sum(v for _, v in pts)
    avg = total / max(len(pts), 1)
    peak = max((v for _, v in pts), default=0)
    left, right, top, bottom = 56, 976, 36, 206
    y_max = max(4, math.ceil(peak / 4) * 4)
    step = (right - left) / max(len(pts) - 1, 1)

    def xy(i: int, v: float) -> tuple[float, float]:
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

    if avg > 0:
        _, avg_y = xy(0, avg)
        body.append(
            f'<line x1="{left}" y1="{avg_y:.1f}" x2="{right}" y2="{avg_y:.1f}" stroke="{T["sky"]}" stroke-opacity=".40" stroke-dasharray="5 5"/>'
        )

    coords = [xy(i, v) for i, (_, v) in enumerate(pts)]
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in coords) if coords else "M0,0"
    area = f"{line} L{coords[-1][0]:.1f},{bottom} L{coords[0][0]:.1f},{bottom} Z" if coords else ""
    css = (
        "@keyframes draw { from { stroke-dashoffset: 1; } } "
        ".draw { stroke-dasharray: 1; stroke-dashoffset: 0; animation: draw 2.2s ease-out both; }"
    )
    body.append(
        f'<defs><linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{T["accent"]}" stop-opacity=".28"/><stop offset="1" stop-color="{T["accent"]}" stop-opacity="0"/>'
        f"</linearGradient></defs>"
        f'<path class="fade" {delay(0.7)} d="{area}" fill="url(#areaGrad)"/>'
        f'<path class="draw" pathLength="1" d="{line}" fill="none" stroke="url(#accentLine)" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>'
    )
    if pts and peak:
        i_peak = max(range(len(pts)), key=lambda i: pts[i][1])
        px, py = coords[i_peak]
        anchor = "end" if px > right - 85 else "start"
        dx = -10 if anchor == "end" else 10
        body.append(
            f'<g class="fade" {delay(1.6)}><circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{T["bg"]}" stroke="{T["accent"]}" stroke-width="2.2"/>'
            f'<text x="{px + dx:.1f}" y="{py + 4:.1f}" font-size="11" class="mono accent" text-anchor="{anchor}">PEAK {peak}</text></g>'
        )
    body.append(
        f'<text x="{left}" y="20" font-size="11" class="mono"><tspan class="accent" font-weight="700">{fmt_int(total)}</tspan> '
        f'<tspan class="muted">CONTRIBUTIONS · AVG {avg:.1f}/DAY</tspan></text>'
    )
    return panel(w, h, f"CONTRIBUTION TIMELINE · {span}D", "\n".join(body), extra_css=css, tag="ROLLING WINDOW", accent=T["accent"])


# ------------------------------------------------------------- milestones ----

TIER_COLORS = {"S": T["amber"], "A": T["accent"], "B": T["sky"], "C": T["muted"]}


def _hex_badge(cx: float, cy: float, color: str, tier: str | None) -> str:
    r = 24
    pts = " ".join(f"{cx + r * math.cos(math.radians(60 * k - 90)):.1f},{cy + r * math.sin(math.radians(60 * k - 90)):.1f}" for k in range(6))
    label = esc(tier or "—")
    fill = color if tier else T["grid"]
    return (
        f'<polygon points="{pts}" fill="{fill}" fill-opacity=".14" stroke="{fill}" stroke-width="1.8"/>'
        f'<text x="{cx:.1f}" y="{cy + 5:.1f}" text-anchor="middle" font-size="{14 if len(label) < 3 else 11.5}" font-weight="800" fill="{fill}">{label}</text>'
    )


def trophies_card(s: dict) -> str:
    """Hexagon Milestone Badges."""
    items = [
        ("Contributions", s["contrib_all"], fmt_short(s["contrib_all"])),
        ("Stars", s["stars"], fmt_short(s["stars"])),
        ("Followers", s["followers"], fmt_short(s["followers"])),
        ("Repos", s["repos"], fmt_short(s["repos"])),
        ("Pull Reqs", s["prs"], fmt_short(s["prs"])),
        ("Issues", s["issues"], fmt_short(s["issues"])),
        ("Reviews", s["reviews_year"], fmt_short(s["reviews_year"])),
        ("Tenure", s["years"], f"{s['years']:.1f}y"),
    ]
    from .github import trophy_tier

    w, h = 1000, 194
    col = (w - 32) / len(items)
    body = []
    for i, (name, value, shown) in enumerate(items):
        key = {"Repos": "Repositories", "Pull Reqs": "Pull Requests", "Tenure": "Experience"}.get(name, name)
        tier = trophy_tier(key, value)
        color = TIER_COLORS[tier[0]] if tier else T["dim"]
        cx = 16 + col * i + col / 2
        body.append(
            f'<g class="fade" {delay(0.06 * i)}>'
            f'<rect x="{cx - col / 2 + 5:.1f}" y="14" width="{col - 10:.1f}" height="128" rx="12" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f"{_hex_badge(cx, 53, color, tier)}"
            f'<text x="{cx:.1f}" y="104" text-anchor="middle" font-size="12" font-weight="700">{esc(name)}</text>'
            f'<text x="{cx:.1f}" y="124" text-anchor="middle" font-size="11" class="mono muted">{esc(shown)}</text>'
            f"</g>"
        )
    return panel(w, h, "MILESTONES", "\n".join(body), tag="SSS › C", accent=T["amber"])


def views_badge(count: int) -> str:
    """28px badge matching the restrained Material badge row."""
    label, value = "VIEWS", fmt_int(count)
    left = 34 + len(label) * 7.2 + 10
    right = len(value) * 8.2 + 22
    w, h = round(left + right), 28
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Profile views: {value}">
<title>Profile views: {value}</title>
<defs><clipPath id="vc"><rect width="{w}" height="{h}" rx="7"/></clipPath></defs>
<g clip-path="url(#vc)">
  <rect width="{w}" height="{h}" fill="{T['surface']}"/>
  <rect x="{left:.1f}" width="{right:.1f}" height="{h}" fill="{T['chrome']}"/>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="7" fill="none" stroke="{T['border']}"/>
<g transform="translate(11 6)" fill="none" stroke="{T['accent']}" stroke-width="1.6">
  <path d="M1 8s2.8-5 7-5 7 5 7 5-2.8 5-7 5-7-5-7-5z"/><circle cx="8" cy="8" r="2.2" fill="{T['accent']}"/>
</g>
<text x="33" y="18" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="0.8" fill="{T['muted']}" style="white-space:pre">{label}</text>
<text x="{left + right / 2:.1f}" y="18.5" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{T['accent']}">{value}</text>
</svg>
"""


def placeholder_card(w: int, h: int, title: str, message: str) -> str:
    body = f'<text x="{w / 2}" y="{(h - HEADER_H) / 2 + 4}" text-anchor="middle" font-size="13" class="mono muted">{esc(message)}</text>'
    return panel(w, h, title, body)
