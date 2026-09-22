from typing import Literal
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.dependencies import get_current_user
from app.processors.split import get_page_count_for_split, split_pdf
from app.schemas import PdfInfoResponse
from app.services.archive_service import zip_files
from app.services.upload_service import PDF_EXTENSIONS, download_stem, save_upload
from app.services.workspace import Workspace
router = APIRouter(prefix="/tools/split-pdf", tags=["split"], dependencies=[Depends(get_current_user)])
@router.post("/info", response_model=PdfInfoResponse)
def pdf_info(file: UploadFile = File(...)) -> PdfInfoResponse:
    with Workspace() as workspace:
        source = save_upload(file, workspace.path, PDF_EXTENSIONS); count = get_page_count_for_split(source)
    return PdfInfoResponse(filename=source["label"], page_count=count)
@router.post("")
def split(file: UploadFile = File(...), ranges: str = Form(..., max_length=500), mode: Literal["ranges", "pages"] = Form("ranges")):
    workspace = Workspace()
    try:
        source = save_upload(file, workspace.path, PDF_EXTENSIONS); stem = download_stem(file.filename); parts_dir = workspace.path / "parts"; parts_dir.mkdir(); parts = split_pdf(source, ranges, mode, parts_dir, stem)
        if len(parts) == 1: output, name, media = parts[0], parts[0].name, "application/pdf"
        else: name = f"{stem}_split.zip"; output = workspace.path / name; zip_files(parts, output); media = "application/zip"
    except Exception:
        workspace.cleanup(); raise
    return workspace.file_response(output, name, media)
