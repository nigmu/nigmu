"""Pattachitra: Odisha scroll painting, festival colours."""

from __future__ import annotations

from .common import PROJECTS, SERIF, TOOL_GROUPS, arc_band, esc, fitted, glyph_paths, language_rows, load_glyph, polar, svg

THEMES = {
    "light": {
        "paper": "#f6e3bd",
        "panel": "#fbefd4",
        "arch": "#f7d58c",
        "red": "#c8281e",
        "yellow": "#f0b323",
        "blue": "#14507a",
        "green": "#3f7d3a",
        "magenta": "#b8325e",
        "orange": "#e2711d",
        "ink": "#1d120c",
        "muted": "#6b4a2e",
        "white": "#fff8e6",
        "line": "#1d120c",
        "rule": "#1d120c",
    },
    "dark": {
        "paper": "#17112e",
        "panel": "#211941",
        "arch": "#2d2358",
        "red": "#ff5a4a",
        "yellow": "#ffc93c",
        "blue": "#4fb3d9",
        "green": "#7cc46a",
        "magenta": "#ff6f9f",
        "orange": "#ff9a3c",
        "ink": "#fdf1d6",
        "muted": "#cdb68f",
        "white": "#fff8e6",
        "line": "#0b0716",
        "rule": "#cdb68f",
    },
}

SWAY = """
    .breathe { animation: breathe 8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
    @keyframes breathe { 50% { transform: scale(1.035); } }
    .turn { animation: turn 90s linear infinite; transform-box: fill-box; transform-origin: center; }
    @keyframes turn { to { transform: rotate(360deg); } }"""


def petal(cx: float, cy: float, length: float, width: float, angle: float, fill: str, line: str, sw: float = 2.5) -> str:
    d = (
        f"M0 0 C{width / 2:.1f} {-length * 0.25:.1f} {width / 2:.1f} {-length * 0.7:.1f} 0 {-length:.1f} "
        f"C{-width / 2:.1f} {-length * 0.7:.1f} {-width / 2:.1f} {-length * 0.25:.1f} 0 0Z"
    )
    return f'<path d="{d}" transform="translate({cx:.1f} {cy:.1f}) rotate({angle:.1f})" fill="{fill}" stroke="{line}" stroke-width="{sw}" stroke-linejoin="round"/>'


def lotus(cx: float, cy: float, size: float, t: dict) -> str:
    parts = []
    for i, a in enumerate((-78, -52, -26, 26, 52, 78)):
        parts.append(petal(cx, cy, size * (0.8 if abs(a) > 60 else 0.95), size * 0.42, a, t["red"] if i % 2 else t["magenta"], t["line"], 2))
    parts.append(petal(cx, cy, size * 1.05, size * 0.46, 0, t["white"], t["line"], 2))
    parts.append(
        f'<path d="M{cx - size * 0.55:.1f} {cy:.1f} Q{cx:.1f} {cy + size * 0.42:.1f} {cx + size * 0.55:.1f} {cy:.1f}Z" fill="{t["green"]}" stroke="{t["line"]}" stroke-width="2"/>'
    )
    return "".join(parts)


def dots_line(x0: float, x1: float, y: float, step: float, r: float, colors: list[str]) -> str:
    out = []
    n = int((x1 - x0) / step)
    for i in range(n + 1):
        out.append(f'<circle cx="{x0 + i * step:.1f}" cy="{y:.1f}" r="{r}" fill="{colors[i % len(colors)]}"/>')
    return "".join(out)


def frame(w: float, h: float, t: dict, band: float = 22) -> str:
    """Red border band with white dots, an ink rule and a row of inward teeth."""
    teeth = []
    step = 24
    inner = band + 3
    depth = 12
    for x in range(int(inner), int(w - inner - step) + 1, step):
        c = t["yellow"] if (x // step) % 2 else t["green"]
        teeth.append(f'<path d="M{x} {inner} l{step / 2} {depth} l{step / 2} {-depth}Z" fill="{c}" stroke="{t["line"]}" stroke-width="1.5"/>')
        teeth.append(f'<path d="M{x} {h - inner} l{step / 2} {-depth} l{step / 2} {depth}Z" fill="{c}" stroke="{t["line"]}" stroke-width="1.5"/>')
    for y in range(int(inner), int(h - inner - step) + 1, step):
        c = t["yellow"] if (y // step) % 2 else t["green"]
        teeth.append(f'<path d="M{inner} {y} l{depth} {step / 2} l{-depth} {step / 2}Z" fill="{c}" stroke="{t["line"]}" stroke-width="1.5"/>')
        teeth.append(f'<path d="M{w - inner} {y} l{-depth} {step / 2} l{depth} {step / 2}Z" fill="{c}" stroke="{t["line"]}" stroke-width="1.5"/>')
    dots = (
        dots_line(14, w - 14, band / 2, 16, 3, [t["white"]])
        + dots_line(14, w - 14, h - band / 2, 16, 3, [t["white"]])
    )
    side = "".join(
        f'<circle cx="{band / 2}" cy="{y}" r="3" fill="{t["white"]}"/><circle cx="{w - band / 2}" cy="{y}" r="3" fill="{t["white"]}"/>'
        for y in range(30, int(h - 20), 16)
    )
    return (
        f'<path d="M0 0H{w}V{h}H0Z M{band} {band}V{h - band}H{w - band}V{band}Z" fill="{t["red"]}" fill-rule="evenodd"/>'
        f"{dots}{side}"
        f'<rect x="{band}" y="{band}" width="{w - 2 * band}" height="{h - 2 * band}" fill="none" stroke="{t["line"]}" stroke-width="3"/>'
        f'{"".join(teeth)}'
    )


def wheel(cx: float, cy: float, r: float, t: dict) -> str:
    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["red"]}" stroke="{t["line"]}" stroke-width="4"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r - 20}" fill="{t["arch"]}" stroke="{t["line"]}" stroke-width="3"/>',
    ]
    for i in range(36):
        x, y = polar(cx, cy, r - 10, i * 10)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="1.2"/>')
    for i in range(16):
        a = i * 22.5
        thick = i % 2 == 0
        width = 18 if thick else 7
        length = r - 20 - 34
        parts.append(
            f'<rect x="{cx - width / 2:.1f}" y="{cy - r + 20:.1f}" width="{width}" height="{length:.1f}" rx="{width / 2:.1f}" '
            f'fill="{t["yellow"] if thick else t["orange"]}" stroke="{t["line"]}" stroke-width="2.5" transform="rotate({a} {cx} {cy})"/>'
        )
        if thick:
            x, y = polar(cx, cy, r * 0.56, a)
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{t["blue"]}" stroke="{t["line"]}" stroke-width="2.5"/>')
            x, y = polar(cx, cy, r * 0.56, a)
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{t["white"]}"/>')
    for i in range(8):
        parts.append(petal(cx, cy, 44, 20, i * 45 + 22.5, t["white"], t["line"], 2))
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="{t["blue"]}" stroke="{t["line"]}" stroke-width="3"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{t["red"]}" stroke="{t["line"]}" stroke-width="2"/>')
    return "".join(parts)


def banner(t: dict) -> str:
    nigam = load_glyph("patta-nigam")
    odia = load_glyph("odia-bold")
    tf_n, _, nh = fitted(nigam, 520, 74, width=400)
    tf_o, ow, _ = fitted(odia, 526, 74 + nh + 26, height=58)
    divider_y = 74 + nh + 26 + 58 + 40
    corners = "".join(
        f'<g transform="translate({x} {y}) rotate({r})">{lotus(0, 0, 26, t)}</g>'
        for x, y, r in ((74, 92, 135), (1126, 92, -135), (74, 368, 45), (1126, 368, -45))
    )
    body = f'''  <rect width="1200" height="460" fill="{t["paper"]}"/>
  {frame(1200, 460, t)}
  {corners}
  <g class="turn">{wheel(290, 230, 162, t)}</g>
  <g transform="{tf_n}">{glyph_paths(nigam, f'fill="{t["ink"]}"')}</g>
  <g transform="{tf_o}">{glyph_paths(odia, f'fill="{t["red"]}"')}</g>
  <line x1="526" y1="{divider_y}" x2="760" y2="{divider_y}" stroke="{t["rule"]}" stroke-width="2"/>
  <line x1="840" y1="{divider_y}" x2="1090" y2="{divider_y}" stroke="{t["rule"]}" stroke-width="2"/>
  {dots_line(540, 750, divider_y + 10, 14, 2.5, [t["red"], t["yellow"]])}
  {dots_line(850, 1080, divider_y + 10, 14, 2.5, [t["red"], t["yellow"]])}
  <g transform="translate(800 {divider_y + 12})">{lotus(0, 0, 30, t)}</g>
  <text x="528" y="{divider_y + 52}" font-family="{SERIF}" font-size="23" font-style="italic" fill="{t["muted"]}">full stack developer · android · machine learning</text>'''
    return svg(
        1200, 460, "Nigam",
        "A Pattachitra-style painting: a turning Konark sun-temple wheel, lotus corners, the name Nigam "
        "and the Odia greeting namaskar. Full stack developer, Android, machine learning.",
        body, SWAY,
    )


def motif_kalasha(t: dict) -> str:
    leaves = "".join(petal(0, -44, 54, 22, a, t["green"], t["line"], 2.5) for a in (-60, -30, 0, 30, 60))
    coins = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="18" ry="7" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="2.5"/>'
        for x, y in ((-84, 98), (-64, 88), (-84, 80), (84, 98), (64, 90))
    )
    return f'''{leaves}
    <circle cx="0" cy="-70" r="22" fill="#8c5a2b" stroke="{t["line"]}" stroke-width="3"/>
    <ellipse cx="0" cy="40" rx="72" ry="62" fill="{t["red"]}" stroke="{t["line"]}" stroke-width="3.5"/>
    <rect x="-30" y="-46" width="60" height="30" rx="6" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="3"/>
    <ellipse cx="0" cy="-16" rx="40" ry="10" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="3"/>
    <path d="M-70 36 Q0 62 70 36" fill="none" stroke="{t["white"]}" stroke-width="6"/>
    {dots_line(-56, 56, 52, 14, 3.5, [t["white"]])}
    <path d="M-40 82 Q0 98 40 82" fill="none" stroke="{t["yellow"]}" stroke-width="4"/>
    {coins}'''


def motif_palmleaf(t: dict) -> str:
    leaves = []
    for i in range(4):
        y = -60 + i * 34
        x = -112 + (i % 2) * 8
        script = " ".join(
            f"M{x + 22 + k * 22} {y + 15} q5 -8 10 0 t10 0" for k in range(8)
        )
        leaves.append(
            f'<rect x="{x}" y="{y}" width="224" height="28" rx="14" fill="#e3bd6c" stroke="{t["line"]}" stroke-width="2.5"/>'
            f'<path d="{script}" fill="none" stroke="#5a3a1a" stroke-width="2"/>'
        )
    return f'''<rect x="-122" y="-86" width="244" height="24" rx="8" fill="#8c5a2b" stroke="{t["line"]}" stroke-width="3"/>
    {"".join(leaves)}
    <rect x="-122" y="78" width="244" height="24" rx="8" fill="#8c5a2b" stroke="{t["line"]}" stroke-width="3"/>
    <circle cx="-60" cy="8" r="6" fill="{t["line"]}"/><circle cx="60" cy="8" r="6" fill="{t["line"]}"/>
    <path d="M-60 -86 V106 Q-60 126 -40 126" fill="none" stroke="{t["red"]}" stroke-width="4" stroke-linecap="round"/>
    <circle cx="-38" cy="126" r="7" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="2"/>'''


def motif_conch(t: dict) -> str:
    waves = "".join(
        f'<path d="M{70 + k * 22} {-40 - k * 10} Q{96 + k * 26} 0 {70 + k * 22} {40 + k * 10}" fill="none" stroke="{t["blue"]}" stroke-width="5" stroke-linecap="round"/>'
        for k in range(3)
    )
    ridges = "".join(
        f'<path d="M{-58 + k * 8} {-30 + k * 22} Q{-10 + k * 4} {-46 + k * 22} {34 - k * 4} {-34 + k * 22}" fill="none" stroke="{t["line"]}" stroke-width="2.5"/>'
        for k in range(4)
    )
    return f'''{waves}
    <path d="M-30 -110 C40 -96 76 -40 58 30 C46 82 4 112 -34 96 C-74 78 -86 20 -70 -36 C-60 -72 -50 -96 -30 -110Z" fill="{t["white"]}" stroke="{t["line"]}" stroke-width="4"/>
    <path d="M-30 -110 L-38 -134 L-18 -112Z" fill="{t["white"]}" stroke="{t["line"]}" stroke-width="3" stroke-linejoin="round"/>
    {ridges}
    <path d="M10 40 C30 10 54 20 52 46 C48 76 14 92 -6 80 C14 70 20 56 10 40Z" fill="{t["magenta"]}" stroke="{t["line"]}" stroke-width="3"/>
    {dots_line(-56, 20, -60, 12, 3, [t["red"], t["yellow"]])}'''


def motif_jaali(t: dict) -> str:
    cells = []
    for r in range(3):
        for c in range(5):
            x, y = -96 + c * 48, -50 + r * 46
            cells.append(
                "".join(petal(x, y, 18, 12, a, t["white"], t["line"], 1.5) for a in (0, 90, 180, 270))
                + f'<circle cx="{x}" cy="{y}" r="4" fill="{t["red"]}"/>'
            )
    return f'''<rect x="-130" y="-84" width="260" height="168" rx="14" fill="{t["red"]}" stroke="{t["line"]}" stroke-width="4"/>
    <rect x="-118" y="-72" width="236" height="144" rx="8" fill="{t["blue"]}" stroke="{t["line"]}" stroke-width="3"/>
    {"".join(cells)}
    <path d="M-60 84 L-80 118 M60 84 L80 118" stroke="{t["line"]}" stroke-width="7" stroke-linecap="round"/>
    {dots_line(-118, 118, -78, 13, 2.5, [t["yellow"]])}'''


def motif_feather(t: dict) -> str:
    barbs = []
    for i in range(22):
        s = i / 21
        y = -40 + s * 150
        spread = 70 * (1 - s) + 16
        x = 6 * s
        barbs.append(
            f'<path d="M{x:.1f} {y:.1f} Q{x - spread * 0.6:.1f} {y - 18:.1f} {x - spread:.1f} {y - 34:.1f}" fill="none" stroke="{t["green"]}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M{x:.1f} {y:.1f} Q{x + spread * 0.6:.1f} {y - 18:.1f} {x + spread:.1f} {y - 34:.1f}" fill="none" stroke="{t["green"]}" stroke-width="3" stroke-linecap="round"/>'
        )
    return f'''{"".join(barbs)}
    <path d="M0 -50 Q4 40 14 126" fill="none" stroke="{t["rule"]}" stroke-width="4" stroke-linecap="round"/>
    <ellipse cx="0" cy="-58" rx="50" ry="64" fill="{t["green"]}" stroke="{t["line"]}" stroke-width="3"/>
    <ellipse cx="0" cy="-54" rx="38" ry="48" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="2.5"/>
    <ellipse cx="0" cy="-50" rx="27" ry="34" fill="#1f8a9e" stroke="{t["line"]}" stroke-width="2.5"/>
    <ellipse cx="0" cy="-46" rx="15" ry="20" fill="#14215a" stroke="{t["line"]}" stroke-width="2"/>
    <ellipse cx="-4" cy="-52" rx="4" ry="6" fill="{t["white"]}" opacity="0.8"/>'''


def motif_tiers(t: dict) -> str:
    tiers = []
    y = 90
    for i in range(6):
        w = 220 - i * 32
        h = 24
        fill = t["red"] if i % 2 == 0 else t["yellow"]
        tiers.append(
            f'<path d="M{-w / 2} {y} L{-w / 2 + 10} {y - h} L{w / 2 - 10} {y - h} L{w / 2} {y}Z" fill="{fill}" stroke="{t["line"]}" stroke-width="3" stroke-linejoin="round"/>'
            + dots_line(-w / 2 + 18, w / 2 - 18, y - h / 2, 14, 2.5, [t["white"] if i % 2 == 0 else t["red"]])
        )
        y -= h + 4
    return f'''<rect x="-120" y="90" width="240" height="30" fill="{t["blue"]}" stroke="{t["line"]}" stroke-width="3"/>
    <rect x="-22" y="96" width="44" height="24" rx="10" fill="{t["line"]}"/>
    {"".join(tiers)}
    <ellipse cx="0" cy="{y + 2}" rx="34" ry="12" fill="{t["green"]}" stroke="{t["line"]}" stroke-width="3"/>
    <circle cx="0" cy="{y - 18}" r="14" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="3"/>
    <path d="M0 {y - 32} V{y - 60} L22 {y - 52} L0 {y - 46}" fill="{t["red"]}" stroke="{t["line"]}" stroke-width="2.5" stroke-linejoin="round"/>'''


TILES = {
    "trackmyspend": (motif_kalasha, "bank SMS, kept in a ledger"),
    "resume-ledger": (motif_palmleaf, "a career log, retold for each job"),
    "odia-stt": (motif_conch, "spoken Odia, written down"),
    "clean-tv": (motif_jaali, "a calmer Android TV home"),
    "bg-download": (motif_feather, "wallpapers, gathered fresh"),
    "warehouse": (motif_tiers, "Django and React, stacked well"),
}


def tile(t: dict, slug: str, name: str, index: int) -> str:
    motif, tagline = TILES[slug]
    arch = "M84 314 V168 C84 98 200 66 280 40 C360 66 476 98 476 168 V314 Z"
    side = "".join(
        f'<circle cx="{x}" cy="{y}" r="5" fill="{t["red"] if (y // 22) % 2 else t["yellow"]}" stroke="{t["line"]}" stroke-width="1.2"/>'
        for x in (54, 506)
        for y in range(70, 318, 22)
    )
    body = f'''  <rect width="560" height="440" fill="{t["panel"]}"/>
  {frame(560, 440, t, 16)}
  {side}
  <path d="{arch}" fill="{t["arch"]}" stroke="{t["rule"]}" stroke-width="4" stroke-linejoin="round"/>
  <path d="{arch}" fill="none" stroke="{t["red"]}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round" transform="translate(28 20) scale(0.9)"/>
  <circle cx="280" cy="36" r="9" fill="{t["yellow"]}" stroke="{t["line"]}" stroke-width="2.5"/>
  <g class="breathe" style="animation-delay:-{index * 1.3:.1f}s"><g transform="translate(280 192)">{motif(t)}</g></g>
  <text x="280" y="360" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="700" fill="{t["ink"]}">{esc(name)}</text>
  <text x="280" y="392" text-anchor="middle" font-family="{SERIF}" font-size="18" font-style="italic" fill="{t["muted"]}">{esc(tagline)}</text>'''
    return svg(560, 440, f"{name} tile", f"Pattachitra tile under a temple arch for {name}: {tagline}.", body, SWAY)


def mandala(t: dict) -> str:
    rows = language_rows()
    colors = [t["red"], t["yellow"], t["blue"], t["green"], t["magenta"], t["orange"], "#2a9d8f", "#8c5a2b", "#9c8f80"]
    cx, cy = 330, 290
    petals = "".join(
        petal(*polar(cx, cy, 196, a), 40, 22, a, t["red"] if i % 2 else t["yellow"], t["line"], 2)
        for i, a in enumerate(range(0, 360, 12))
    )
    segs = []
    start = 0.0
    for i, (_, pct) in enumerate(rows):
        sweep = 360 * pct / 100
        segs.append(f'<path d="{arc_band(cx, cy, 186, 118, start, start + sweep)}" fill="{colors[i]}" stroke="{t["line"]}" stroke-width="2.5" stroke-linejoin="round"/>')
        start += sweep
    legend = []
    for i, (name, pct) in enumerate(rows):
        y = 210 + i * 34
        legend.append(
            f'<path d="M660 {y - 6} l9 -9 l9 9 l-9 9z" fill="{colors[i]}" stroke="{t["line"]}" stroke-width="1.5"/>'
            f'<text x="692" y="{y}" font-family="{SERIF}" font-size="20" fill="{t["ink"]}">{esc(name)}</text>'
            f'<text x="1110" y="{y}" text-anchor="end" font-family="{SERIF}" font-size="20" font-weight="700" fill="{t["ink"]}">{pct:.1f}%</text>'
            f'<line x1="692" y1="{y + 11}" x2="1110" y2="{y + 11}" stroke="{t["muted"]}" stroke-width="1" stroke-dasharray="1 5"/>'
        )
    height = 210 + len(rows) * 34 + 40
    body = f'''  <rect width="1200" height="{height}" fill="{t["paper"]}"/>
  {frame(1200, height, t)}
  <g class="turn">{petals}</g>
  {"".join(segs)}
  <circle cx="{cx}" cy="{cy}" r="118" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2.5"/>
  {"".join(f'<circle cx="{polar(cx, cy, 100, a)[0]:.1f}" cy="{polar(cx, cy, 100, a)[1]:.1f}" r="3.5" fill="{t["red"] if a % 30 else t["yellow"]}"/>' for a in range(0, 360, 15))}
  <g transform="translate({cx} {cy + 30})">{lotus(0, 0, 62, t)}</g>
  <text x="660" y="120" font-family="{SERIF}" font-size="34" font-weight="700" fill="{t["ink"]}">Colours of the code</text>
  <text x="660" y="154" font-family="{SERIF}" font-size="17" font-style="italic" fill="{t["muted"]}">public repositories by bytes, forks excluded, notebooks included</text>
  {"".join(legend)}'''
    summary = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return svg(1200, height, "Colours of the code", f"A mandala ring chart of the language mix: {summary}.", body, SWAY)


def marigold(x: float, y: float, color: str, t: dict) -> str:
    ring = "".join(
        f'<circle cx="{polar(x, y, 8, a)[0]:.1f}" cy="{polar(x, y, 8, a)[1]:.1f}" r="5.5" fill="{color}" stroke="{t["line"]}" stroke-width="1"/>'
        for a in range(0, 360, 40)
    )
    return f'{ring}<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{color}" stroke="{t["line"]}" stroke-width="1.2"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{t["red"]}"/>'


def garland(t: dict) -> str:
    rows = []
    sag = 46
    for r, (group, tools) in enumerate(TOOL_GROUPS):
        y0 = 150 + r * 140

        def rope_y(x: float) -> float:
            s = (x - 60) / 1080
            return y0 + 4 * sag * s * (1 - s)

        flowers = "".join(
            marigold(x, rope_y(x), t["orange"] if i % 2 else t["yellow"], t)
            for i, x in enumerate(range(72, 1132, 26))
        )
        tags = []
        n = len(tools)
        for i, tool in enumerate(tools):
            x = 180 + (i + 0.5) * (900 / n)
            yr = rope_y(x)
            w = len(tool) * 10.5 + 34
            tags.append(
                f'<line x1="{x:.1f}" y1="{yr:.1f}" x2="{x:.1f}" y2="{yr + 22:.1f}" stroke="{t["rule"]}" stroke-width="2"/>'
                f'<rect x="{x - w / 2:.1f}" y="{yr + 22:.1f}" width="{w:.1f}" height="36" rx="8" fill="{t["yellow"]}" stroke="{t["red"]}" stroke-width="3"/>'
                f'<rect x="{x - w / 2 + 4:.1f}" y="{yr + 26:.1f}" width="{w - 8:.1f}" height="28" rx="5" fill="none" stroke="{t["line"]}" stroke-width="1.2"/>'
                f'<text x="{x:.1f}" y="{yr + 46:.1f}" text-anchor="middle" font-family="{SERIF}" font-size="17" font-weight="700" fill="#1d120c">{esc(tool)}</text>'
                f'<path d="M{x:.1f} {yr + 60:.1f} l6 8 l-6 8 l-6 -8z" fill="{t["red"]}" stroke="{t["line"]}" stroke-width="1.2"/>'
            )
        label_w = len(group) * 10 + 28
        rows.append(
            f'<g class="sway" style="animation-delay:-{r * 1.7:.1f}s;transform-origin:600px {y0}px">'
            f'<path d="M60 {y0} Q600 {y0 + 2 * sag} 1140 {y0}" fill="none" stroke="{t["green"]}" stroke-width="5"/>'
            f'{"".join(tags)}{flowers}</g>'
            f'<rect x="56" y="{y0 - 44}" width="{label_w}" height="26" rx="13" fill="{t["red"]}" stroke="{t["line"]}" stroke-width="2"/>'
            f'<text x="{56 + label_w / 2}" y="{y0 - 26}" text-anchor="middle" font-family="{SERIF}" font-size="14" font-weight="700" letter-spacing="2" fill="{t["white"]}">{esc(group)}</text>'
        )
    height = 150 + len(TOOL_GROUPS) * 140 + 30
    body = f'''  <rect width="1200" height="{height}" fill="{t["paper"]}"/>
  {frame(1200, height, t)}
  <text x="600" y="92" text-anchor="middle" font-family="{SERIF}" font-size="34" font-weight="700" fill="{t["ink"]}">Tools on the garland</text>
  {"".join(rows)}'''
    style = """
    .sway { animation: sway 7s ease-in-out infinite; }
    @keyframes sway { 0%, 100% { transform: rotate(-0.5deg); } 50% { transform: rotate(0.5deg); } }"""
    tools = "; ".join(f"{g.title()}: {', '.join(ts)}" for g, ts in TOOL_GROUPS)
    return svg(1200, height, "Tools on the garland", f"Toolbox hung as tags on marigold garlands. {tools}.", body, style)


BUTTONS = {
    "email": ("Email", "nigmucode@gmail.com"),
    "x": ("X", "@nigmu7161"),
    "linkedin": ("LinkedIn", "nigamananda-behera"),
}


def button(slug: str) -> str:
    t = THEMES["light"]
    title, handle = BUTTONS[slug]
    if slug == "email":
        icon = (
            f'<rect x="-17" y="-12" width="34" height="24" rx="3" fill="none" stroke="{t["white"]}" stroke-width="3"/>'
            f'<path d="M-15 -9 L0 3 L15 -9" fill="none" stroke="{t["white"]}" stroke-width="3" stroke-linejoin="round"/>'
        )
    elif slug == "x":
        icon = f'<path d="M-12 -12 L12 12 M12 -12 L-12 12" stroke="{t["white"]}" stroke-width="4.5" stroke-linecap="round"/>'
    else:
        icon = f'<text x="0" y="9" text-anchor="middle" font-family="{SERIF}" font-size="26" font-weight="700" fill="{t["white"]}">in</text>'
    body = f'''  <rect x="3" y="3" width="354" height="104" rx="18" fill="{t["red"]}" stroke="{t["line"]}" stroke-width="3"/>
  {dots_line(24, 336, 12, 14, 2.4, [t["white"]])}
  {dots_line(24, 336, 98, 14, 2.4, [t["white"]])}
  <rect x="14" y="20" width="332" height="70" rx="12" fill="{t["paper"]}" stroke="{t["line"]}" stroke-width="2.5"/>
  <circle cx="58" cy="55" r="27" fill="{t["blue"]}" stroke="{t["line"]}" stroke-width="2.5"/>
  <g transform="translate(58 55)">{icon}</g>
  <text x="100" y="51" font-family="{SERIF}" font-size="24" font-weight="700" fill="{t["ink"]}">{title}</text>
  <text x="100" y="76" font-family="{SERIF}" font-size="15" font-style="italic" fill="{t["muted"]}">{esc(handle)}</text>'''
    return svg(360, 110, f"{title} button", f"Painted button: {title}, {handle}.", body)


def footer(t: dict) -> str:
    odia = load_glyph("odia-bold")
    tf, w, h = fitted(odia, 0, 0, height=60)
    body = f'''  <rect width="1200" height="220" fill="{t["paper"]}"/>
  {frame(1200, 220, t)}
  <g class="breathe"><g transform="translate(330 140)">{lotus(0, 0, 56, t)}</g></g>
  <g class="breathe" style="animation-delay:-4s"><g transform="translate(870 140)">{lotus(0, 0, 56, t)}</g></g>
  <g transform="translate({600 - w / 2:.1f} 66)"><g transform="{tf}">{glyph_paths(odia, f'fill="{t["red"]}"')}</g></g>
  <text x="600" y="168" text-anchor="middle" font-family="{SERIF}" font-size="20" font-style="italic" fill="{t["muted"]}">thank you for visiting</text>'''
    return svg(1200, 220, "Namaskar", "Closing border with two lotuses and the Odia greeting namaskar: thank you for visiting.", body, SWAY)


def build() -> dict[str, str]:
    files: dict[str, str] = {}
    for theme, t in THEMES.items():
        files[f"assets/banner-{theme}.svg"] = banner(t)
        files[f"assets/mandala-{theme}.svg"] = mandala(t)
        files[f"assets/garland-{theme}.svg"] = garland(t)
        files[f"assets/namaskar-{theme}.svg"] = footer(t)
        for index, (slug, name, _) in enumerate(PROJECTS):
            files[f"assets/tiles/{slug}-{theme}.svg"] = tile(t, slug, name, index)
    for slug in BUTTONS:
        files[f"assets/buttons/{slug}.svg"] = button(slug)
    return files
