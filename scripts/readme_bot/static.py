"""Static artwork: executive Hero Banner, 2x2 Stack Matrix, SentinalX + flagship Project Cards, Badges & Footer."""

from __future__ import annotations

import base64
from pathlib import Path

from .svg import MONO, SANS, THEME, delay, esc, panel, write

T = THEME
ICONS = Path(__file__).with_name("icons")

NAME = "Aditya Kumar Mishra"
HANDLE = "@2b-adrix"
ROLE = "Native Android & Backend Systems Engineer"
META = "India  ·  B.Tech CSE, Mewar University '28  ·  Alpha-coders"
SUMMARY_LINE_1 = "Building resilient Jetpack Compose applications, security-first mobile"
SUMMARY_LINE_2 = "architectures, and scalable Spring Boot REST services."
CHIPS = ["Kotlin", "Jetpack Compose", "Spring Boot", "TFLite", "SQLCipher"]

TOOLKIT_GRID = [
    (
        "LANGUAGES",
        T["violet"],
        ["Kotlin-Dark", "Java-Dark", "Python-Dark", "TypeScript", "JavaScript", "HTML", "CSS"],
        [],
    ),
    (
        "ANDROID & MOBILE",
        T["accent"],
        ["AndroidStudio-Dark", "Gradle-Dark", "Firebase-Dark", "SQLite"],
        ["Jetpack Compose", "MVVM", "Room", "TFLite"],
    ),
    (
        "BACKEND & DATA",
        T["sky"],
        ["Spring-Dark", "MongoDB", "MySQL-Dark", "NodeJS-Dark", "REST", "Postman"],
        ["JWT", "REST APIs"],
    ),
    (
        "SECURITY & TOOLING",
        T["amber"],
        ["Linux-Dark", "Git", "Github-Dark", "GithubActions-Dark", "VSCode-Dark"],
        ["SQLCipher", "DSA"],
    ),
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
        "file": "sentinalx.svg",
        "name": "SentinalX",
        "tag": "CYBERSECURITY · ML",
        "lang": "Kotlin",
        "lang_color": T["violet"],
        "desc": [
            "Real-time Android threat shield pairing TFLite scam",
            "classification with an encrypted Room/SQLCipher vault.",
        ],
        "pills": ["Kotlin 2.1", "Compose", "TFLite", "SQLCipher"],
        "accent": T["accent"],
    },
    {
        "file": "krishiva-native.svg",
        "name": "Krishiva-Native",
        "tag": "AI · AGRITECH",
        "lang": "Kotlin",
        "lang_color": T["violet"],
        "desc": [
            "AI agricultural intelligence app for crop disease",
            "diagnosis via Gemini AI & CameraX plus Mandi prices.",
        ],
        "pills": ["Jetpack Compose", "CameraX", "Gemini AI"],
        "accent": T["accent"],
    },
    {
        "file": "arogyagrid.svg",
        "name": "Arogyagrid",
        "tag": "HEALTHTECH · API",
        "lang": "Kotlin + Java",
        "lang_color": T["sky"],
        "desc": [
            "Native Android healthcare client integrated with a",
            "dedicated Spring Boot REST backend.",
        ],
        "pills": ["Kotlin", "Spring Boot", "REST API"],
        "accent": T["sky"],
    },
    {
        "file": "alpha-chat-native.svg",
        "name": "Alpha-Chat-Native",
        "tag": "REALTIME · MOBILE",
        "lang": "Kotlin",
        "lang_color": T["violet"],
        "desc": [
            "Native real-time Android messaging client built",
            "around Firebase authentication and live sync.",
        ],
        "pills": ["Kotlin", "Android", "Firebase"],
        "accent": T["sky"],
    },
]

BADGES = [
    (
        "portfolio.svg",
        "ADRIX.IS-A.DEV",
        T["accent"],
        '<svg fill="#3ddc84" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm6.93 6h-2.95a15.65 15.65 0 0 0-1.38-3.56A8.03 8.03 0 0 1 18.93 8ZM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96ZM4.26 14a7.83 7.83 0 0 1 0-4h3.38a16.5 16.5 0 0 0-.14 2c0 .68.05 1.35.14 2H4.26Zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56A7.99 7.99 0 0 1 5.08 16Zm2.95-8H5.08a7.99 7.99 0 0 1 4.33-3.56A15.65 15.65 0 0 0 8.03 8ZM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96ZM14.34 14H9.66a14.7 14.7 0 0 1-.16-2c0-.68.06-1.35.16-2h4.68c.1.65.16 1.32.16 2 0 .68-.06 1.35-.16 2Zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95a8.03 8.03 0 0 1-4.33 3.56ZM16.36 14c.09-.65.14-1.32.14-2 0-.68-.05-1.35-.14-2h3.38a7.83 7.83 0 0 1 0 4h-3.38Z"/></svg>',
    ),
    (
        "email.svg",
        "EMAIL",
        T["muted"],
        '<svg fill="#cbd5e1" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"/></svg>',
    ),
    (
        "linkedin.svg",
        "LINKEDIN",
        T["sky"],
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#38bdf8" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.125 2.062 2.062 0 0 1 0 4.125zM7.119 20.452H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    ),
    (
        "x.svg",
        "X / TWITTER",
        T["text"],
        '<svg fill="#f8fafc" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/></svg>',
    ),
    (
        "instagram.svg",
        "INSTAGRAM",
        T["muted"],
        '<svg fill="#cbd5e1" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>',
    ),
    (
        "leetcode.svg",
        "LEETCODE",
        T["amber"],
        '<svg fill="#f59e0b" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.116 6.226l-3.854 4.126a5.266 5.266 0 0 0-1.209 2.104 5.35 5.35 0 0 0-.125.513 5.527 5.527 0 0 0 .062 2.362 5.83 5.83 0 0 0 .349 1.017 5.938 5.938 0 0 0 1.271 1.818l4.277 4.193.039.038c2.248 2.165 5.852 2.133 8.063-.074l2.396-2.392c.54-.54.54-1.414.003-1.955a1.378 1.378 0 0 0-1.951-.003l-2.396 2.392a3.021 3.021 0 0 1-4.205.038l-.02-.019-4.276-4.193c-.652-.64-.972-1.469-.948-2.263a2.68 2.68 0 0 1 .066-.523 2.545 2.545 0 0 1 .619-1.164L9.13 8.114c1.058-1.134 3.204-1.27 4.43-.278l3.501 2.831c.593.48 1.461.387 1.94-.207a1.384 1.384 0 0 0-.207-1.943l-3.5-2.831c-.8-.647-1.766-1.045-2.774-1.202l2.015-2.158A1.384 1.384 0 0 0 13.483 0zm-2.866 12.815a1.38 1.38 0 0 0-1.38 1.382 1.38 1.38 0 0 0 1.38 1.382H20.79a1.38 1.38 0 0 0 1.38-1.382 1.38 1.38 0 0 0-1.38-1.382z"/></svg>',
    ),
]


def _icon_uri(name: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode((ICONS / f"{name}.svg").read_bytes()).decode()


def badge_svg(label: str, accent: str, icon_svg: str) -> str:
    text_len = len(label) * 7.2
    w = round(text_len + 44)
    h = 28
    icon_b64 = base64.b64encode(icon_svg.encode("utf-8")).decode("ascii")
    cx = round((32 + w - 8) / 2 * 10)
    tlen = round(text_len * 10)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
        f'<title>{esc(label)}</title>'
        f'<rect width="{w}" height="{h}" rx="7" fill="{T["surface"]}" stroke="{T["border"]}"/>'
        f'<image x="10" y="7.5" width="13" height="13" href="data:image/svg+xml;base64,{icon_b64}"/>'
        f'<g fill="{T["text"]}" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="100">'
        f'<text transform="scale(.1)" x="{cx}" y="175" textLength="{tlen}" font-weight="bold">{esc(label)}</text>'
        f'</g></svg>'
    )


def header_svg() -> str:
    """Clean editorial two-column banner (Linear / Stripe-inspired engineering aesthetic)."""
    w, h = 1000, 290
    chips_svg, cx = [], 44
    for i, chip in enumerate(CHIPS):
        cw = len(chip) * 6.9 + 22
        chips_svg.append(
            f'<g class="fade" {delay(0.45 + i * 0.06)}>'
            f'<rect x="{cx}" y="226" width="{cw:.0f}" height="26" rx="6" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<text x="{cx + cw / 2:.0f}" y="243" text-anchor="middle" class="mono muted" font-size="11">{esc(chip)}</text>'
            f'</g>'
        )
        cx += cw + 8

    # Right side: crisp Engineering Spec Card (replaces cartoon phone & bash terminal)
    rx, ry, rw, rh = 618, 28, 342, 234
    spec_rows = [
        ("PRIMARY", "Kotlin · Jetpack Compose", T["accent"]),
        ("SECURITY", "TFLite · SQLCipher · Biometrics", T["accent"]),
        ("BACKEND", "Java · Spring Boot · MongoDB", T["sky"]),
        ("FOCUS", "Clean Architecture · DSA", T["muted"]),
    ]
    rows_svg = []
    for idx, (k, v, col) in enumerate(spec_rows):
        sy = ry + 64 + idx * 36
        rows_svg.append(
            f'<text x="{rx + 20}" y="{sy}" class="mono dim" font-size="10" letter-spacing="0.6">{k}</text>'
            f'<text x="{rx + 98}" y="{sy}" font-size="12.5" font-weight="600" fill="{col if idx == 0 else T["text"]}">{esc(v)}</text>'
        )
        if idx < len(spec_rows) - 1:
            rows_svg.append(f'<line x1="{rx + 20}" y1="{sy + 14}" x2="{rx + rw - 20}" y2="{sy + 14}" stroke="{T["grid"]}"/>')

    spec_card = f"""
  <g class="fade" {delay(0.2)}>
    <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="12" fill="{T['chrome']}" stroke="{T['border']}"/>
    <text x="{rx + 20}" y="{ry + 28}" class="mono dim" font-size="10.5" letter-spacing="0.8">ENGINEERING SPEC</text>
    <circle class="pulse" cx="{rx + rw - 88}" cy="{ry + 24}" r="3.5" fill="{T['accent']}"/>
    <text x="{rx + rw - 20}" y="{ry + 28}" text-anchor="end" class="mono accent" font-size="10">OPEN TO COLLAB</text>
    <line x1="{rx}" y1="{ry + 42}" x2="{rx + rw}" y2="{ry + 42}" stroke="{T['border']}"/>
    {''.join(rows_svg)}
    <rect x="{rx + 20}" y="{ry + rh - 36}" width="{rw - 40}" height="22" rx="5" fill="{T['bg']}" stroke="{T['border']}"/>
    <text x="{rx + rw / 2:.0f}" y="{ry + rh - 21.5}" text-anchor="middle" class="mono dim" font-size="10">“Engineering products, not just projects.”</text>
  </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(NAME)} — {esc(ROLE)}">
<title>{esc(NAME)} — {esc(ROLE)}</title>
<style>
text {{ font-family: {SANS}; fill: {T['text']}; }}
.mono {{ font-family: {MONO}; white-space: pre; }}
.muted {{ fill: {T['muted']}; }} .dim {{ fill: {T['dim']}; }} .accent {{ fill: {T['accent']}; }}
.fade {{ animation: fadeIn .6s ease-out both; }}
.pulse {{ animation: pulseDot 2.6s ease-in-out infinite; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes pulseDot {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
</style>
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="1.2" cy="1.2" r="1" fill="{T['grid']}"/>
  </pattern>
  <radialGradient id="topGlow" cx="25%" cy="0%" r="65%">
    <stop offset="0" stop-color="{T['accent']}" stop-opacity=".10"/><stop offset="1" stop-color="{T['accent']}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="topBar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{T['accent']}"/><stop offset="1" stop-color="{T['sky']}" stop-opacity=".2"/>
  </linearGradient>
  <clipPath id="frame"><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{w}" height="{h}" fill="{T['bg']}"/>
  <rect width="{w}" height="{h}" fill="url(#dots)"/>
  <rect width="{w}" height="{h}" fill="url(#topGlow)"/>
  <rect x="0" y="0" width="{w}" height="2" fill="url(#topBar)"/>

  <g class="fade">
    <text x="44" y="50" class="mono accent" font-size="11.5" font-weight="600" letter-spacing="1.2">{esc(HANDLE.upper())}  ·  PORTFOLIO PROFILE</text>
    <text x="42" y="96" font-size="40" font-weight="800" letter-spacing="-0.8">{esc(NAME)}</text>
    <text x="44" y="128" font-size="18" font-weight="600" fill="{T['sky']}">{esc(ROLE)}</text>
  </g>

  <g class="fade" {delay(0.18)}>
    <text x="44" y="162" font-size="13.5" class="muted">{esc(SUMMARY_LINE_1)}</text>
    <text x="44" y="182" font-size="13.5" class="muted">{esc(SUMMARY_LINE_2)}</text>
    <text x="44" y="208" class="mono dim" font-size="11">{esc(META)}</text>
  </g>

  {''.join(chips_svg)}
  {spec_card}
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{T['border']}"/>
</svg>
"""


def toolkit_svg() -> str:
    """2x2 Architecture Matrix with clean iconography and subtle category accents."""
    w, h = 1000, 312
    box_w, box_h = 468, 118
    positions = [(22, 16), (510, 16), (22, 146), (510, 146)]
    body = []
    for idx, ((title, accent, icons, pills), (bx, by)) in enumerate(zip(TOOLKIT_GRID, positions)):
        body.append(
            f'<g class="fade" {delay(idx * 0.08)}>'
            f'<rect x="{bx}" y="{by}" width="{box_w}" height="{box_h}" rx="12" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<circle cx="{bx + 18}" cy="{by + 23}" r="3.5" fill="{accent}"/>'
            f'<text x="{bx + 29}" y="{by + 27}" class="mono muted" font-size="10.5" font-weight="700" letter-spacing="0.9">{esc(title)}</text>'
        )
        ix, iy = bx + 16, by + 42
        for name in icons:
            short = name.split("-")[0]
            body.append(
                f'<image x="{ix}" y="{iy}" width="40" height="40" href="{_icon_uri(name)}">'
                f'<title>{esc(LABELS.get(short, short))}</title></image>'
            )
            ix += 50
        if pills:
            px, py = bx + 16, by + 90
            for pill in pills:
                pw = len(pill) * 6.5 + 18
                body.append(
                    f'<rect x="{px}" y="{py}" width="{pw:.0f}" height="19" rx="5" fill="{T["bg"]}" stroke="{T["border"]}"/>'
                    f'<text x="{px + pw / 2:.0f}" y="{py + 13}" text-anchor="middle" class="mono muted" font-size="10">{esc(pill)}</text>'
                )
                px += pw + 6
        body.append("</g>")
    return panel(w, h, "TECHNICAL STACK", "\n".join(body), tag="22 TOOLS · 4 DOMAINS", accent=T["accent"])


def project_card(p: dict) -> str:
    w, h = 490, 168
    ac = p["accent"]
    pills_svg, px = [], 20
    for pill in p["pills"]:
        pw = len(pill) * 6.6 + 18
        pills_svg.append(
            f'<rect x="{px}" y="92" width="{pw:.0f}" height="21" rx="5" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<text x="{px + pw / 2:.0f}" y="106" text-anchor="middle" class="mono muted" font-size="10">{esc(pill)}</text>'
        )
        px += pw + 6
    body = [
        f'<text x="20" y="32" font-size="17.5" font-weight="700">{esc(p["name"])}</text>',
        f'<text x="20" y="56" font-size="12.5" class="muted">{esc(p["desc"][0])}</text>',
        f'<text x="20" y="74" font-size="12.5" class="muted">{esc(p["desc"][1])}</text>',
        "".join(pills_svg),
        f'<circle cx="{w - 92}" cy="102" r="4" fill="{p["lang_color"]}"/>',
        f'<text x="{w - 83}" y="106" class="mono dim" font-size="10.5">{esc(p["lang"])}</text>',
    ]
    return panel(w, h, p["tag"], "\n".join(body), tag="VIEW REPO ↗", accent=ac)


def footer_svg() -> str:
    w, h = 1000, 52
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Footer">
<rect width="{w}" height="{h}" rx="12" fill="{T['chrome']}" stroke="{T['border']}"/>
<circle cx="22" cy="26" r="3.5" fill="{T['accent']}"/>
<text x="34" y="30" font-family="{MONO}" font-size="11" fill="{T['muted']}">
  Aditya Kumar Mishra · Automated in Python &amp; GitHub Actions
</text>
<text x="{w - 22}" y="30" text-anchor="end" font-family="{MONO}" font-size="11" fill="{T['dim']}">
  github.com/2b-adrix  ·  adrix.is-a.dev
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
