from pathlib import Path
import pymupdf
from app.errors import AppError

def open_pdf(path: Path, label: str) -> pymupdf.Document:
    try:
        with path.open("rb") as handle:
            if b"%PDF-" not in handle.read(1024):
                raise AppError(f'"{label}" is not a valid PDF file.', 422)
        document = pymupdf.open(str(path), filetype="pdf")
        if document.needs_pass or document.page_count == 0:
            document.close()
            raise AppError(f'"{label}" could not be opened or has no pages.', 422)
        return document
    except AppError:
        raise
    except Exception:
        raise AppError(f'"{label}" looks corrupted and could not be opened.', 422) from None
