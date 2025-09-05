# remove_empty_pages.py
# Usage:
#   python remove_empty_pages.py input.pdf output.pdf --threshold 0.995 --zoom 2.0
#
# The script considers a page "blank" if at least `threshold` fraction of pixels
# are white when rendered in grayscale at the chosen zoom factor (about DPI).
# It also treats pages with no content stream as empty.

import argparse
import fitz  # PyMuPDF

def is_blank_page(page, threshold=0.995, zoom=2.0):
    """
    Return True if the page is blank based on:
    1) No content stream (/Contents) -> definitely blank
    2) Visual check: render to grayscale and measure white pixel ratio
    """

    try:
        if page.get_contents() == []:  
            return True
    except Exception:
        
        pass

    
    mat = fitz.Matrix(zoom, zoom)  
    pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)  
    if pix.alpha: 
        pix = fitz.Pixmap(pix, 0)

    total_pixels = pix.width * pix.height
    white_pixels = pix.samples.count(255)  
    near_white = sum(b >= 250 for b in pix.samples)
    white_pixels = max(white_pixels, near_white)

    white_ratio = white_pixels / total_pixels if total_pixels else 1.0
    return white_ratio >= threshold

def remove_empty_pages(input_pdf, output_pdf, threshold=0.995, zoom=2.0):
    doc = fitz.open(input_pdf)
    keep_pages = []
    for pno in range(len(doc)):
        page = doc.load_page(pno)
        if not is_blank_page(page, threshold=threshold, zoom=zoom):
            keep_pages.append(pno)

    # Write only the kept pages to a new PDF
    new_doc = fitz.open()
    for pno in keep_pages:
        new_doc.insert_pdf(doc, from_page=pno, to_page=pno)
    new_doc.save(output_pdf)
    new_doc.close()
    doc.close()

    print(f"Total pages: {pno + 1}")
    print(f"Kept pages: {len(keep_pages)}")
    print(f"Removed pages: {pno + 1 - len(keep_pages)}")
    print(f"Output written to: {output_pdf}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Remove empty/blank pages from a PDF.")
    ap.add_argument("input_pdf", help="Path to input PDF")
    ap.add_argument("output_pdf", help="Path to output PDF (filtered)")
    ap.add_argument("--threshold", type=float, default=0.995,
                    help="Fraction of white pixels to consider a page blank (default: 0.995)")
    ap.add_argument("--zoom", type=float, default=2.0,
                    help="Rendering zoom factor for analysis (default: 2.0)")
    args = ap.parse_args()

    remove_empty_pages(args.input_pdf, args.output_pdf, threshold=args.threshold, zoom=args.zoom)
