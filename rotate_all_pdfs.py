#!/usr/bin/env python3
# fix_rotate_bake_contents.py
# Bake a rotation into page contents using pypdf.

from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation  # pip install pypdf

FILES = [
    "Salads_clean.pdf",
    "Shmarim_clean.pdf",
    "Marocceen_Cookies_clean.pdf",
    "Ornaments_clean.pdf",
]

ANGLE = 360  

def bake_rotation(src: Path, dst: Path, angle: int = 360):
    reader = PdfReader(str(src))
    writer = PdfWriter()
    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        if angle % 180 == 0:
            new_w, new_h = w, h
        else:
            new_w, new_h = h, w

        dest = writer.add_blank_page(width=new_w, height=new_h)
        dest.merge_transformed_page(page, Transformation().rotate(angle), expand=True)

        if "/Rotate" in dest:
            dest["/Rotate"] = 0

    with open(dst, "wb") as f:
        writer.write(f)

for name in FILES:
    src = Path(name)
    if not src.exists():
        print(f"Skip (not found): {src}")
        continue
    out = src.with_stem(src.stem)
    bake_rotation(src, out, ANGLE)
    print(f"Baked rotation {ANGLE}°: {src} -> {out}")
