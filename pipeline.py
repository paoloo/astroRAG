"""Top-level CLI orchestrating the arXiv exoplanet/astronomy RAG pipeline.

Each phase is manifest-tracked and idempotent, so `run-all` safely skips
whatever a paper has already completed on a rerun.

Usage:
    python pipeline.py fetch --seed-set curated-v1 --target-total 400
    python pipeline.py run-all
    python pipeline.py status
"""

from __future__ import annotations

import logging

import typer

from chunking.chunker import chunk_pending
from config import settings
from embedding.embedder import embed_pending
from extraction.entities import extract_pending
from indexing.build_index import build_indices
from parsing.pdf_to_markdown import parse_pending
from retrieval.fetch import fetch_curated, fetch_incremental
from state.manifest import Manifest
from storage.vector_store import store_pending

app = typer.Typer(add_completion=False)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@app.command()
def fetch(
    seed_set: str = "curated-v1",
    max_results_per_query: int = 40,
    target_total: int = 400,
    since: str | None = typer.Option(None, help="YYYYMMDD - switches to incremental mode"),
) -> None:
    """Phase 1: pull papers from arXiv into data/raw/."""
    summary = fetch_incremental(since) if since else fetch_curated(
        seed_set, max_results_per_query, target_total
    )
    typer.echo(summary)


@app.command()
def parse() -> None:
    """Phase 2: PDF -> markdown."""
    typer.echo(parse_pending())


@app.command()
def extract() -> None:
    """Phase 3: astronomy entity/metadata extraction."""
    typer.echo(extract_pending())


@app.command()
def chunk() -> None:
    """Phase 4: split parsed papers into RAG chunks."""
    typer.echo(chunk_pending())


@app.command()
def embed() -> None:
    """Phase 5: embed chunks via Ollama."""
    typer.echo(embed_pending())


@app.command()
def store() -> None:
    """Phase 6: persist chunks+vectors into LanceDB."""
    typer.echo(store_pending())


@app.command()
def index() -> None:
    """Phase 7: build ANN + full-text search indices."""
    typer.echo(build_indices())


@app.command(name="run-all")
def run_all(
    seed_set: str = "curated-v1",
    max_results_per_query: int = 40,
    target_total: int = 400,
) -> None:
    """Run every phase in order, skipping whatever the manifest marks done."""
    typer.echo("=== fetch ===")
    typer.echo(fetch_curated(seed_set, max_results_per_query, target_total))
    typer.echo("=== parse ===")
    typer.echo(parse_pending())
    typer.echo("=== extract ===")
    typer.echo(extract_pending())
    typer.echo("=== chunk ===")
    typer.echo(chunk_pending())
    typer.echo("=== embed ===")
    typer.echo(embed_pending())
    typer.echo("=== store ===")
    typer.echo(store_pending())
    typer.echo("=== index ===")
    typer.echo(build_indices())


@app.command()
def status() -> None:
    """Print per-stage paper counts from the manifest."""
    manifest = Manifest(settings.manifest_path)
    typer.echo(manifest.status_summary())


if __name__ == "__main__":
    app()
