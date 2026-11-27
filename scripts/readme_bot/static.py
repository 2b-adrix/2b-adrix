"""Static artwork: animated header banner, toolkit card, project cards, badges & footer."""

from __future__ import annotations

import base64
from pathlib import Path

from .svg import MONO, SANS, THEME, card, delay, esc, write

T = THEME
ICONS = Path(__file__).with_name("icons")

NAME = "Aditya Mishra"
ROLE = "Android & Backend Engineer"
TAGLINE = "B.Tech CSE · Mewar University '28 · Alpha-coders"
MOTTO = "Engineering products, not just projects."
CHIPS = ["Kotlin", "Jetpack Compose", "Spring Boot", "Firebase", "Clean Arch"]

TERMINAL = [
    (True, "whoami", ""),
    (False, "adrix — android & backend engineer", "muted"),
    (True, "adb shell getprop ro.adrix.stack", ""),
    (False, "MODULE        STATUS     STACK", "dim"),
    (False, "android-ui    Active     Kotlin · Compose", "ok"),
    (False, "backend-api   Active     Spring · MongoDB", "ok"),
    (False, "app-security  Learning   Clean Arch · DSA", "ok"),
    (True, "./gradlew :app:ship --release", ""),
    (False, "BUILD SUCCESSFUL — shipping products ✓", "accent"),
]

TOOLKIT = [
    ("Languages", ["Kotlin-Dark", "Java-Dark", "Python-Dark", "TypeScript", "JavaScript", "HTML", "CSS"], []),
    ("Android & UI", ["AndroidStudio-Dark", "Gradle-Dark", "Firebase-Dark", "SQLite"], ["Jetpack Compose", "MVVM", "Room", "CameraX"]),
    ("Backend & APIs", ["Spring-Dark", "MongoDB", "MySQL-Dark", "NodeJS-Dark", "REST", "Postman"], ["JWT", "RESTful"]),
    ("DevOps & Tools", ["Linux-Dark", "Git", "Github-Dark", "GithubActions-Dark", "VSCode-Dark"], ["App Security", "DSA"]),
]

LABELS = {
    "Kotlin": "Kotlin",
    "Java": "Java",
    "Python": "Python",
    "TypeScript": "TypeScript",
    "JavaScript": "JavaScript",
    "HTML": "HTML5",
    "CSS": "CSS3",
    "AndroidStudio": "Android Studio",
    "Gradle": "Gradle",
    "Firebase": "Firebase",
    "SQLite": "SQLite",
    "Spring": "Spring Boot",
    "MongoDB": "MongoDB",
    "MySQL": "MySQL",
    "NodeJS": "Node.js",
    "REST": "REST API",
    "Postman": "Postman",
    "Linux": "Linux",
    "Git": "Git",
    "Github": "GitHub",
    "GithubActions": "GitHub Actions",
    "VSCode": "VS Code",
}

PROJECTS = [
    {
        "file": "krishiva-native.svg",
        "name": "Krishiva-Native",
        "tag": "AI · AGRITECH",
        "lang": "Kotlin",
        "lang_color": "#a97bff",
        "desc": [
            "AI agricultural platform with instant crop disease",
            "diagnosis via Gemini AI + CameraX & Mandi prices.",
        ],
        "pills": ["Jetpack Compose", "CameraX", "Gemini AI"],
        "accent": "#34d399",
    },
    {
        "file": "arogyagrid.svg",
        "name": "Arogyagrid",
        "tag": "HEALTHTECH · FULLSTACK",
        "lang": "Kotlin + Java",
        "lang_color": "#22d3ee",
        "desc": [
            "Native Android healthcare client powered by a",
            "dedicated Spring Boot REST API backend.",
        ],
        "pills": ["Kotlin", "Spring Boot", "REST API"],
        "accent": "#22d3ee",
    },
    {
        "file": "phantom-lens.svg",
        "name": "Phantom-Lens",
        "tag": "ANDROID · CAMERA",
        "lang": "Kotlin",
        "lang_color": "#a97bff",
        "desc": [
            "Native Kotlin Android camera & visual utility",
            "built around clean MVVM separation of concerns.",
        ],
        "pills": ["Kotlin", "Android", "MVVM"],
        "accent": "#a78bfa",
    },
    {
        "file": "alpha-chat-native.svg",
        "name": "Alpha-Chat-Native",
        "tag": "REALTIME · MESSAGING",
        "lang": "Kotlin",
        "lang_color": "#a97bff",
        "desc": [
            "Native real-time Android chat application with",
            "instant sync and Firebase authentication.",
        ],
        "pills": ["Kotlin", "Firebase", "Realtime"],
        "accent": "#fbbf24",
    },
]

BADGES = [
    (
        "portfolio.svg",
        "ADRIX.IS-A.DEV",
        "#070b12",
        '<svg fill="#22d3ee" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm6.93 6h-2.95a15.65 15.65 0 0 0-1.38-3.56A8.03 8.03 0 0 1 18.93 8ZM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96ZM4.26 14a7.83 7.83 0 0 1 0-4h3.38a16.5 16.5 0 0 0-.14 2c0 .68.05 1.35.14 2H4.26Zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56A7.99 7.99 0 0 1 5.08 16Zm2.95-8H5.08a7.99 7.99 0 0 1 4.33-3.56A15.65 15.65 0 0 0 8.03 8ZM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96ZM14.34 14H9.66a14.7 14.7 0 0 1-.16-2c0-.68.06-1.35.16-2h4.68c.1.65.16 1.32.16 2 0 .68-.06 1.35-.16 2Zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95a8.03 8.03 0 0 1-4.33 3.56ZM16.36 14c.09-.65.14-1.32.14-2 0-.68-.05-1.35-.14-2h3.38a7.83 7.83 0 0 1 0 4h-3.38Z"/></svg>',
    ),
    (
        "email.svg",
        "EMAIL",
        "#070b12",
        '<svg fill="#22d3ee" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"/></svg>',
    ),
    (
        "linkedin.svg",
        "LINKEDIN",
        "#0a66c2",
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#fff" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.125 2.062 2.062 0 0 1 0 4.125zM7.119 20.452H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    ),
    (
        "x.svg",
        "X (TWITTER)",
        "#000000",
        '<svg fill="white" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/></svg>',
    ),
    (
        "instagram.svg",
        "INSTAGRAM",
        "#e4405f",
        '<svg fill="white" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>',
    ),
    (
        "leetcode.svg",
        "LEETCODE",
        "#000000",
        '<svg fill="#FFA116" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.116 6.226l-3.854 4.126a5.266 5.266 0 0 0-1.209 2.104 5.35 5.35 0 0 0-.125.513 5.527 5.527 0 0 0 .062 2.362 5.83 5.83 0 0 0 .349 1.017 5.938 5.938 0 0 0 1.271 1.818l4.277 4.193.039.038c2.248 2.165 5.852 2.133 8.063-.074l2.396-2.392c.54-.54.54-1.414.003-1.955a1.378 1.378 0 0 0-1.951-.003l-2.396 2.392a3.021 3.021 0 0 1-4.205.038l-.02-.019-4.276-4.193c-.652-.64-.972-1.469-.948-2.263a2.68 2.68 0 0 1 .066-.523 2.545 2.545 0 0 1 .619-1.164L9.13 8.114c1.058-1.134 3.204-1.27 4.43-.278l3.501 2.831c.593.48 1.461.387 1.94-.207a1.384 1.384 0 0 0-.207-1.943l-3.5-2.831c-.8-.647-1.766-1.045-2.774-1.202l2.015-2.158A1.384 1.384 0 0 0 13.483 0zm-2.866 12.815a1.38 1.38 0 0 0-1.38 1.382 1.38 1.38 0 0 0 1.38 1.382H20.79a1.38 1.38 0 0 0 1.38-1.382 1.38 1.38 0 0 0-1.38-1.382z"/></svg>',
    ),
]


def _icon_uri(name: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode((ICONS / f"{name}.svg").read_bytes()).decode()


def badge_svg(label: str, color: str, icon_svg: str) -> str:
    text_len = len(label) * 7.8
    w = round(text_len + 44)
    h = 28
    icon_b64 = base64.b64encode(icon_svg.encode("utf-8")).decode("ascii")
    cx = round((32 + w - 8) / 2 * 10)
    tlen = round(text_len * 10)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
        f'<title>{esc(label)}</title>'
        f'<defs><clipPath id="r"><rect width="{w}" height="{h}" rx="6"/></clipPath></defs>'
        f'<g clip-path="url(#r)"><rect width="{w}" height="{h}" fill="{color}"/></g>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="6" fill="none" stroke="{T["border"]}"/>'
        f'<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="100">'
        f'<image x="10" y="7" width="14" height="14" href="data:image/svg+xml;base64,{icon_b64}"/>'
        f'<text transform="scale(.1)" x="{cx}" y="175" textLength="{tlen}" font-weight="bold">{esc(label)}</text>'
        f'</g></svg>'
    )


def header_svg() -> str:
    w, h = 1000, 336
    char_w, type_speed = 7.9, 0.052
    tx, ty0, line_h = 548, 96, 21

    lines_svg, clips = [], []
    t = 0.5
    for i, (prompt, text, cls) in enumerate(TERMINAL):
        y = ty0 + i * line_h
        if prompt:
            prefix_w = 4 * char_w
            n = len(text)
            values = ";".join(f"{prefix_w + k * char_w:.1f}" for k in range(n + 1))
            anim = (
                f'<set attributeName="width" to="0" begin="0s"/>'
                f'<animate attributeName="width" values="{values}" calcMode="discrete" begin="{t:.2f}s" dur="{n * type_speed:.2f}s" fill="freeze"/>'
            )
            t += n * type_speed + 0.30
        else:
            anim = f'<set attributeName="width" to="0" begin="0s"/><set attributeName="width" to="440" begin="{t:.2f}s"/>'
            t += 0.11
        clips.append(f'<clipPath id="ln{i}"><rect x="{tx - 2}" y="{y - 15}" height="{line_h}" width="440">{anim}</rect></clipPath>')
        content = (
            f'<tspan class="ok">~</tspan> <tspan class="accent">$</tspan> {esc(text)}' if prompt else f'<tspan class="{cls}">{esc(text)}</tspan>'
        )
        lines_svg.append(f'<text clip-path="url(#ln{i})" x="{tx}" y="{y}" class="mono" font-size="13">{content}</text>')
    cursor_y = ty0 + len(TERMINAL) * line_h
    cursor = (
        f'<text x="{tx}" y="{cursor_y}" class="mono" font-size="13"><tspan class="ok">~</tspan> <tspan class="accent">$</tspan></text>'
        f'<rect x="{tx + 4 * char_w}" y="{cursor_y - 12}" width="8" height="15" fill="{T["accent"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
    )

    chips_svg, cx = [], 40
    for i, chip in enumerate(CHIPS):
        cw = len(chip) * 7.2 + 22
        chips_svg.append(
            f'<g class="fade" {delay(0.85 + i * 0.08)}><rect x="{cx}" y="256" width="{cw:.0f}" height="26" rx="13" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<text x="{cx + cw / 2:.0f}" y="273" text-anchor="middle" class="mono" font-size="11.5" style="fill:{T["text"]}">{esc(chip)}</text></g>'
        )
        cx += cw + 8

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(NAME)} — {esc(ROLE)}">
<title>{esc(NAME)} — {esc(ROLE)}</title>
<style>
text {{ font-family: {SANS}; fill: {T['text']}; }}
.mono {{ font-family: {MONO}; white-space: pre; }}
.muted {{ fill: {T['muted']}; }} .dim {{ fill: {T['dim']}; }} .accent {{ fill: {T['accent']}; }} .ok {{ fill: {T['ok']}; }}
.fade {{ animation: fadeIn .8s ease-out both; }}
.pulse {{ animation: pulseDot 2.2s ease-in-out infinite; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes pulseDot {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
.glow {{ animation: drift 14s ease-in-out infinite alternate; }}
@keyframes drift {{ from {{ transform: translate(0,0); }} to {{ transform: translate(40px,-14px); }} }}
</style>
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="{T['grid']}"/></pattern>
  <radialGradient id="g1" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{T['accent']}" stop-opacity=".22"/><stop offset="1" stop-color="{T['accent']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{T['ok']}" stop-opacity=".18"/><stop offset="1" stop-color="{T['ok']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g3" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{T['accent2']}" stop-opacity=".20"/><stop offset="1" stop-color="{T['accent2']}" stop-opacity="0"/></radialGradient>
  <linearGradient id="roleGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T['accent']}"/><stop offset=".5" stop-color="{T['ok']}"/><stop offset="1" stop-color="{T['accent2']}"/></linearGradient>
  <linearGradient id="topSheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T['accent']}" stop-opacity="0"/><stop offset=".5" stop-color="{T['ok']}" stop-opacity=".85"/><stop offset="1" stop-color="{T['accent2']}" stop-opacity="0"/></linearGradient>
  <clipPath id="frame"><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16"/></clipPath>
  {''.join(clips)}
</defs>
<g clip-path="url(#frame)">
  <rect width="{w}" height="{h}" fill="{T['bg']}"/>
  <rect width="{w}" height="{h}" fill="url(#dots)"/>
  <rect x="0" y="0" width="{w}" height="2" fill="url(#topSheen)"/>
  <ellipse class="glow" cx="160" cy="70" rx="310" ry="190" fill="url(#g1)"/>
  <ellipse class="glow" cx="420" cy="300" rx="260" ry="150" fill="url(#g2)" style="animation-delay:-4s"/>
  <ellipse class="glow" cx="870" cy="270" rx="330" ry="200" fill="url(#g3)" style="animation-delay:-8s"/>

  <g class="fade">
    <text x="40" y="54" class="mono" font-size="13"><tspan class="accent">//</tspan> <tspan class="muted">hello, world — i'm</tspan></text>
    <rect x="335" y="37" width="166" height="24" rx="12" fill="{T['surface']}" stroke="{T['border']}"/>
    <circle class="pulse" cx="350" cy="49" r="4" fill="{T['ok']}"/>
    <text x="362" y="53" class="mono" font-size="10.5" fill="{T['ok']}">OPEN TO COLLAB</text>
    <text x="38" y="116" font-size="54" font-weight="800" letter-spacing="-1">{esc(NAME)}</text>
  </g>
  <g class="fade" {delay(0.25)}>
    <text x="40" y="156" font-size="24" font-weight="700" fill="url(#roleGrad)" style="fill:url(#roleGrad)">{esc(ROLE)}</text>
    <text x="40" y="186" font-size="14" class="muted">{esc(TAGLINE)}</text>
  </g>
  <g class="fade" {delay(0.5)}>
    <rect x="40" y="206" width="3.5" height="24" rx="1.75" fill="url(#roleGrad)"/>
    <text x="53" y="223" font-size="14" font-style="italic" style="fill:{T['text']}">“{esc(MOTTO)}”</text>
  </g>
  {''.join(chips_svg)}

  <g>
    <rect x="526" y="32" width="444" height="272" rx="12" fill="{T['chrome']}" fill-opacity=".94" stroke="{T['border']}"/>
    <path d="M526 64 h444" stroke="{T['border']}"/>
    <circle cx="546" cy="48" r="5.5" fill="#ff5f57"/><circle cx="564" cy="48" r="5.5" fill="#febc2e"/><circle cx="582" cy="48" r="5.5" fill="#28c840"/>
    <text x="748" y="52" text-anchor="middle" class="mono dim" font-size="11.5">adrix@pixel-dev: ~</text>
    <circle class="pulse" cx="950" cy="48" r="4" fill="{T['ok']}"/>
    {''.join(lines_svg)}
    {cursor}
  </g>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{T['border']}"/>
</svg>
"""


def toolkit_svg() -> str:
    w = 1000
    row_h, icon, gap = 66, 44, 12
    h = 36 + 24 + row_h * len(TOOLKIT) + 10
    row_colors = [T["kotlin"], T["ok"], T["accent"], T["accent2"]]
    body = []
    for r, (label, icons, pills) in enumerate(TOOLKIT):
        y = 24 + r * row_h
        key = label.lower().replace(" & ", "_").replace(" ", "_")
        rc = row_colors[r % len(row_colors)]
        body.append(
            f'<g class="fade" {delay(r * 0.12)}>'
            f'<rect x="20" y="{y + 10}" width="3" height="24" rx="1.5" fill="{rc}"/>'
            f'<text x="32" y="{y + 27}" class="mono" font-size="12.5"><tspan fill="{rc}">{esc(key)}</tspan><tspan class="dim">:</tspan></text>'
        )
        x = 180
        for name in icons:
            short = name.split("-")[0]
            body.append(f'<image x="{x}" y="{y}" width="{icon}" height="{icon}" href="{_icon_uri(name)}"><title>{esc(LABELS.get(short, short))}</title></image>')
            x += icon + gap
        for pill in pills:
            pw = len(pill) * 7.4 + 22
            body.append(
                f'<rect x="{x}" y="{y + 9}" width="{pw:.0f}" height="26" rx="13" fill="{T["surface"]}" stroke="{T["border"]}"/>'
                f'<text x="{x + pw / 2:.0f}" y="{y + 26}" text-anchor="middle" class="mono" font-size="11.5">{esc(pill)}</text>'
            )
            x += pw + 8
        body.append("</g>")
        if r < len(TOOLKIT) - 1:
            body.append(f'<line x1="20" y1="{y + row_h - 10}" x2="{w - 20}" y2="{y + row_h - 10}" stroke="{T["grid"]}"/>')
    return card(w, h, "~/toolkit.yaml", "\n".join(body), right_label="22 tools · 4 layers")


def project_card(p: dict) -> str:
    w, h = 490, 168
    ac = p["accent"]
    pills_svg, px = [], 20
    for pill in p["pills"]:
        pw = len(pill) * 6.8 + 18
        pills_svg.append(
            f'<rect x="{px}" y="94" width="{pw:.0f}" height="22" rx="11" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<text x="{px + pw / 2:.0f}" y="109" text-anchor="middle" class="mono muted" font-size="10.5">{esc(pill)}</text>'
        )
        px += pw + 7
    body = [
        f'<rect x="0" y="0" width="3.5" height="{h - 36}" fill="{ac}"/>',
        f'<text x="20" y="28" font-size="17" font-weight="700">{esc(p["name"])}</text>',
        f'<rect x="336" y="12" width="134" height="20" rx="10" fill="{T["surface"]}" stroke="{T["border"]}"/>',
        f'<text x="403" y="26" text-anchor="middle" class="mono" font-size="9.5" fill="{ac}">{esc(p["tag"])}</text>',
        f'<text x="20" y="54" font-size="12.5" class="muted">{esc(p["desc"][0])}</text>',
        f'<text x="20" y="72" font-size="12.5" class="muted">{esc(p["desc"][1])}</text>',
        "".join(pills_svg),
        f'<circle cx="{w - 86}" cy="105" r="4.5" fill="{p["lang_color"]}"/>',
        f'<text x="{w - 76}" y="109" class="mono dim" font-size="10.5">{esc(p["lang"])}</text>',
    ]
    return card(w, h, f"~/projects/{p['name']}", "\n".join(body), right_label="open repo ↗")


def footer_svg() -> str:
    w, h = 1000, 56
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Footer">
<defs>
  <linearGradient id="fg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{T['accent']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{T['ok']}" stop-opacity=".7"/>
    <stop offset="1" stop-color="{T['accent2']}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{w}" height="{h}" rx="10" fill="{T['chrome']}" stroke="{T['border']}"/>
<rect x="0" y="0" width="{w}" height="1.5" fill="url(#fg)"/>
<text x="24" y="32" font-family="{MONO}" font-size="11.5" fill="{T['muted']}">
  <tspan fill="{T['ok']}">✓</tspan> rendered in-repo with Python stdlib · automated via GitHub Actions
</text>
<text x="{w - 24}" y="32" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{T['dim']}">
  @2b-adrix · adrix.is-a.dev
</text>
</svg>
"""


def build(root: Path) -> None:
    out = root / "assets" / "static"
    write(out / "header.svg", header_svg())
    write(out / "toolkit.svg", toolkit_svg())
    write(out / "footer.svg", footer_svg())
    for p in PROJECTS:
        write(out / "projects" / p["file"], project_card(p))
    for filename, label, color, icon_svg in BADGES:
        write(out / "badges" / filename, badge_svg(label, color, icon_svg))
