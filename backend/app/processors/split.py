import re
from pathlib import Path
import pymupdf
from app.config import settings
from app.errors import AppError, translate_errors
from app.processors.pdf_common import open_pdf
_TOKEN = re.compile(r"([0-9]{1,6})\s*(?:-\s*([0-9]{1,6}))?")

def parse_page_ranges(spec: str, page_count: int) -> list[tuple[int, int]]:
    tokens = [token.strip() for token in spec.split(",") if token.strip()]
    if not tokens: raise AppError("Enter at least one page or range, for example: 1-3, 5.")
    ranges = []
    for token in tokens:
        match = _TOKEN.fullmatch(token)
        if not match: raise AppError(f'"{token}" is not a valid page or range. Use a format like 1-3, 5.')
        start, end = int(match.group(1)), int(match.group(2) or match.group(1))
        if start < 1 or end > page_count: raise AppError(f'"{token}" is outside the document, which has {page_count} page(s).')
        if start > end: raise AppError(f'"{token}" is backwards: the first page must come before the last.')
        ranges.append((start, end))
    return ranges

def get_page_count_for_split(source: dict) -> int:
    with open_pdf(source["path"], source["label"]) as pdf: return pdf.page_count

def split_pdf(source: dict, spec: str, mode: str, output_dir: Path, stem: str) -> list[Path]:
    with translate_errors("Could not split this PDF."):
        with open_pdf(source["path"], source["label"]) as pdf:
            ranges = parse_page_ranges(spec, pdf.page_count)
            groups = [(page, page) for start, end in ranges for page in range(start, end + 1)] if mode == "pages" else ranges
            groups = list(dict.fromkeys(groups))
            if len(groups) > settings.max_split_outputs: raise AppError(f"That would create {len(groups)} files. The limit is {settings.max_split_outputs}.")
            outputs = []
            for start, end in groups:
                destination = output_dir / (f"{stem}_page_{start}.pdf" if start == end else f"{stem}_pages_{start}-{end}.pdf")
                with pymupdf.open() as part:
                    part.insert_pdf(pdf, from_page=start - 1, to_page=end - 1)
                    part.save(str(destination), garbage=3, deflate=True)
                outputs.append(destination)
            return outputs
