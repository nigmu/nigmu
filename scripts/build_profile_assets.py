#!/usr/bin/env python3
"""Build the profile art committed under assets/.

Banner, icons, and chips are deterministic and do not use the network.
`Nigam` and the Odia greeting are outlined once (`--trace`) so a later
machine does not need the fonts. `--languages` reads only Nigam's public
repositories.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLYPHS = Path(__file__).resolve().parent / "glyphs"
ASSETS = ROOT / "assets"
README = ROOT / "README.md"

LANG_START = "<!-- languages:start -->"
LANG_END = "<!-- languages:end -->"

REQUIRED = [
    "nigmucode@gmail.com",
    "https://x.com/nigmu7161",
    "https://linkedin.com/in/nigamananda-behera",
    "ukulele",
    "https://github.com/nigmu/TrackMySpend",
    "https://github.com/nigmu/resume-ledger",
    "https://github.com/nigmu/bg_download",
    "https://github.com/nigmu/odia-STT",
    "https://github.com/nigmu/Clean_TV_MiTV-MOOQ0",
    "https://github.com/nigmu/warehouse_management",
    "https://github.com/nigmu/WMS_DEPLOY_FRONTEND",
    "https://github.com/nigmu/neetcode-submissions",
    "https://github.com/nigmu/nigmu-parkinsons_disease_prediction",
    "FastAPI",
    "ElevenLabs Scribe v2",
    "Wallhaven",
    "Plasma",
]

# Slugs that must never appear. WMS_DEPLOY_FRONTEND is public and allowed.
FORBIDDEN = [
    "MI11X-Debloat",
    "madhu-smruti",
    "FoodTracker",
    "nigmu-debian-server",
    "Sahayak",
    "fast-api-project",
    "pyspark-practice",
    "banking-system",
    "warehouse_ui",
    "/WMS_DEPLOY)",
    "WMS_DEPLOY/",
    "java_practice",
    "nigmu/test_repo",
    "nigmu/portfolio",
    "count_private",
    "github-readme-stats",
    "shields.io",
    "komarev.com",
    "Svelte",
    "svelte",
]

THEMES = {
    "light": {
        "bg": "#f4f0e6",
        "ink": "#1c1915",
        "muted": "#7d756b",
        "teal": "#0f6e56",
        "amber": "#c9842a",
        "frame": "#e3dacb",
        "string": "#1c1915",
    },
    "dark": {
        "bg": "#121611",
        "ink": "#f4f0e6",
        "muted": "#b3a898",
        "teal": "#8fd0c3",
        "amber": "#e6b15c",
        "frame": "#343c36",
        "string": "#f4f0e6",
    },
}

CHIPS = [
    "Python",
    "Kotlin",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "FastAPI",
    "Django",
    "Flask",
    "React",
    "Node.js",
    "PostgreSQL",
    "MySQL",
    "Pandas",
    "Seaborn",
    "scikit-learn",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "Android",
    "Docker",
    "Linux",
    "Git",
]


def quantize(d: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return f"{float(match.group()):.1f}"

    return re.sub(r"-?\d+\.\d+(?:e[+-]?\d+)?", repl, d)


def trace_text(font_path: str, text: str, size: float, bold_tracking: float = 0) -> dict:
    import subprocess

    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    raw = subprocess.check_output(
        ["hb-shape", "--font-file", font_path, "--output-format=json", text],
        text=True,
    )
    glyphs = json.loads(raw)
    font = TTFont(font_path)
    glyphset = font.getGlyphSet()
    scale = size / font["head"].unitsPerEm
    cursor = 0.0
    placed = []
    minx = miny = 1e9
    maxx = maxy = -1e9
    for index, glyph in enumerate(glyphs):
        name = glyph["g"]
        tx = cursor + glyph["dx"] * scale
        ty = -(glyph["dy"] * scale)
        from fontTools.pens.boundsPen import BoundsPen

        bounds = BoundsPen(glyphset)
        glyphset[name].draw(bounds)
        if bounds.bounds:
            x0, y0, x1, y1 = bounds.bounds
            xs = [scale * x0 + tx, scale * x1 + tx]
            ys = [-scale * y0 + ty, -scale * y1 + ty]
            minx, maxx = min(minx, *xs), max(maxx, *xs)
            miny, maxy = min(miny, *ys), max(maxy, *ys)
        placed.append((name, tx, ty))
        cursor += glyph["ax"] * scale
        if index != len(glyphs) - 1:
            cursor += bold_tracking

    paths = []
    for name, tx, ty in placed:
        pen = SVGPathPen(glyphset)
        tpen = TransformPen(pen, (scale, 0, 0, -scale, tx - minx, ty - miny))
        glyphset[name].draw(tpen)
        commands = pen.getCommands()
        if commands:
            paths.append(quantize(commands))
    return {
        "width": round(maxx - minx, 2),
        "height": round(maxy - miny, 2),
        "paths": paths,
    }


def load_glyph(name: str) -> dict:
    return json.loads((GLYPHS / f"{name}.json").read_text())


def glyph_group(data: dict, fill: str) -> str:
    paths = "\n".join(f'    <path d="{d}"/>' for d in data["paths"])
    return f'<g fill="{fill}">\n{paths}\n  </g>'


def speech_wave(x0: float, x1: float, y: float, amp: float = 22) -> str:
    import math

    syllables = (
        (0.08, 0.028, 0.25),
        (0.20, 0.034, 1.0),
        (0.34, 0.02, 0.12),
        (0.46, 0.04, 0.82),
        (0.62, 0.022, 0.08),
        (0.76, 0.038, 1.0),
        (0.90, 0.03, 0.4),
    )
    points = []
    steps = 160
    for i in range(steps + 1):
        t = i / steps
        env = 0.0
        for center, width, height in syllables:
            env += height * math.exp(-((t - center) ** 2) / (2 * width * width))
        env = max(0.0, min(env, 1.0))
        yy = y + math.sin(t * math.pi * 9) * amp * env
        points.append((x0 + (x1 - x0) * t, yy))
    d = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
    d += "".join(f" L {x:.1f} {yy:.1f}" for x, yy in points[1:])
    return d


def banner(theme_name: str) -> str:
    color = THEMES[theme_name]
    nigam = load_glyph("nigam")
    odia = load_glyph("namaskar")
    wave = speech_wave(72, 1128, 348, 16)
    strings = [118, 154, 190, 226]
    string_lines = []
    for index, y in enumerate(strings):
        width = 1.7 if index == 1 else 1.15
        opacity = 0.85 if index == 1 else 0.38
        string_lines.append(
            f'<line x1="530" y1="{y}" x2="1132" y2="{y}" stroke="{color["string"]}" '
            f'stroke-width="{width}" stroke-linecap="round" opacity="{opacity}"/>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" role="img" aria-labelledby="title desc">
  <title id="title">Nigam</title>
  <desc id="desc">Poster for Nigam. Ukulele strings, a speech waveform, and the Odia greeting namaskar.</desc>
  <rect width="1200" height="420" fill="{color["bg"]}"/>
  <rect x="28" y="28" width="1144" height="364" rx="22" fill="none" stroke="{color["frame"]}" stroke-width="1.5"/>
  <rect x="508" y="104" width="10" height="136" rx="3" fill="{color["amber"]}"/>
  {chr(10).join(string_lines)}
  <g class="motion">
    <circle cx="820" cy="154" r="6.5" fill="{color["amber"]}">
      <animate attributeName="cx" values="820;1100;540;820" dur="8s" repeatCount="indefinite"/>
    </circle>
  </g>
  <g transform="translate(68 86)">
    {glyph_group(nigam, color["ink"])}
  </g>
  <g transform="translate(72 232)">
    {glyph_group(odia, color["teal"])}
  </g>
  <path d="{wave}" fill="none" stroke="{color["teal"]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="0.22"/>
  <path d="{wave}" fill="none" stroke="{color["teal"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2400" stroke-dashoffset="0">
    <animate attributeName="stroke-dashoffset" values="2200;0" dur="2.6s" fill="freeze" repeatCount="1"/>
  </path>
  <style>
    @media (prefers-reduced-motion: reduce) {{
      .motion {{ display: none; }}
    }}
  </style>
</svg>
'''


def icon(body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" role="img">
  <rect width="36" height="36" rx="10" fill="#0f6e56"/>
  {body}
</svg>
'''


def icons() -> dict[str, str]:
    cream = "#f6f3ec"
    return {
        "ledger": icon(
            f'<rect x="11" y="8" width="14" height="20" rx="2" fill="none" stroke="{cream}" stroke-width="1.6"/>'
            f'<path d="M14 14h8M14 18h8M14 22h5" fill="none" stroke="{cream}" stroke-width="1.4" stroke-linecap="round"/>'
        ),
        "resume": icon(
            f'<path d="M12 8h8l5 5v15H12V8z" fill="none" stroke="{cream}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M20 8v5h5" fill="none" stroke="{cream}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M15 18h7M15 22h5" fill="none" stroke="{cream}" stroke-width="1.4" stroke-linecap="round"/>'
        ),
        "screen": icon(
            f'<rect x="7" y="9" width="22" height="14" rx="2" fill="none" stroke="{cream}" stroke-width="1.6"/>'
            f'<path d="M18 23v4M13 27h10" fill="none" stroke="{cream}" stroke-width="1.6" stroke-linecap="round"/>'
        ),
        "wave": icon(
            f'<path d="M7 19c2.2-6 4.2-6 6.4 0s4.2 6 6.4 0 4.2-6 6.4 0 4.2 6 6.2 0" fill="none" stroke="{cream}" stroke-width="1.7" stroke-linecap="round"/>'
        ),
        "frames": icon(
            f'<rect x="7" y="13" width="14" height="12" rx="1.5" fill="none" stroke="{cream}" stroke-width="1.6"/>'
            f'<rect x="14" y="8" width="14" height="12" rx="1.5" fill="#0f6e56" stroke="{cream}" stroke-width="1.6"/>'
        ),
        "boxes": icon(
            f'<path d="M8 20h10v8H8zM16 15h10v8H16zM12 10h10v8H12z" fill="#0f6e56" stroke="{cream}" stroke-width="1.5" stroke-linejoin="round"/>'
        ),
    }


def chip(label: str) -> str:
    width = int(round(13 * 0.62 * len(label) + 26))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28" role="img" aria-label="{label}">
  <rect width="{width}" height="28" rx="14" fill="#0f6e56"/>
  <text x="{width / 2:.1f}" y="18" text-anchor="middle" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" fill="#f6f3ec">{label}</text>
</svg>
'''


def chip_filename(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-") + ".svg"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text)


def build_art() -> dict[str, str]:
    files: dict[str, str] = {}
    for theme in THEMES:
        files[f"assets/banner-{theme}.svg"] = banner(theme)
    for name, svg in icons().items():
        files[f"assets/icons/{name}.svg"] = svg
    for label in CHIPS:
        files[f"assets/chips/{chip_filename(label)}"] = chip(label)
    return files


def github_json(url: str) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "nigmu-profile-assets",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def public_language_bytes() -> dict[str, int]:
    totals: dict[str, int] = {}
    page = 1
    while True:
        repos = github_json(
            f"https://api.github.com/users/nigmu/repos?per_page=100&page={page}&type=owner"
        )
        if not isinstance(repos, list):
            raise SystemExit("unexpected repository listing")
        for repo in repos:
            if repo.get("private") or repo.get("fork") or repo["name"] == "nigmu":
                continue
            languages = github_json(repo["languages_url"])
            if not isinstance(languages, dict):
                continue
            for name, count in languages.items():
                totals[name] = totals.get(name, 0) + int(count)
        if len(repos) < 100:
            break
        page += 1
    if not totals:
        raise SystemExit("no public language bytes returned")
    return totals


def language_markdown(totals: dict[str, int]) -> str:
    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    top = ranked[:8]
    other = sum(count for _, count in ranked[8:])
    rows = list(top)
    if other:
        rows.append(("Other", other))
    total = sum(count for _, count in rows)
    label_width = max(len(label) for label, _ in rows)
    lines = ["public repository bytes, forks excluded", ""]
    for label, count in rows:
        pct = 100 * count / total
        filled = round(pct / 100 * 16)
        if pct >= 0.5 and filled == 0:
            filled = 1
        bar = "█" * filled + "░" * (16 - filled)
        lines.append(f"{label:<{label_width}}  {bar}  {pct:5.1f}%")
    return "```text\n" + "\n".join(lines) + "\n```"


def replace_languages(readme: str, block: str) -> str:
    if LANG_START not in readme or LANG_END not in readme:
        raise SystemExit("README is missing language markers")
    pattern = re.compile(
        re.escape(LANG_START) + r".*?" + re.escape(LANG_END),
        re.DOTALL,
    )
    return pattern.sub(f"{LANG_START}\n{block}\n{LANG_END}", readme, count=1)


def check_readme(text: str) -> None:
    missing = [item for item in REQUIRED if item not in text]
    found = [item for item in FORBIDDEN if item in text]
    if missing or found:
        raise SystemExit(f"readme check failed missing={missing} forbidden={found}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", action="store_true", help="rebuild outlined glyphs from local fonts")
    parser.add_argument("--check", action="store_true", help="fail if committed art differs")
    parser.add_argument("--write-languages", action="store_true")
    parser.add_argument("--languages-smoke", action="store_true")
    args = parser.parse_args()

    if args.trace:
        GLYPHS.mkdir(parents=True, exist_ok=True)
        nigam = trace_text(
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "Nigam",
            112,
            bold_tracking=-1.5,
        )
        odia = trace_text(
            "/usr/share/fonts/truetype/noto/NotoSansOriya-Regular.ttf",
            "ନମସ୍କାର",
            44,
        )
        (GLYPHS / "nigam.json").write_text(json.dumps(nigam))
        (GLYPHS / "namaskar.json").write_text(json.dumps(odia))
        print(f"traced Nigam {nigam['width']}x{nigam['height']} namaskar {odia['width']}x{odia['height']}")

    files = build_art()
    if args.check:
        drifted = []
        for rel, text in files.items():
            path = ROOT / rel
            current = path.read_text() if path.exists() else ""
            if not current.endswith("\n"):
                current += "\n"
            expected = text if text.endswith("\n") else text + "\n"
            if current != expected:
                drifted.append(rel)
        check_readme(README.read_text())
        if drifted:
            raise SystemExit("art drift: " + ", ".join(drifted))
        print("art matches")
    else:
        for rel, text in files.items():
            write(ROOT / rel, text)
        print(f"wrote {len(files)} files")

    if args.write_languages or args.languages_smoke:
        block = language_markdown(public_language_bytes())
        print(block)
        if "Python" not in block:
            raise SystemExit("language block did not include Python")
        if args.write_languages:
            write(README, replace_languages(README.read_text(), block))
            print("updated language block")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        sys.stderr.write(error.read().decode()[:500] + "\n")
        raise
