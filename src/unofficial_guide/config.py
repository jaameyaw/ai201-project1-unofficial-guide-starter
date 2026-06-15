from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = ROOT_DIR / "documents"
CHROMA_DIR = ROOT_DIR / "chroma_db"

COLLECTION_NAME = "unofficial_guide"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 150
DEFAULT_TOP_K = 4

load_dotenv(ROOT_DIR / ".env")
