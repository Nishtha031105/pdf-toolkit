import re
from pathlib import Path
from fastapi import UploadFile
from app.config import settings
from app.errors import AppError

IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png"})
PDF_EXTENSIONS = frozenset({".pdf"})
CHUNK_SIZE = 1024 * 1024

def display_name(filename: str | None) -> str:
    return (Path(filename or "").name or "file")[:80]

def download_stem(filename: str | None, fallback: str = "document") -> str:
    cleaned = re.sub(r"[^\w.-]+", "_", Path(filename or "").stem).strip("._")
    return cleaned[:60] or fallback

def save_upload(upload: UploadFile, directory: Path, allowed_extensions: frozenset[str], index: int = 0):
    label = display_name(upload.filename)
    suffix = Path(label).suffix.lower()
    if suffix not in allowed_extensions:
        raise AppError(f'"{label}" is not a supported file type. Allowed: {", ".join(sorted(allowed_extensions))}.', 415)
    destination = directory / f"upload_{index:03d}{suffix}"
    size = 0
    with destination.open("wb") as output:
        while chunk := upload.file.read(CHUNK_SIZE):
            size += len(chunk)
            if size > settings.max_file_size_bytes:
                raise AppError(f'"{label}" is larger than the {settings.max_file_size_mb} MB limit.', 413)
            output.write(chunk)
    if size == 0:
        raise AppError(f'"{label}" is empty.', 400)
    return {"path": destination, "label": label, "size": size}

def save_uploads(uploads: list[UploadFile], directory: Path, allowed_extensions: frozenset[str], min_files: int = 1):
    if len(uploads) < min_files:
        raise AppError(f"Please upload at least {min_files} file(s).", 400)
    if len(uploads) > settings.max_files_per_request:
        raise AppError(f"You can upload up to {settings.max_files_per_request} files at once.", 400)
    saved = []
    total = 0
    for index, upload in enumerate(uploads):
        source = save_upload(upload, directory, allowed_extensions, index)
        total += source["size"]
        if total > settings.max_total_upload_bytes:
            raise AppError(f"The files together exceed the {settings.max_total_upload_mb} MB limit.", 413)
        saved.append(source)
    return saved
