from __future__ import annotations

from pathlib import Path

from .cleaning import clean_text
from .models import SourceDocument


def _read_pdf(path: Path) -> str:
    try:
        import pdfplumber
    except ImportError as exc:  # pragma: no cover - import guard
        raise RuntimeError("pdfplumber is required to read PDF files") from exc

    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text() or ""
            if extracted.strip():
                pages.append(extracted)
    return "\n\n".join(pages)


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_source_documents(documents_dir: Path) -> list[SourceDocument]:
    if not documents_dir.exists():
        return []

    documents: list[SourceDocument] = []
    for path in sorted(p for p in documents_dir.rglob("*") if p.is_file()):
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md", ".markdown"}:
            raw_text = _read_text_file(path)
        elif suffix == ".pdf":
            raw_text = _read_pdf(path)
        elif suffix in {".html", ".htm"}:
            raw_text = _read_text_file(path)
        else:
            continue

        cleaned = clean_text(raw_text)
        if cleaned:
            documents.append(SourceDocument(path=path, title=path.stem, text=cleaned))

    return documents
