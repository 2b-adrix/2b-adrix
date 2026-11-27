"""SVG primitives for @2b-adrix's original Material HUD / Android Blueprint theme."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

THEME = {
    "bg": "#0c0e12",       # warm carbon graphite
    "chrome": "#12161f",   # elevated panel header
    "surface": "#181d29",  # Material card surface
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
    """Wrap `body` in an original Material Dark HUD card (no macOS traffic lights)."""
    t = THEME
    ac = accent or t["mint"]
    right_tag = ""
    if tag:
        tw = len(tag) * 6.8 + 20
        tx = width - 16 - tw
        right_tag = (
            f'<rect x="{tx:.1f}" y="10" width="{tw:.1f}" height="20" rx="10" fill="{t["surface"]}" stroke="{t["border"]}"/>'
            f'<text x="{tx + tw / 2:.1f}" y="23.5" text-anchor="middle" class="mono dim" font-size="10">{esc(tag)}</text>'
        )

    # Blueprint corner reticles
    reticles = (
        f'<path d="M12 6 h-6 v6 M{width - 12} 6 h6 v6 M12 {height - 6} h-6 v-6 M{width - 12} {height - 6} h6 v-6" '
        f'fill="none" stroke="{ac}" stroke-opacity=".35" stroke-width="1.2"/>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(kicker)}">
<title>{esc(kicker)}</title>
<style>{BASE_CSS}{extra_css}</style>
<defs>
  <linearGradient id="brandGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['mint']}"/><stop offset=".55" stop-color="{t['sky']}"/><stop offset="1" stop-color="{t['coral']}"/>
  </linearGradient>
  <radialGradient id="hudGlow" cx="12%" cy="10%" r="75%">
    <stop offset="0" stop-color="{ac}" stop-opacity=".08"/>
    <stop offset="1" stop-color="{ac}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="panelClip"><rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#panelClip)">
  <rect width="{width}" height="{height}" fill="{t['bg']}"/>
  <rect width="{width}" height="{height}" fill="url(#hudGlow)"/>
  <rect width="{width}" height="{HEADER_H}" fill="{t['chrome']}"/>
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
