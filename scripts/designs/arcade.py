"""Arcade cabinet: a pixel marquee, a CRT, and a high-score table."""

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

_RAW = """
A 01110 10001 10001 11111 10001 10001 10001
B 11110 10001 10001 11110 10001 10001 11110
C 01111 10000 10000 10000 10000 10000 01111
D 11110 10001 10001 10001 10001 10001 11110
E 11111 10000 10000 11110 10000 10000 11111
F 11111 10000 10000 11110 10000 10000 10000
G 01111 10000 10000 10011 10001 10001 01111
H 10001 10001 10001 11111 10001 10001 10001
I 01110 00100 00100 00100 00100 00100 01110
J 00001 00001 00001 00001 10001 10001 01110
K 10001 10010 10100 11000 10100 10010 10001
L 10000 10000 10000 10000 10000 10000 11111
M 10001 11011 10101 10101 10001 10001 10001
N 10001 11001 10101 10011 10001 10001 10001
O 01110 10001 10001 10001 10001 10001 01110
P 11110 10001 10001 11110 10000 10000 10000
Q 01110 10001 10001 10001 10101 10010 01101
R 11110 10001 10001 11110 10100 10010 10001
S 01111 10000 10000 01110 00001 00001 11110
T 11111 00100 00100 00100 00100 00100 00100
U 10001 10001 10001 10001 10001 10001 01110
V 10001 10001 10001 10001 10001 01010 00100
W 10001 10001 10001 10101 10101 11011 10001
X 10001 10001 01010 00100 01010 10001 10001
Y 10001 10001 01010 00100 00100 00100 00100
Z 11111 00001 00010 00100 01000 10000 11111
0 01110 10001 10011 10101 11001 10001 01110
1 00100 01100 00100 00100 00100 00100 01110
2 01110 10001 00001 00110 01000 10000 11111
3 11110 00001 00001 01110 00001 00001 11110
4 00010 00110 01010 10010 11111 00010 00010
5 11111 10000 11110 00001 00001 10001 01110
6 00110 01000 10000 11110 10001 10001 01110
7 11111 00001 00010 00100 01000 01000 01000
8 01110 10001 10001 01110 10001 10001 01110
9 01110 10001 10001 01111 00001 00010 01100
- 00000 00000 00000 11111 00000 00000 00000
. 00000 00000 00000 00000 00000 01100 01100
"""

FONT = {}
for _line in _RAW.strip().splitlines():
    _ch, *_bits = _line.split()
    FONT[_ch] = _bits


def _advance(ch: str, scale: float) -> float:
    return (4 if ch == " " else 6) * scale


def pixel_text(text: str, x: float, y: float, scale: float, fill: str) -> tuple[str, float]:
    rects = []
    cx = x
    for ch in text:
        if ch == " ":
            cx += _advance(ch, scale)
            continue
        rows = FONT.get(ch.upper())
        if not rows:
            cx += _advance(" ", scale)
            continue
        for r, bits in enumerate(rows):
            for c, bit in enumerate(bits):
                if bit == "1":
                    rects.append(
                        f'<rect x="{cx + c * scale:.1f}" y="{y + r * scale:.1f}" '
                        f'width="{scale:.1f}" height="{scale:.1f}" fill="{fill}"/>'
                    )
        cx += _advance(ch, scale)
    return "".join(rects), cx - x


def _shift(drawn: str, dx: float) -> str:
    import re

    def repl(match: re.Match[str]) -> str:
        return f'x="{float(match.group(1)) + dx:.1f}"'

    return re.sub(r'x="([\d.]+)"', repl, drawn)


THEMES = {
    "dark": {
        "cabinet": "#160a18",
        "stripe": "#ff2d3a",
        "marquee": "#ffd000",
        "marquee_ink": "#1a0a00",
        "crt": "#05060a",
        "screen": "#071526",
        "ink": "#e9fff4",
        "muted": "#8aa0b4",
        "a": "#ffe14a",
        "b": "#ff4d8d",
        "c": "#7ad7ff",
        "d": "#c6ff4a",
        "wood": "#c47a3a",
        "bars": ["#ff4d8d", "#ffe14a", "#c6ff4a", "#7ad7ff", "#c77dff", "#ff8c42", "#7af0c0", "#ffd23f", "#9aa8b4"],
    },
    "light": {
        "cabinet": "#fff7ec",
        "stripe": "#e10600",
        "marquee": "#ffd000",
        "marquee_ink": "#1a0a00",
        "crt": "#1a1a1a",
        "screen": "#e5fbff",
        "ink": "#102033",
        "muted": "#5c6b7a",
        "a": "#b45309",
        "b": "#c2185b",
        "c": "#0369a1",
        "d": "#3f6212",
        "wood": "#c47a3a",
        "bars": ["#c2185b", "#b45309", "#3f6212", "#0369a1", "#7b2ff7", "#c2410c", "#0f766e", "#a16207", "#64748b"],
    },
}

BLINK = """
    .blink { animation: blink 2.8s ease-in-out infinite; }
    @keyframes blink { 50% { opacity: 0.25; } }
    .bob { animation: bob 3.4s ease-in-out infinite; }
    @keyframes bob { 50% { transform: translateY(-7px); } }"""


def _bulbs(x0: float, x1: float, y: float, colors: list[str], step: float = 36) -> str:
    out = []
    x = x0
    i = 0
    while x <= x1 + 0.1:
        color = colors[i % len(colors)]
        glow = ' class="blink"' if i % 4 == 0 else ""
        out.append(f'<circle{glow} cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{color}" opacity="0.35"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{color}" stroke="#1a0a00" stroke-width="1.5"/>')
        x += step
        i += 1
    return "".join(out)


def _character(x: float, y: float, t: dict) -> str:
    s = t["a"]
    hair, skin, shirt = t["marquee_ink"], "#ffd0a8", t["b"]
    return f'''<g transform="translate({x} {y})">
    <rect x="18" y="78" width="150" height="10" fill="{t["d"]}"/>
    <rect x="34" y="8" width="40" height="12" fill="{hair}"/>
    <rect x="30" y="18" width="48" height="36" fill="{skin}"/>
    <rect x="40" y="30" width="8" height="8" fill="{hair}"/><rect x="60" y="30" width="8" height="8" fill="{hair}"/>
    <rect x="44" y="44" width="20" height="4" fill="{t["b"]}"/>
    <rect x="26" y="54" width="56" height="36" fill="{shirt}"/>
    <rect x="30" y="90" width="16" height="28" fill="{t["c"]}"/><rect x="62" y="90" width="16" height="28" fill="{t["c"]}"/>
    <rect x="96" y="20" width="8" height="52" fill="{t["wood"]}"/>
    <rect x="86" y="62" width="40" height="30" rx="8" fill="{t["wood"]}" stroke="{hair}" stroke-width="3"/>
    <circle cx="106" cy="76" r="6" fill="{t["screen"]}"/>
    <rect x="98" y="28" width="2" height="40" fill="{s}"/><rect x="104" y="28" width="2" height="40" fill="{s}"/>
  </g>'''


def hero(t: dict) -> str:
    title, title_w = pixel_text("NIGAM", 0, 52, 10, t["marquee_ink"])
    title = _shift(title, (1200 - title_w) / 2)
    one, _ = pixel_text("1UP", 48, 62, 4, t["marquee_ink"])
    free, _ = pixel_text("FREE", 1048, 62, 4, t["marquee_ink"])
    lines = []
    y = 196
    for text, scale, color in (
        ("FULL STACK", 6, t["a"]),
        ("ANDROID", 6, t["b"]),
        ("MACHINE LEARNING", 5, t["c"]),
    ):
        drawn, _ = pixel_text(text, 78, y, scale, color)
        lines.append(drawn)
        y += scale * 7 + 22
    start, _ = pixel_text("PRESS START", 78, 430, 4, t["d"])
    bonus, _ = pixel_text("BONUS  UKULELE", 78, 392, 3, t["muted"])
    body = f'''  <rect width="1200" height="520" fill="{t["cabinet"]}"/>
  <rect width="22" height="520" fill="{t["stripe"]}"/>
  <rect x="1178" width="22" height="520" fill="{t["stripe"]}"/>
  <rect x="40" y="18" width="1120" height="124" fill="{t["marquee"]}" stroke="#1a0a00" stroke-width="4"/>
  {_bulbs(64, 1136, 32, [t["stripe"], t["c"], t["d"], t["b"]])}
  {one}{free}{title}
  <rect x="48" y="158" width="1104" height="336" fill="{t["crt"]}"/>
  <rect x="64" y="172" width="1072" height="308" fill="{t["screen"]}"/>
  <rect x="64" y="172" width="1072" height="308" fill="url(#scan)"/>
  {"".join(lines)}
  {bonus}
  <g class="blink">{start}</g>
  {_character(820, 210, t)}
  <g class="bob"><circle cx="760" cy="250" r="16" fill="{t["a"]}" stroke="{t["ink"]}" stroke-width="3"/>
    <text x="760" y="256" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="{t["marquee_ink"]}">C</text></g>'''
    defs = '''    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.1" fill="#000" opacity="0.28"/>
    </pattern>'''
    return svg(
        1200, 520, "Nigam arcade",
        "Arcade cabinet. The marquee reads NIGAM. The screen reads full stack, Android, machine learning, bonus ukulele, press start.",
        body, BLINK, defs,
    )


def _sprite(slug: str, t: dict) -> str:
    ink = t["ink"]
    if slug == "trackmyspend":
        return (
            f'<rect x="8" y="8" width="70" height="118" rx="10" fill="{t["screen"]}" stroke="{ink}" stroke-width="5"/>'
            f'<rect x="18" y="24" width="50" height="14" rx="4" fill="{t["d"]}"/>'
            f'<rect x="18" y="46" width="50" height="14" rx="4" fill="{t["c"]}"/>'
            f'<rect x="18" y="68" width="50" height="14" rx="4" fill="{t["b"]}"/>'
            f'<circle cx="108" cy="108" r="22" fill="{t["a"]}" stroke="{ink}" stroke-width="4"/>'
            f'<circle cx="132" cy="86" r="18" fill="{t["a"]}" stroke="{ink}" stroke-width="4"/>'
        )
    if slug == "resume-ledger":
        return (
            f'<rect x="18" y="16" width="96" height="120" fill="{t["screen"]}" stroke="{ink}" stroke-width="5"/>'
            f'<path d="M78 16 h28 v28" fill="{t["a"]}" stroke="{ink}" stroke-width="5"/>'
            + "".join(f'<rect x="32" y="{48 + i * 16}" width="{70 - (i % 2) * 20}" height="8" fill="{t["c"]}"/>' for i in range(4))
            + f'<circle cx="124" cy="112" r="22" fill="{t["d"]}" stroke="{ink}" stroke-width="4"/>'
            f'<path d="M112 112 l8 8 16 -18" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>'
        )
    if slug == "odia-stt":
        return (
            f'<rect x="48" y="8" width="44" height="78" rx="22" fill="{t["muted"]}" stroke="{ink}" stroke-width="5"/>'
            f'<path d="M40 70 q30 48 60 0" fill="none" stroke="{ink}" stroke-width="5"/>'
            f'<rect x="64" y="112" width="12" height="22" fill="{ink}"/>'
            f'<path d="M16 40 q-16 16 0 32 M124 40 q16 16 0 32" fill="none" stroke="{t["b"]}" stroke-width="5" stroke-linecap="round"/>'
        )
    if slug == "clean-tv":
        colors = [t["b"], t["a"], t["d"], t["c"], "#c77dff", t["stripe"]]
        tiles = "".join(
            f'<rect x="{22 + (i % 3) * 34}" y="{22 + (i // 3) * 30}" width="28" height="24" fill="{colors[i]}" stroke="{ink}" stroke-width="3"/>'
            for i in range(6)
        )
        return (
            f'<rect x="8" y="8" width="124" height="96" fill="{t["screen"]}" stroke="{ink}" stroke-width="5"/>{tiles}'
            f'<path d="M40 104 v22 M100 104 v22 M28 126 h84" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>'
        )
    if slug == "bg-download":
        return (
            f'<rect x="16" y="20" width="112" height="88" fill="{t["c"]}" stroke="{ink}" stroke-width="5"/>'
            f'<circle cx="96" cy="48" r="14" fill="{t["a"]}"/>'
            f'<path d="M16 108 l36 -36 24 24 16 -14 36 26" fill="{t["d"]}" stroke="{ink}" stroke-width="4"/>'
        )
    boxes = "".join(
        f'<rect x="{18 + (i % 2) * 52}" y="{70 - (i // 2) * 40}" width="48" height="36" fill="{t["a"] if i % 2 else t["wood"]}" stroke="{ink}" stroke-width="4"/>'
        for i in range(4)
    )
    return boxes + f'<rect x="44" y="18" width="48" height="36" fill="{t["d"]}" stroke="{ink}" stroke-width="4"/>'


def game(t: dict, slug: str, name: str, index: int) -> str:
    stage, _ = pixel_text(f"STAGE {index + 1}", 200, 36, 4, t["a"])
    size = 26 if len(name) < 16 else 20
    body = f'''  <rect width="560" height="340" fill="{t["cabinet"]}"/>
  <rect width="14" height="340" fill="{t["stripe"]}"/>
  <rect x="18" y="16" width="526" height="308" fill="{t["crt"]}"/>
  <rect x="30" y="28" width="502" height="284" fill="{t["screen"]}"/>
  <rect x="30" y="28" width="502" height="284" fill="url(#scan)"/>
  <g transform="translate(44 78)">{_sprite(slug, t)}</g>
  {stage}
  <text x="200" y="108" font-family="{SANS}" font-size="{size}" font-weight="800" fill="{t["ink"]}">{esc(name)}</text>
  <text x="200" y="146" font-family="{MONO}" font-size="16" fill="{t["c"]}">{esc(TAGLINES[slug])}</text>
  <g class="blink">{pixel_text("SELECT", 200, 250, 3, t["d"])[0]}</g>'''
    defs = '''    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.1" fill="#000" opacity="0.28"/>
    </pattern>'''
    return svg(560, 340, f"{name} stage", f"Arcade stage {index + 1}: {name}. {TAGLINES[slug]}.", body, BLINK, defs)


def scores(t: dict) -> str:
    rows = language_rows()
    lines = []
    for i, (name, pct) in enumerate(rows):
        y = 108 + i * 46
        blocks = max(2, round(24 * meter(pct)))
        color = t["bars"][i]
        label = name.upper().replace(" NOTEBOOK", "")
        drawn, _ = pixel_text(label, 48, y, 3, t["ink"])
        cells = "".join(
            f'<rect x="{300 + n * 22}" y="{y - 2}" width="18" height="24" fill="{color if n < blocks else t["crt"]}"/>'
            for n in range(24)
        )
        pct_draw, _ = pixel_text(f"{pct:.1f}", 860, y, 3, color)
        lines.append(drawn + cells + pct_draw)
    height = 108 + len(rows) * 46 + 56
    header, _ = pixel_text("HIGH SCORES", 48, 40, 5, t["a"])
    note, _ = pixel_text("LOG METER  TRUE PERCENTS", 520, 48, 2, t["muted"])
    body = f'''  <rect width="1200" height="{height}" fill="{t["cabinet"]}"/>
  <rect x="24" y="24" width="1152" height="{height - 48}" fill="{t["screen"]}" stroke="{t["crt"]}" stroke-width="8"/>
  {header}{note}{"".join(lines)}'''
    summary = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return svg(
        1200, height, "High scores",
        f"Language mix as an arcade high-score table. The blocks use a compressed meter; the numbers are true shares. {summary}.",
        body, "",
    )


def controls(t: dict) -> str:
    rows = []
    y = 118
    for g, (group, tools) in enumerate(TOOL_GROUPS):
        label, _ = pixel_text(group, 36, y + 10, 2, t["a"])
        buttons = []
        for i, tool in enumerate(tools):
            x = 250 + i * 150
            color = t["bars"][(g + i) % len(t["bars"])]
            buttons.append(
                f'<circle cx="{x}" cy="{y + 8}" r="24" fill="{color}" stroke="{t["marquee_ink"]}" stroke-width="4"/>'
                f'<circle cx="{x - 6}" cy="{y}" r="7" fill="#ffffff" opacity="0.35"/>'
                f'<text x="{x}" y="{y + 52}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="{t["ink"]}">{esc(tool)}</text>'
            )
        rows.append(label + "".join(buttons))
        y += 108
    height = y + 24
    header, _ = pixel_text("BUTTON MAP", 36, 48, 5, t["a"])
    body = f'''  <rect width="1200" height="{height}" fill="{t["cabinet"]}"/>
  <rect x="24" y="24" width="1152" height="{height - 48}" fill="{t["screen"]}" stroke="{t["crt"]}" stroke-width="8"/>
  {header}{"".join(rows)}'''
    tools = "; ".join(f"{g.title()}: {', '.join(ts)}" for g, ts in TOOL_GROUPS)
    return svg(1200, height, "Button map", f"Toolbox as arcade buttons. {tools}.", body)


BUTTONS = {
    "email": ("P1", "EMAIL", "nigmucode@gmail.com", "#ff2d3a"),
    "x": ("P2", "X", "@nigmu7161", "#7ad7ff"),
    "linkedin": ("P3", "LINKEDIN", "nigamananda-behera", "#ffd000"),
}


def button(slug: str) -> str:
    code, title, handle, color = BUTTONS[slug]
    ink = "#1a0a00" if slug == "linkedin" else "#fff7ec"
    body = f'''  <rect width="360" height="110" fill="#160a18"/>
  <circle cx="62" cy="55" r="34" fill="{color}" stroke="#1a0a00" stroke-width="4"/>
  <circle cx="50" cy="44" r="8" fill="#ffffff" opacity="0.4"/>
  <text x="62" y="60" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="{ink}">{code}</text>
  <text x="114" y="50" font-family="{SANS}" font-size="22" font-weight="800" fill="#fff7ec">{title}</text>
  <text x="114" y="76" font-family="{MONO}" font-size="14" fill="{color}">{esc(handle)}</text>'''
    return svg(360, 110, f"{title} button", f"Arcade button {code}: {title}, {handle}.", body)


def footer(t: dict) -> str:
    odia = load_glyph("odia-bold")
    tf, w, h = fitted(odia, 0, 0, height=42)
    thanks, _ = pixel_text("THANKS FOR PLAYING", 80, 36, 4, t["a"])
    body = f'''  <rect width="1200" height="150" fill="{t["cabinet"]}"/>
  <rect width="22" height="150" fill="{t["stripe"]}"/><rect x="1178" width="22" height="150" fill="{t["stripe"]}"/>
  {thanks}
  <g transform="translate({980 - w / 2:.0f} {36})"><g transform="{tf}">{glyph_paths(odia, f'fill="{t["d"]}"')}</g></g>
  {pixel_text("NAMASKAR", 900, 100, 2, t["muted"])[0]}'''
    return svg(1200, 150, "Thanks for playing", "Thanks for playing, and the Odia greeting namaskar.", body, "", )


def build() -> dict[str, str]:
    files: dict[str, str] = {}
    for theme, t in THEMES.items():
        files[f"assets/hero-{theme}.svg"] = hero(t)
        files[f"assets/scores-{theme}.svg"] = scores(t)
        files[f"assets/controls-{theme}.svg"] = controls(t)
        files[f"assets/footer-{theme}.svg"] = footer(t)
        for index, (slug, name, _) in enumerate(PROJECTS):
            files[f"assets/games/{slug}-{theme}.svg"] = game(t, slug, name, index)
    for slug in BUTTONS:
        files[f"assets/buttons/{slug}.svg"] = button(slug)
    return files
