"""Phase 2: PDF -> structured markdown (pymupdf4llm), preserving section headings
so `chunking/chunker.py` can split on document structure rather than raw pages.
"""

from __future__ import annotations

import logging

import pymupdf4llm

from config import settings
from state.manifest import Manifest

logger = logging.getLogger(__name__)


def parse_one(arxiv_id: str, pdf_path: str) -> str:
    return pymupdf4llm.to_markdown(pdf_path)


def parse_pending() -> dict[str, int]:
    manifest = Manifest(settings.manifest_path)
    pending = manifest.ids_ready_for("parsed")
    logger.info("parsing %d papers", len(pending))

    for arxiv_id in pending:
        record = manifest.get(arxiv_id)
        stem = arxiv_id.replace("/", "_")
        out_path = settings.parsed_dir / f"{stem}.md"
        try:
            markdown = parse_one(arxiv_id, record["pdf_path"])
            out_path.write_text(markdown)
            manifest.mark_stage(arxiv_id, "parsed")
            logger.info("parsed %s (%d chars)", arxiv_id, len(markdown))
        except Exception as exc:  # noqa: BLE001 - keep going on individual paper failures
            manifest.record_error(arxiv_id, f"parse error: {exc}")
            logger.warning("failed to parse %s: %s", arxiv_id, exc)

    return manifest.status_summary()
