from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from .chunking import chunk_documents
from .config import COLLECTION_NAME, DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE, EMBEDDING_MODEL_NAME
from .ingestion import load_source_documents
from .models import Chunk


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def _chunk_to_record(chunk: Chunk) -> tuple[str, str, dict[str, object]]:
    return (
        chunk.chunk_id,
        chunk.text,
        {
            "document_title": chunk.document_title,
            "source_path": chunk.source_path,
            "chunk_index": chunk.chunk_index,
            "start_char": chunk.start_char,
            "end_char": chunk.end_char,
        },
    )


def build_vector_store(
    documents_dir: Path,
    persist_dir: Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> int:
    documents = load_source_documents(documents_dir)
    if not documents:
        raise RuntimeError(f"No supported documents were found in {documents_dir}")

    chunks = chunk_documents(documents, chunk_size=chunk_size, overlap=overlap)
    if not chunks:
        raise RuntimeError("Document loading succeeded, but no chunks were produced")

    model = get_embedding_model()
    texts = [chunk.text for chunk in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()

    persist_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(persist_dir))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

    ids: list[str] = []
    documents_payload: list[str] = []
    metadatas: list[dict[str, object]] = []
    for chunk in chunks:
        chunk_id, text, metadata = _chunk_to_record(chunk)
        ids.append(chunk_id)
        documents_payload.append(text)
        metadatas.append(metadata)

    collection.add(ids=ids, documents=documents_payload, embeddings=embeddings, metadatas=metadatas)
    return len(chunks)


def get_collection(persist_dir: Path):
    client = chromadb.PersistentClient(path=str(persist_dir))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def retrieve_chunks(query: str, persist_dir: Path, top_k: int) -> list[dict[str, object]]:
    collection = get_collection(persist_dir)
    model = get_embedding_model()
    query_embedding = model.encode([query], normalize_embeddings=True).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved: list[dict[str, object]] = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(documents, metadatas, distances, strict=False):
        retrieved.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": float(distance),
            }
        )

    return retrieved
