from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from app.processors.pdf_tools import info_from_pdf, merge_pdfs, split_pdf

router = APIRouter(prefix="/pdf", tags=["pdf"])


@router.post("/info")
def get_pdf_info(file: Annotated[UploadFile, File(...)]) -> dict[str, object]:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    content = file.file.read()
    return info_from_pdf(content)


@router.post("/merge")
def merge_pdf_files(files: list[UploadFile] = File(...)) -> Response:
    if not files:
        raise HTTPException(status_code=400, detail="Please upload at least one PDF file")

    payload = []
    for uploaded in files:
        if not uploaded.filename or not uploaded.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Invalid file: {uploaded.filename}")
        payload.append(uploaded.file.read())

    pdf_bytes = merge_pdfs(payload)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=merged.pdf"})


@router.post("/split")
def split_pdf_file(
    file: Annotated[UploadFile, File(...)],
    pages: Annotated[str, Form(...)],
) -> list[bytes]:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    try:
        page_numbers = [int(part.strip()) for part in pages.split(",") if part.strip()]
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Pages must be comma-separated integers") from exc

    pdf_bytes = file.file.read()
    return split_pdf(pdf_bytes, page_numbers)
