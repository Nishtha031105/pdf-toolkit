from pathlib import Path
import pymupdf
from app.errors import AppError, translate_errors
from app.processors.pdf_common import open_pdf

def parse_page_order(text: str, page_count: int) -> list[int]:
    try: order = [int(part) for part in text.split(",") if part.strip()]
    except ValueError: raise AppError("The page order is invalid.") from None
    if sorted(order) != list(range(1, page_count + 1)): raise AppError("The page order must include every page exactly once.")
    return order

def reorder_pdf(source: dict, order_text: str, output: Path) -> None:
    with translate_errors("Could not reorder the pages of this PDF."):
        with open_pdf(source["path"], source["label"]) as pdf:
            pdf.select([page - 1 for page in parse_page_order(order_text, pdf.page_count)])
            pdf.save(str(output), garbage=3, deflate=True)
