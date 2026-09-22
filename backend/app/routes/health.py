import PIL
import pymupdf
from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Confirms the API is up and that the PDF libraries import correctly."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "pymupdf_version": str(pymupdf.VersionBind),
        "pillow_version": PIL.__version__,
    }
