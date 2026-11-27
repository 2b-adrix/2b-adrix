"""Static artwork: Android+Backend dual-node hero, End-to-End Architecture card, 2x2 Bento toolkit, 6 project cards, pill badges & footer."""

from __future__ import annotations

import base64
from pathlib import Path

from .svg import MONO, SANS, THEME, delay, esc, panel, write

T = THEME
ICONS = Path(__file__).with_name("icons")

NAME = "ADITYA MISHRA"
HANDLE = "@2b-adrix"
ROLE = "Android & Backend Engineer"
SUB = "B.Tech CSE · Mewar University '28 · Alpha-coders"
MOTTO = "Engineering products, not just projects."
CHIPS = [
    ("Kotlin", T["kotlin"]),
    ("Jetpack Compose", T["mint"]),
    ("Spring Boot", T["sky"]),
    ("JWT · REST", T["gold"]),
    ("MongoDB · SQL", T["coral"]),
]

TOOLKIT_GRID = [
    (
        "01 // LANGUAGES",
        T["kotlin"],
        ["Kotlin-Dark", "Java-Dark", "Python-Dark", "TypeScript", "JavaScript", "HTML", "CSS"],
        [],
    ),
    (
        "02 // ANDROID & MOBILE",
        T["mint"],
        ["AndroidStudio-Dark", "Gradle-Dark", "Firebase-Dark", "SQLite"],
        ["Jetpack Compose", "MVVM", "Room", "TFLite"],
    ),
    (
        "03 // BACKEND & APIS",
        T["sky"],
        ["Spring-Dark", "MongoDB", "MySQL-Dark", "NodeJS-Dark", "REST", "Postman"],
        ["Spring Security", "JWT", "JPA"],
    ),
    (
        "04 // DEVOPS & SECURITY",
        T["coral"],
        ["Docker", "Linux-Dark", "Git", "Github-Dark", "GithubActions-Dark", "VSCode-Dark"],
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
    "Docker": "Docker",
    "Linux": "Linux",
    "Git": "Git",
    "Github": "GitHub",
    "GithubActions": "GitHub Actions",
    "VSCode": "VS Code",
}

PROJECTS = [
    {
        "file": "krishiva-native.svg",
        "num": "01",
        "name": "Krishiva-Native",
        "tag": "ANDROID · AI",
        "lang": "Kotlin",
        "lang_color": T["kotlin"],
        "desc": [
            "AI agricultural platform with instant crop disease",
            "diagnosis via Gemini AI + CameraX & Mandi prices.",
        ],
        "pills": ["Jetpack Compose", "CameraX", "Gemini AI"],
        "accent": T["mint"],
    },
    {
        "file": "sentinalx.svg",
        "num": "02",
        "name": "SentinalX",
        "tag": "ANDROID · SECURITY",
        "lang": "Kotlin",
        "lang_color": T["kotlin"],
        "desc": [
            "Real-time Android threat shield with TFLite scam",
            "detection and an encrypted SQLCipher Room vault.",
        ],
        "pills": ["Compose", "TFLite", "SQLCipher"],
        "accent": T["kotlin"],
    },
    {
        "file": "arogyagrid.svg",
        "num": "03",
        "name": "Arogyagrid",
        "tag": "ANDROID CLIENT",
        "lang": "Kotlin",
        "lang_color": T["kotlin"],
        "desc": [
            "Native Android smart-health supply chain client",
            "synced with the Arogyagrid Spring Boot API.",
        ],
        "pills": ["Kotlin", "Android", "REST Client"],
        "accent": T["mint"],
    },
    {
        "file": "arogyagrid-backend.svg",
        "num": "04",
        "name": "arogyagrid-backend",
        "tag": "SPRING BOOT API",
        "lang": "Java 17",
        "lang_color": T["sky"],
        "desc": [
            "Production Spring Boot 3 REST API with Spring",
            "Security, JJWT auth, JPA persistence & Docker.",
        ],
        "pills": ["Spring Boot 3", "JJWT", "JPA · Docker"],
        "accent": T["sky"],
    },
    {
        "file": "alpha-chat-native.svg",
        "num": "05",
        "name": "Alpha-Chat-Native",
        "tag": "ANDROID · REALTIME",
        "lang": "Kotlin",
        "lang_color": T["coral"],
        "desc": [
            "Native real-time Android chat application with",
            "instant sync and Firebase authentication.",
        ],
        "pills": ["Kotlin", "Firebase", "Realtime"],
        "accent": T["coral"],
    },
    {
        "file": "oracle-plate-backend.svg",
        "num": "06",
        "name": "ORACLE-S-PLATE_BACKEND",
        "tag": "JAVA 21 · BACKEND",
        "lang": "Java 21",
        "lang_color": T["sky"],
        "desc": [
            "Modern Java 21 + Spring Boot 4 backend service",
            "with Spring Security and modular REST endpoints.",
        ],
        "pills": ["Java 21", "Spring Boot 4", "Security"],
        "accent": T["sky"],
    },
]

BADGES = [
    (
        "portfolio.svg",
        "ADRIX.IS-A.DEV",
        T["mint"],
        '<svg fill="#3ddc84" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm6.93 6h-2.95a15.65 15.65 0 0 0-1.38-3.56A8.03 8.03 0 0 1 18.93 8ZM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96ZM4.26 14a7.83 7.83 0 0 1 0-4h3.38a16.5 16.5 0 0 0-.14 2c0 .68.05 1.35.14 2H4.26Zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56A7.99 7.99 0 0 1 5.08 16Zm2.95-8H5.08a7.99 7.99 0 0 1 4.33-3.56A15.65 15.65 0 0 0 8.03 8ZM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96ZM14.34 14H9.66a14.7 14.7 0 0 1-.16-2c0-.68.06-1.35.16-2h4.68c.1.65.16 1.32.16 2 0 .68-.06 1.35-.16 2Zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95a8.03 8.03 0 0 1-4.33 3.56ZM16.36 14c.09-.65.14-1.32.14-2 0-.68-.05-1.35-.14-2h3.38a7.83 7.83 0 0 1 0 4h-3.38Z"/></svg>',
    ),
    (
        "email.svg",
        "EMAIL",
        T["coral"],
        '<svg fill="#ff8a4c" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"/></svg>',
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
        "#f472b6",
        '<svg fill="#f472b6" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>',
    ),
    (
        "leetcode.svg",
        "LEETCODE",
        T["gold"],
        '<svg fill="#fbbf24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.116 6.226l-3.854 4.126a5.266 5.266 0 0 0-1.209 2.104 5.35 5.35 0 0 0-.125.513 5.527 5.527 0 0 0 .062 2.362 5.83 5.83 0 0 0 .349 1.017 5.938 5.938 0 0 0 1.271 1.818l4.277 4.193.039.038c2.248 2.165 5.852 2.133 8.063-.074l2.396-2.392c.54-.54.54-1.414.003-1.955a1.378 1.378 0 0 0-1.951-.003l-2.396 2.392a3.021 3.021 0 0 1-4.205.038l-.02-.019-4.276-4.193c-.652-.64-.972-1.469-.948-2.263a2.68 2.68 0 0 1 .066-.523 2.545 2.545 0 0 1 .619-1.164L9.13 8.114c1.058-1.134 3.204-1.27 4.43-.278l3.501 2.831c.593.48 1.461.387 1.94-.207a1.384 1.384 0 0 0-.207-1.943l-3.5-2.831c-.8-.647-1.766-1.045-2.774-1.202l2.015-2.158A1.384 1.384 0 0 0 13.483 0zm-2.866 12.815a1.38 1.38 0 0 0-1.38 1.382 1.38 1.38 0 0 0 1.38 1.382H20.79a1.38 1.38 0 0 0 1.38-1.382 1.38 1.38 0 0 0-1.38-1.382z"/></svg>',
    ),
]


def _icon_uri(name: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode((ICONS / f"{name}.svg").read_bytes()).decode()


def badge_svg(label: str, accent: str, icon_svg: str) -> str:
    text_len = len(label) * 7.6
    w = round(text_len + 48)
    h = 30
    icon_b64 = base64.b64encode(icon_svg.encode("utf-8")).decode("ascii")
    cx = round((34 + w - 8) / 2 * 10)
    tlen = round(text_len * 10)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
        f'<title>{esc(label)}</title>'
        f'<rect width="{w}" height="{h}" rx="15" fill="{T["surface"]}" stroke="{T["border"]}"/>'
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="none" stroke="{accent}" stroke-opacity=".22"/>'
        f'<circle cx="17" cy="15" r="10" fill="{accent}" fill-opacity=".16"/>'
        f'<image x="10.5" y="8.5" width="13" height="13" href="data:image/svg+xml;base64,{icon_b64}"/>'
        f'<g fill="{T["text"]}" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="100">'
        f'<text transform="scale(.1)" x="{cx}" y="185" textLength="{tlen}" font-weight="bold">{esc(label)}</text>'
        f'</g></svg>'
    )


def header_svg() -> str:
    """Dual-Node Hero: Pixel Android Client linked via live REST/JWT pulse to Spring Boot Backend."""
    w, h = 1000, 348
    chips_svg, cx = [], 44
    for i, (chip, dot_color) in enumerate(CHIPS):
        cw = len(chip) * 6.9 + 30
        chips_svg.append(
            f'<g class="fade" {delay(0.6 + i * 0.08)}>'
            f'<rect x="{cx}" y="268" width="{cw:.0f}" height="28" rx="14" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<circle cx="{cx + 12}" cy="282" r="3" fill="{dot_color}"/>'
            f'<text x="{cx + 21}" y="286" class="mono" font-size="10.8" fill="{T["text"]}">{esc(chip)}</text>'
            f'</g>'
        )
        cx += cw + 7

    # Left-of-right-panel: Pixel Android Client (x=612..792, y=24..324)
    px, py, pw, ph = 612, 24, 180, 300
    # Right-of-right-panel: Spring Boot Backend Server Node (x=830..976, y=42..306)
    sx, sy, sw, sh = 830, 42, 146, 264

    dual_rig = f"""
  <g class="fade" {delay(0.22)}>
    <!-- Animated REST/JWT data bridge connecting Android Phone <-> Spring Boot API -->
    <line x1="{px + pw}" y1="146" x2="{sx}" y2="146" stroke="{T['sky']}" stroke-width="1.6" stroke-dasharray="4 3"/>
    <line x1="{px + pw}" y1="196" x2="{sx}" y2="196" stroke="{T['mint']}" stroke-width="1.6" stroke-dasharray="4 3"/>
    <circle cx="{px + pw + 19}" cy="146" r="3.5" fill="{T['sky']}">
      <animate attributeName="cx" values="{px + pw + 3};{sx - 3};{px + pw + 3}" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{sx - 19}" cy="196" r="3.5" fill="{T['mint']}">
      <animate attributeName="cx" values="{sx - 3};{px + pw + 3};{sx - 3}" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <rect x="{px + pw + 3}" y="160" width="32" height="20" rx="5" fill="{T['surface']}" stroke="{T['border']}"/>
    <text x="{px + pw + 19}" y="173.5" text-anchor="middle" class="mono sky" font-size="8.5" font-weight="700">REST</text>

    <!-- Pixel Hardware Chassis -->
    <rect x="{px + pw - 1}" y="{py + 68}" width="3.5" height="24" rx="1.5" fill="#334155"/>
    <rect x="{px + pw - 1}" y="{py + 104}" width="3.5" height="40" rx="1.5" fill="#334155"/>
    <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="26" fill="#080a0f" stroke="#334155" stroke-width="1.8"/>
    <rect x="{px + 6}" y="{py + 6}" width="{pw - 12}" height="{ph - 12}" rx="20" fill="{T['chrome']}" stroke="{T['border']}"/>
    <circle cx="{px + pw / 2:.0f}" cy="{py + 18}" r="4" fill="#040609" stroke="#1e293b"/>
    <text x="{px + 18}" y="{py + 22}" class="mono muted" font-size="9">9:41</text>
    <text x="{px + pw - 18}" y="{py + 22}" text-anchor="end" class="mono mint" font-size="8.5">5G</text>

    <!-- Identity inside Pixel -->
    <rect x="{px + 14}" y="{py + 34}" width="{pw - 28}" height="56" rx="12" fill="{T['surface']}" stroke="{T['border']}"/>
    <rect x="{px + 22}" y="{py + 44}" width="34" height="34" rx="9" fill="{T['mint']}" fill-opacity=".15" stroke="{T['mint']}" stroke-opacity=".45"/>
    <path d="M{px + 31},{py + 64} a8,8 0 0 1 16,0 Z" fill="{T['mint']}"/>
    <circle cx="{px + 36}" cy="{py + 60}" r="1" fill="{T['bg']}"/>
    <circle cx="{px + 42}" cy="{py + 60}" r="1" fill="{T['bg']}"/>
    <text x="{px + 63}" y="{py + 59}" font-size="11.5" font-weight="800">Aditya Mishra</text>
    <text x="{px + 63}" y="{py + 74}" class="mono mint" font-size="8.8">@2b-adrix · India</text>

    <!-- Who Am I Bio Block -->
    <rect x="{px + 14}" y="{py + 100}" width="{pw - 28}" height="122" rx="12" fill="{T['bg']}" stroke="{T['border']}"/>
    <text x="{px + 24}" y="{py + 120}" class="mono coral" font-size="9.2" font-weight="700">$ whoami</text>
    <text x="{px + 24}" y="{py + 139}" font-size="11" font-weight="700" fill="{T['text']}">Android &amp; Backend</text>
    <text x="{px + 24}" y="{py + 159}" class="mono mint" font-size="9">· B.Tech CSE '28</text>
    <text x="{px + 24}" y="{py + 176}" class="mono mint" font-size="9">· Mewar University</text>
    <text x="{px + 24}" y="{py + 193}" class="mono mint" font-size="9">· Team Alpha-coders</text>
    <text x="{px + 24}" y="{py + 210}" class="mono sky" font-size="9">· Open to Collab</text>

    <!-- Phone bottom status pill -->
    <rect x="{px + 14}" y="{py + 234}" width="{pw - 28}" height="32" rx="16" fill="{T['mint']}" fill-opacity=".14" stroke="{T['mint']}" stroke-opacity=".5"/>
    <circle class="pulse" cx="{px + 30}" cy="{py + 250}" r="3.8" fill="{T['mint']}"/>
    <text x="{px + 41}" y="{py + 253.5}" class="mono mint" font-size="9.2" font-weight="700">ANDROID CLIENT</text>
    <polygon points="{px + 7},{py + 7} {px + 105},{py + 7} {px + 55},{py + ph - 7} {px + 7},{py + ph - 7}" fill="url(#phoneGlare)" opacity=".05"/>

    <!-- Spring Boot Backend Server Node -->
    <rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="16" fill="{T['chrome']}" stroke="{T['border']}"/>
    <rect x="{sx + 20}" y="{sy}" width="{sw - 40}" height="2.5" rx="1.25" fill="{T['sky']}"/>
    <text x="{sx + 14}" y="{sy + 24}" class="mono sky" font-size="9.5" font-weight="700">API SERVER</text>
    <circle class="pulse" cx="{sx + sw - 16}" cy="{sy + 20}" r="3.5" fill="{T['mint']}"/>

    <!-- Server rack modules -->
    <rect x="{sx + 12}" y="{sy + 38}" width="{sw - 24}" height="50" rx="9" fill="{T['surface']}" stroke="{T['border']}"/>
    <text x="{sx + 20}" y="{sy + 57}" font-size="11.5" font-weight="800">Spring Boot</text>
    <text x="{sx + 20}" y="{sy + 74}" class="mono sky" font-size="9">Java 17/21 · API</text>

    <rect x="{sx + 12}" y="{sy + 96}" width="{sw - 24}" height="74" rx="9" fill="{T['bg']}" stroke="{T['border']}"/>
    <text x="{sx + 20}" y="{sy + 114}" class="mono coral" font-size="9">POST /v1/auth</text>
    <text x="{sx + 20}" y="{sy + 131}" class="mono mint" font-size="9">200 OK · JWT</text>
    <text x="{sx + 20}" y="{sy + 148}" class="mono muted" font-size="9">GET /v1/sync</text>
    <text x="{sx + 20}" y="{sy + 163}" class="mono dim" font-size="8.5">JPA · Security</text>

    <rect x="{sx + 12}" y="{sy + 178}" width="{sw - 24}" height="42" rx="9" fill="{T['surface']}" stroke="{T['border']}"/>
    <text x="{sx + 20}" y="{sy + 196}" class="mono gold" font-size="9">DATA + CLOUD</text>
    <text x="{sx + 20}" y="{sy + 211}" class="mono muted" font-size="8.5">Mongo · SQL · Fb</text>

    <rect x="{sx + 12}" y="{sy + 228}" width="{sw - 24}" height="24" rx="12" fill="{T['sky']}" fill-opacity=".14" stroke="{T['sky']}" stroke-opacity=".45"/>
    <text x="{sx + sw / 2:.0f}" y="{sy + 243.5}" text-anchor="middle" class="mono sky" font-size="8.8" font-weight="700">DOCKER READY</text>
  </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(NAME)} — {esc(ROLE)}">
<title>{esc(NAME)} — {esc(ROLE)}</title>
<style>
text {{ font-family: {SANS}; fill: {T['text']}; }}
.mono {{ font-family: {MONO}; white-space: pre; }}
.muted {{ fill: {T['muted']}; }} .dim {{ fill: {T['dim']}; }} .mint {{ fill: {T['mint']}; }} .coral {{ fill: {T['coral']}; }} .sky {{ fill: {T['sky']}; }} .gold {{ fill: {T['gold']}; }}
.fade {{ animation: fadeIn .8s ease-out both; }}
.pulse {{ animation: pulseDot 2.2s ease-in-out infinite; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes pulseDot {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
.glow {{ animation: drift 14s ease-in-out infinite alternate; }}
@keyframes drift {{ from {{ transform: translate(0,0); }} to {{ transform: translate(34px,-12px); }} }}
</style>
<defs>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
    <path d="M 28 0 L 0 0 0 28" fill="none" stroke="{T['grid']}" stroke-width="0.8"/>
  </pattern>
  <radialGradient id="gMint" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{T['mint']}" stop-opacity=".24"/><stop offset="1" stop-color="{T['mint']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="gSky" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{T['sky']}" stop-opacity=".18"/><stop offset="1" stop-color="{T['sky']}" stop-opacity="0"/></radialGradient>
  <linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T['mint']}"/><stop offset=".55" stop-color="{T['sky']}"/><stop offset="1" stop-color="{T['coral']}"/></linearGradient>
  <linearGradient id="topBar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T['mint']}" stop-opacity="0"/><stop offset=".5" stop-color="{T['sky']}" stop-opacity=".85"/><stop offset="1" stop-color="{T['coral']}" stop-opacity="0"/></linearGradient>
  <linearGradient id="phoneGlare" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
  <clipPath id="frame"><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{w}" height="{h}" fill="{T['bg']}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)" opacity=".75"/>
  <rect x="0" y="0" width="{w}" height="2" fill="url(#topBar)"/>
  <ellipse class="glow" cx="150" cy="80" rx="300" ry="180" fill="url(#gMint)"/>
  <ellipse class="glow" cx="840" cy="240" rx="280" ry="170" fill="url(#gSky)" style="animation-delay:-7s"/>

  <g class="fade">
    <rect x="44" y="34" width="286" height="26" rx="13" fill="{T['surface']}" stroke="{T['border']}"/>
    <circle class="pulse" cx="60" cy="47" r="4" fill="{T['mint']}"/>
    <text x="72" y="51" class="mono" font-size="10.2" fill="{T['mint']}">ANDROID + BACKEND // {esc(HANDLE)}</text>
    <text x="42" y="120" font-size="50" font-weight="900" letter-spacing="1">{esc(NAME)}</text>
    <rect x="44" y="132" width="136" height="4" rx="2" fill="url(#nameGrad)"/>
  </g>

  <g class="fade" {delay(0.2)}>
    <text x="44" y="170" font-size="23" font-weight="700" fill="url(#nameGrad)" style="fill:url(#nameGrad)">{esc(ROLE)}</text>
    <text x="44" y="198" font-size="13.5" class="muted">{esc(SUB)}</text>
  </g>

  <g class="fade" {delay(0.4)}>
    <rect x="44" y="218" width="4" height="24" rx="2" fill="{T['coral']}"/>
    <text x="58" y="235" font-size="14" font-style="italic" fill="{T['text']}">“{esc(MOTTO)}”</text>
  </g>

  {''.join(chips_svg)}
  {dual_rig}
</g>
<path d="M22 10 h-12 v12 M{w - 22} 10 h12 v12 M22 {h - 10} h-12 v-12 M{w - 22} {h - 10} h12 v-12" fill="none" stroke="{T['mint']}" stroke-opacity=".48" stroke-width="1.5"/>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="22" fill="none" stroke="{T['border']}"/>
</svg>
"""


def architecture_svg() -> str:
    """Animated End-to-End Android Client -> Spring Boot API -> Data & Cloud Architecture Card."""
    w, h = 1000, 224
    nodes = [
        (
            24,
            T["mint"],
            "01 · MOBILE CLIENT",
            "Native Android App",
            ["Kotlin · Jetpack Compose · Material 3", "MVVM · Room + SQLCipher Vault", "CameraX · TFLite ML · Biometrics"],
        ),
        (
            356,
            T["sky"],
            "02 · BACKEND SERVICES",
            "Spring Boot REST API",
            ["Java 17/21 · Spring Boot 3 & 4", "Spring Security · JJWT Auth", "REST Controllers · Spring Data JPA"],
        ),
        (
            688,
            T["coral"],
            "03 · DATA & CLOUD",
            "Persistence & AI Layer",
            ["MongoDB · MySQL · SQLite", "Firebase Auth & Realtime Sync", "Docker Containers · Gemini AI"],
        ),
    ]
    body = []
    # Connecting lines + animated glowing packets
    for x_start, x_end, label, color in ((312, 356, "HTTPS", T["mint"]), (644, 688, "JPA/DB", T["sky"])):
        body.append(
            f'<line x1="{x_start}" y1="84" x2="{x_end}" y2="84" stroke="{color}" stroke-width="1.8" stroke-dasharray="4 3"/>'
            f'<circle cx="{x_start + 8}" cy="84" r="3.5" fill="{color}">'
            f'<animate attributeName="cx" values="{x_start + 4};{x_end - 4};{x_start + 4}" dur="2.1s" repeatCount="indefinite"/></circle>'
            f'<rect x="{x_start + 4}" y="58" width="36" height="16" rx="4" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<text x="{(x_start + x_end) / 2:.0f}" y="69" text-anchor="middle" class="mono" font-size="8.5" fill="{color}">{label}</text>'
        )

    for idx, (nx, ac, kicker, title, bullets) in enumerate(nodes):
        body.append(
            f'<g class="fade" {delay(0.1 * idx)}>'
            f'<rect x="{nx}" y="18" width="288" height="144" rx="14" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<rect x="{nx}" y="34" width="3.5" height="28" rx="1.75" fill="{ac}"/>'
            f'<text x="{nx + 16}" y="40" class="mono" font-size="9.5" font-weight="700" fill="{ac}" letter-spacing="0.8">{esc(kicker)}</text>'
            f'<text x="{nx + 16}" y="62" font-size="16" font-weight="800">{esc(title)}</text>'
            f'<line x1="{nx + 16}" y1="74" x2="{nx + 272}" y2="74" stroke="{T["grid"]}"/>'
            f'<text x="{nx + 16}" y="96" class="mono muted" font-size="10.8">› {esc(bullets[0])}</text>'
            f'<text x="{nx + 16}" y="117" class="mono muted" font-size="10.8">› {esc(bullets[1])}</text>'
            f'<text x="{nx + 16}" y="138" class="mono muted" font-size="10.8">› {esc(bullets[2])}</text>'
            f'</g>'
        )
    return panel(w, h, "ARCHITECTURE // END-TO-END SYSTEM FLOW", "\n".join(body), tag="MOBILE ↔ API ↔ DATA", accent=T["sky"])


def toolkit_svg() -> str:
    """2x2 Bento Material Grid with uniform rounded icon sockets."""
    w, h = 1000, 326
    box_w, box_h = 468, 124
    positions = [(22, 16), (510, 16), (22, 152), (510, 152)]
    body = []
    for idx, ((title, accent, icons, pills), (bx, by)) in enumerate(zip(TOOLKIT_GRID, positions)):
        body.append(
            f'<g class="fade" {delay(idx * 0.09)}>'
            f'<rect x="{bx}" y="{by}" width="{box_w}" height="{box_h}" rx="14" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<rect x="{bx}" y="{by + 16}" width="3.5" height="24" rx="1.75" fill="{accent}"/>'
            f'<text x="{bx + 16}" y="{by + 27}" class="mono" font-size="11" font-weight="700" fill="{accent}" letter-spacing="0.8">{esc(title)}</text>'
        )
        ix, iy = bx + 16, by + 40
        for name in icons:
            short = name.split("-")[0]
            body.append(
                f'<rect x="{ix}" y="{iy}" width="44" height="44" rx="10" fill="{T["bg"]}" stroke="{T["border"]}"/>'
                f'<image x="{ix + 5}" y="{iy + 5}" width="34" height="34" href="{_icon_uri(name)}">'
                f'<title>{esc(LABELS.get(short, short))}</title></image>'
            )
            ix += 52
        if pills:
            px, py = bx + 16, by + 93
            for pill in pills:
                pw = len(pill) * 6.5 + 22
                body.append(
                    f'<rect x="{px}" y="{py}" width="{pw:.0f}" height="20" rx="10" fill="{T["bg"]}" stroke="{T["border"]}"/>'
                    f'<circle cx="{px + 9}" cy="{py + 10}" r="2.2" fill="{accent}"/>'
                    f'<text x="{px + 16}" y="{py + 13.5}" class="mono muted" font-size="10">{esc(pill)}</text>'
                )
                px += pw + 6
        body.append("</g>")
    return panel(w, h, "STACK // ARCHITECTURE MATRIX", "\n".join(body), tag="23 TOOLS · 4 LAYERS", accent=T["mint"])


def project_card(p: dict) -> str:
    w, h = 490, 178
    ac = p["accent"]
    pills_svg, px = [], 20
    for pill in p["pills"]:
        pw = len(pill) * 6.8 + 20
        pills_svg.append(
            f'<rect x="{px}" y="97" width="{pw:.0f}" height="22" rx="11" fill="{T["surface"]}" stroke="{T["border"]}"/>'
            f'<text x="{px + pw / 2:.0f}" y="111.5" text-anchor="middle" class="mono muted" font-size="10.2">{esc(pill)}</text>'
        )
        px += pw + 7
    body = [
        f'<rect x="20" y="15" width="4" height="24" rx="2" fill="{ac}"/>',
        f'<text x="33" y="33" font-size="18" font-weight="800">{esc(p["name"])}</text>',
        f'<text x="20" y="57" font-size="12.5" class="muted">{esc(p["desc"][0])}</text>',
        f'<text x="20" y="75" font-size="12.5" class="muted">{esc(p["desc"][1])}</text>',
        f'<line x1="20" y1="87" x2="{w - 20}" y2="87" stroke="{T["grid"]}"/>',
        "".join(pills_svg),
        f'<circle cx="{w - 92}" cy="108" r="4.2" fill="{p["lang_color"]}"/>',
        f'<text x="{w - 82}" y="112" class="mono dim" font-size="10.5">{esc(p["lang"])}</text>',
    ]
    return panel(w, h, f"BUILD #{p['num']} · {p['tag']}", "\n".join(body), tag="OPEN REPO ↗", accent=ac)


def footer_svg() -> str:
    w, h = 1000, 56
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Footer">
<defs>
  <linearGradient id="fg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{T['mint']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{T['sky']}" stop-opacity=".8"/>
    <stop offset="1" stop-color="{T['coral']}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{w}" height="{h}" rx="14" fill="{T['chrome']}" stroke="{T['border']}"/>
<rect x="0" y="0" width="{w}" height="1.6" fill="url(#fg)"/>
<circle cx="24" cy="28" r="4" fill="{T['mint']}"/>
<text x="38" y="32" font-family="{MONO}" font-size="11.5" fill="{T['muted']}">
  ANDROID + BACKEND ENGINE · PURE PYTHON SVG · SYNCED BY GITHUB ACTIONS
</text>
<text x="{w - 24}" y="32" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{T['coral']}">
  adrix.is-a.dev
</text>
</svg>
"""


def build(root: Path) -> None:
    out = root / "assets" / "static"
    write(out / "header.svg", header_svg())
    write(out / "architecture.svg", architecture_svg())
    write(out / "toolkit.svg", toolkit_svg())
    write(out / "footer.svg", footer_svg())
    for p in PROJECTS:
        write(out / "projects" / p["file"], project_card(p))
    for filename, label, color, icon_svg in BADGES:
        write(out / "badges" / filename, badge_svg(label, color, icon_svg))
