"""Helpers shared by the three alternate profile designs."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import build_profile_assets as base  # noqa: E402

ROOT = base.ROOT
GLYPHS = base.GLYPHS
DESIGNS = ROOT / "designs"
LANGUAGES = SCRIPTS / "data" / "languages.json"

SANS = "'Segoe UI', Helvetica, Arial, sans-serif"
HEAVY = "'Arial Black', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SERIF = "Georgia, 'Times New Roman', serif"

PROJECTS = [
    ("trackmyspend", "TrackMySpend", "https://github.com/nigmu/TrackMySpend"),
    ("resume-ledger", "resume-ledger", "https://github.com/nigmu/resume-ledger"),
    ("odia-stt", "odia-STT", "https://github.com/nigmu/odia-STT"),
    ("clean-tv", "Clean_TV", "https://github.com/nigmu/Clean_TV_MiTV-MOOQ0"),
    ("bg-download", "bg_download", "https://github.com/nigmu/bg_download"),
    ("warehouse", "warehouse_management", "https://github.com/nigmu/warehouse_management"),
]

TOOL_GROUPS = [
    ("LANGUAGES", ["Python", "Kotlin", "Java", "JavaScript", "HTML", "CSS"]),
    ("BACKEND", ["FastAPI", "Django", "Flask", "Node.js", "PostgreSQL", "MySQL"]),
    ("DATA + ML", ["Pandas", "Seaborn", "scikit-learn", "TensorFlow", "PyTorch", "OpenCV"]),
    ("APPS + OPS", ["React", "Android", "Docker", "Linux", "Git"]),
]

REDUCED_MOTION = """
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
    }"""


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def svg(width: int, height: int, title: str, desc: str, body: str, style: str = "", defs: str = "") -> str:
    css = f"\n  <style>{style}{REDUCED_MOTION}\n  </style>"
    defs_block = f"\n  <defs>\n{defs}\n  </defs>" if defs else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
        f'  <title id="title">{esc(title)}</title>\n'
        f'  <desc id="desc">{esc(desc)}</desc>{defs_block}{css}\n'
        f"{body}\n</svg>\n"
    )


def load_glyph(name: str) -> dict:
    return base.load_glyph(name)


def glyph_paths(data: dict, attrs: str) -> str:
    paths = "".join(f'<path d="{d}"/>' for d in data["paths"])
    return f"<g {attrs}>{paths}</g>"


def fitted(data: dict, x: float, y: float, width: float | None = None, height: float | None = None) -> tuple[str, float, float]:
    """Return a transform placing glyph data at (x, y) scaled to a width or height."""
    if width is not None:
        s = width / data["width"]
    elif height is not None:
        s = height / data["height"]
    else:
        s = 1.0
    return f"translate({x:.1f} {y:.1f}) scale({s:.4f})", data["width"] * s, data["height"] * s


def language_rows(top: int = 8) -> list[tuple[str, float]]:
    totals: dict[str, int] = json.loads(LANGUAGES.read_text())
    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    rows = list(ranked[:top])
    other = sum(count for _, count in ranked[top:])
    if other:
        rows.append(("Other", other))
    total = sum(count for _, count in rows)
    return [(name, 100 * count / total) for name, count in rows]


def polar(cx: float, cy: float, r: float, degrees: float) -> tuple[float, float]:
    a = math.radians(degrees - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def star_points(cx: float, cy: float, r_out: float, r_in: float, spikes: int, jitter: float = 0.0, rx: float = 1.0) -> str:
    points = []
    for i in range(spikes * 2):
        r = r_out if i % 2 == 0 else r_in
        if jitter and i % 2 == 0:
            r *= 1 - jitter * (((i * 37) % 7) / 7)
        x, y = polar(cx, cy, r, 360 * i / (spikes * 2))
        points.append(f"{cx + (x - cx) * rx:.1f},{y:.1f}")
    return " ".join(points)


def arc_band(cx: float, cy: float, r_out: float, r_in: float, start: float, end: float) -> str:
    large = 1 if end - start > 180 else 0
    x1, y1 = polar(cx, cy, r_out, start)
    x2, y2 = polar(cx, cy, r_out, end)
    x3, y3 = polar(cx, cy, r_in, end)
    x4, y4 = polar(cx, cy, r_in, start)
    return (
        f"M{x1:.1f} {y1:.1f} A{r_out} {r_out} 0 {large} 1 {x2:.1f} {y2:.1f} "
        f"L{x3:.1f} {y3:.1f} A{r_in} {r_in} 0 {large} 0 {x4:.1f} {y4:.1f}Z"
    )


def rand(seed: int) -> float:
    """Deterministic 0..1 noise so builds are reproducible."""
    x = math.sin(seed * 12.9898 + 78.233) * 43758.5453
    return x - math.floor(x)


def meter(pct: float) -> float:
    """Compressed 0..1 level so a small share stays visible. Not the percentage."""
    return max(0.08, min(1.0, 1 + math.log10(max(pct, 0.01) / 100) / 2.4))


TAGLINES = {
    "trackmyspend": "bank SMS → ledger",
    "resume-ledger": "a resume for each job",
    "odia-stt": "Odia speech → text",
    "clean-tv": "a calmer Android TV",
    "bg-download": "wallpapers, fetched",
    "warehouse": "Django + React WMS",
}
