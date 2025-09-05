#!/usr/bin/env python3
# fix_rotate_rasterize.py
# Rasterize each page with a rotation and rebuild the PDF.
import fitz  # PyMuPDF: pip install pymupdf
from pathlib import Path

FILES = [
    "Salads_clean.pdf",
    "Shmarim_clean.pdf",
    "Marocceen_Cookies_clean.pdf",
    "Ornaments_clean.pdf",
]

ANGLE = 180  # change to 90/180 as desired
DPI = 200

for name in FILES:
    src = Path(name)
    if not src.exists():
        print(f"Skip (not found): {src}")
        continue
    doc = fitz.open(src)
    out = fitz.open()
    for page in doc:
        # Render with rotation baked at chosen DPI
        mat = fitz.Matrix(DPI / 72, DPI / 72).preRotate(ANGLE)
        pix = page.get_pixmap(matrix=mat)
        # Create a new page sized to the rendered image and insert it
        new_page = out.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(new_page.rect, stream=pix.tobytes(), keep_proportion=False)
    dst = src.with_stem(src.stem + f"_raster{ANGLE}")
    out.save(dst)
    out.close()
    doc.close()
    print(f"Raster-baked rotation {ANGLE}°: {src} -> {dst}")
