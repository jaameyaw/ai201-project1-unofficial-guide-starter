from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import gradio as gr  # noqa: E402

from unofficial_guide.pipeline import ask, rebuild_index  # noqa: E402


def handle_query(question: str) -> tuple[str, str]:
    result = ask(question)
    sources = "\n".join(f"- {source}" for source in result["sources"]) or "No sources returned."
    return result["answer"], sources


def handle_rebuild() -> str:
    count = rebuild_index()
    return f"Indexed {count} chunks"


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("# The Unofficial Guide\nAsk questions against your collected student knowledge.")
    with gr.Row():
        question = gr.Textbox(label="Question", placeholder="Ask about professor reviews, housing, dining, and more.", lines=2)
    with gr.Row():
        ask_button = gr.Button("Ask")
        rebuild_button = gr.Button("Rebuild Index")
    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Retrieved Sources", lines=6)
    status = gr.Textbox(label="Index Status", value="Ready", interactive=False)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])
    rebuild_button.click(handle_rebuild, inputs=None, outputs=status)


if __name__ == "__main__":
    demo.launch()
