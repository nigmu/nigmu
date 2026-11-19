"""Nigam FM: a retro neon radio station."""

from __future__ import annotations

import math

from .common import (
    MONO,
    PROJECTS,
    SANS,
    TOOL_GROUPS,
    base,
    esc,
    fitted,
    glyph_paths,
    language_rows,
    load_glyph,
    rand,
    svg,
)

THEMES = {
    "dark": {
        "panel": "#1f0b3a",
        "well": "#0d0420",
        "line": "#3d1f6b",
        "ink": "#f7ecff",
        "muted": "#a993cf",
        "pink": "#ff2e88",
        "cyan": "#00e5ff",
        "orange": "#ff9e2c",
        "lime": "#c6ff00",
        "yellow": "#ffd23f",
        "violet": "#b47cff",
        "mint": "#7af0c0",
        "sky": ("#0d0221", "#2a0845", "#7a2178"),
        "floor": "#12052a",
        "grid": "#ff2e88",
        "grid_op": 0.75,
        "chrome": ("#ffffff", "#8fd3ff", "#2b0a4a", "#ff6ec7", "#ffe0f4"),
        "glow": 0.85,
        "stars": True,
    },
    "light": {
        "panel": "#fff7f0",
        "well": "#f3e6ff",
        "line": "#e2cdf5",
        "ink": "#2b1240",
        "muted": "#7d6496",
        "pink": "#e0186f",
        "cyan": "#008fb0",
        "orange": "#e06a00",
        "lime": "#4c9a00",
        "yellow": "#c98d00",
        "violet": "#7b2ff7",
        "mint": "#0f9d74",
        "sky": ("#ffe9d2", "#ffd0e2", "#e7cfff"),
        "floor": "#f4e6ff",
        "grid": "#b03cff",
        "grid_op": 0.45,
        "chrome": ("#4b1a82", "#7b2ff7", "#e0186f", "#ff4f8b", "#ff8a3d"),
        "glow": 0.35,
        "stars": False,
    },
}

DARK_INK = "#1a0b2e"


def hero(t: dict) -> str:
    horizon = 300
    nigam = load_glyph("fm-nigam")
    tf, _, title_h = fitted(nigam, 70, 118, width=560)
    sky0, sky1, sky2 = t["sky"]
    c0, c1, c2, c3, c4 = t["chrome"]

    stars = []
    if t["stars"]:
        for i in range(70):
            x = 20 + rand(i) * 1160
            y = 16 + rand(i + 300) * (horizon - 40)
            r = 0.6 + rand(i + 600) * 1.4
            cls = ' class="twinkle"' if i % 5 == 0 else ""
            delay = f' style="animation-delay:-{rand(i + 900) * 5:.1f}s"' if cls else ""
            stars.append(f'<circle{cls}{delay} cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#ffffff" opacity="{0.35 + rand(i + 1200) * 0.5:.2f}"/>')

    stripes = []
    y = 222
    gap = 3
    while y < horizon:
        stripes.append(f'<rect x="600" y="{y}" width="600" height="{gap}" fill="black"/>')
        y += gap + 12
        gap += 2

    verticals = []
    for k in range(-16, 17):
        verticals.append(
            f'<line x1="600" y1="{horizon - 60}" x2="{600 + k * 120}" y2="440" stroke="{t["grid"]}" stroke-width="1.4" opacity="{t["grid_op"]}"/>'
        )
    lanes = []
    for i in range(8):
        lanes.append(
            f'<line class="lane" style="animation-delay:-{i * 7 / 8:.3f}s" x1="0" y1="{horizon}" x2="1200" y2="{horizon}" '
            f'stroke="{t["grid"]}" stroke-width="1.6"/>'
        )

    mountains = (
        f"M600 {horizon} L640 248 L700 270 L780 214 L840 262 L905 228 L980 276 L1050 232 L1120 268 L1200 240 L1200 {horizon} Z"
    )

    body = f'''  <rect width="1200" height="440" fill="url(#sky)"/>
  {"".join(stars)}
  <g mask="url(#sunstripes)">
    <circle cx="880" cy="{horizon}" r="176" fill="url(#sun)"/>
  </g>
  <path d="{mountains}" fill="{t["floor"]}" stroke="{t["cyan"]}" stroke-width="2" stroke-linejoin="round" opacity="0.95"/>
  <rect y="{horizon}" width="1200" height="140" fill="{t["floor"]}"/>
  <g clip-path="url(#floorclip)">
    {"".join(verticals)}
    {"".join(lanes)}
  </g>
  <rect y="{horizon - 1}" width="1200" height="3" fill="{t["pink"]}" opacity="0.9"/>
  <g transform="{tf}">
    {glyph_paths(nigam, f'fill="{t["pink"]}" opacity="{t["glow"]}" filter="url(#glow)"')}
    {glyph_paths(nigam, 'fill="url(#chrome)"')}
  </g>
  <text x="74" y="{118 + title_h + 44:.0f}" font-family="{MONO}" font-size="19" letter-spacing="4" fill="{t["cyan"]}">FULL STACK · ANDROID · MACHINE LEARNING</text>
  <g transform="translate(74 50)">
    <rect width="128" height="36" rx="18" fill="{t["well"]}" stroke="{t["pink"]}" stroke-width="2"/>
    <circle class="onair" cx="22" cy="18" r="7" fill="{t["pink"]}"/>
    <text x="40" y="24" font-family="{MONO}" font-size="16" font-weight="700" letter-spacing="2" fill="{t["ink"]}">ON AIR</text>
  </g>
  <text x="1126" y="74" text-anchor="end" font-family="{MONO}" font-size="16" letter-spacing="3" fill="{t["ink"]}" opacity="0.8">107.7 MHz · NIGAM FM</text>'''

    defs = f'''    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{sky0}"/><stop offset="0.55" stop-color="{sky1}"/><stop offset="0.7" stop-color="{sky2}"/>
    </linearGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffe45c"/><stop offset="0.45" stop-color="#ff9e2c"/><stop offset="0.8" stop-color="#ff2e88"/>
    </linearGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{c0}"/><stop offset="0.47" stop-color="{c1}"/><stop offset="0.5" stop-color="{c2}"/>
      <stop offset="0.53" stop-color="{c3}"/><stop offset="1" stop-color="{c4}"/>
    </linearGradient>
    <mask id="sunstripes">
      <rect width="1200" height="{horizon}" fill="white"/>
      {"".join(stripes)}
    </mask>
    <clipPath id="floorclip"><rect y="{horizon}" width="1200" height="140"/></clipPath>
    <filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>'''

    style = f"""
    .lane {{ animation: lane 7s linear infinite; }}
    @keyframes lane {{
      0% {{ transform: translateY(0); opacity: 0; }}
      12% {{ opacity: {t["grid_op"]}; }}
      25% {{ transform: translateY(9px); }}
      50% {{ transform: translateY(35px); }}
      75% {{ transform: translateY(79px); }}
      100% {{ transform: translateY(140px); opacity: {t["grid_op"]}; }}
    }}
    .onair {{ animation: onair 2.4s ease-in-out infinite; }}
    @keyframes onair {{ 50% {{ opacity: 0.25; }} }}
    .twinkle {{ animation: twinkle 5s ease-in-out infinite; }}
    @keyframes twinkle {{ 50% {{ opacity: 0.1; }} }}"""

    return svg(
        1200, 440, "Nigam FM",
        "Synthwave poster: a striped sunset over a neon grid, the name NIGAM in chrome lettering, "
        "and an ON AIR light. Full stack, Android and machine learning.",
        body, style, defs,
    )


def tuner(t: dict) -> str:
    x0, x1 = 90, 1110

    def mhz(f: float) -> float:
        return x0 + (f - 88) / 20 * (x1 - x0)

    ticks = []
    for i in range(41):
        f = 88 + i * 0.5
        major = i % 4 == 0
        h = 22 if major else 10
        ticks.append(
            f'<line x1="{mhz(f):.1f}" y1="72" x2="{mhz(f):.1f}" y2="{72 + h}" stroke="{t["muted"]}" stroke-width="{1.6 if major else 1}"/>'
        )
        if major:
            ticks.append(
                f'<text x="{mhz(f):.1f}" y="166" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{int(f)}</text>'
            )

    channels = [("FULL-STACK", 92.1, t["pink"]), ("ANDROID", 98.7, t["lime"]), ("ML", 104.3, t["cyan"])]
    marks = []
    for label, f, color in channels:
        x = mhz(f)
        marks.append(
            f'<circle cx="{x:.1f}" cy="108" r="5" fill="{color}"/>'
            f'<text x="{x:.1f}" y="140" text-anchor="middle" font-family="{MONO}" font-size="19" font-weight="700" letter-spacing="2" fill="{color}">{label}</text>'
        )
    p1, p2, p3 = (mhz(f) for _, f, _ in channels)

    items = [
        ("TrackMySpend", t["lime"]),
        ("resume-ledger", t["pink"]),
        ("bg_download", t["cyan"]),
        ("fun fact: Nigam plays the ukulele", t["orange"]),
    ]
    spans = []
    chars = 0
    for label, color in items:
        spans.append(f'<tspan fill="{color}">{esc(label)}</tspan><tspan fill="{t["muted"]}">  ◆  </tspan>')
        chars += len(label) + 5
    advance = 12
    width = chars * advance
    ticker = "".join(
        f'<text x="{232 + n * width}" y="236" font-family="{MONO}" font-size="20" textLength="{width - advance * 2}" '
        f'lengthAdjust="spacingAndGlyphs">{"".join(spans)}</text>'
        for n in range(3)
    )

    body = f'''  <rect x="6" y="6" width="1188" height="276" rx="22" fill="{t["panel"]}" stroke="url(#rim)" stroke-width="3"/>
  <text x="40" y="44" font-family="{MONO}" font-size="14" letter-spacing="3" fill="{t["muted"]}">STATION ID</text>
  <text x="1160" y="44" text-anchor="end" font-family="{MONO}" font-size="14" letter-spacing="3" fill="{t["muted"]}">STEREO · 24/7 · OPEN SOURCE</text>
  <rect x="40" y="58" width="1120" height="124" rx="14" fill="{t["well"]}" stroke="{t["line"]}" stroke-width="2"/>
  {"".join(ticks)}
  {"".join(marks)}
  <g class="needle">
    <line x1="0" y1="62" x2="0" y2="178" stroke="{t["orange"]}" stroke-width="8" opacity="0.35" filter="url(#soft)"/>
    <line x1="0" y1="62" x2="0" y2="178" stroke="{t["orange"]}" stroke-width="3" stroke-linecap="round"/>
  </g>
  <rect x="40" y="200" width="1120" height="56" rx="12" fill="{t["well"]}" stroke="{t["line"]}" stroke-width="2"/>
  <g clip-path="url(#tickerclip)"><g class="ticker">{ticker}</g></g>
  <rect x="40" y="200" width="180" height="56" rx="12" fill="{t["pink"]}"/>
  <text x="130" y="234" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" letter-spacing="2" fill="#ffffff">NOW PLAYING</text>'''

    defs = f'''    <linearGradient id="rim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t["pink"]}"/><stop offset="0.5" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["cyan"]}"/>
    </linearGradient>
    <clipPath id="tickerclip"><rect x="220" y="200" width="936" height="56"/></clipPath>
    <filter id="soft" x="-200%" y="-10%" width="500%" height="120%"><feGaussianBlur stdDeviation="3"/></filter>'''

    style = f"""
    .needle {{ animation: sweep 15s ease-in-out infinite; transform: translateX({p1:.1f}px); }}
    @keyframes sweep {{
      0%, 24% {{ transform: translateX({p1:.1f}px); }}
      33%, 57% {{ transform: translateX({p2:.1f}px); }}
      66%, 90% {{ transform: translateX({p3:.1f}px); }}
      100% {{ transform: translateX({p1:.1f}px); }}
    }}
    .ticker {{ animation: ticker {width / 45:.1f}s linear infinite; }}
    @keyframes ticker {{ to {{ transform: translateX(-{width}px); }} }}"""

    return svg(
        1200, 288, "Station ID",
        "A radio tuner dial sweeping between three channels: full-stack, Android and ML. "
        "A ticker reads: now playing TrackMySpend, resume-ledger, bg_download; fun fact: Nigam plays the ukulele.",
        body, style, defs,
    )


CASSETTES = {
    "trackmyspend": ("#c6ff00", "#ff2e88", "#00b8d4", "bank SMS → ledger"),
    "resume-ledger": ("#ff2e88", "#ffd23f", "#00e5ff", "career log → résumé"),
    "odia-stt": ("#00e5ff", "#ff2e88", "#ff9e2c", "Odia speech → text"),
    "clean-tv": ("#ff9e2c", "#00e5ff", "#ff2e88", "a calmer Android TV"),
    "bg-download": ("url(#body)", "#ffd23f", "#c6ff00", "wallpapers, fetched"),
    "warehouse": ("#ffd23f", "#7b2ff7", "#ff2e88", "Django + React WMS"),
}


def cassette(slug: str, name: str, index: int) -> str:
    body_fill, stripe_a, stripe_b, tagline = CASSETTES[slug]
    label = "#fff6e3"

    def hub(cx: float, delay: float) -> str:
        teeth = "".join(
            f'<rect x="{cx - 3:.1f}" y="153" width="6" height="8" rx="1.5" fill="{DARK_INK}" transform="rotate({a} {cx} 170)"/>'
            for a in range(0, 360, 60)
        )
        return (
            f'<g class="spin" style="animation-delay:-{delay:.1f}s">'
            f'<circle cx="{cx}" cy="170" r="17" fill="{label}"/>{teeth}'
            f'<circle cx="{cx}" cy="170" r="5" fill="{DARK_INK}"/></g>'
        )

    screws = "".join(
        f'<circle cx="{x}" cy="{y}" r="7" fill="{DARK_INK}" opacity="0.35"/>'
        f'<path d="M{x - 4} {y}h8" stroke="{label}" stroke-width="1.6" opacity="0.7"/>'
        for x, y in ((34, 34), (526, 34), (34, 326), (526, 326))
    )

    body = f'''  <rect x="8" y="8" width="544" height="344" rx="26" fill="{body_fill}" stroke="{DARK_INK}" stroke-width="4"/>
  <rect x="20" y="16" width="520" height="10" rx="5" fill="#ffffff" opacity="0.25"/>
  {screws}
  <rect x="46" y="38" width="468" height="200" rx="14" fill="{label}" stroke="{DARK_INK}" stroke-width="3"/>
  <rect x="49" y="188" width="462" height="12" fill="{stripe_a}"/>
  <rect x="49" y="204" width="462" height="7" fill="{stripe_b}"/>
  <text x="74" y="84" font-family="{SANS}" font-size="{31 if len(name) <= 14 else 25}" font-weight="800" fill="{DARK_INK}">{esc(name)}</text>
  <text x="76" y="114" font-family="{MONO}" font-size="16" fill="#5b4a6b">SIDE A · {esc(tagline)}</text>
  <circle cx="478" cy="74" r="20" fill="{DARK_INK}"/>
  <text x="478" y="81" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="800" fill="{label}">A</text>
  <rect x="150" y="128" width="260" height="84" rx="42" fill="{DARK_INK}" stroke="{DARK_INK}" stroke-width="3"/>
  <g clip-path="url(#window)">
    <circle cx="215" cy="170" r="{38 - index % 3 * 4}" fill="#5a3a26"/>
    <circle cx="345" cy="170" r="{24 + index % 3 * 4}" fill="#5a3a26"/>
    <rect x="236" y="196" width="88" height="3" fill="#5a3a26"/>
  </g>
  {hub(215, index * 0.7)}
  {hub(345, index * 0.7 + 1.3)}
  <path d="M118 352 L150 270 L410 270 L442 352 Z" fill="{DARK_INK}" opacity="0.16"/>
  <path d="M118 352 L150 270 L410 270 L442 352" fill="none" stroke="{DARK_INK}" stroke-width="3" stroke-linejoin="round"/>
  <circle cx="186" cy="312" r="10" fill="{DARK_INK}"/>
  <circle cx="374" cy="312" r="10" fill="{DARK_INK}"/>
  <rect x="250" y="300" width="14" height="18" rx="3" fill="{DARK_INK}"/>
  <rect x="296" y="300" width="14" height="18" rx="3" fill="{DARK_INK}"/>
  <text x="62" y="318" font-family="{MONO}" font-size="14" font-weight="700" fill="{DARK_INK}" opacity="0.6">NIGAM FM</text>
  <text x="498" y="318" text-anchor="end" font-family="{MONO}" font-size="14" font-weight="700" fill="{DARK_INK}" opacity="0.6">C-60</text>'''

    defs = '''    <linearGradient id="body" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#8a2be2"/><stop offset="1" stop-color="#ff2e88"/>
    </linearGradient>
    <clipPath id="window"><rect x="150" y="128" width="260" height="84" rx="42"/></clipPath>'''

    style = """
    .spin { animation: spin 6s linear infinite; transform-box: fill-box; transform-origin: center; }
    @keyframes spin { to { transform: rotate(360deg); } }"""

    return svg(560, 360, f"{name} cassette", f"A cassette tape labelled {name}: {tagline}.", body, style, defs)


def equalizer(t: dict) -> str:
    rows = language_rows()
    segments, seg_h, seg_gap = 20, 11, 4
    top, left, right = 92, 130, 1160
    bottom = top + segments * (seg_h + seg_gap)
    col = (right - left) / len(rows)
    bar_w = 62

    def seg_color(i: int) -> str:
        return t["lime"] if i < 12 else t["orange"] if i < 16 else t["pink"]

    scale = []
    for db in (0, -10, -20, -30, -40, -50):
        level = 1 + db / 50
        y = bottom - level * segments * (seg_h + seg_gap) + seg_gap / 2
        scale.append(
            f'<text x="104" y="{y + 4:.1f}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{db}</text>'
            f'<line x1="112" y1="{y:.1f}" x2="1164" y2="{y:.1f}" stroke="{t["line"]}" stroke-width="1" stroke-dasharray="2 6"/>'
        )

    bars = []
    for c, (name, pct) in enumerate(rows):
        lit = max(1, min(segments, round(segments * (1 + math.log10(pct / 100) / 2.5))))
        cx = left + col * c + col / 2
        x = cx - bar_w / 2
        for i in range(segments):
            y = bottom - (i + 1) * (seg_h + seg_gap) + seg_gap
            on = i < lit
            cls = f' class="flick" style="animation-delay:-{c * 0.37:.2f}s"' if on and i == lit - 1 else ""
            bars.append(
                f'<rect{cls} x="{x:.1f}" y="{y}" width="{bar_w}" height="{seg_h}" rx="2.5" fill="{seg_color(i)}" opacity="{1 if on else 0.13}"/>'
            )
        peak = min(lit, segments - 1)
        py = bottom - (peak + 1) * (seg_h + seg_gap) + seg_gap
        bars.append(
            f'<rect class="peak" style="animation-duration:{2.6 + (c % 4) * 0.45:.2f}s;animation-delay:-{c * 0.5:.1f}s" '
            f'x="{x:.1f}" y="{py - 6}" width="{bar_w}" height="4" rx="2" fill="{t["ink"]}"/>'
        )
        bars.append(
            f'<text x="{cx:.1f}" y="{bottom + 30}" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="700" fill="{seg_color(lit - 1)}">{pct:.1f}%</text>'
            f'<text x="{cx:.1f}" y="{bottom + 52}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{t["ink"]}">{esc(name.replace(" Notebook", ""))}</text>'
        )

    body = f'''  <rect x="6" y="6" width="1188" height="{bottom + 76}" rx="22" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>
  <text x="40" y="54" font-family="{MONO}" font-size="22" font-weight="700" letter-spacing="4" fill="{t["ink"]}">LEVELS</text>
  <text x="168" y="54" font-family="{MONO}" font-size="14" fill="{t["muted"]}">public code by bytes · forks excluded · meters read in dB, labels are true shares</text>
  {"".join(scale)}
  {"".join(bars)}'''

    style = """
    .peak { animation: peak 3s ease-in-out infinite; }
    @keyframes peak { 50% { transform: translateY(-15px); } }
    .flick { animation: flick 1.8s ease-in-out infinite; }
    @keyframes flick { 50% { opacity: 0.45; } }"""

    summary = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return svg(1200, bottom + 88, "Levels", f"Language mix of public repositories as a graphic equalizer: {summary}.", body, style)


PATCHES = [
    ("Python", "FastAPI", "pink"),
    ("FastAPI", "PostgreSQL", "pink"),
    ("Django", "React", "violet"),
    ("Pandas", "scikit-learn", "lime"),
    ("Python", "PyTorch", "cyan"),
    ("PyTorch", "OpenCV", "cyan"),
    ("Kotlin", "Android", "orange"),
    ("JavaScript", "React", "yellow"),
    ("Docker", "Linux", "mint"),
]

PATCH_ROWS = TOOL_GROUPS[:3] + [("APPS + OPS", ["Docker", "Linux", "React", "Git", "Android"])]


def patchbay(t: dict) -> str:
    row_y = [124, 254, 384, 514]
    pos: dict[str, tuple[float, float]] = {}
    sockets, labels, rowlabels = [], [], []
    for r, (group, tools) in enumerate(PATCH_ROWS):
        y = row_y[r]
        rowlabels.append(
            f'<text x="40" y="{y + 5}" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="2" fill="{t["muted"]}">{esc(group)}</text>'
        )
        for c, tool in enumerate(tools):
            x = 270 + c * 166
            pos[tool] = (x, y)
            sockets.append(
                f'<circle cx="{x}" cy="{y}" r="20" fill="{t["well"]}" stroke="{t["line"]}" stroke-width="3"/>'
                f'<circle cx="{x}" cy="{y}" r="9" fill="{DARK_INK}"/>'
            )
            w = len(tool) * 8.6 + 22
            labels.append(
                f'<rect x="{x - w / 2:.1f}" y="{y + 30}" width="{w:.1f}" height="24" rx="12" fill="{t["panel"]}" opacity="0.92"/>'
                f'<text x="{x}" y="{y + 47}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["ink"]}">{esc(tool)}</text>'
            )

    cables, plugs = [], []
    for i, (a, b, key) in enumerate(PATCHES):
        color = t[key]
        (ax, ay), (bx, by) = pos[a], pos[b]
        if ay == by:
            sag = min(46 + abs(bx - ax) * 0.06, 84)
        else:
            sag = 70
        low = max(ay, by) + sag
        d = f"M{ax} {ay} C{ax + (bx - ax) * 0.15:.1f} {low:.1f} {bx - (bx - ax) * 0.15:.1f} {low:.1f} {bx} {by}"
        cables.append(
            f'<path d="{d}" fill="none" stroke="#000000" stroke-opacity="0.22" stroke-width="11" stroke-linecap="round" transform="translate(2 4)"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/>'
            f'<path class="pulse" style="animation-delay:-{i * 1.1:.1f}s;animation-duration:{6 + i % 3}s" d="{d}" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 1600" opacity="0.85"/>'
        )
        for x, y in ((ax, ay), (bx, by)):
            plugs.append(
                f'<circle cx="{x}" cy="{y}" r="13" fill="{color}" stroke="{DARK_INK}" stroke-width="3"/>'
                f'<circle cx="{x - 3}" cy="{y - 3}" r="4" fill="#ffffff" opacity="0.6"/>'
            )

    height = row_y[-1] + 92
    body = f'''  <rect x="6" y="6" width="1188" height="{height - 12}" rx="22" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>
  <text x="40" y="54" font-family="{MONO}" font-size="22" font-weight="700" letter-spacing="4" fill="{t["ink"]}">PATCH BAY</text>
  <text x="214" y="54" font-family="{MONO}" font-size="14" fill="{t["muted"]}">the toolbox · cables join tools that ship together</text>
  {"".join(rowlabels)}
  {"".join(sockets)}
  {"".join(cables)}
  {"".join(plugs)}
  {"".join(labels)}'''

    style = """
    .pulse { animation: pulse 7s linear infinite; }
    @keyframes pulse { from { stroke-dashoffset: 0; } to { stroke-dashoffset: -1610; } }"""

    tools = "; ".join(f"{g.title()}: {', '.join(ts)}" for g, ts in TOOL_GROUPS)
    return svg(1200, height, "Patch bay", f"Toolbox drawn as an audio patch bay. {tools}.", body, style)


BUTTONS = {
    "email": ("P1", "EMAIL", "nigmucode@gmail.com", "#ff2e88"),
    "x": ("P2", "X", "@nigmu7161", "#00e5ff"),
    "linkedin": ("P3", "LINKEDIN", "nigamananda-behera", "#ff9e2c"),
}


def button(slug: str) -> str:
    preset, title, handle, color = BUTTONS[slug]
    if slug == "email":
        glyph = (
            f'<rect x="-20" y="-14" width="40" height="28" rx="4" fill="none" stroke="{color}" stroke-width="3"/>'
            f'<path d="M-18 -11 L0 3 L18 -11" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>'
        )
    elif slug == "x":
        glyph = f'<path d="M-15 -15 L15 15 M15 -15 L-15 15" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
    else:
        glyph = (
            f'<rect x="-19" y="-19" width="38" height="38" rx="8" fill="{color}"/>'
            f'<text x="0" y="10" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="800" fill="{DARK_INK}">in</text>'
        )
    body = f'''  <rect x="6" y="6" width="348" height="98" rx="20" fill="{color}" opacity="0.35" filter="url(#halo)"/>
  <rect x="6" y="6" width="348" height="98" rx="20" fill="{DARK_INK}" stroke="{color}" stroke-width="3"/>
  <text x="28" y="34" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{color}">{preset}</text>
  <g transform="translate(58 62)">{glyph}</g>
  <text x="102" y="52" font-family="{MONO}" font-size="21" font-weight="700" letter-spacing="3" fill="#f7ecff">{title}</text>
  <text x="102" y="78" font-family="{MONO}" font-size="15" fill="{color}">{esc(handle)}</text>'''
    defs = '    <filter id="halo" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="5"/></filter>'
    return svg(360, 110, f"{title} preset", f"Radio preset button: {title}, {handle}.", body, "", defs)


def footer(t: dict) -> str:
    odia = load_glyph("odia-bold")
    tf, w, h = fitted(odia, 0, 0, height=42)
    left = base.speech_wave(40, 470, 64, 20)
    right = base.speech_wave(730, 1160, 64, 20)
    body = f'''  <path d="{left}" fill="none" stroke="url(#wave)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="{right}" fill="none" stroke="url(#wave)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path class="drift" d="{left}" fill="none" stroke="{t["ink"]}" stroke-width="3" stroke-dasharray="3 14" stroke-linecap="round" opacity="0.5"/>
  <path class="drift" d="{right}" fill="none" stroke="{t["ink"]}" stroke-width="3" stroke-dasharray="3 14" stroke-linecap="round" opacity="0.5"/>
  <g transform="translate({600 - w / 2:.1f} {64 - h / 2 - 4:.1f})"><g transform="{tf}">{glyph_paths(odia, f'fill="{t["pink"]}"')}</g></g>
  <text x="600" y="126" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="3" fill="{t["muted"]}">THANKS FOR TUNING IN · SIGNING OFF</text>'''
    defs = f'''    <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t["cyan"]}"/><stop offset="0.5" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["pink"]}"/>
    </linearGradient>'''
    style = """
    .drift { animation: drift 4s linear infinite; }
    @keyframes drift { to { stroke-dashoffset: -34; } }"""
    return svg(1200, 140, "Namaskar", "A neon waveform with the Odia greeting namaskar, and the words: thanks for tuning in.", body, style, defs)


def build() -> dict[str, str]:
    files: dict[str, str] = {}
    for theme, t in THEMES.items():
        files[f"assets/hero-{theme}.svg"] = hero(t)
        files[f"assets/tuner-{theme}.svg"] = tuner(t)
        files[f"assets/levels-{theme}.svg"] = equalizer(t)
        files[f"assets/patchbay-{theme}.svg"] = patchbay(t)
        files[f"assets/signoff-{theme}.svg"] = footer(t)
    for index, (slug, name, _) in enumerate(PROJECTS):
        files[f"assets/tapes/{slug}.svg"] = cassette(slug, name, index)
    for slug in BUTTONS:
        files[f"assets/presets/{slug}.svg"] = button(slug)
    return files
