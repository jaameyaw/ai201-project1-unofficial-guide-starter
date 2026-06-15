from __future__ import annotations

from .models import Chunk, SourceDocument


def _move_to_boundary(text: str, index: int) -> int:
    boundary = max(
        text.rfind("\n\n", 0, index),
        text.rfind(". ", 0, index),
        text.rfind("! ", 0, index),
        text.rfind("? ", 0, index),
    )
    if boundary == -1:
        return index
    return boundary + 2


def chunk_document(document: SourceDocument, chunk_size: int, overlap: int) -> list[Chunk]:
    text = document.text.strip()
    if not text:
        return []

    chunks: list[Chunk] = []
    start = 0
    chunk_index = 0
    total_length = len(text)

    while start < total_length:
        end = min(total_length, start + chunk_size)
        if end < total_length:
            adjusted_end = _move_to_boundary(text, end)
            if adjusted_end > start + 100:
                end = min(adjusted_end, total_length)

        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(
                Chunk(
                    chunk_id=f"{document.path.stem}-{chunk_index}",
                    document_title=document.title,
                    source_path=str(document.path),
                    chunk_index=chunk_index,
                    text=chunk_text,
                    start_char=start,
                    end_char=end,
                )
            )

        if end >= total_length:
            break

        next_start = max(0, end - overlap)
        if next_start <= start:
            next_start = end
        while next_start < total_length and text[next_start].isspace():
            next_start += 1
        start = next_start
        chunk_index += 1

    return chunks


def chunk_documents(documents: list[SourceDocument], chunk_size: int, overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(chunk_document(document, chunk_size=chunk_size, overlap=overlap))
    return chunks
