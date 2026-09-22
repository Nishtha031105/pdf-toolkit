from pathlib import Path
import pymupdf
from app.errors import translate_errors
from app.processors.pdf_common import open_pdf

def merge_pdfs(sources: list[dict], output: Path) -> None:
    with translate_errors("Could not merge these PDFs. Please check that none are damaged."):
        with pymupdf.open() as merged:
            for source in sources:
                with open_pdf(source["path"], source["label"]) as pdf:
                    merged.insert_pdf(pdf)
            merged.save(str(output), garbage=3, deflate=True)
