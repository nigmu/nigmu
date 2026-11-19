"""Stamp album: perforated postage, a postmark, and airmail stickers."""

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

INK = "#1c140c"
PAPER = {
    "trackmyspend": "#ffe08a",
    "resume-ledger": "#ffd0e0",
    "odia-stt": "#d6f3ff",
    "clean-tv": "#ffe0cc",
    "bg-download": "#e4ffc8",
    "warehouse": "#fff1c9",
}
ACCENT = {
    "trackmyspend": "#c45500",
    "resume-ledger": "#b4235b",
    "odia-stt": "#0b6e99",
    "clean-tv": "#d35400",
    "bg-download": "#2f7d32",
    "warehouse": "#8a5a00",
}

THEMES = {
    "light": {"page": "#efe4d0", "ink": "#2a2118", "muted": "#7a6552", "mount": "#c9a36a", "leather": "#8a5a3a"},
    "dark": {"page": "#2c241e", "ink": "#f6ead7", "muted": "#cbb89a", "mount": "#e6c27a", "leather": "#1a1410"},
}

MOTION = """
    .ink { stroke-dasharray: 7 9; animation: ink 14s linear infinite; }
    @keyframes ink { to { stroke-dashoffset: -64; } }"""


def holes(w: float, h: float, step: float = 22, r: float = 7) -> str:
    pts = []
    x = step / 2
    while x < w:
        pts += [(x, 0), (x, h)]
        x += step
    y = step / 2
    while y < h:
        pts += [(0, y), (w, y)]
        y += step
    circles = "".join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="black"/>' for px, py in pts)
    return f'<mask id="holes"><rect width="{w}" height="{h}" fill="white"/>{circles}</mask>'


def postmark(cx: float, cy: float, color: str = INK) -> str:
    return (
        f'<g transform="translate({cx} {cy}) rotate(-18)" fill="none" stroke="{color}" stroke-width="3">'
        f'<circle class="ink" r="46"/><circle r="36"/>'
        f'<text y="-4" text-anchor="middle" font-family="{SERIF}" font-size="13" font-weight="700" fill="{color}" stroke="none">OPEN SOURCE</text>'
        f'<text y="16" text-anchor="middle" font-family="{SERIF}" font-size="12" fill="{color}" stroke="none">ODISHA</text></g>'
    )


def scene(slug: str, accent: str) -> str:
    if slug == "trackmyspend":
        return (
            f'<rect x="-28" y="-70" width="56" height="96" rx="8" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-16" y="-52" width="32" height="10" rx="3" fill="{accent}"/>'
            f'<rect x="-16" y="-34" width="32" height="10" rx="3" fill="#0b6e99"/>'
            f'<circle cx="36" cy="20" r="18" fill="#f0b429" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="54" cy="-2" r="14" fill="#f0b429" stroke="{INK}" stroke-width="3"/>'
        )
    if slug == "resume-ledger":
        pages = "".join(
            f'<rect x="{-40 + i * 8}" y="{-50 + i * 4}" width="78" height="100" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>'
            for i in range(3)
        )
        return pages + f'<path d="M-6 20 l10 10 22 -24" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>'
    if slug == "odia-stt":
        return (
            f'<rect x="-16" y="-78" width="32" height="70" rx="16" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M-28 -20 q28 40 56 0" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-48 -40 q-18 16 0 32 M48 -40 q18 16 0 32" fill="none" stroke="{accent}" stroke-width="4" stroke-linecap="round"/>'
        )
    if slug == "clean-tv":
        colors = ["#e23d3d", "#f0b429", "#3aaa35", "#0b6e99", "#7b2ff7", "#ff8c42"]
        tiles = "".join(
            f'<rect x="{-46 + (i % 3) * 32}" y="{-40 + (i // 3) * 28}" width="26" height="22" fill="{colors[i]}" stroke="{INK}" stroke-width="2"/>'
            for i in range(6)
        )
        return f'<rect x="-58" y="-52" width="116" height="84" fill="#fffaf0" stroke="{INK}" stroke-width="3"/>{tiles}'
    if slug == "bg-download":
        return (
            f'<rect x="-50" y="-46" width="100" height="78" fill="#c9ecff" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="24" cy="-18" r="12" fill="#f0b429"/>'
            f'<path d="M-50 32 l30 -30 18 16 14 -12 38 26 v8 h-100z" fill="#3aaa35" stroke="{INK}" stroke-width="3"/>'
        )
    return (
        f'<rect x="-46" y="10" width="40" height="32" fill="#e0b07a" stroke="{INK}" stroke-width="3"/>'
        f'<rect x="6" y="10" width="40" height="32" fill="#c45500" stroke="{INK}" stroke-width="3"/>'
        f'<rect x="-20" y="-28" width="40" height="32" fill="#f0b429" stroke="{INK}" stroke-width="3"/>'
    )


def stamp(slug: str, name: str, index: int) -> str:
    w, h = 560, 400
    paper = PAPER[slug]
    accent = ACCENT[slug]
    size = 28 if len(name) < 16 else 22
    body = f'''  <g mask="url(#holes)">
    <rect width="{w}" height="{h}" fill="{paper}"/>
    <text x="36" y="58" font-family="{SERIF}" font-size="14" letter-spacing="3" fill="{accent}">POSTAGE</text>
    <text x="524" y="64" text-anchor="end" font-family="{SERIF}" font-size="32" font-weight="700" fill="{accent}">{index + 1:02d}</text>
    <g transform="translate(250 190)">{scene(slug, accent)}</g>
    {postmark(430, 168)}
    <text x="280" y="328" text-anchor="middle" font-family="{SERIF}" font-size="{size}" font-weight="700" fill="{INK}">{esc(name)}</text>
    <text x="280" y="360" text-anchor="middle" font-family="{SERIF}" font-size="16" font-style="italic" fill="{accent}">{esc(TAGLINES[slug])}</text>
  </g>'''
    return svg(w, h, f"{name} stamp", f"Postage stamp {index + 1} for {name}: {TAGLINES[slug]}. Cancelled in Odisha.", body, MOTION, holes(w, h))


def hero(t: dict) -> str:
    w, h = 1200, 480
    body = f'''  <rect width="{w}" height="{h}" fill="{t["page"]}"/>
  <rect x="18" y="18" width="1164" height="444" fill="none" stroke="{t["mount"]}" stroke-width="3" stroke-dasharray="2 10"/>
  <g mask="url(#holes)">
    <rect x="300" y="48" width="600" height="360" fill="#fff6df"/>
    <text x="330" y="100" font-family="{SERIF}" font-size="16" letter-spacing="4" fill="#a33b32">FOREVER</text>
    <text x="860" y="108" text-anchor="end" font-family="{SERIF}" font-size="28" font-weight="700" fill="#a33b32">№ 1</text>
    <text x="600" y="200" text-anchor="middle" font-family="{SERIF}" font-size="92" font-weight="700" fill="{INK}">Nigam</text>
    <text x="600" y="250" text-anchor="middle" font-family="{SERIF}" font-size="22" font-style="italic" fill="#a33b32">full stack · android · machine learning</text>
    <text x="340" y="318" font-family="{SERIF}" font-size="18" fill="{INK}">plays the ukulele</text>
    <text x="340" y="368" font-family="{SERIF}" font-size="14" letter-spacing="3" fill="{INK}">ODISHA · OPEN SOURCE</text>
    {postmark(800, 336, "#a33b32")}
  </g>
  <circle cx="70" cy="70" r="10" fill="{t["mount"]}"/><circle cx="1130" cy="70" r="10" fill="{t["mount"]}"/>
  <circle cx="70" cy="410" r="10" fill="{t["mount"]}"/><circle cx="1130" cy="410" r="10" fill="{t["mount"]}"/>'''
    return svg(
        w, h, "Nigam postage",
        "A forever stamp on an album page. Nigam, full stack, Android and machine learning, plays the ukulele. Postmarked Odisha, open source.",
        body, MOTION, _mask_at(300, 48, 600, 360),
    )


def _mask_at(x: float, y: float, w: float, h: float) -> str:
    raw = holes(w, h)
    raw = raw.replace(f'width="{w:.0f}"', f'width="{w:.0f}"')
    # Rebuild circles in the stamp's own coordinates.
    step, r = 22, 7
    pts = []
    cursor = step / 2
    while cursor < w:
        pts += [(x + cursor, y), (x + cursor, y + h)]
        cursor += step
    cursor = step / 2
    while cursor < h:
        pts += [(x, y + cursor), (x + w, y + cursor)]
        cursor += step
    circles = "".join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="black"/>' for px, py in pts)
    return (
        f'<mask id="holes"><rect width="1200" height="480" fill="black"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/>{circles}</mask>'
    )


def values(t: dict) -> str:
    rows = language_rows()
    items = []
    for i, (name, pct) in enumerate(rows):
        y = 108 + i * 52
        band = 80 + 640 * meter(pct)
        paper = list(PAPER.values())[i % 6]
        items.append(
            f'<rect x="48" y="{y - 28}" width="1104" height="44" fill="{paper}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="48" y="{y - 28}" width="{band:.0f}" height="44" fill="{ACCENT[list(ACCENT)[i % 6]]}" opacity="0.35"/>'
            f'<text x="68" y="{y}" font-family="{SERIF}" font-size="20" fill="{INK}">{esc(name)}</text>'
            f'<text x="1120" y="{y}" text-anchor="end" font-family="{SERIF}" font-size="20" font-weight="700" fill="{INK}">{pct:.1f}</text>'
        )
    height = 108 + len(rows) * 52 + 36
    body = f'''  <rect width="1200" height="{height}" fill="{t["page"]}"/>
  <text x="48" y="58" font-family="{SERIF}" font-size="32" font-weight="700" fill="{t["ink"]}">Denominations</text>
  <text x="48" y="84" font-family="{SERIF}" font-size="15" font-style="italic" fill="{t["muted"]}">the band is compressed · the numbers are the true share of public bytes</text>
  {"".join(items)}'''
    summary = ", ".join(f"{n} {p:.1f}%" for n, p in rows)
    return svg(1200, height, "Denominations", f"Language mix as stamp denominations. {summary}.", body)


def airmail(t: dict) -> str:
    rows = []
    y = 130
    for group, tools in TOOL_GROUPS:
        rows.append(
            f'<rect x="40" y="{y - 18}" width="{len(group) * 9 + 28}" height="24" fill="#c0392b"/>'
            f'<text x="52" y="{y}" font-family="{SERIF}" font-size="13" font-weight="700" letter-spacing="1" fill="#ffffff">{esc(group)}</text>'
        )
        x = 48
        tags = []
        for tool in tools:
            label = tool.upper()
            w = len(label) * 11 + 36
            tags.append(
                f'<rect x="{x}" y="{y + 16}" width="{w}" height="48" fill="#fffdf8" stroke="{INK}" stroke-width="2"/>'
                f'<rect x="{x}" y="{y + 16}" width="10" height="48" fill="#1d4e89"/>'
                f'<rect x="{x + w - 10}" y="{y + 16}" width="10" height="48" fill="#c0392b"/>'
                f'<text x="{x + w / 2:.0f}" y="{y + 46}" text-anchor="middle" font-family="{SERIF}" font-size="16" font-weight="700" fill="{INK}">{esc(label)}</text>'
            )
            x += w + 12
        rows.append("".join(tags))
        y += 100
    height = y + 24
    body = f'''  <rect width="1200" height="{height}" fill="{t["page"]}"/>
  <text x="48" y="64" font-family="{SERIF}" font-size="32" font-weight="700" fill="{t["ink"]}">Airmail</text>
  <text x="200" y="64" font-family="{SERIF}" font-size="16" font-style="italic" fill="{t["muted"]}">the toolbox, labelled for abroad</text>
  {"".join(rows)}'''
    tools = "; ".join(f"{g.title()}: {', '.join(ts)}" for g, ts in TOOL_GROUPS)
    return svg(1200, height, "Airmail", f"Toolbox as airmail stickers. {tools}.", body)


BUTTONS = {
    "email": ("EMAIL", "nigmucode@gmail.com"),
    "x": ("X", "@nigmu7161"),
    "linkedin": ("LINKEDIN", "nigamananda-behera"),
}


def sticker(slug: str) -> str:
    title, handle = BUTTONS[slug]
    body = f'''  <rect width="360" height="110" fill="#fffdf8" stroke="{INK}" stroke-width="3"/>
  <rect width="16" height="110" fill="#1d4e89"/>
  <rect x="344" width="16" height="110" fill="#c0392b"/>
  <text x="40" y="48" font-family="{SERIF}" font-size="22" font-weight="700" fill="{INK}">{title}</text>
  <text x="40" y="78" font-family="{SERIF}" font-size="15" font-style="italic" fill="#a33b32">{esc(handle)}</text>'''
    return svg(360, 110, f"{title} sticker", f"Airmail sticker: {title}, {handle}.", body)


def footer(t: dict) -> str:
    odia = load_glyph("odia-bold")
    tf, w, _ = fitted(odia, 0, 0, height=46)
    body = f'''  <rect width="1200" height="180" fill="{t["page"]}"/>
  {postmark(180, 90, t["ink"])}
  <g transform="translate({600 - w / 2:.0f} 48)"><g transform="{tf}">{glyph_paths(odia, f'fill="{t["ink"]}"')}</g></g>
  <text x="600" y="140" text-anchor="middle" font-family="{SERIF}" font-size="16" font-style="italic" fill="{t["muted"]}">posted with thanks</text>'''
    return svg(1200, 180, "Posted with thanks", "A postmark and the Odia greeting namaskar. Posted with thanks.", body, MOTION)


def build() -> dict[str, str]:
    files: dict[str, str] = {}
    for theme, palette in THEMES.items():
        files[f"assets/hero-{theme}.svg"] = hero(palette)
        files[f"assets/values-{theme}.svg"] = values(palette)
        files[f"assets/airmail-{theme}.svg"] = airmail(palette)
        files[f"assets/footer-{theme}.svg"] = footer(palette)
    for index, (slug, name, _) in enumerate(PROJECTS):
        files[f"assets/stamps/{slug}.svg"] = stamp(slug, name, index)
    for slug in BUTTONS:
        files[f"assets/stickers/{slug}.svg"] = sticker(slug)
    return files
