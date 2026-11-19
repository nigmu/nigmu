#!/usr/bin/env python3
"""Build the alternate profile designs under designs/.

Art is deterministic and offline. Headline lettering is outlined once with
`--trace` (needs fonttools and uharfbuzz plus the Noto fonts) so other machines
do not need the fonts. Language charts read scripts/data/languages.json, which
`--refresh-languages` rewrites from Nigam's public repositories.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_profile_assets as base  # noqa: E402
from designs import arcade, comic, fm, garden, market, mission, pattachitra, stamps  # noqa: E402
from designs.common import DESIGNS, GLYPHS, LANGUAGES, ROOT  # noqa: E402

NOTO = "/usr/share/fonts/truetype/noto"

TRACES = {
    "fm-nigam": (f"{NOTO}/NotoSansDisplay-Black.ttf", "NIGAM", 150, 6),
    "comic-nigam": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "NIGAM", 200, 4),
    "comic-amazing": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "THE AMAZING", 64, 3),
    "comic-kaching": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "KA-CHING!", 100, 2),
    "comic-tada": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "TA-DA!", 100, 2),
    "comic-zap": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "ZAP!", 100, 2),
    "comic-whoosh": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "WHOOSH!", 100, 2),
    "comic-thud": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "THUD!", 100, 2),
    "comic-power": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "POWER LEVELS!", 80, 2),
    "comic-arsenal": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "THE ARSENAL!", 80, 2),
    "comic-continued": (f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf", "TO BE CONTINUED...", 80, 2),
    "odia-bold": (f"{NOTO}/NotoSansOriya-Bold.ttf", "ନମସ୍କାର", 80, 0),
    "patta-nigam": (f"{NOTO}/NotoSerifDisplay-CondensedExtraBold.ttf", "Nigam", 150, 2),
}

BUILDERS = {
    "nigam-fm": fm.build,
    "comic": comic.build,
    "pattachitra": pattachitra.build,
    "arcade": arcade.build,
    "mission": mission.build,
    "stamps": stamps.build,
    "market": market.build,
    "garden": garden.build,
}


def trace(font_path: str, text: str, size: float, tracking: float) -> dict:
    import uharfbuzz as hb
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    face = hb.Face(hb.Blob.from_file_path(font_path))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb.Font(face), buf, {})

    tt = TTFont(font_path)
    glyphset = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / tt["head"].unitsPerEm
    cursor = 0.0
    placed = []
    minx = miny = 1e9
    maxx = maxy = -1e9
    count = len(buf.glyph_infos)
    for index, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        name = order[info.codepoint]
        tx = cursor + pos.x_offset * scale
        ty = -pos.y_offset * scale
        bounds = BoundsPen(glyphset)
        glyphset[name].draw(bounds)
        if bounds.bounds:
            x0, y0, x1, y1 = bounds.bounds
            minx = min(minx, scale * x0 + tx)
            maxx = max(maxx, scale * x1 + tx)
            miny = min(miny, -scale * y1 + ty)
            maxy = max(maxy, -scale * y0 + ty)
        placed.append((name, tx, ty))
        cursor += pos.x_advance * scale
        if index != count - 1:
            cursor += tracking

    paths = []
    for name, tx, ty in placed:
        pen = SVGPathPen(glyphset)
        glyphset[name].draw(TransformPen(pen, (scale, 0, 0, -scale, tx - minx, ty - miny)))
        commands = pen.getCommands()
        if commands:
            paths.append(base.quantize(commands))
    return {"width": round(maxx - minx, 2), "height": round(maxy - miny, 2), "paths": paths}


def build_all() -> dict[str, str]:
    files: dict[str, str] = {}
    for name, builder in BUILDERS.items():
        for rel, text in builder().items():
            files[f"designs/{name}/{rel}"] = text
    return files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", action="store_true", help="re-outline headline lettering from local fonts")
    parser.add_argument("--refresh-languages", action="store_true", help="rewrite the language snapshot from the GitHub API")
    parser.add_argument("--check", action="store_true", help="fail if committed design art differs")
    args = parser.parse_args()

    if args.trace:
        for name, spec in TRACES.items():
            data = trace(*spec)
            (GLYPHS / f"{name}.json").write_text(json.dumps(data))
            print(f"traced {name} {data['width']}x{data['height']}")

    if args.refresh_languages:
        totals = base.public_language_bytes()
        ranked = dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))
        LANGUAGES.parent.mkdir(parents=True, exist_ok=True)
        LANGUAGES.write_text(json.dumps(ranked, indent=2) + "\n")
        print(f"wrote {LANGUAGES.relative_to(ROOT)}")

    files = build_all()
    if args.check:
        drifted = []
        for rel, text in files.items():
            path = ROOT / rel
            current = path.read_text() if path.exists() else ""
            if current.rstrip("\n") != text.rstrip("\n"):
                drifted.append(rel)
        for name in BUILDERS:
            base.check_readme((DESIGNS / name / "README.md").read_text())
        if drifted:
            raise SystemExit("design art drift: " + ", ".join(drifted))
        print(f"design art matches ({len(files)} files)")
    else:
        for rel, text in files.items():
            base.write(ROOT / rel, text)
        print(f"wrote {len(files)} design files")


if __name__ == "__main__":
    main()
