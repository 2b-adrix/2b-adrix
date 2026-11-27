"""SVG primitives shared by every generated card."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

THEME = {
    "bg": "#0b0f14",
    "chrome": "#11161d",
    "border": "#232b36",
    "grid": "#1b222c",
    "text": "#e6edf3",
    "muted": "#8b949e",
    "dim": "#4b5563",
    "accent": "#22d3ee",   # cyan
    "accent2": "#a78bfa",  # violet
    "ok": "#34d399",       # emerald
    "warn": "#fbbf24",     # amber
}

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

CHROME_H = 36

BASE_CSS = f"""
text {{ font-family: {SANS}; fill: {THEME['text']}; }}
.mono {{ font-family: {MONO}; white-space: pre; }}
.muted {{ fill: {THEME['muted']}; }}
.dim {{ fill: {THEME['dim']}; }}
.accent {{ fill: {THEME['accent']}; }}
.accent2 {{ fill: {THEME['accent2']}; }}
.ok {{ fill: {THEME['ok']}; }}
.fade {{ animation: fadeIn .6s ease-out both; }}
.grow {{ animation: growX .9s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: left center; }}
.rise {{ animation: growY .9s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: center bottom; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes growX {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
@keyframes growY {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
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


def card(width: int, height: int, title: str, body: str, *, extra_css: str = "", right_label: str = "") -> str:
    """Wrap `body` in a rounded terminal-window chrome."""
    t = THEME
    right = (
        f'<text x="{width - 18}" y="{CHROME_H / 2 + 4}" text-anchor="end" class="mono dim" font-size="11">{esc(right_label)}</text>'
        if right_label
        else ""
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>{BASE_CSS}{extra_css}</style>
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


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote {path.as_posix()} ({len(content):,} bytes)")
