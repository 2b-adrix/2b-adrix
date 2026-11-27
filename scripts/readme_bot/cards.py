"""Renderers that turn collected data into terminal-themed SVG cards."""

from __future__ import annotations

import math
from datetime import date

from .svg import CHROME_H, MONO, THEME, card, delay, esc, fmt_int, fmt_short

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
        f'<circle cx="{cx}" cy="{cy}" r="{r + 9}" fill="none" stroke="{T["grid"]}" stroke-width="1" stroke-dasharray="3 4"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{T["grid"]}" stroke-width="8"/>'
        f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#accentGrad)" stroke-width="8" '
        f'stroke-linecap="round" stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}" transform="rotate(-90 {cx} {cy})"/>'
        f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" font-size="30" font-weight="700" class="fade" {delay(0.6)}>{esc(s["rank"]["level"])}</text>'
        f'<rect x="{cx - 42}" y="{cy + r + 16}" width="84" height="20" rx="10" fill="{T["surface"]}" stroke="{T["border"]}"/>'
        f'<text x="{cx}" y="{cy + r + 30}" text-anchor="middle" class="mono accent" font-size="10.5">top {max(s["rank"]["percentile"], 0.1):.1f}%</text>'
    )
    return card(w, h, "~/github/stats.yaml", "\n".join(body), extra_css=css, right_label=s["name"])


def streak_card(st: dict) -> str:
    w, h = 500, 240
    today = st["today"]
    cols = [83, 250, 417]
    body = [
        f'<line x1="166" y1="30" x2="166" y2="166" stroke="{T["border"]}"/>',
        f'<line x1="334" y1="30" x2="334" y2="166" stroke="{T["border"]}"/>',
        f'<g class="fade" {delay(0.1)}>'
        f'<text x="{cols[0]}" y="88" text-anchor="middle" font-size="28" font-weight="700">{fmt_short(st["total"])}</text>'
        f'<text x="{cols[0]}" y="118" text-anchor="middle" font-size="13" class="muted">Total Contributions</text>'
        f'<text x="{cols[0]}" y="142" text-anchor="middle" font-size="11" class="mono dim">since {esc(_fmt_day(st["first"]))}</text>'
        f"</g>",
        f'<circle cx="{cols[1]}" cy="78" r="46" fill="none" stroke="{T["grid"]}" stroke-width="1" stroke-dasharray="3 4"/>'
        f'<circle cx="{cols[1]}" cy="78" r="39" fill="none" stroke="url(#accentGrad)" stroke-width="5"/>'
        f'<g class="fade" {delay(0.3)}>'
        f'<text x="{cols[1]}" y="88" text-anchor="middle" font-size="28" font-weight="700">{st["current"]}</text>'
        f'<text x="{cols[1]}" y="142" text-anchor="middle" font-size="13" font-weight="600" class="ok">Current Streak</text>'
        f'<text x="{cols[1]}" y="162" text-anchor="middle" font-size="11" class="mono dim">{esc(_fmt_range(st["current_range"], today))}</text>'
        f"</g>",
        f'<g class="fade" {delay(0.5)}>'
        f'<text x="{cols[2]}" y="88" text-anchor="middle" font-size="28" font-weight="700">{st["longest"]}</text>'
        f'<text x="{cols[2]}" y="118" text-anchor="middle" font-size="13" class="muted">Longest Streak</text>'
        f'<text x="{cols[2]}" y="142" text-anchor="middle" font-size="11" class="mono dim">{esc(_fmt_range(st["longest_range"], today))}</text>'
        f"</g>",
        '<text x="250" y="192" text-anchor="middle" font-size="11" class="mono dim">days with ≥1 contribution · UTC</text>',
    ]
    return card(w, h, "~/github/streak.log", "\n".join(body), right_label="since day one")


def languages_card(langs: list[dict], sample: int) -> str:
    w, h = 500, 240
    x0, bar_w = 24, 452
    body = [f'<clipPath id="barClip"><rect x="{x0}" y="22" width="{bar_w}" height="11" rx="5.5"/></clipPath>']
    cursor = float(x0)
    segs = []
    for lang in langs:
        seg = bar_w * lang["pct"] / 100
        segs.append(f'<rect x="{cursor:.2f}" y="22" width="{max(seg, 0):.2f}" height="11" fill="{lang["color"]}"><title>{esc(lang["name"])}: {lang["pct"]:.1f}%</title></rect>')
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
    body.append(f'<text x="24" y="194" font-size="11" class="mono dim">weighted by last {fmt_int(sample)} commits</text>')
    return card(w, h, "~/github/languages.json", "\n".join(body), right_label="top languages")


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
    cx0, base, max_h, step = 24, 158, 94, 11.5
    peak = max(hours) or 1
    body.append(f'<line x1="{cx0}" y1="{base + 0.5}" x2="{cx0 + 24 * step}" y2="{base + 0.5}" stroke="{T["border"]}"/>')
    for i, v in enumerate(hours):
        bh = max(2, max_h * v / peak)
        body.append(
            f'<rect class="rise" {delay(i * 0.025)} x="{cx0 + i * step + 1.5:.1f}" y="{base - bh:.1f}" width="8" height="{bh:.1f}" rx="2" fill="{color_of[i]}" opacity="{0.45 + 0.55 * v / peak:.2f}"><title>{i:02d}:00 — {v} commits</title></rect>'
        )
    for hr in (0, 6, 12, 18, 23):
        body.append(f'<text x="{cx0 + hr * step + 5.5:.1f}" y="{base + 15}" font-size="10" class="mono dim" text-anchor="middle">{hr:02d}h</text>')

    wx, peak_d = 330, max(weekdays) or 1
    for i, (label, v) in enumerate(zip(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), weekdays)):
        y = 54 + i * 17
        bw = 90 * v / peak_d
        body.append(
            f'<text x="{wx}" y="{y + 8}" font-size="10.5" class="mono muted">{label}</text>'
            f'<rect x="{wx + 32}" y="{y}" width="90" height="9" rx="4.5" fill="{T["grid"]}"/>'
            f'<rect class="grow" {delay(0.3 + i * 0.05)} x="{wx + 32}" y="{y}" width="{max(bw, 3):.1f}" height="9" rx="4.5" fill="url(#accentGrad)"/>'
            f'<text x="{wx + 146}" y="{y + 8}" font-size="10" class="mono dim" text-anchor="end">{v * 100 / sample:.0f}%</text>'
        )
    body.append(f'<text x="24" y="194" font-size="11" class="mono dim">author-local time · last {fmt_int(clock["sample"])} commits</text>')
    return card(w, h, "~/github/commit-clock.sh", "\n".join(body), right_label="when I ship")


def contributions_card(days: list[tuple[str, int]], span: int = 90) -> str:
    w, h = 1000, 300
    pts = days[-span:]
    total = sum(v for _, v in pts)
    avg = total / max(len(pts), 1)
    peak = max((v for _, v in pts), default=0)
    left, right, top, bottom = 56, 976, 36, 212
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
            f'<line x1="{left}" y1="{avg_y:.1f}" x2="{right}" y2="{avg_y:.1f}" stroke="{T["ok"]}" stroke-opacity=".35" stroke-dasharray="4 4"/>'
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
        f'<stop offset="0" stop-color="{T["ok"]}" stop-opacity=".30"/><stop offset="1" stop-color="{T["accent"]}" stop-opacity="0"/>'
        f"</linearGradient></defs>"
        f'<path class="fade" {delay(0.8)} d="{area}" fill="url(#areaGrad)"/>'
        f'<path class="draw" pathLength="1" d="{line}" fill="none" stroke="url(#accentGrad)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'
    )
    if pts and peak:
        i_peak = max(range(len(pts)), key=lambda i: pts[i][1])
        px, py = coords[i_peak]
        anchor = "end" if px > right - 85 else "start"
        dx = -10 if anchor == "end" else 10
        body.append(
            f'<g class="fade" {delay(1.8)}><circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{T["bg"]}" stroke="{T["accent2"]}" stroke-width="2"/>'
            f'<text x="{px + dx:.1f}" y="{py + 4:.1f}" font-size="11" class="mono accent2" text-anchor="{anchor}">peak {peak}</text></g>'
        )
    body.append(
        f'<text x="{left}" y="20" font-size="12" class="mono"><tspan class="accent">$</tspan> git log --since="{span} days ago" '
        f'<tspan class="muted">| wc -l</tspan>  <tspan font-weight="700">{fmt_int(total)}</tspan> <tspan class="muted">contributions · avg {avg:.1f}/day</tspan></text>'
    )
    return card(w, h, "~/github/contributions.graph", "\n".join(body), extra_css=css, right_label=f"last {span} days")


TIER_COLORS = {"S": "#fbbf24", "A": "#22d3ee", "B": "#a78bfa", "C": "#94a3b8"}


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
            f'<rect x="{cx - col / 2 + 6:.1f}" y="14" width="{col - 12:.1f}" height="132" rx="10" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f"{_cup(cx, 28, color, tier)}"
            f'<text x="{cx:.1f}" y="104" text-anchor="middle" font-size="12.5" font-weight="600">{esc(name)}</text>'
            f'<text x="{cx:.1f}" y="124" text-anchor="middle" font-size="11.5" class="mono muted">{esc(shown)}</text>'
            f"</g>"
        )
    return card(w, h, "~/github/trophies", "\n".join(body), right_label="SSS › SS › S › AAA › AA › A › B › C")


def views_badge(count: int) -> str:
    """Profile-views pill sized to match the 28px social badges."""
    label, value = "PROFILE VIEWS", fmt_int(count)
    left = 34 + len(label) * 7.4 + 12
    right = len(value) * 8.4 + 26
    w, h = round(left + right), 28
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Profile views: {value}">
<title>Profile views: {value}</title>
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T['accent']}"/><stop offset=".5" stop-color="{T['ok']}"/><stop offset="1" stop-color="{T['accent2']}"/></linearGradient>
  <clipPath id="c"><rect width="{w}" height="{h}" rx="6"/></clipPath>
</defs>
<g clip-path="url(#c)">
  <rect width="{w}" height="{h}" fill="{T['chrome']}"/>
  <rect x="{left:.1f}" width="{right:.1f}" height="{h}" fill="{T['bg']}"/>
  <rect x="{left:.1f}" y="{h - 2}" width="{right:.1f}" height="2" fill="url(#g)"/>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="6" fill="none" stroke="{T['border']}"/>
<g transform="translate(11 6)" fill="none" stroke="{T['ok']}" stroke-width="1.6">
  <path d="M1 8s2.8-5 7-5 7 5 7 5-2.8 5-7 5-7-5-7-5z"/><circle cx="8" cy="8" r="2.2" fill="{T['ok']}"/>
</g>
<text x="34" y="18" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1" fill="{T['muted']}" style="white-space:pre">{label}</text>
<text x="{left + right / 2:.1f}" y="18.5" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="800" fill="{T['text']}">{value}</text>
</svg>
"""


def placeholder_card(w: int, h: int, title: str, message: str) -> str:
    body = f'<text x="{w / 2}" y="{(h - CHROME_H) / 2 + 4}" text-anchor="middle" font-size="13" class="mono muted">{esc(message)}</text>'
    return card(w, h, title, body)
