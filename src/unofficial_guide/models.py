from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SourceDocument:
    path: Path
    title: str
    text: str


@dataclass(slots=True)
class Chunk:
    chunk_id: str
    document_title: str
    source_path: str
    chunk_index: int
    text: str
    start_char: int
    end_char: int


@dataclass(slots=True)
class RetrievedChunk:
    chunk_id: str
    document_title: str
    source_path: str
    chunk_index: int
    text: str
    distance: float
