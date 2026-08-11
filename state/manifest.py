"""SQLite-backed manifest tracking each paper's progress through the pipeline.

Every phase (fetch -> parse -> extract -> chunk -> embed -> store -> index)
checks/updates this manifest so `pipeline.py run-all` is idempotent: reruns
skip whatever a paper has already completed, and later incremental/weekly
fetches only need to look at what's missing a given stage.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

STAGES = ("fetched", "parsed", "extracted", "chunked", "embedded", "stored", "indexed")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    arxiv_id TEXT PRIMARY KEY,
    title TEXT,
    published TEXT,
    updated TEXT,
    categories TEXT,
    pdf_path TEXT,
    meta_path TEXT,
    fetched_at TEXT,
    parsed_at TEXT,
    extracted_at TEXT,
    chunked_at TEXT,
    embedded_at TEXT,
    stored_at TEXT,
    indexed_at TEXT,
    last_error TEXT
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class PaperRecord:
    arxiv_id: str
    title: str | None
    published: str | None
    updated: str | None
    categories: str | None
    pdf_path: str | None
    meta_path: str | None


class Manifest:
    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db_path = db_path
        with self._connect() as conn:
            conn.execute(_SCHEMA)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def upsert_fetched(self, record: PaperRecord) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO papers (arxiv_id, title, published, updated, categories,
                                     pdf_path, meta_path, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(arxiv_id) DO UPDATE SET
                    title=excluded.title,
                    published=excluded.published,
                    updated=excluded.updated,
                    categories=excluded.categories,
                    pdf_path=excluded.pdf_path,
                    meta_path=excluded.meta_path,
                    fetched_at=excluded.fetched_at
                """,
                (
                    record.arxiv_id,
                    record.title,
                    record.published,
                    record.updated,
                    record.categories,
                    record.pdf_path,
                    record.meta_path,
                    _now(),
                ),
            )

    def mark_stage(self, arxiv_id: str, stage: str) -> None:
        if stage not in STAGES:
            raise ValueError(f"unknown stage: {stage}")
        with self._connect() as conn:
            conn.execute(
                f"UPDATE papers SET {stage}_at = ?, last_error = NULL WHERE arxiv_id = ?",
                (_now(), arxiv_id),
            )

    def record_error(self, arxiv_id: str, message: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE papers SET last_error = ? WHERE arxiv_id = ?", (message, arxiv_id)
            )

    def ids_ready_for(self, stage: str) -> list[str]:
        """IDs that have completed the stage before `stage` but not `stage` itself."""
        idx = STAGES.index(stage)
        if idx == 0:
            raise ValueError("fetched is the entry stage, nothing precedes it")
        prev_stage = STAGES[idx - 1]
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT arxiv_id FROM papers WHERE {prev_stage}_at IS NOT NULL "
                f"AND {stage}_at IS NULL"
            ).fetchall()
        return [r[0] for r in rows]

    def get(self, arxiv_id: str) -> sqlite3.Row | None:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(
                "SELECT * FROM papers WHERE arxiv_id = ?", (arxiv_id,)
            ).fetchone()

    def status_summary(self) -> dict[str, int]:
        with self._connect() as conn:
            counts = {}
            for stage in STAGES:
                counts[stage] = conn.execute(
                    f"SELECT COUNT(*) FROM papers WHERE {stage}_at IS NOT NULL"
                ).fetchone()[0]
            counts["total"] = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
        return counts

    def all_fetched_ids(self) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT arxiv_id FROM papers WHERE fetched_at IS NOT NULL"
            ).fetchall()
        return [r[0] for r in rows]
