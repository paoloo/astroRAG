"""Phase 6: persist chunks + embeddings into LanceDB.

One embedded, on-disk LanceDB table (`chunks`) holds every chunk's text,
metadata, and vector. No server process — the table is just files under
`data/lancedb/`. Re-running `store_pending()` after a paper's chunks changed
deletes and re-adds that paper's rows so it stays idempotent.

`db.table_names()` is used deliberately despite the deprecation warning in
this lancedb version: its suggested replacement, `db.list_tables()`, returns
a paginated `ListTablesResponse` object here, not a plain list of names, so
`TABLE_NAME in db.list_tables()` silently always evaluates false. Caught by
tests/integration/test_retriever_smoke.py. Revisit once the installed
lancedb version's `list_tables()` API stabilizes.
"""

from __future__ import annotations

import json
import logging

import lancedb
import numpy as np

from config import settings
from state.manifest import Manifest

logger = logging.getLogger(__name__)

TABLE_NAME = "chunks"


def _db() -> lancedb.DBConnection:
    return lancedb.connect(str(settings.lancedb_dir))


def _rows_for_paper(arxiv_id: str) -> list[dict]:
    stem = arxiv_id.replace("/", "_")
    chunks_path = settings.chunks_dir / f"{stem}.jsonl"
    vec_path = settings.embeddings_cache_dir / f"{stem}.npy"
    ids_path = settings.embeddings_cache_dir / f"{stem}.ids.json"

    chunk_rows = {
        (obj := json.loads(line))["chunk_id"]: obj
        for line in chunks_path.read_text().splitlines()
        if line
    }
    vectors = np.load(vec_path)
    chunk_ids = json.loads(ids_path.read_text())

    rows = []
    for chunk_id, vector in zip(chunk_ids, vectors):
        r = chunk_rows[chunk_id]
        rows.append(
            {
                "chunk_id": r["chunk_id"],
                "arxiv_id": r["arxiv_id"],
                "chunk_index": r["chunk_index"],
                "title": r["title"] or "",
                "published": r["published"] or "",
                "categories": r["categories"] or "",
                "text": r["text"],
                "designations": ", ".join(r["designations"]),
                "detection_methods": ", ".join(r["detection_methods"]),
                "vector": vector.tolist(),
            }
        )
    return rows


def store_pending() -> dict[str, int]:
    manifest = Manifest(settings.manifest_path)
    pending = manifest.ids_ready_for("stored")
    logger.info("storing %d papers into LanceDB", len(pending))
    if not pending:
        return manifest.status_summary()

    db = _db()
    table = db.open_table(TABLE_NAME) if TABLE_NAME in db.table_names() else None

    for arxiv_id in pending:
        try:
            rows = _rows_for_paper(arxiv_id)
            if not rows:
                manifest.mark_stage(arxiv_id, "stored")
                continue
            if table is None:
                table = db.create_table(TABLE_NAME, data=rows)
            else:
                table.delete(f"arxiv_id = '{arxiv_id}'")
                table.add(rows)
            manifest.mark_stage(arxiv_id, "stored")
            logger.info("stored %s: %d chunks", arxiv_id, len(rows))
        except Exception as exc:  # noqa: BLE001
            manifest.record_error(arxiv_id, f"store error: {exc}")
            logger.warning("failed to store %s: %s", arxiv_id, exc)

    return manifest.status_summary()


def get_table():
    db = _db()
    if TABLE_NAME not in db.table_names():
        raise RuntimeError(
            f"LanceDB table '{TABLE_NAME}' does not exist yet — run the store phase first"
        )
    return db.open_table(TABLE_NAME)
