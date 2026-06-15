from __future__ import annotations

import os

from groq import Groq

from .config import GROQ_MODEL_NAME


def _format_context(retrieved_chunks: list[dict[str, object]]) -> str:
    blocks: list[str] = []
    for index, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]
        blocks.append(
            f"[Chunk {index}]\nSource: {metadata['document_title']}\nPath: {metadata['source_path']}\nDistance: {chunk['distance']:.3f}\nText: {chunk['text']}"
        )
    return "\n\n".join(blocks)


def generate_answer(question: str, retrieved_chunks: list[dict[str, object]]) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise RuntimeError("Set GROQ_API_KEY in your .env file to generate answers")

    if not retrieved_chunks:
        return "I don't have enough information to answer that from the available documents."

    client = Groq(api_key=api_key)
    context = _format_context(retrieved_chunks)
    system_prompt = (
        "You are answering questions about student-generated knowledge using only the provided context. "
        "Do not use outside knowledge. If the context does not contain enough information, say so explicitly. "
        "Keep the answer concise and cite the most relevant source names in the response."
    )
    user_prompt = (
        f"Question: {question}\n\n"
        f"Context:\n{context}\n\n"
        "Write a grounded answer based only on the context."
    )
    completion = client.chat.completions.create(
        model=GROQ_MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    answer = completion.choices[0].message.content.strip()

    source_names = []
    seen_sources = set()
    for chunk in retrieved_chunks:
        source = str(chunk["metadata"]["document_title"])
        if source not in seen_sources:
            seen_sources.add(source)
            source_names.append(source)

    attribution = ", ".join(source_names)
    return f"{answer}\n\nSources: {attribution}"
