"""Interactive RAG chat REPL — `python -m query.cli` — for testing the pipeline
with a real model against real retrieved papers.
"""

from __future__ import annotations

import typer

from query.generator import generate_answer
from query.retriever import hybrid_search

app = typer.Typer(add_completion=False)


@app.command()
def chat() -> None:
    typer.echo("Exoplanet/astronomy RAG. Ask a question ('exit' to quit).")
    while True:
        try:
            question = typer.prompt("\n>")
        except (KeyboardInterrupt, EOFError):
            typer.echo("")
            break
        if question.strip().lower() in {"exit", "quit"}:
            break

        chunks = hybrid_search(question)
        if not chunks:
            typer.echo("No relevant chunks found in the corpus yet.")
            continue

        answer = generate_answer(question, chunks)
        typer.echo(f"\n{answer}\n")

        typer.echo("Sources:")
        seen: set[str] = set()
        for c in chunks:
            if c["arxiv_id"] in seen:
                continue
            seen.add(c["arxiv_id"])
            typer.echo(f"  - arXiv:{c['arxiv_id']} — {c['title']}")


if __name__ == "__main__":
    app()
