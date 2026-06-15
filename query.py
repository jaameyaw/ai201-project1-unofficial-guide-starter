from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from unofficial_guide.pipeline import ask, rebuild_index  # noqa: E402


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Query the Unofficial Guide index")
    parser.add_argument("question", nargs="*", help="Question to ask")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the vector index first")
    args = parser.parse_args()

    if args.rebuild:
        count = rebuild_index()
        print(f"Indexed {count} chunks")

    question = " ".join(args.question).strip()
    if not question:
        raise SystemExit("Provide a question to ask.")

    result = ask(question)
    print(result["answer"])
    print()
    print("Retrieved sources:")
    for source in result["sources"]:
        print(f"- {source}")


if __name__ == "__main__":
    main()
