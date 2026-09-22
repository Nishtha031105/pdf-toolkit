from fastapi import APIRouter, Depends, File, UploadFile
from app.dependencies import get_current_user
from app.processors.merge import merge_pdfs
from app.services.upload_service import PDF_EXTENSIONS, save_uploads
from app.services.workspace import Workspace
router = APIRouter(prefix="/tools", tags=["merge"], dependencies=[Depends(get_current_user)])
@router.post("/merge-pdf")
def merge(files: list[UploadFile] = File(...)):
    workspace = Workspace()
    try:
        sources = save_uploads(files, workspace.path, PDF_EXTENSIONS, min_files=2); output = workspace.path / "merged.pdf"; merge_pdfs(sources, output)
    except Exception:
        workspace.cleanup(); raise
    return workspace.file_response(output, "merged.pdf", "application/pdf")
