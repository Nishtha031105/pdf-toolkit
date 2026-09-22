from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.config import settings
from app.dependencies import get_current_user
from app.processors.preview import render_page_previews
from app.processors.shuffle import reorder_pdf
from app.schemas import PagePreviewsResponse
from app.services.upload_service import PDF_EXTENSIONS, download_stem, save_upload
from app.services.workspace import Workspace
router = APIRouter(prefix="/tools/shuffle-pdf", tags=["shuffle"], dependencies=[Depends(get_current_user)])
@router.post("/preview", response_model=PagePreviewsResponse)
def preview(file: UploadFile = File(...)) -> PagePreviewsResponse:
    with Workspace() as workspace:
        source = save_upload(file, workspace.path, PDF_EXTENSIONS); pages = render_page_previews(source, settings.thumbnail_width, settings.max_preview_pages)
    return PagePreviewsResponse(page_count=len(pages), pages=pages)
@router.post("")
def shuffle(file: UploadFile = File(...), order: str = Form(..., max_length=5000)):
    workspace = Workspace()
    try:
        source = save_upload(file, workspace.path, PDF_EXTENSIONS); name = f"{download_stem(file.filename)}_shuffled.pdf"; output = workspace.path / "shuffled.pdf"; reorder_pdf(source, order, output)
    except Exception:
        workspace.cleanup(); raise
    return workspace.file_response(output, name, "application/pdf")
