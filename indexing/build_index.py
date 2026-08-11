"""Phase 7: build/optimize the ANN vector index and full-text (BM25) index on
the LanceDB `chunks` table, so `query/retriever.py` can do hybrid search.

The ANN (IVF_PQ) index needs enough rows to train partitions meaningfully;
below that, LanceDB's brute-force vector search is already fast, so it's
skipped rather than erroring on a too-small curated corpus.
"""

from __future__ import annotations

import logging

from config import settings
from state.manifest import Manifest
from storage.vector_store import get_table

logger = logging.getLogger(__name__)

MIN_ROWS_FOR_ANN_INDEX = 256


def build_indices() -> dict[str, int]:
    table = get_table()
    n = table.count_rows()
    logger.info("building indices over %d chunk rows", n)

    if n >= MIN_ROWS_FOR_ANN_INDEX:
        table.create_index(metric=settings.vector_index_metric, vector_column_name="vector")
        logger.info("built ANN vector index (metric=%s)", settings.vector_index_metric)
    else:
        logger.info(
            "skipping ANN index (%d rows < %d) — brute-force vector search is used instead",
            n,
            MIN_ROWS_FOR_ANN_INDEX,
        )

    table.create_fts_index("text", replace=True)
    logger.info("built full-text (BM25) index on 'text'")

    manifest = Manifest(settings.manifest_path)
    for arxiv_id in manifest.ids_ready_for("indexed"):
        manifest.mark_stage(arxiv_id, "indexed")

    return manifest.status_summary()
