import io
from pathlib import Path
import pymupdf
from PIL import Image, ImageOps
from app.errors import translate_errors, AppError
A4_WIDTH, A4_HEIGHT, A4_MARGIN = 595, 842, 24

def images_to_pdf(sources: list[dict], output: Path, page_size: str) -> None:
    with translate_errors("Could not create the PDF from these images."):
        with pymupdf.open() as document:
            for source in sources:
                try:
                    with Image.open(source["path"]) as image:
                        if image.format not in {"JPEG", "PNG"}: raise AppError(f'"{source["label"]}" is not a real JPG or PNG image.', 422)
                        image = ImageOps.exif_transpose(image).convert("RGB")
                        buffer = io.BytesIO(); image.save(buffer, format="JPEG", quality=95)
                        width, height = image.size
                except AppError: raise
                except Exception: raise AppError(f'"{source["label"]}" could not be read as an image. It may be corrupted.', 422) from None
                if page_size == "fit":
                    scale = A4_HEIGHT / max(width, height); page = document.new_page(width=width * scale, height=height * scale); target = page.rect
                else:
                    landscape = width > height; page_width, page_height = (A4_HEIGHT, A4_WIDTH) if landscape else (A4_WIDTH, A4_HEIGHT)
                    page = document.new_page(width=page_width, height=page_height); target = pymupdf.Rect(A4_MARGIN, A4_MARGIN, page_width - A4_MARGIN, page_height - A4_MARGIN)
                page.insert_image(target, stream=buffer.getvalue(), keep_proportion=True)
            document.save(str(output), garbage=3, deflate=True)
