"""Window garden: a greenhouse, specimen plates, and seed packets."""

from __future__ import annotations

from .common import (
    PROJECTS,
    SERIF,
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
    "light": {
        "glass": "#e5f6ea",
        "frame": "#f7f1e6",
        "muntin": "#6b4428",
        "ink": "#1c2b22",
        "muted": "#5e6b58",
        "leaf": "#2f7d4a",
        "soil": "#8a5a3a",
        "pot": "#c45c26",
        "paper": "#fbf6ea",
    },
    "dark": {
        "glass": "#0e2a22",
        "frame": "#10241c",
        "muntin": "#e6d3b0",
        "ink": "#f3efe2",
        "muted": "#b7c7b4",
        "leaf": "#7dcc6a",
        "soil": "#c4a574",
        "pot": "#e07a45",
        "paper": "#fbf6ea",
    },
}

PLATE = {
    "trackmyspend": "#c45c26",
    "resume-ledger": "#1d4e89",
    "odia-stt": "#b4235b",
    "clean-tv": "#0f766e",
    "bg-download": "#2f7d4a",
    "warehouse": "#d97706",
}

MOTION = """
    .sway { animation: sway 8s ease-in-out infinite; transform-box: fill-box; transform-origin: center bottom; }
    @keyframes sway { 50% { transform: rotate(1.8deg); } }"""


def flower(cx: float, cy: float, color: str, leaf: str, pot: str) -> str:
    petals = "".join(
        f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="14" ry="22" fill="{color}" stroke="#1c2b22" stroke-width="2"/>'
        for dx, dy in ((0, -20), (18, -6), (12, 16), (-12, 16), (-18, -6))
    )
    return (
        f'<rect x="{cx - 4}" y="{cy}" width="8" height="70" fill="{leaf}"/>'
        f'<ellipse cx="{cx - 18}" cy="{cy + 36}" rx="16" ry="8" fill="{leaf}" transform="rotate(-30 {cx - 18} {cy + 36})"/>'
        f'<ellipse cx="{cx + 18}" cy="{cy + 44}" rx="16" ry="8" fill="{leaf}" transform="rotate(30 {cx + 18} {cy + 44})"/>'
        f"{petals}"
        f'<circle cx="{cx}" cy="{cy}" r="8" fill="#f0b429" stroke="#1c2b22" stroke-width="2"/>'
        f'<path d="M{cx - 22} {cy + 70} h44 l-6 22 h-32 z" fill="{pot}" stroke="#1c2b22" stroke-width="2"/>'
    )


def hero(t: dict) -> str:
    muntin = t["muntin"]
    bars = (
        f'<rect x="28" y="28" width="1144" height="420" fill="none" stroke="{muntin}" stroke-width="14"/>'
        f'<path d="M600 36 V440 M36 268 H1164" stroke="{muntin}" stroke-width="10"/>'
    )
    blooms = []
    colors = ["#e23d5a", "#f0b429", "#7b2ff7", "#ff8c42", "#3ec6ff"]
    for i, x in enumerate((160, 360, 840, 1040)):
        klass = ' class="sway"' if i % 2 == 0 else ""
        blooms.append(f'<g{klass}>{flower(x, 332, colors[i], t["leaf"], t["pot"])}</g>')
    odia = load_glyph("odia-bold")
    tf, w, _ = fitted(odia, 0, 0, height=36)
    body = f'''  <rect width="1200" height="480" fill="{t["frame"]}"/>
  <rect x="36" y="36" width="1128" height="404" fill="{t["glass"]}"/>
  {bars}
  <text x="600" y="128" text-anchor="middle" font-family="{SERIF}" font-size="68" font-weight="700" fill="{t["ink"]}">Nigam</text>
  <text x="600" y="164" text-anchor="middle" font-family="{SERIF}" font-size="18" font-style="italic" fill="{t["muted"]}">full stack · android · machine learning</text>
  <text x="600" y="190" text-anchor="middle" font-family="{SERIF}" font-size="16" font-style="italic" fill="{t["muted"]}">a ukulele lives by the potting bench</text>
  <g transform="translate({600 - w / 2:.0f} 214)"><g transform="{tf}">{glyph_paths(odia, f'fill="{t["leaf"]}"')}</g></g>
  {"".join(blooms)}'''
    return svg(
        1200, 480, "Nigam's glasshouse",
        "A greenhouse window. Nigam, the Odia greeting namaskar, full stack, Android and machine learning. A ukulele lives by the potting bench.",
        body, MOTION,
    )


def drawing(slug: str) -> str:
    ink = "#1c2b22"
    leaf = "#2f7d4a"
    if slug == "trackmyspend":
        coins = "".join(
            f'<circle cx="{x}" cy="{y}" r="16" fill="#f0b429" stroke="{ink}" stroke-width="3"/>'
            for x, y in ((0, -30), (-28, -8), (28, -4), (-12, 24), (18, 28))
        )
        return (
            f'<path d="M0 70 C-8 20 8 -10 0 -40" fill="none" stroke="{ink}" stroke-width="4"/>'
            f"{coins}"
            f'<path d="M-36 78 h72 l-8 28 h-56 z" fill="#c45c26" stroke="{ink}" stroke-width="3"/>'
        )
    if slug == "resume-ledger":
        leaves = "".join(
            f'<rect x="{-8 if i % 2 else -70}" y="{-60 + i * 28}" width="78" height="22" rx="4" fill="#fffaf0" stroke="{ink}" stroke-width="2" transform="rotate({-18 if i % 2 else 18})"/>'
            for i in range(5)
        )
        return f'<path d="M0 90 V-70" stroke="{leaf}" stroke-width="5"/>{leaves}'
    if slug == "odia-stt":
        bells = "".join(
            f'<path d="M{x} {y} q18 -28 36 0 q-18 10 -36 0z" fill="#b4235b" stroke="{ink}" stroke-width="2"/>'
            for x, y in ((-70, -10), (-20, -40), (30, -8))
        )
        return (
            f'<path d="M-80 60 C-20 60 0 0 40 -50" fill="none" stroke="{leaf}" stroke-width="5"/>'
            f"{bells}"
            f'<path d="M70 -20 q16 10 0 24 M88 -28 q20 14 0 30" fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>'
        )
    if slug == "clean-tv":
        colors = ["#e23d5a", "#f0b429", "#2f7d4a", "#1d4e89", "#7b2ff7", "#ff8c42"]
        tiles = "".join(
            f'<rect x="{-46 + (i % 3) * 32}" y="{-36 + (i // 3) * 28}" width="26" height="22" rx="4" fill="{colors[i]}" stroke="{ink}" stroke-width="2"/>'
            for i in range(6)
        )
        return f'<rect x="-70" y="-8" width="140" height="28" fill="#c45c26" stroke="{ink}" stroke-width="3"/>{tiles}'
    if slug == "bg-download":
        frames = "".join(
            f'<rect x="{x}" y="{y}" width="36" height="28" fill="#dff3ff" stroke="{ink}" stroke-width="2"/>'
            f'<path d="M{x} {y + 28} l12 -14 8 8 6 -6 10 12z" fill="#7dcc6a"/>'
            for x, y in ((-50, -20), (-8, -46), (34, -16))
        )
        return f'<path d="M0 -70 V70" stroke="{leaf}" stroke-width="4"/>{frames}'
    tiers = "".join(
        f'<ellipse cx="0" cy="{20 - i * 28}" rx="{48 - i * 10}" ry="16" fill="{leaf}" stroke="{ink}" stroke-width="2"/>'
        for i in range(3)
    )
    return f'<rect x="-40" y="36" width="80" height="26" fill="#c45c26" stroke="{ink}" stroke-width="3"/>{tiers}'


def plate(slug: str, name: str, index: int) -> str:
    accent = PLATE[slug]
    size = 28 if len(name) < 16 else 20
    body = f'''  <rect width="560" height="420" fill="#fbf6ea" stroke="#1c2b22" stroke-width="4"/>
  <rect x="16" y="16" width="528" height="388" fill="none" stroke="{accent}" stroke-width="3"/>
  <rect x="16" y="16" width="528" height="14" fill="{accent}"/>
  <g class="sway" transform="translate(280 200)">{drawing(slug)}</g>
  <text x="280" y="330" text-anchor="middle" font-family="{SERIF}" font-size="{size}" font-weight="700" fill="#1c2b22">{esc(name)}</text>
  <text x="280" y="362" text-anchor="middle" font-family="{SERIF}" font-size="18" font-style="italic" fill="{accent}">{esc(TAGLINES[slug])}</text>
  <text x="280" y="392" text-anchor="middle" font-family="{SERIF}" font-size="13" letter-spacing="2" fill="#5e6b58">PLATE {index + 1:02d}</text>'''
    return svg(560, 420, f"{name} plate", f"Specimen plate {index + 1} for {name}: {TAGLINES[slug]}.", body, MOTION)


def growth(t: dict) -> str:
    rows = language_rows()
    n = len(rows)
    gap = 1080 / n
    stems = []
    colors = ["#e23d5a", "#f0b429", "#7b2ff7", "#2f7d4a", "#ff8c42", "#1d4e89", "#0f766e", "#d97706", "#94a3b8"]
    for i, (name, pct) in enumerate(rows):
        x = 60 + gap * i + gap / 2
        h = 30 + 180 * meter(pct)
        base = 300
        parts = name.split(" ", 1)
        stems.append(
            f'<rect x="{x - 4:.0f}" y="{base - h:.0f}" width="8" height="{h:.0f}" fill="{t["leaf"]}"/>'
            f'<circle cx="{x:.0f}" cy="{base - h:.0f}" r="16" fill="{colors[i]}" stroke="{t["ink"]}" stroke-width="2"/>'
            f'<text x="{x:.0f}" y="330" text-anchor="middle" font-family="{SERIF}" font-size="14" font-weight="700" fill="{t["ink"]}">{pct:.1f}%</text>'
            f'<text x="{x:.0f}" y="352" text-anchor="middle" font-family="{SERIF}" font-size="13" fill="{t["ink"]}">{esc(parts[0])}</text>'
            + (f'<text x="{x:.0f}" y="370" text-anchor="middle" font-family="{SERIF}" font-size="13" fill="{t["ink"]}">{esc(parts[1])}</text>' if len(parts) > 1 else "")
        )
    body = f'''  <rect width="1200" height="420" fill="{t["glass"]}"/>
  <rect x="20" y="20" width="1160" height="380" fill="none" stroke="{t["muntin"]}" stroke-width="8"/>
  <text x="48" y="64" font-family="{SERIF}" font-size="32" font-weight="700" fill="{t["ink"]}">Growth</text>
  <text x="190" y="64" font-family="{SERIF}" font-size="15" font-style="italic" fill="{t["muted"]}">stem height is compressed · percents are the true share</text>
  <rect x="48" y="300" width="1104" height="16" fill="{t["soil"]}"/>
  {"".join(stems)}'''
    summary = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return svg(1200, 420, "Growth", f"Language mix as stems in a glasshouse bed. {summary}.", body)


def seeds(t: dict) -> str:
    rows = []
    y = 110
    colors = ["#2f7d4a", "#1d4e89", "#b4235b", "#d97706"]
    for i, (group, tools) in enumerate(TOOL_GROUPS):
        rows.append(
            f'<rect x="36" y="{y - 8}" width="1128" height="92" rx="12" fill="{t["soil"]}" opacity="0.25"/>'
            f'<text x="52" y="{y + 18}" font-family="{SERIF}" font-size="14" font-weight="700" letter-spacing="1" fill="{t["ink"]}">{esc(group)}</text>'
        )
        x = 200
        span = 940 / len(tools)
        for tool in tools:
            w = span - 14
            rows.append(
                f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="70" rx="6" fill="{t["paper"]}" stroke="{t["ink"]}" stroke-width="2"/>'
                f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="16" fill="{colors[i]}"/>'
                f'<text x="{x + w / 2:.0f}" y="{y + 48}" text-anchor="middle" font-family="{SERIF}" font-size="15" font-weight="700" fill="{t["ink"]}">{esc(tool)}</text>'
            )
            x += span
        y += 108
    height = y + 16
    body = f'''  <rect width="1200" height="{height}" fill="{t["glass"]}"/>
  <text x="40" y="52" font-family="{SERIF}" font-size="32" font-weight="700" fill="{t["ink"]}">Seed packets</text>
  {"".join(rows)}'''
    tools = "; ".join(f"{g.title()}: {', '.join(ts)}" for g, ts in TOOL_GROUPS)
    return svg(1200, height, "Seed packets", f"Toolbox as seed packets in trays. {tools}.", body)


BUTTONS = {
    "email": ("Email", "nigmucode@gmail.com", "#2f7d4a"),
    "x": ("X", "@nigmu7161", "#1d4e89"),
    "linkedin": ("LinkedIn", "nigamananda-behera", "#b4235b"),
}


def label(slug: str) -> str:
    title, handle, color = BUTTONS[slug]
    body = f'''  <rect width="360" height="110" fill="#fbf6ea" stroke="#1c2b22" stroke-width="3"/>
  <rect width="360" height="12" fill="{color}"/>
  <rect x="24" y="28" width="8" height="70" fill="{color}"/>
  <text x="48" y="58" font-family="{SERIF}" font-size="24" font-weight="700" fill="#1c2b22">{title}</text>
  <text x="48" y="86" font-family="{SERIF}" font-size="15" font-style="italic" fill="{color}">{esc(handle)}</text>'''
    return svg(360, 110, f"{title} label", f"Plant label: {title}, {handle}.", body)


def footer(t: dict) -> str:
    odia = load_glyph("odia-bold")
    tf, w, _ = fitted(odia, 0, 0, height=40)
    body = f'''  <rect width="1200" height="160" fill="{t["glass"]}"/>
  <rect x="20" y="16" width="1160" height="128" fill="none" stroke="{t["muntin"]}" stroke-width="8"/>
  <g class="sway">{flower(160, 40, "#e23d5a", t["leaf"], t["pot"])}</g>
  <g transform="translate({600 - w / 2:.0f} 48)"><g transform="{tf}">{glyph_paths(odia, f'fill="{t["leaf"]}"')}</g></g>
  <text x="600" y="120" text-anchor="middle" font-family="{SERIF}" font-size="16" font-style="italic" fill="{t["muted"]}">the glasshouse is always open</text>'''
    return svg(1200, 160, "Namaskar", "The glasshouse is always open. The Odia greeting namaskar.", body, MOTION)


def build() -> dict[str, str]:
    files: dict[str, str] = {}
    for theme, palette in THEMES.items():
        files[f"assets/hero-{theme}.svg"] = hero(palette)
        files[f"assets/growth-{theme}.svg"] = growth(palette)
        files[f"assets/seeds-{theme}.svg"] = seeds(palette)
        files[f"assets/footer-{theme}.svg"] = footer(palette)
    for index, (slug, name, _) in enumerate(PROJECTS):
        files[f"assets/plates/{slug}.svg"] = plate(slug, name, index)
    for slug in BUTTONS:
        files[f"assets/labels/{slug}.svg"] = label(slug)
    return files
