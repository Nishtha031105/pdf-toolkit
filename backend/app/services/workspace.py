import shutil
import tempfile
from pathlib import Path
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

class Workspace:
    def __init__(self) -> None:
        self.path = Path(tempfile.mkdtemp(prefix="pdftoolkit_"))
    def cleanup(self) -> None:
        shutil.rmtree(self.path, ignore_errors=True)
    def __enter__(self) -> "Workspace":
        return self
    def __exit__(self, *exc_info: object) -> None:
        self.cleanup()
    def file_response(self, file_path: Path, download_name: str, media_type: str) -> FileResponse:
        return FileResponse(file_path, media_type=media_type, filename=download_name, background=BackgroundTask(self.cleanup))
