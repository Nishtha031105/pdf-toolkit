import base64
import pymupdf
from app.errors import AppError, translate_errors
from app.processors.pdf_common import open_pdf

def render_page_previews(source: dict, width: int, max_pages: int) -> list[str]:
    with translate_errors("Could not generate page previews for this PDF."):
        with open_pdf(source["path"], source["label"]) as pdf:
            if pdf.page_count > max_pages: raise AppError(f"This PDF has {pdf.page_count} pages. Reordering supports up to {max_pages}.")
            result = []
            for page in pdf:
                zoom = width / (page.rect.width or width)
                pixmap = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
                result.append("data:image/jpeg;base64," + base64.b64encode(pixmap.tobytes("jpeg", jpg_quality=70)).decode("ascii"))
            return result
