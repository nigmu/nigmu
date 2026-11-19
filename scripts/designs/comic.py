"""The Amazing Nigam: a pop-art comic book."""

from __future__ import annotations

from .common import HEAVY, PROJECTS, TOOL_GROUPS, esc, language_rows, load_glyph, polar, rand, star_points, svg

PAPER = "#fff8e7"
INK = "#111111"
RED = "#e63946"
YELLOW = "#ffd60a"
GOLD = "#ffb703"
BLUE = "#1d6fe0"
CYAN = "#2ec4f1"
PINK = "#ff3d9a"
GREEN = "#2bb673"
ORANGE = "#ff8c1a"
PURPLE = "#7b2ff7"


def dots(pid: str, color: str, r: float = 2.6, step: int = 12) -> str:
    return (
        f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<circle cx="{step / 2}" cy="{step / 2}" r="{r}" fill="{color}"/>'
        f'<circle cx="0" cy="0" r="{r}" fill="{color}"/><circle cx="{step}" cy="0" r="{r}" fill="{color}"/>'
        f'<circle cx="0" cy="{step}" r="{r}" fill="{color}"/><circle cx="{step}" cy="{step}" r="{r}" fill="{color}"/></pattern>'
    )


def fade(fid: str, cx: str, cy: str, r: str, inner: float = 0.25, invert: bool = False) -> str:
    near, far = ("black", "white") if invert else ("white", "black")
    return (
        f'<radialGradient id="{fid}g" cx="{cx}" cy="{cy}" r="{r}">'
        f'<stop offset="{inner}" stop-color="{near}"/><stop offset="1" stop-color="{far}"/></radialGradient>'
        f'<mask id="{fid}"><rect width="100%" height="100%" fill="url(#{fid}g)"/></mask>'
    )


def lettering(name: str, x: float, y: float, width: float, fill: str, shadow: str = INK,
              outline: float = 5, offset: float = 7, rotate: float = 0, cls: str = "") -> str:
    data = load_glyph(name)
    s = width / data["width"]
    h = data["height"] * s
    sw = outline / s
    paths = "".join(f'<path d="{d}"/>' for d in data["paths"])
    klass = f' class="{cls}"' if cls else ""
    return (
        f'<g{klass} transform="translate({x:.1f} {y:.1f}) rotate({rotate} {width / 2:.1f} {h / 2:.1f})">'
        f'<g transform="translate({offset} {offset}) scale({s:.4f})" fill="{shadow}" stroke="{INK}" stroke-width="{sw:.1f}" stroke-linejoin="round">{paths}</g>'
        f'<g transform="scale({s:.4f})" fill="{fill}" stroke="{INK}" stroke-width="{sw:.1f}" stroke-linejoin="round" paint-order="stroke">{paths}</g>'
        f"</g>"
    )


def caption(x: float, y: float, text: str, size: int = 18, fill: str = YELLOW, pad: int = 14) -> str:
    w = len(text) * size * 0.74 + pad * 2
    h = size + pad * 1.4
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h:.0f}" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
        f'<text x="{x + pad}" y="{y + h / 2 + size * 0.36:.1f}" font-family="{HEAVY}" font-size="{size}" font-weight="900" fill="{INK}">{esc(text)}</text>'
    )


THROB = """
    .throb { animation: throb 3.2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
    @keyframes throb { 50% { transform: scale(1.05); } }"""


def cover() -> str:
    cx, cy = 600, 330
    rays = []
    n = 28
    for i in range(0, n * 2, 2):
        a0, a1 = 360 * i / (n * 2), 360 * (i + 1) / (n * 2)
        x0, y0 = polar(cx, cy, 1100, a0)
        x1, y1 = polar(cx, cy, 1100, a1)
        rays.append(f"M{cx} {cy} L{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}Z")

    title_w = 780
    title = lettering("comic-nigam", (1200 - title_w) / 2, 128, title_w, "url(#titlefill)", BLUE, outline=9, offset=14)
    amazing = lettering("comic-amazing", 44, 22, 340, YELLOW, INK, outline=4, offset=4)

    ribbon = "M150 372 L1050 372 L1020 402 L1050 432 L150 432 L180 402 Z"
    body = f'''  <rect width="1200" height="560" fill="{YELLOW}"/>
  <g class="rays"><path d="{" ".join(rays)}" fill="{GOLD}"/></g>
  <rect width="1200" height="560" fill="url(#reddots)" mask="url(#edge)" opacity="0.55"/>
  <rect width="1200" height="96" fill="{RED}"/>
  <rect y="96" width="1200" height="6" fill="{INK}"/>
  {amazing}
  <rect x="972" y="16" width="196" height="66" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>
  <text x="1070" y="46" text-anchor="middle" font-family="{HEAVY}" font-size="24" font-weight="900" fill="{INK}">ISSUE #01</text>
  <text x="1070" y="70" text-anchor="middle" font-family="{HEAVY}" font-size="12" font-weight="900" letter-spacing="1" fill="{RED}">OPEN-SOURCE COMICS</text>
  {title}
  <path d="{ribbon}" fill="{INK}" transform="translate(6 6)"/>
  <path d="{ribbon}" fill="{BLUE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
  <text x="600" y="411" text-anchor="middle" font-family="{HEAVY}" font-size="24" font-weight="900" fill="#ffffff" letter-spacing="1">FULL STACK! ★ ANDROID! ★ MACHINE LEARNING!</text>
  <g class="throb">
    <polygon points="{star_points(1050, 478, 100, 70, 20, 0.25)}" fill="{INK}" transform="translate(6 6)"/>
    <polygon points="{star_points(1050, 478, 100, 70, 20, 0.25)}" fill="{RED}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
    <text x="1050" y="470" text-anchor="middle" font-family="{HEAVY}" font-size="17" font-weight="900" fill="{YELLOW}" transform="rotate(-10 1050 478)">NOW WITH</text>
    <text x="1050" y="498" text-anchor="middle" font-family="{HEAVY}" font-size="25" font-weight="900" fill="{YELLOW}" transform="rotate(-10 1050 478)">UKULELE!</text>
  </g>
  <polygon points="{star_points(150, 482, 88, 64, 18, 0.2)}" fill="{INK}" transform="translate(6 6)"/>
  <polygon points="{star_points(150, 482, 88, 64, 18, 0.2)}" fill="{CYAN}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
  <text x="150" y="480" text-anchor="middle" font-family="{HEAVY}" font-size="30" font-weight="900" fill="{INK}" transform="rotate(8 150 482)">100%</text>
  <text x="150" y="504" text-anchor="middle" font-family="{HEAVY}" font-size="13" font-weight="900" fill="{INK}" transform="rotate(8 150 482)">OPEN SOURCE</text>
  <rect x="5" y="5" width="1190" height="550" fill="none" stroke="{INK}" stroke-width="10"/>'''

    defs = f'''    {dots("reddots", RED, 3.2, 14)}
    {fade("edge", "50%", "55%", "75%", 0.3, invert=True)}
    <linearGradient id="titlefill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ff5964"/><stop offset="1" stop-color="#c1121f"/>
    </linearGradient>'''

    style = f"""
    .rays {{ animation: rays 120s linear infinite; transform-origin: {cx}px {cy}px; }}
    @keyframes rays {{ to {{ transform: rotate(360deg); }} }}{THROB}"""

    return svg(
        1200, 560, "The Amazing Nigam, issue 1",
        "Comic book cover on a yellow sunburst: THE AMAZING NIGAM. Full stack! Android! Machine learning! "
        "Starbursts read 100% open source and now with ukulele.",
        body, style, defs,
    )


def ukulele(x: float, y: float) -> str:
    strings = "".join(
        f'<line x1="{-6 + i * 4}" y1="-150" x2="{-6 + i * 4}" y2="58" stroke="#f1e3c8" stroke-width="1.4"/>' for i in range(4)
    )
    return f'''<g transform="translate({x} {y}) rotate(28) scale(0.86)">
    <rect x="-13" y="-170" width="26" height="150" rx="4" fill="#8b4a1c" stroke="{INK}" stroke-width="4"/>
    <path d="M-20 -210 L20 -210 L16 -165 L-16 -165 Z" fill="#6b3410" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
    <circle cx="0" cy="18" r="40" fill="{ORANGE}" stroke="{INK}" stroke-width="5"/>
    <circle cx="0" cy="70" r="52" fill="{ORANGE}" stroke="{INK}" stroke-width="5"/>
    <rect x="-36" y="20" width="72" height="40" fill="{ORANGE}"/>
    <circle cx="0" cy="22" r="15" fill="{INK}"/>
    <rect x="-20" y="80" width="40" height="9" rx="2" fill="#6b3410" stroke="{INK}" stroke-width="3"/>
    {strings}
  </g>'''


def note(x: float, y: float, color: str, delay: float) -> str:
    return (
        f'<g class="bob" style="animation-delay:-{delay}s"><g transform="translate({x} {y})">'
        f'<ellipse cx="0" cy="0" rx="11" ry="8" transform="rotate(-20)" fill="{color}" stroke="{INK}" stroke-width="3"/>'
        f'<path d="M9 -2 V-42 L26 -34" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g></g>'
    )


def origin() -> str:
    lines = [
        "BY DAY, NIGAM BUILDS FULL STACK",
        "APPS, ANDROID TOOLS AND",
        "MACHINE LEARNING MODELS.",
        "",
        "BY NIGHT, HE PLAYS THE UKULELE.",
    ]
    text = "".join(
        f'<text x="58" y="{124 + i * 30}" font-family="{HEAVY}" font-size="19" font-weight="900" fill="{INK}">{esc(line)}</text>'
        for i, line in enumerate(lines)
        if line
    )
    bubble = "M770 52 H1150 Q1170 52 1170 72 V218 Q1170 238 1150 238 H900 L860 292 L866 238 H770 Q750 238 750 218 V72 Q750 52 770 52 Z"
    body = f'''  <rect width="1200" height="340" fill="{PAPER}"/>
  <rect x="12" y="12" width="702" height="316" fill="#c7ecff"/>
  <rect x="12" y="12" width="702" height="316" fill="url(#bluedots)" mask="url(#fadeA)" opacity="0.6"/>
  <rect x="38" y="92" width="452" height="182" fill="#ffffff" stroke="{INK}" stroke-width="4"/>
  {text}
  {ukulele(596, 214)}
  {note(520, 96, PINK, 0)}
  {note(668, 70, YELLOW, 1.2)}
  {caption(12, 12, "MEANWHILE, ON GITHUB...", 18)}
  <rect x="12" y="12" width="702" height="316" fill="none" stroke="{INK}" stroke-width="6"/>
  <rect x="732" y="12" width="456" height="316" fill="#ffd1e8"/>
  <rect x="732" y="12" width="456" height="316" fill="url(#pinkdots)" mask="url(#fadeB)" opacity="0.6"/>
  <path d="{bubble}" fill="#ffffff" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
  <text x="960" y="96" text-anchor="middle" font-family="{HEAVY}" font-size="18" font-weight="900" fill="{INK}">NOW WORKING ON:</text>
  <text x="960" y="138" text-anchor="middle" font-family="{HEAVY}" font-size="27" font-weight="900" fill="{RED}">TRACKMYSPEND,</text>
  <text x="960" y="174" text-anchor="middle" font-family="{HEAVY}" font-size="27" font-weight="900" fill="{BLUE}">RESUME-LEDGER</text>
  <text x="960" y="210" text-anchor="middle" font-family="{HEAVY}" font-size="27" font-weight="900" fill="{GREEN}">&amp; BG_DOWNLOAD!</text>
  {caption(1026, 282, "— NIGAM", 16, YELLOW, 12)}
  <rect x="732" y="12" width="456" height="316" fill="none" stroke="{INK}" stroke-width="6"/>'''

    defs = f'''    {dots("bluedots", BLUE, 2.4, 11)}
    {dots("pinkdots", PINK, 2.4, 11)}
    {fade("fadeA", "100%", "0%", "90%", 0.05)}
    {fade("fadeB", "0%", "100%", "90%", 0.05)}'''

    style = """
    .bob { animation: bob 3.6s ease-in-out infinite; }
    @keyframes bob { 50% { transform: translateY(-8px); } }"""

    return svg(
        1200, 340, "Origin story",
        "Two comic panels. By day, Nigam builds full stack apps, Android tools and machine learning models. "
        "By night, he plays the ukulele. Speech bubble: now working on TrackMySpend, resume-ledger and bg_download.",
        body, style, defs,
    )


def art_phone() -> str:
    bubbles = "".join(
        f'<rect x="{34 + (i % 2) * 18}" y="{30 + i * 30}" width="58" height="20" rx="8" fill="{c}" stroke="{INK}" stroke-width="2.5"/>'
        for i, c in enumerate((GREEN, CYAN, GREEN, PINK))
    )
    coins = "".join(
        f'<ellipse cx="160" cy="{160 - i * 13}" rx="34" ry="11" fill="{YELLOW}" stroke="{INK}" stroke-width="3.5"/>' for i in range(5)
    )
    return f'''<rect x="20" y="0" width="110" height="180" rx="16" fill="{INK}"/>
    <rect x="29" y="16" width="92" height="140" rx="4" fill="#ffffff"/>{bubbles}
    <circle cx="75" cy="167" r="6" fill="#555"/>{coins}
    <text x="160" y="112" text-anchor="middle" font-family="{HEAVY}" font-size="22" font-weight="900" fill="{INK}">₹</text>'''


def art_papers() -> str:
    sheets = "".join(
        f'<g transform="rotate({r} 100 90)"><rect x="40" y="10" width="120" height="160" fill="#ffffff" stroke="{INK}" stroke-width="4"/>'
        + "".join(f'<rect x="56" y="{36 + k * 18}" width="{88 - (k % 3) * 18}" height="7" rx="3" fill="#c9c9c9"/>' for k in range(6))
        + "</g>"
        for r in (-12, 6, -2)
    )
    return f'''{sheets}
    <circle cx="160" cy="150" r="30" fill="{GREEN}" stroke="{INK}" stroke-width="4"/>
    <path d="M146 150 L157 162 L176 138" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'''


def art_mic() -> str:
    arcs = "".join(
        f'<path d="M{100 - d} {60 - d * 0.6} Q{100 - d - 22} 70 {100 - d} {80 + d * 0.6}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M{100 + d} {60 - d * 0.6} Q{100 + d + 22} 70 {100 + d} {80 + d * 0.6}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
        for d in (52, 74)
    )
    grille = "".join(f'<line x1="74" y1="{22 + k * 14}" x2="126" y2="{22 + k * 14}" stroke="#888" stroke-width="3"/>' for k in range(6))
    return f'''{arcs}
    <path d="M60 80 Q60 130 100 130 Q140 130 140 80" fill="none" stroke="{INK}" stroke-width="6"/>
    <rect x="70" y="0" width="60" height="110" rx="30" fill="#e0e0e0" stroke="{INK}" stroke-width="5"/>{grille}
    <rect x="94" y="130" width="12" height="36" fill="{INK}"/>
    <rect x="64" y="164" width="72" height="12" rx="5" fill="{INK}"/>'''


def art_tv() -> str:
    tiles = "".join(
        f'<rect x="{26 + (i % 3) * 52}" y="{30 + (i // 3) * 42}" width="44" height="34" rx="5" fill="{c}" stroke="{INK}" stroke-width="2.5"/>'
        for i, c in enumerate((PINK, YELLOW, GREEN, ORANGE, PURPLE, CYAN))
    )
    return f'''<rect x="6" y="10" width="190" height="130" rx="12" fill="{INK}"/>
    <rect x="16" y="20" width="170" height="104" rx="4" fill="#e8f7ff"/>{tiles}
    <path d="M60 140 L44 172 M142 140 L158 172" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
    <path d="M196 -6 L170 50 L190 50 L172 104 L224 34 L202 34 L220 -6 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'''


def art_frame() -> str:
    lines = "".join(
        f'<line x1="{-40 + k * 6}" y1="{40 + k * 34}" x2="{10 + k * 6}" y2="{40 + k * 34}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        for k in range(4)
    )
    return f'''{lines}
    <rect x="30" y="10" width="180" height="150" fill="#ffffff" stroke="{INK}" stroke-width="5"/>
    <rect x="42" y="22" width="156" height="126" fill="#9fdcff"/>
    <circle cx="160" cy="58" r="18" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>
    <path d="M42 148 L92 74 L126 118 L148 92 L198 148 Z" fill="{GREEN}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'''


def art_boxes() -> str:
    def box(x: float, y: float) -> str:
        return (
            f'<rect x="{x}" y="{y}" width="84" height="66" fill="#d9a066" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x + 34}" y="{y}" width="16" height="66" fill="#f4d6a8" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x + 10} {y + 50} h18" stroke="{INK}" stroke-width="3"/>'
        )

    return f'''{box(14, 108)}{box(102, 108)}{box(58, 42)}
    <path d="M10 178 H200" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
    <path d="M40 30 l-10 -16 M100 24 v-20 M160 30 l10 -16" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'''


PANELS = {
    "trackmyspend": ("#c8f7c5", GREEN, ("comic-kaching", 290), YELLOW, RED, "BANK SMS BECOMES A LEDGER!", art_phone),
    "resume-ledger": ("#ffe0ef", PINK, ("comic-tada", 230), CYAN, YELLOW, "A TAILORED RÉSUMÉ FOR EVERY JOB!", art_papers),
    "odia-stt": ("#d6ecff", BLUE, ("odia-bold", 240), YELLOW, PINK, "SPEAK ODIA, GET UNICODE TEXT!", art_mic),
    "clean-tv": ("#ffe8c7", ORANGE, ("comic-zap", 200), YELLOW, BLUE, "A CLEAN HOME SCREEN FOR A MI TV!", art_tv),
    "bg-download": ("#e7dcff", PURPLE, ("comic-whoosh", 280), PINK, YELLOW, "FRESH WALLPAPERS, FETCHED!", art_frame),
    "warehouse": ("#fff3b0", ORANGE, ("comic-thud", 240), RED, CYAN, "DJANGO + REACT RUN THE WAREHOUSE!", art_boxes),
}


def panel(slug: str, name: str, index: int) -> str:
    bg, dot, (glyph, width), word_fill, burst, tagline, art = PANELS[slug]
    data = load_glyph(glyph)
    h = data["height"] * width / data["width"]
    wx, wy = 386 - width / 2, 150 - h / 2
    tilt = -8 if index % 2 == 0 else 6
    spikes = star_points(386, 150, 118, 80, 16, 0.3, 1.2)
    body = f'''  <rect width="560" height="400" fill="{PAPER}"/>
  <rect x="10" y="10" width="540" height="380" fill="{bg}"/>
  <rect x="10" y="10" width="540" height="380" fill="url(#dots)" mask="url(#fade)" opacity="0.55"/>
  <g class="throb">
    <polygon points="{spikes}" fill="{INK}" transform="translate(6 6)"/>
    <polygon points="{spikes}" fill="{burst}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
  </g>
  {lettering(glyph, wx, wy, width, word_fill, INK, outline=5, offset=6, rotate=tilt)}
  <g transform="translate(42 132)">{art()}</g>
  {caption(10, 10, name.upper(), 19)}
  <rect x="10" y="336" width="540" height="54" fill="#ffffff" stroke="{INK}" stroke-width="4"/>
  <text x="280" y="371" text-anchor="middle" font-family="{HEAVY}" font-size="18" font-weight="900" fill="{INK}">{esc(tagline)}</text>
  <rect x="10" y="10" width="540" height="380" fill="none" stroke="{INK}" stroke-width="6"/>'''
    defs = f'''    {dots("dots", dot, 2.6, 12)}
    {fade("fade", "100%" if index % 2 else "0%", "100%", "95%", 0.05)}'''
    return svg(560, 400, f"{name} comic panel", f"Comic panel for {name}: {tagline.capitalize()}", body, THROB, defs)


def power() -> str:
    rows = language_rows()
    top = max(p for _, p in rows)
    colors = [RED, BLUE, GREEN, ORANGE, PINK, PURPLE, CYAN, GOLD, "#8d8d8d"]
    x0, track = 316, 740
    bars, clips, labels = [], [], []
    for i, (name, pct) in enumerate(rows):
        y = 132 + i * 46
        w = max(18, track * pct / top)
        labels.append(
            f'<text x="296" y="{y + 22}" text-anchor="end" font-family="{HEAVY}" font-size="17" font-weight="900" fill="{INK}">{esc(name.upper())}</text>'
            f'<rect x="{x0}" y="{y}" width="{track}" height="30" rx="6" fill="#ffffff" stroke="{INK}" stroke-width="3"/>'
            f'<text x="{x0 + track + 16}" y="{y + 23}" font-family="{HEAVY}" font-size="19" font-weight="900" fill="{INK}">{pct:.1f}%</text>'
        )
        bars.append(f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="30" rx="6" fill="{colors[i]}" stroke="{INK}" stroke-width="3"/>')
        clips.append(f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="30" rx="6"/>')
    stripes = "".join(
        f'<path d="M{x} 120 l-60 440" stroke="#ffffff" stroke-width="9" opacity="0.28"/>' for x in range(x0 - 40, x0 + track + 120, 28)
    )
    height = 132 + len(rows) * 46 + 52
    body = f'''  <rect width="1200" height="{height}" fill="{PAPER}"/>
  <rect width="1200" height="{height}" fill="url(#dots)" mask="url(#fade)" opacity="0.35"/>
  {lettering("comic-power", 40, 30, 460, YELLOW, RED, outline=4, offset=6, rotate=-2)}
  <text x="1160" y="70" text-anchor="end" font-family="{HEAVY}" font-size="14" font-weight="900" fill="{INK}">PUBLIC REPOS BY BYTES · FORKS EXCLUDED · NOTEBOOKS COUNT TOO!</text>
  {"".join(labels)}
  {"".join(bars)}
  <g clip-path="url(#barclip)"><g class="slide">{stripes}</g></g>
  <rect x="5" y="5" width="1190" height="{height - 10}" fill="none" stroke="{INK}" stroke-width="10"/>'''
    defs = f'''    {dots("dots", CYAN, 2.4, 12)}
    {fade("fade", "100%", "0%", "80%", 0.05)}
    <clipPath id="barclip">{"".join(clips)}</clipPath>'''
    style = """
    .slide { animation: slide 4s linear infinite; }
    @keyframes slide { to { transform: translateX(28px); } }"""
    summary = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return svg(1200, height, "Power levels", f"Comic power meters for the language mix of public repositories: {summary}.", body, style, defs)


def arsenal() -> str:
    group_colors = [YELLOW, CYAN, PINK, GREEN]
    items = []
    y = 136
    n = 0
    for g, (group, tools) in enumerate(TOOL_GROUPS):
        items.append(caption(40, y - 4, group, 14, "#ffffff", 10))
        x = 200
        for tool in tools:
            label = tool.upper()
            w = len(label) * 12.6 + 40
            rot = (rand(n + 40) - 0.5) * 7
            color = group_colors[g]
            tail = f"M{x + 22} {y + 50} l-6 18 l22 -18" if n % 2 == 0 else f"M{x + w - 34} {y + 50} l14 18 l2 -18"
            shape = f'<rect x="{x}" y="{y}" width="{w:.1f}" height="50" rx="{25 if n % 3 else 6}"/>'
            items.append(
                f'<g transform="rotate({rot:.1f} {x + w / 2:.1f} {y + 25})">'
                f'<g fill="{INK}" transform="translate(5 5)">{shape}<path d="{tail}"/></g>'
                f'<g fill="{color}" stroke="{INK}" stroke-width="4" stroke-linejoin="round">{shape}<path d="{tail}"/></g>'
                f'<text x="{x + w / 2:.1f}" y="{y + 32}" text-anchor="middle" font-family="{HEAVY}" font-size="17" font-weight="900" fill="{INK}">{esc(label)}</text></g>'
            )
            x += w + 16
            n += 1
        y += 104
    height = y + 10
    body = f'''  <rect width="1200" height="{height}" fill="{PAPER}"/>
  <rect width="1200" height="{height}" fill="url(#dots)" mask="url(#fade)" opacity="0.3"/>
  {lettering("comic-arsenal", 40, 30, 420, CYAN, PINK, outline=4, offset=6, rotate=-2)}
  <text x="1160" y="70" text-anchor="end" font-family="{HEAVY}" font-size="14" font-weight="900" fill="{INK}">EVERY HERO NEEDS GADGETS!</text>
  {"".join(items)}
  <rect x="5" y="5" width="1190" height="{height - 10}" fill="none" stroke="{INK}" stroke-width="10"/>'''
    defs = f'''    {dots("dots", PINK, 2.4, 12)}
    {fade("fade", "0%", "100%", "80%", 0.05)}'''
    tools = "; ".join(f"{g.title()}: {', '.join(ts)}" for g, ts in TOOL_GROUPS)
    return svg(1200, height, "The arsenal", f"Toolbox as comic speech bubbles. {tools}.", body, "", defs)


BUTTONS = {
    "email": ("POW!", "EMAIL", "NIGMUCODE@GMAIL.COM", YELLOW, RED),
    "x": ("ZAP!", "X", "@NIGMU7161", CYAN, YELLOW),
    "linkedin": ("BAM!", "LINKEDIN", "NIGAMANANDA-BEHERA", PINK, CYAN),
}


def button(slug: str) -> str:
    word, title, handle, color, burst = BUTTONS[slug]
    shape = "M14 14 H340 Q350 14 350 24 V92 Q350 102 340 102 H14 Q4 102 4 92 V24 Q4 14 14 14 Z"
    body = f'''  <path d="{shape}" fill="{INK}" transform="translate(5 5)"/>
  <path d="{shape}" fill="{color}" stroke="{INK}" stroke-width="4"/>
  <polygon points="{star_points(62, 58, 48, 32, 12, 0.2)}" fill="{burst}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>
  <text x="62" y="65" text-anchor="middle" font-family="{HEAVY}" font-size="17" font-weight="900" fill="{INK}" transform="rotate(-10 62 58)">{word}</text>
  <text x="122" y="55" font-family="{HEAVY}" font-size="26" font-weight="900" fill="{INK}">{title}</text>
  <text x="123" y="82" font-family="{HEAVY}" font-size="13" font-weight="900" fill="{INK}" opacity="0.8">{esc(handle)}</text>'''
    return svg(362, 112, f"{title} button", f"Comic button: {title}, {handle.lower()}.", body)


def continued() -> str:
    odia = load_glyph("odia-bold")
    ow = 190
    oh = odia["height"] * ow / odia["width"]
    s = ow / odia["width"]
    bubble = "M846 34 H1150 Q1170 34 1170 54 V136 Q1170 156 1150 156 H930 L884 186 L894 156 H846 Q826 156 826 136 V54 Q826 34 846 34 Z"
    body = f'''  <rect width="1200" height="200" fill="{PAPER}"/>
  <rect width="1200" height="200" fill="url(#dots)" mask="url(#fade)" opacity="0.4"/>
  <polygon points="40,44 770,30 784,152 54,166" fill="{INK}" transform="translate(7 7)"/>
  <polygon points="40,44 770,30 784,152 54,166" fill="{YELLOW}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  {lettering("comic-continued", 78, 72, 660, RED, INK, outline=3, offset=4, rotate=-1)}
  <path d="{bubble}" fill="#ffffff" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
  <g transform="translate({998 - ow / 2:.1f} {95 - oh / 2:.1f}) scale({s:.4f})" fill="{BLUE}">{"".join(f'<path d="{d}"/>' for d in odia["paths"])}</g>
  <rect x="5" y="5" width="1190" height="190" fill="none" stroke="{INK}" stroke-width="10"/>'''
    defs = f'''    {dots("dots", RED, 2.4, 12)}
    {fade("fade", "50%", "50%", "70%", 0.2)}'''
    return svg(1200, 200, "To be continued", "Caption box: to be continued. A speech bubble says namaskar in Odia.", body, "", defs)


def build() -> dict[str, str]:
    files = {
        "assets/cover.svg": cover(),
        "assets/origin.svg": origin(),
        "assets/power-levels.svg": power(),
        "assets/arsenal.svg": arsenal(),
        "assets/continued.svg": continued(),
    }
    for index, (slug, name, _) in enumerate(PROJECTS):
        files[f"assets/panels/{slug}.svg"] = panel(slug, name, index)
    for slug in BUTTONS:
        files[f"assets/buttons/{slug}.svg"] = button(slug)
    return files
