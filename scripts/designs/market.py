"""Night market: bulb strings, painted stalls, and price tags."""

from __future__ import annotations

from .common import (
    HEAVY,
    MONO,
    PROJECTS,
    SANS,
    TAGLINES,
    TOOL_GROUPS,
    esc,
    fitted,
    glyph_paths,
    language_rows,
    load_glyph,
    meter,
    svg,
)

THEMES = {
    "dark": {
        "sky": "#241433",
        "sky2": "#4a1d4e",
        "ink": "#2a160c",
        "paper": "#fff4d8",
        "muted": "#e7c9a0",
        "wood": "#7a4324",
        "sign": "#b4232a",
        "gold": "#ffe08a",
        "title": "#ffe08a",
        "caption": "#fff4d8",
    },
    "light": {
        "sky": "#ffd7b0",
        "sky2": "#ff8f6b",
        "ink": "#2a160c",
        "paper": "#fffaf0",
        "muted": "#6b3a22",
        "wood": "#8a4b2a",
        "sign": "#b4232a",
        "gold": "#ffe08a",
        "title": "#7a1020",
        "caption": "#2a160c",
    },
}

AWNINGS = {
    "trackmyspend": ("#c6f54a", "#16321a"),
    "resume-ledger": ("#ff4f8b", "#fff4d8"),
    "odia-stt": ("#3ec6ff", "#12324a"),
    "clean-tv": ("#ffb703", "#5c2a12"),
    "bg-download": ("#c77dff", "#2a1248"),
    "warehouse": ("#ff5a36", "#ffe08a"),
}

MOTION = """
    .glow { animation: glow 3.6s ease-in-out infinite; }
    @keyframes glow { 50% { opacity: 0.2; } }"""


def bulbs(x0: float, x1: float, y: float, step: float = 42, r: float = 7) -> str:
    colors = ["#ffe08a", "#ff4f8b", "#3ec6ff", "#c6f54a", "#ffb703"]
    out = [f'<path d="M{x0 - 10} {y} H{x1 + 10}" fill="none" stroke="#1a120c" stroke-width="2"/>']
    x = x0
    i = 0
    while x <= x1 + 0.1:
        color = colors[i % len(colors)]
        glow = ' class="glow"' if i % 3 == 0 else ""
        out.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y + 12}" stroke="#1a120c" stroke-width="2"/>')
        out.append(f'<circle{glow} cx="{x:.1f}" cy="{y + 12 + r:.1f}" r="{r + 5}" fill="{color}" opacity="0.45"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y + 12 + r:.1f}" r="{r}" fill="{color}" stroke="#1a120c" stroke-width="2"/>')
        x += step
        i += 1
    return "".join(out)


def hero(t: dict) -> str:
    flags = []
    colors = ["#ff5a36", "#ffb703", "#3ec6ff", "#c6f54a", "#ff4f8b", "#c77dff"]
    for i, x in enumerate(range(70, 1140, 46)):
        flags.append(
            f'<path d="M{x} 78 L{x + 28} 78 L{x + 14} 112 Z" fill="{colors[i % 6]}" stroke="#1a120c" stroke-width="2"/>'
        )
    body = f'''  <rect width="1200" height="460" fill="url(#sky)"/>
  {bulbs(60, 1140, 36, 48, 8)}
  {"".join(flags)}
  <rect x="230" y="150" width="740" height="190" rx="16" fill="{t["sign"]}" stroke="{t["gold"]}" stroke-width="8"/>
  <text x="606" y="278" text-anchor="middle" font-family="{HEAVY}" font-size="96" font-weight="900" fill="#7a1020">NIGAM</text>
  <text x="600" y="272" text-anchor="middle" font-family="{HEAVY}" font-size="96" font-weight="900" fill="{t["gold"]}">NIGAM</text>
  <rect x="330" y="360" width="540" height="46" rx="8" fill="{t["wood"]}" stroke="#1a120c" stroke-width="3"/>
  <text x="600" y="390" text-anchor="middle" font-family="{SANS}" font-size="18" font-weight="700" fill="{t["gold"]}">FULL STACK · ANDROID · MACHINE LEARNING</text>
  <text x="600" y="436" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{t["caption"]}">plays the ukulele · open tonight</text>'''
    defs = f'''    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["sky"]}"/><stop offset="1" stop-color="{t["sky2"]}"/>
    </linearGradient>'''
    return svg(
        1200, 460, "Nigam night market",
        "A night-market sign reading NIGAM, hung under bare bulbs and bunting. Full stack, Android and machine learning. Plays the ukulele.",
        body, MOTION, defs,
    )


def stall(t: dict, slug: str, name: str) -> str:
    cloth, letter = AWNINGS[slug]
    size = 26 if len(name) < 16 else 18
    stripes = []
    for i, x in enumerate(range(24, 536, 32)):
        stripes.append(f'<rect x="{x}" y="78" width="32" height="70" fill="{cloth if i % 2 == 0 else letter}"/>')
    scallops = "".join(
        f'<path d="M{x} 148 Q{x + 16} 176 {x + 32} 148 Z" fill="{cloth if ((x - 24) // 32) % 2 == 0 else letter}"/>'
        for x in range(24, 536, 32)
    )
    body = f'''  <rect width="560" height="380" fill="url(#sky)"/>
  {bulbs(30, 520, 16, 46, 6)}
  <path d="M24 78 H536 V148 H24 Z" fill="{cloth}" stroke="#1a120c" stroke-width="3"/>
  {"".join(stripes)}
  <path d="M24 78 H536 V148 H24 Z" fill="none" stroke="#1a120c" stroke-width="3"/>
  {scallops}
  <rect x="70" y="186" width="420" height="64" rx="8" fill="{t["wood"]}" stroke="#1a120c" stroke-width="3"/>
  <text x="280" y="226" text-anchor="middle" font-family="{HEAVY}" font-size="{size}" font-weight="800" fill="{t["gold"]}">{esc(name)}</text>
  <rect x="90" y="268" width="380" height="78" rx="8" fill="{t["paper"]}" stroke="#1a120c" stroke-width="3"/>
  <text x="280" y="300" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["muted"]}">ON THE MENU</text>
  <text x="280" y="328" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="700" fill="{t["ink"]}">{esc(TAGLINES[slug])}</text>'''
    defs = f'''    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["sky"]}"/><stop offset="1" stop-color="{t["sky2"]}"/>
    </linearGradient>'''
    return svg(560, 380, f"{name} stall", f"Market stall for {name}: {TAGLINES[slug]}.", body, MOTION, defs)


def shelf(t: dict) -> str:
    rows = language_rows()
    n = len(rows)
    gap = 1080 / n
    jars = []
    for i, (name, pct) in enumerate(rows):
        x = 70 + gap * i + gap / 2
        liquid = 150 * meter(pct)
        color = ["#ff5a36", "#ffb703", "#3ec6ff", "#c6f54a", "#ff4f8b", "#c77dff", "#ffe08a", "#7af0c0", "#d9c3a1"][i]
        parts = name.split(" ", 1)
        jars.append(
            f'<path d="M{x - 28:.0f} 150 h56 v150 a28 28 0 0 1 -56 0z" fill="{t["paper"]}" stroke="#1a120c" stroke-width="3"/>'
            f'<path d="M{x - 22:.0f} {300 - liquid:.0f} h44 v{liquid - 8:.0f} a22 22 0 0 1 -44 0z" fill="{color}"/>'
            f'<rect x="{x - 22:.0f}" y="138" width="44" height="16" rx="3" fill="{t["wood"]}" stroke="#1a120c" stroke-width="2"/>'
            f'<text x="{x:.0f}" y="340" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="800" fill="{t["title"]}">{pct:.1f}%</text>'
            f'<text x="{x:.0f}" y="362" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{t["caption"]}">{esc(parts[0])}</text>'
            + (f'<text x="{x:.0f}" y="380" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{t["caption"]}">{esc(parts[1])}</text>' if len(parts) > 1 else "")
        )
    body = f'''  <rect width="1200" height="430" fill="url(#sky)"/>
  <rect x="40" y="300" width="1120" height="18" fill="{t["wood"]}" stroke="#1a120c" stroke-width="3"/>
  <text x="48" y="64" font-family="{HEAVY}" font-size="32" fill="{t["title"]}">THE SHELF</text>
  <text x="280" y="64" font-family="{SANS}" font-size="15" fill="{t["caption"]}">jars are compressed · percents are the true share</text>
  {"".join(jars)}'''
    defs = f'''    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["sky"]}"/><stop offset="1" stop-color="{t["sky2"]}"/>
    </linearGradient>'''
    summary = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return svg(1200, 430, "The shelf", f"Language mix as jars on a market shelf. {summary}.", body, "", defs)


def tags(t: dict) -> str:
    rows = []
    y = 120
    for group, tools in TOOL_GROUPS:
        rows.append(f'<text x="40" y="{y - 28}" font-family="{SANS}" font-size="13" font-weight="800" letter-spacing="1" fill="{t["title"]}">{esc(group)}</text>')
        rows.append(f'<path d="M48 {y} H1160" stroke="#1a120c" stroke-width="3"/>')
        rows.append(bulbs(70, 1120, y - 8, 70, 5))
        x = 70
        span = 1040 / len(tools)
        for tool in tools:
            cx = x + span / 2
            w = max(96, len(tool) * 8 + 28)
            rows.append(
                f'<line x1="{cx:.0f}" y1="{y}" x2="{cx:.0f}" y2="{y + 22}" stroke="#1a120c" stroke-width="2"/>'
                f'<rect x="{cx - w / 2:.0f}" y="{y + 22}" width="{w:.0f}" height="40" rx="4" fill="{t["paper"]}" stroke="#1a120c" stroke-width="2"/>'
                f'<circle cx="{cx:.0f}" cy="{y + 30}" r="3" fill="{t["sign"]}"/>'
                f'<text x="{cx:.0f}" y="{y + 48}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="{t["ink"]}">{esc(tool)}</text>'
            )
            x += span
        y += 130
    height = y + 10
    body = f'''  <rect width="1200" height="{height}" fill="url(#sky)"/>
  <text x="40" y="52" font-family="{HEAVY}" font-size="32" fill="{t["title"]}">PRICE TAGS</text>
  {"".join(rows)}'''
    defs = f'''    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["sky"]}"/><stop offset="1" stop-color="{t["sky2"]}"/>
    </linearGradient>'''
    tools = "; ".join(f"{g.title()}: {', '.join(ts)}" for g, ts in TOOL_GROUPS)
    return svg(1200, height, "Price tags", f"Toolbox hung as market price tags. {tools}.", body, MOTION, defs)


BUTTONS = {
    "email": ("EMAIL", "nigmucode@gmail.com", "#ff5a36"),
    "x": ("X", "@nigmu7161", "#3ec6ff"),
    "linkedin": ("LINKEDIN", "nigamananda-behera", "#c6f54a"),
}


def lantern(slug: str) -> str:
    title, handle, color = BUTTONS[slug]
    ink = "#1a120c"
    body = f'''  <rect width="360" height="120" fill="#241433"/>
  <line x1="180" y1="0" x2="180" y2="18" stroke="{ink}" stroke-width="3"/>
  <rect x="28" y="18" width="304" height="78" rx="10" fill="{color}" stroke="{ink}" stroke-width="3"/>
  <path d="M28 96 H332 L300 116 H60 Z" fill="{color}" stroke="{ink}" stroke-width="3"/>
  <text x="180" y="52" text-anchor="middle" font-family="{HEAVY}" font-size="20" fill="{ink}">{title}</text>
  <text x="180" y="78" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="{ink}">{esc(handle)}</text>'''
    return svg(360, 120, f"{title} lantern", f"Paper lantern: {title}, {handle}.", body)


def footer(t: dict) -> str:
    odia = load_glyph("odia-bold")
    tf, w, _ = fitted(odia, 0, 0, height=42)
    body = f'''  <rect width="1200" height="160" fill="url(#sky)"/>
  {bulbs(80, 1120, 24, 80, 6)}
  <g transform="translate({600 - w / 2:.0f} 78)"><g transform="{tf}">{glyph_paths(odia, f'fill="{t["gold"]}"')}</g></g>'''
    defs = f'''    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["sky"]}"/><stop offset="1" stop-color="{t["sky2"]}"/>
    </linearGradient>'''
    return svg(1200, 160, "Namaskar", "Bulbs over the Odia greeting namaskar.", body, MOTION, defs)


def build() -> dict[str, str]:
    files: dict[str, str] = {}
    for theme, palette in THEMES.items():
        files[f"assets/hero-{theme}.svg"] = hero(palette)
        files[f"assets/shelf-{theme}.svg"] = shelf(palette)
        files[f"assets/tags-{theme}.svg"] = tags(palette)
        files[f"assets/footer-{theme}.svg"] = footer(palette)
        for slug, name, _ in PROJECTS:
            files[f"assets/stalls/{slug}-{theme}.svg"] = stall(palette, slug, name)
    for slug in BUTTONS:
        files[f"assets/lanterns/{slug}.svg"] = lantern(slug)
    return files
