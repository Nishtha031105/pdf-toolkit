from __future__ import annotations

import io
from pathlib import Path

import fitz


def info_from_pdf(file_bytes: bytes) -> dict[str, object]:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    try:
        title = doc.metadata.get("title") or "Untitled"
        page_sizes = []
        for page in doc:
            rect = page.rect
            page_sizes.append([float(rect.width), float(rect.height)])
        return {
            "page_count": len(doc),
            "title": title,
            "file_size_bytes": len(file_bytes),
            "page_sizes": page_sizes,
        }
    finally:
        doc.close()


def merge_pdfs(files: list[bytes]) -> bytes:
    if not files:
        raise ValueError("No files provided")

    output = fitz.open()
    try:
        for file_bytes in files:
            src = fitz.open(stream=file_bytes, filetype="pdf")
            try:
                output.insert_pdf(src)
            finally:
                src.close()

        buffer = io.BytesIO()
        output.save(buffer)
        return buffer.getvalue()
    finally:
        output.close()


def split_pdf(file_bytes: bytes, page_numbers: list[int]) -> list[bytes]:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    try:
        parts: list[bytes] = []
        for page_no in page_numbers:
            if page_no < 1 or page_no > len(doc):
                raise ValueError(f"Page number {page_no} is out of range")
            page_doc = fitz.open()
            try:
                page_doc.insert_pdf(doc, from_page=page_no - 1, to_page=page_no - 1)
                buffer = io.BytesIO()
                page_doc.save(buffer)
                parts.append(buffer.getvalue())
            finally:
                page_doc.close()
        return parts
    finally:
        doc.close()
