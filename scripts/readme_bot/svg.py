"""SVG primitives for @2b-adrix's executive Monochrome Obsidian + Android Emerald theme."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

THEME = {
    "bg": "#090c10",       # deep obsidian canvas
    "chrome": "#0e131b",   # subtle header strip
    "surface": "#121822",  # card surface
    "border": "#1f2937",   # clean hairline border
    "grid": "#18202c",     # subtle graph grid
    "text": "#f8fafc",     # crisp primary text
    "muted": "#94a3b8",    # secondary text
    "dim": "#64748b",      # muted metadata
    "accent": "#3ddc84",   # Android emerald
    "sky": "#38bdf8",      # subtle cool slate-blue
    "amber": "#f59e0b",    # warm amber
    "violet": "#a78bfa",   # Kotlin accent
}

SANS = "'Inter', 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

HEADER_H = 38

BASE_CSS = f"""
text {{ font-family: {SANS}; fill: {THEME['text']}; }}
.mono {{ font-family: {MONO}; white-space: pre; }}
.muted {{ fill: {THEME['muted']}; }}
.dim {{ fill: {THEME['dim']}; }}
.accent {{ fill: {THEME['accent']}; }}
.sky {{ fill: {THEME['sky']}; }}
.fade {{ animation: fadeIn .55s ease-out both; }}
.grow {{ animation: growX .9s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: left center; }}
.rise {{ animation: growY .9s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: center bottom; }}
.pulse {{ animation: pulseDot 2.6s ease-in-out infinite; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(3px); }} to {{ opacity: 1; transform: none; }} }}
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
    title: str,
    body: str,
    *,
    extra_css: str = "",
    tag: str = "",
    accent: str | None = None,
) -> str:
    """Wrap `body` in a crisp, restrained obsidian engineering panel."""
    t = THEME
    ac = accent or t["accent"]
    right_tag = (
        f'<text x="{width - 20}" y="23" text-anchor="end" class="mono dim" font-size="10">{esc(tag)}</text>'
        if tag
        else ""
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>{BASE_CSS}{extra_css}</style>
<defs>
  <linearGradient id="accentLine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['sky']}"/>
  </linearGradient>
  <clipPath id="panelClip"><rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#panelClip)">
  <rect width="{width}" height="{height}" fill="{t['bg']}"/>
  <rect width="{width}" height="{HEADER_H}" fill="{t['chrome']}"/>
  <line x1="0" y1="{HEADER_H}" x2="{width}" y2="{HEADER_H}" stroke="{t['border']}"/>
  <circle cx="20" cy="19" r="3.5" fill="{ac}"/>
  <text x="32" y="23" class="mono muted" font-size="11" font-weight="600" letter-spacing="0.8">{esc(title)}</text>
  {right_tag}
  <g transform="translate(0 {HEADER_H})">
{body}
  </g>
</g>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="14" fill="none" stroke="{t['border']}"/>
</svg>
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote {path.as_posix()} ({len(content):,} bytes)")
