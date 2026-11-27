"""SVG primitives for @2b-adrix's Material HUD / Android Blueprint theme."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

THEME = {
    "bg": "#0c0e12",       # warm carbon graphite
    "chrome": "#12161f",   # elevated panel header
    "surface": "#181d29",  # Material card surface
    "surface2": "#1e2536", # highlighted surface
    "border": "#262d3d",   # crisp slate hairline
    "grid": "#1c2230",     # subtle blueprint grid
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "dim": "#64748b",
    "mint": "#3ddc84",     # official Android green
    "coral": "#ff8a4c",    # Kotlin / warm amber-coral
    "sky": "#38bdf8",      # electric sky
    "kotlin": "#a97bff",   # Kotlin violet
    "gold": "#fbbf24",
}

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

HEADER_H = 40

BASE_CSS = f"""
text {{ font-family: {SANS}; fill: {THEME['text']}; }}
.mono {{ font-family: {MONO}; white-space: pre; }}
.muted {{ fill: {THEME['muted']}; }}
.dim {{ fill: {THEME['dim']}; }}
.mint {{ fill: {THEME['mint']}; }}
.coral {{ fill: {THEME['coral']}; }}
.sky {{ fill: {THEME['sky']}; }}
.fade {{ animation: fadeIn .65s ease-out both; }}
.grow {{ animation: growX .95s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: left center; }}
.rise {{ animation: growY .95s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: center bottom; }}
.pulse {{ animation: pulseDot 2.4s ease-in-out infinite; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes growX {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
@keyframes growY {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
@keyframes pulseDot {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
"""


def esc(value: object) -> str:
    return escape(str(value), {'"': "&quot;"})


def delay(seconds: float) -> str:
    return f'style="animation-delay:{seconds:.2f}s"'


def fmt_int(n: int | float) -> str:
    return f"{int(n):,}"


def fmt_short(n: int | float) -> str:
    n = float(n)
    for div, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "k")):
        if abs(n) >= div:
            v = n / div
            return f"{v:.1f}".rstrip("0").rstrip(".") + suffix
    return f"{int(n)}"


def panel(
    width: int,
    height: int,
    kicker: str,
    body: str,
    *,
    extra_css: str = "",
    tag: str = "",
    accent: str | None = None,
) -> str:
    """Wrap `body` in an elevated Material Dark HUD card with specular sheen & corner reticles."""
    t = THEME
    ac = accent or t["mint"]
    right_tag = ""
    if tag:
        tw = len(tag) * 6.8 + 30
        tx = width - 16 - tw
        right_tag = (
            f'<rect x="{tx:.1f}" y="10" width="{tw:.1f}" height="20" rx="10" fill="{t["surface"]}" stroke="{t["border"]}"/>'
            f'<circle cx="{tx + 11:.1f}" cy="20" r="2.5" fill="{ac}"/>'
            f'<text x="{tx + 20:.1f}" y="23.5" class="mono dim" font-size="9.8">{esc(tag)}</text>'
        )

    reticles = (
        f'<path d="M12 6 h-6 v6 M{width - 12} 6 h6 v6 M12 {height - 6} h-6 v-6 M{width - 12} {height - 6} h6 v-6" '
        f'fill="none" stroke="{ac}" stroke-opacity=".42" stroke-width="1.3"/>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(kicker)}">
<title>{esc(kicker)}</title>
<style>{BASE_CSS}{extra_css}</style>
<defs>
  <linearGradient id="brandGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['mint']}"/><stop offset=".55" stop-color="{t['sky']}"/><stop offset="1" stop-color="{t['coral']}"/>
  </linearGradient>
  <linearGradient id="topSheen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ac}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{ac}" stop-opacity=".75"/>
    <stop offset="1" stop-color="{ac}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="hudGlow" cx="14%" cy="10%" r="75%">
    <stop offset="0" stop-color="{ac}" stop-opacity=".11"/>
    <stop offset="1" stop-color="{ac}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="panelClip"><rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#panelClip)">
  <rect width="{width}" height="{height}" fill="{t['bg']}"/>
  <rect width="{width}" height="{height}" fill="url(#hudGlow)"/>
  <rect width="{width}" height="{HEADER_H}" fill="{t['chrome']}"/>
  <rect x="0" y="0" width="{width}" height="1.6" fill="url(#topSheen)"/>
  <line x1="0" y1="{HEADER_H}" x2="{width}" y2="{HEADER_H}" stroke="{t['border']}"/>
  <rect x="18" y="16" width="16" height="6" rx="3" fill="{ac}"/>
  <text x="42" y="23.5" class="mono muted" font-size="11" font-weight="600" letter-spacing="1">{esc(kicker)}</text>
  {right_tag}
  <g transform="translate(0 {HEADER_H})">
{body}
  </g>
</g>
{reticles}
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="18" fill="none" stroke="{t['border']}"/>
</svg>
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote {path.as_posix()} ({len(content):,} bytes)")


# ------------------------------------ terminal chrome for telemetry cards ----

CHROME_H = 36

TERM_THEME = {
    "bg": "#0b0f14",
    "chrome": "#11161d",
    "border": "#232b36",
    "grid": "#1b222c",
    "text": "#e6edf3",
    "muted": "#8b949e",
    "dim": "#4b5563",
    "accent": "#22d3ee",
    "accent2": "#a78bfa",
    "ok": "#34d399",
    "warn": "#fbbf24",
}

TERM_CSS = f"""
text {{ font-family: {SANS}; fill: {TERM_THEME['text']}; }}
.mono {{ font-family: {MONO}; white-space: pre; }}
.muted {{ fill: {TERM_THEME['muted']}; }}
.dim {{ fill: {TERM_THEME['dim']}; }}
.accent {{ fill: {TERM_THEME['accent']}; }}
.accent2 {{ fill: {TERM_THEME['accent2']}; }}
.ok {{ fill: {TERM_THEME['ok']}; }}
.fade {{ animation: fadeIn .6s ease-out both; }}
.grow {{ animation: growX .9s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: left center; }}
.rise {{ animation: growY .9s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: center bottom; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes growX {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
@keyframes growY {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
"""


def card(width: int, height: int, title: str, body: str, *, extra_css: str = "", right_label: str = "") -> str:
    """Wrap `body` in a rounded terminal-window chrome."""
    t = TERM_THEME
    right = (
        f'<text x="{width - 18}" y="{CHROME_H / 2 + 4}" text-anchor="end" class="mono dim" font-size="11">{esc(right_label)}</text>'
        if right_label
        else ""
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>{TERM_CSS}{extra_css}</style>
<defs>
  <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['accent2']}"/>
  </linearGradient>
  <clipPath id="cardClip"><rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12"/></clipPath>
</defs>
<g clip-path="url(#cardClip)">
  <rect width="{width}" height="{height}" fill="{t['bg']}"/>
  <rect width="{width}" height="{CHROME_H}" fill="{t['chrome']}"/>
  <line x1="0" y1="{CHROME_H}" x2="{width}" y2="{CHROME_H}" stroke="{t['border']}"/>
  <circle cx="20" cy="{CHROME_H / 2}" r="5.5" fill="#ff5f57"/>
  <circle cx="38" cy="{CHROME_H / 2}" r="5.5" fill="#febc2e"/>
  <circle cx="56" cy="{CHROME_H / 2}" r="5.5" fill="#28c840"/>
  <text x="76" y="{CHROME_H / 2 + 4}" class="mono muted" font-size="12">{esc(title)}</text>
  {right}
  <g transform="translate(0 {CHROME_H})">
{body}
  </g>
</g>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="{t['border']}"/>
</svg>
"""
