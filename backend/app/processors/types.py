from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class SourceFile:
    path: Path
    label: str
    size: int = 0
