"""Mission control: a launch board, fuel tanks, and a switch console."""

from __future__ import annotations

from .common import (
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
        "bg": "#071018",
        "panel": "#0d1b2e",
        "ink": "#e7f0ff",
        "muted": "#8aa4c2",
        "line": "#1e3a5f",
        "green": "#3ddc97",
        "amber": "#ffc857",
        "cyan": "#7fd7ff",
        "red": "#ff6b6b",
        "white": "#f4f8ff",
        "radar": "#0b2438",
    },
    "light": {
        "bg": "#f4f1e8",
        "panel": "#fffdf8",
        "ink": "#1c2430",
        "muted": "#6d6256",
        "line": "#e2d8c8",
        "green": "#0c8f4e",
        "amber": "#e39b12",
        "cyan": "#0b6e99",
        "red": "#d23b3b",
        "white": "#ffffff",
        "radar": "#e7f6ee",
    },
}

CALLS = ["TMS-1", "RSM-2", "ODA-3", "CTV-4", "BGD-5", "WMS-6"]

MOTION = """
    .sweep { animation: spin 14s linear infinite; transform-box: fill-box; transform-origin: center; }
    @keyframes spin { to { transform: rotate(360deg); } }
    .lamp { animation: lamp 3.2s ease-in-out infinite; }
    @keyframes lamp { 50% { opacity: 0.35; } }
    .bob { animation: bob 4s ease-in-out infinite; }
    @keyframes bob { 50% { transform: translateY(-8px); } }"""


def _lamp(cx: float, cy: float, color: str, live: bool = False) -> str:
    klass = ' class="lamp"' if live else ""
    return (
        f'<circle{klass} cx="{cx}" cy="{cy}" r="9" fill="{color}"/>'
        f'<circle cx="{cx - 2}" cy="{cy - 2}" r="3" fill="#ffffff" opacity="0.65"/>'
    )


def _rocket(cx: float, cy: float, t: dict) -> str:
    return f'''<g class="bob" transform="translate({cx} {cy})">
    <path d="M0 -78 C26 -46 26 8 0 36 C-26 8 -26 -46 0 -78Z" fill="{t["white"]}" stroke="{t["ink"]}" stroke-width="3"/>
    <circle cy="-18" r="10" fill="{t["cyan"]}" stroke="{t["ink"]}" stroke-width="3"/>
    <path d="M-16 20 L-34 52 L-6 30Z" fill="{t["amber"]}" stroke="{t["ink"]}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M16 20 L34 52 L6 30Z" fill="{t["amber"]}" stroke="{t["ink"]}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M-8 36 H8 L0 64Z" fill="{t["red"]}" stroke="{t["ink"]}" stroke-width="2"/>
  </g>'''


def hero(t: dict) -> str:
    cx, cy, r = 860, 230, 158
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{t["green"]}" stroke-width="1.5" opacity="0.55"/>'
        for radius in (52, 104, 150)
    )
    rows = []
    for i, label in enumerate(("FULL STACK", "ANDROID", "MACHINE LEARNING")):
        y = 214 + i * 42
        rows.append(
            f'{_lamp(78, y - 6, t["green"], live=True)}'
            f'<text x="100" y="{y}" font-family="{MONO}" font-size="20" font-weight="700" letter-spacing="2" fill="{t["ink"]}">{label}</text>'
        )
    body = f'''  <rect width="1200" height="460" fill="{t["bg"]}"/>
  <rect x="28" y="28" width="1144" height="404" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>
  <text x="64" y="78" font-family="{MONO}" font-size="15" letter-spacing="4" fill="{t["amber"]}">MISSION CONTROL</text>
  <text x="60" y="158" font-family="{SANS}" font-size="84" font-weight="800" fill="{t["ink"]}">NIGAM</text>
  {"".join(rows)}
  <text x="64" y="360" font-family="{MONO}" font-size="16" fill="{t["muted"]}">CREW NOTE · PLAYS THE UKULELE</text>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["radar"]}" stroke="{t["green"]}" stroke-width="3"/>
  {rings}
  <path d="M{cx - r} {cy} H{cx + r} M{cx} {cy - r} V{cy + r}" stroke="{t["green"]}" stroke-width="1" opacity="0.4"/>
  <g class="sweep">
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none"/>
    <path d="M{cx} {cy} L{cx} {cy - r} A{r} {r} 0 0 1 {cx + r} {cy} Z" fill="{t["green"]}" opacity="0.28"/>
  </g>
  {_rocket(cx, cy + 8, t)}
  <rect y="436" width="1200" height="24" fill="url(#hazard)"/>'''
    defs = f'''    <pattern id="hazard" width="20" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="20" height="24" fill="{t["amber"]}"/>
      <rect width="10" height="24" fill="{t["bg"]}"/>
    </pattern>'''
    return svg(
        1200, 460, "Mission control",
        "Launch board for Nigam. Status lamps for full stack, Android and machine learning. A radar sweeps behind a small rocket. Crew note: plays the ukulele.",
        body, MOTION, defs,
    )


def card(t: dict, slug: str, name: str, index: int) -> str:
    call = CALLS[index]
    size = 32 if len(name) < 16 else 24
    body = f'''  <rect width="560" height="280" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>
  <rect width="10" height="280" fill="{t["amber"] if index % 2 == 0 else t["cyan"]}"/>
  <text x="32" y="42" font-family="{MONO}" font-size="16" letter-spacing="2" fill="{t["amber"]}">{call}</text>
  {_lamp(430, 36, t["green"], live=True)}
  <text x="448" y="42" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="1" fill="{t["green"]}">NOMINAL</text>
  <text x="32" y="118" font-family="{SANS}" font-size="{size}" font-weight="800" fill="{t["ink"]}">{esc(name)}</text>
  <text x="32" y="158" font-family="{MONO}" font-size="16" fill="{t["muted"]}">OBJECTIVE</text>
  <text x="32" y="190" font-family="{SANS}" font-size="22" fill="{t["ink"]}">{esc(TAGLINES[slug])}</text>
  <g fill="{t["line"]}"><circle cx="36" cy="230" r="3"/><circle cx="52" cy="230" r="3"/><circle cx="68" cy="230" r="3"/><circle cx="84" cy="230" r="3"/></g>
  <text x="104" y="235" font-family="{MONO}" font-size="13" fill="{t["muted"]}">LINK LIVE</text>'''
    return svg(560, 280, f"{call} {name}", f"Mission card {call} for {name}: {TAGLINES[slug]}. Status nominal.", body, MOTION)


def fuel(t: dict) -> str:
    rows = language_rows()
    tubes = []
    n = len(rows)
    span = 1040
    gap = span / n
    for i, (name, pct) in enumerate(rows):
        x = 80 + gap * i + gap / 2
        level = meter(pct)
        liquid_h = 200 * level
        color = (t["green"], t["cyan"], t["amber"], t["red"])[i % 4]
        parts = name.split(" ", 1)
        tubes.append(
            f'<rect x="{x - 22:.1f}" y="120" width="44" height="210" rx="22" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="3"/>'
            f'<rect x="{x - 16:.1f}" y="{324 - liquid_h:.1f}" width="32" height="{liquid_h:.1f}" rx="16" fill="{color}"/>'
            f'<rect x="{x - 10:.1f}" y="132" width="6" height="186" rx="3" fill="#ffffff" opacity="0.18"/>'
            f'<text x="{x:.1f}" y="360" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{color}">{pct:.1f}%</text>'
            f'<text x="{x:.1f}" y="384" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{t["ink"]}">{esc(parts[0])}</text>'
            + (f'<text x="{x:.1f}" y="402" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{t["ink"]}">{esc(parts[1])}</text>' if len(parts) > 1 else "")
        )
    body = f'''  <rect width="1200" height="460" fill="{t["bg"]}"/>
  <rect x="24" y="24" width="1152" height="412" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>
  <text x="48" y="68" font-family="{MONO}" font-size="22" font-weight="700" letter-spacing="3" fill="{t["ink"]}">FUEL</text>
  <text x="160" y="68" font-family="{MONO}" font-size="14" fill="{t["muted"]}">compressed tanks · percents are the true share of public bytes</text>
  {"".join(tubes)}'''
    summary = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return svg(1200, 460, "Fuel", f"Language mix drawn as fuel tanks. The fill is compressed; the percentages are true. {summary}.", body)


def console(t: dict) -> str:
    rows = []
    y = 118
    for g, (group, tools) in enumerate(TOOL_GROUPS):
        rows.append(f'<text x="40" y="{y + 8}" font-family="{MONO}" font-size="13" letter-spacing="1" fill="{t["amber"]}">{esc(group)}</text>')
        switches = []
        for i, tool in enumerate(tools):
            x = 230 + i * 155
            color = (t["green"], t["cyan"], t["amber"], t["red"])[(g + i) % 4]
            switches.append(
                f'<rect x="{x}" y="{y - 16}" width="132" height="36" rx="8" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="2"/>'
                f'<text x="{x + 12}" y="{y + 7}" font-family="{SANS}" font-size="13" font-weight="700" fill="{t["ink"]}">{esc(tool)}</text>'
                f'<circle cx="{x + 112}" cy="{y + 2}" r="8" fill="{color}"/>'
            )
        rows.append("".join(switches))
        y += 96
    height = y + 20
    body = f'''  <rect width="1200" height="{height}" fill="{t["bg"]}"/>
  <rect x="24" y="24" width="1152" height="{height - 48}" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>
  <text x="48" y="68" font-family="{MONO}" font-size="22" font-weight="700" letter-spacing="3" fill="{t["ink"]}">CONSOLE</text>
  <text x="230" y="68" font-family="{MONO}" font-size="14" fill="{t["muted"]}">toolbox · every switch is armed</text>
  {"".join(rows)}'''
    tools = "; ".join(f"{g.title()}: {', '.join(ts)}" for g, ts in TOOL_GROUPS)
    return svg(1200, height, "Console", f"Toolbox as a switch console. {tools}.", body)


BUTTONS = {
    "email": ("CH 1", "EMAIL", "nigmucode@gmail.com"),
    "x": ("CH 2", "X", "@nigmu7161"),
    "linkedin": ("CH 3", "LINKEDIN", "nigamananda-behera"),
}


def button(slug: str) -> str:
    t = THEMES["dark"]
    channel, title, handle = BUTTONS[slug]
    body = f'''  <rect width="360" height="110" rx="16" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>
  {_lamp(36, 55, t["green"], live=True)}
  <text x="56" y="42" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{t["amber"]}">{channel}</text>
  <text x="56" y="68" font-family="{SANS}" font-size="22" font-weight="800" fill="{t["ink"]}">{title}</text>
  <text x="56" y="90" font-family="{MONO}" font-size="13" fill="{t["cyan"]}">{esc(handle)}</text>'''
    return svg(360, 110, f"{title} channel", f"Comm channel {channel}: {title}, {handle}.", body, MOTION)


def footer(t: dict) -> str:
    odia = load_glyph("odia-bold")
    tf, w, _ = fitted(odia, 0, 0, height=48)
    body = f'''  <rect width="1200" height="150" fill="{t["bg"]}"/>
  <rect x="28" y="24" width="1144" height="102" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>
  {_lamp(64, 74, t["green"], live=True)}
  <text x="86" y="70" font-family="{MONO}" font-size="20" font-weight="700" letter-spacing="2" fill="{t["ink"]}">END OF SHIFT</text>
  <text x="86" y="98" font-family="{MONO}" font-size="14" fill="{t["muted"]}">ALL LAMPS NOMINAL</text>
  <g transform="translate({1040 - w:.0f} 40)"><g transform="{tf}">{glyph_paths(odia, f'fill="{t["amber"]}"')}</g></g>'''
    return svg(1200, 150, "End of shift", "End of shift. All lamps nominal. The Odia greeting namaskar.", body, MOTION)


def build() -> dict[str, str]:
    files: dict[str, str] = {}
    for theme, palette in THEMES.items():
        files[f"assets/hero-{theme}.svg"] = hero(palette)
        files[f"assets/fuel-{theme}.svg"] = fuel(palette)
        files[f"assets/console-{theme}.svg"] = console(palette)
        files[f"assets/footer-{theme}.svg"] = footer(palette)
        for index, (slug, name, _) in enumerate(PROJECTS):
            files[f"assets/missions/{slug}-{theme}.svg"] = card(palette, slug, name, index)
    for slug in BUTTONS:
        files[f"assets/buttons/{slug}.svg"] = button(slug)
    return files
