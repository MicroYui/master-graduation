"""Repack the existing four-panel vector plots without changing plotted data.

The original PDFs stay untouched. Coordinates below are in PDF points measured
from the top left of the original 345.83 x 323.15 pt pages. Each panel keeps its
axes, tick labels, title, curves and error bars; only the surrounding whitespace
and the gaps between panels are reduced.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures/rq3"
WIDTH, HEIGHT = 324.0, 295.0
# (source left, top, right, bottom), (destination left, top)
PANELS = [
    ((14, 3, 170, 133), (2, 2)),
    ((188, 3, 344, 133), (166, 2)),
    ((14, 156, 170, 285), (2, 140)),
    ((188, 156, 344, 285), (166, 140)),
]
manifest = []
for name in ("01_fading", "02_feedback", "03_deadline", "04_energy", "05_ablation"):
    source = FIGURES / f"{name}.pdf"
    reader = PdfReader(source)
    original = reader.pages[0]
    original_width = float(original.mediabox.width)
    original_height = float(original.mediabox.height)
    assert abs(original_width - 345.826772) < 0.01
    assert abs(original_height - 323.149606) < 0.01
    writer = PdfWriter()
    output = writer.add_blank_page(WIDTH, HEIGHT)
    regions = PANELS + [
        ((0, 285.25, original_width, 307), ((WIDTH - original_width) / 2, 271.25))
    ]
    for (left, top, right, bottom), (target_left, target_top) in regions:
        panel = deepcopy(original)
        panel.cropbox = RectangleObject(
            (left, original_height - bottom, right, original_height - top)
        )
        move = Transformation().translate(
            target_left - left,
            HEIGHT - target_top - (bottom - top) - (original_height - bottom),
        )
        output.merge_transformed_page(panel, move, expand=False)
    output.compress_content_streams()
    writer.add_metadata({
        "/Title": f"{name}: compact layout",
        "/Subject": "Repacked original vector panels; data and original assets unchanged",
    })
    destination = FIGURES / f"{name}_compact.pdf"
    with destination.open("wb") as stream:
        writer.write(stream)
    manifest.append({
        "source": source.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "output": destination.relative_to(ROOT).as_posix(),
        "source_size_pt": [original_width, original_height],
        "output_size_pt": [WIDTH, HEIGHT],
        "regions": regions,
    })
qa = ROOT / "build/qa/thesis-condense-20261027"
qa.mkdir(parents=True, exist_ok=True)
(qa / "rq3_compaction.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"Repacked {len(manifest)} vector figures; originals retained.")
