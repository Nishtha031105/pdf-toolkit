import io

import fitz
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _make_pdf_bytes(page_count: int = 1) -> bytes:
    doc = fitz.open()
    for idx in range(page_count):
        page = doc.new_page()
        page.insert_text((72, 72), f"Page {idx + 1}")
    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    return buffer.getvalue()


def test_pdf_info_route() -> None:
    response = client.post(
        "/api/pdf/info",
        files={"file": ("sample.pdf", _make_pdf_bytes(2), "application/pdf")},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["page_count"] == 2
    assert data["title"]


def test_pdf_merge_route() -> None:
    first = _make_pdf_bytes(1)
    second = _make_pdf_bytes(2)
    response = client.post(
        "/api/pdf/merge",
        files=[
            ("files", ("first.pdf", first, "application/pdf")),
            ("files", ("second.pdf", second, "application/pdf")),
        ],
    )
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("application/pdf")
