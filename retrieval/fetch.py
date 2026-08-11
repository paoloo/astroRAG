"""Phase 1: fetch papers from arXiv into data/raw/ and register them in the manifest.

Two modes, same underlying code path:
- `fetch_curated`: runs the curated-v1 seed queries for the initial small corpus.
- `fetch_incremental`: pulls everything new since a date, for later weekly/broad ingestion.
"""

from __future__ import annotations

import json
import logging

from config import settings
from retrieval import arxiv_client, seeds
from state.manifest import Manifest, PaperRecord

logger = logging.getLogger(__name__)


def _safe_filename(arxiv_id: str) -> str:
    return arxiv_id.replace("/", "_")


def _save_paper(paper: arxiv_client.ArxivPaper, manifest: Manifest) -> None:
    stem = _safe_filename(paper.arxiv_id)
    pdf_path = settings.raw_dir / f"{stem}.pdf"
    meta_path = settings.raw_dir / f"{stem}.json"

    if not pdf_path.exists():
        arxiv_client.download_pdf(paper, str(pdf_path))

    meta_path.write_text(
        json.dumps(
            {
                "arxiv_id": paper.arxiv_id,
                "versioned_id": paper.versioned_id,
                "title": paper.title,
                "abstract": paper.abstract,
                "published": paper.published,
                "updated": paper.updated,
                "categories": paper.categories,
                "pdf_url": paper.pdf_url,
                "entry_id": paper.entry_id,
            },
            indent=2,
        )
    )

    manifest.upsert_fetched(
        PaperRecord(
            arxiv_id=paper.arxiv_id,
            title=paper.title,
            published=paper.published,
            updated=paper.updated,
            categories=",".join(paper.categories),
            pdf_path=str(pdf_path),
            meta_path=str(meta_path),
        )
    )


def fetch_curated(
    seed_set: str = "curated-v1",
    max_results_per_query: int = 40,
    target_total: int | None = 400,
) -> dict[str, int]:
    manifest = Manifest(settings.manifest_path)
    seen = set(manifest.all_fetched_ids())
    queries = seeds.SEED_SETS[seed_set]

    for query in queries:
        if target_total and len(seen) >= target_total:
            break
        logger.info("arXiv query: %s", query)
        try:
            for paper in arxiv_client.search(query, max_results=max_results_per_query):
                if target_total and len(seen) >= target_total:
                    break
                if paper.arxiv_id in seen:
                    continue
                try:
                    _save_paper(paper, manifest)
                    seen.add(paper.arxiv_id)
                    logger.info("fetched %s: %s", paper.arxiv_id, paper.title[:80])
                except Exception as exc:  # noqa: BLE001 - keep going on individual paper failures
                    manifest.record_error(paper.arxiv_id, str(exc))
                    logger.warning("failed to fetch %s: %s", paper.arxiv_id, exc)
        except Exception as exc:  # noqa: BLE001 - arXiv's API is intermittently flaky; skip the query, not the whole run
            logger.warning("query failed after retries, skipping: %s (%s)", query, exc)

    return manifest.status_summary()


def fetch_incremental(since_date: str, max_results: int = 1000) -> dict[str, int]:
    """since_date format: YYYYMMDD. For the later broad/weekly ingestion mode."""
    manifest = Manifest(settings.manifest_path)
    seen = set(manifest.all_fetched_ids())

    for paper in arxiv_client.search_since(since_date, max_results=max_results):
        if paper.arxiv_id in seen:
            continue
        try:
            _save_paper(paper, manifest)
            seen.add(paper.arxiv_id)
        except Exception as exc:  # noqa: BLE001
            manifest.record_error(paper.arxiv_id, str(exc))
            logger.warning("failed to fetch %s: %s", paper.arxiv_id, exc)

    return manifest.status_summary()
