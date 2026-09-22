from typing import Literal
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.dependencies import get_current_user
from app.processors.images import images_to_pdf
from app.services.upload_service import IMAGE_EXTENSIONS, save_uploads
from app.services.workspace import Workspace
router = APIRouter(prefix="/tools", tags=["images"], dependencies=[Depends(get_current_user)])
@router.post("/images-to-pdf")
def create_pdf_from_images(files: list[UploadFile] = File(...), page_size: Literal["a4", "fit"] = Form("a4")):
    workspace = Workspace()
    try:
        sources = save_uploads(files, workspace.path, IMAGE_EXTENSIONS); output = workspace.path / "images.pdf"; images_to_pdf(sources, output, page_size)
    except Exception:
        workspace.cleanup(); raise
    return workspace.file_response(output, "images.pdf", "application/pdf")
