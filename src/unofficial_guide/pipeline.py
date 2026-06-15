from __future__ import annotations

from pathlib import Path

from .config import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE, DEFAULT_TOP_K, CHROMA_DIR, DOCUMENTS_DIR
from .embedding import build_vector_store, retrieve_chunks
from .generation import generate_answer


def rebuild_index(documents_dir: Path = DOCUMENTS_DIR, persist_dir: Path = CHROMA_DIR) -> int:
    return build_vector_store(
        documents_dir=documents_dir,
        persist_dir=persist_dir,
        chunk_size=DEFAULT_CHUNK_SIZE,
        overlap=DEFAULT_CHUNK_OVERLAP,
    )


def ask(question: str, persist_dir: Path = CHROMA_DIR, top_k: int = DEFAULT_TOP_K) -> dict[str, object]:
    retrieved = retrieve_chunks(question, persist_dir=persist_dir, top_k=top_k)
    answer = generate_answer(question, retrieved)
    sources = []
    for chunk in retrieved:
        metadata = chunk["metadata"]
        source = f"{metadata['document_title']} ({metadata['source_path']})"
        if source not in sources:
            sources.append(source)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved,
    }
