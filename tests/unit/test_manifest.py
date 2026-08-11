"""Tests for state/manifest.py - the SQLite manifest every pipeline phase
relies on for idempotency. If this is wrong, reruns can silently duplicate
work or skip work that was never actually done.
"""

from __future__ import annotations

import pytest

from state.manifest import Manifest, PaperRecord


def _record(arxiv_id: str = "1234.5678") -> PaperRecord:
    return PaperRecord(
        arxiv_id=arxiv_id,
        title="Test Paper",
        published="2026-01-01",
        updated="2026-01-01",
        categories="astro-ph.EP",
        pdf_path="/tmp/x.pdf",
        meta_path="/tmp/x.json",
    )


def test_upsert_fetched_and_status_summary(tmp_path):
    m = Manifest(tmp_path / "manifest.sqlite3")
    m.upsert_fetched(_record())

    summary = m.status_summary()
    assert summary["fetched"] == 1
    assert summary["parsed"] == 0
    assert summary["total"] == 1


def test_mark_stage_progresses_and_ids_ready_for(tmp_path):
    m = Manifest(tmp_path / "manifest.sqlite3")
    m.upsert_fetched(_record("a"))
    m.upsert_fetched(_record("b"))

    assert set(m.ids_ready_for("parsed")) == {"a", "b"}

    m.mark_stage("a", "parsed")
    assert m.ids_ready_for("parsed") == ["b"]
    assert m.ids_ready_for("extracted") == ["a"]


def test_mark_stage_rejects_unknown_stage(tmp_path):
    m = Manifest(tmp_path / "manifest.sqlite3")
    m.upsert_fetched(_record())
    with pytest.raises(ValueError):
        m.mark_stage("1234.5678", "not-a-real-stage")


def test_ids_ready_for_rejects_entry_stage(tmp_path):
    m = Manifest(tmp_path / "manifest.sqlite3")
    with pytest.raises(ValueError):
        m.ids_ready_for("fetched")


def test_record_error_and_clear_on_next_stage_success(tmp_path):
    m = Manifest(tmp_path / "manifest.sqlite3")
    m.upsert_fetched(_record())

    m.record_error("1234.5678", "boom")
    assert m.get("1234.5678")["last_error"] == "boom"

    m.mark_stage("1234.5678", "parsed")
    assert m.get("1234.5678")["last_error"] is None


def test_rerunning_fetch_on_same_paper_is_idempotent(tmp_path):
    """Core guarantee: re-fetching (or any upsert) on an already-seen paper
    must not duplicate its row or clobber progress already made on later
    stages - this is what makes `pipeline.py run-all` safe to rerun."""
    m = Manifest(tmp_path / "manifest.sqlite3")
    m.upsert_fetched(_record())
    m.mark_stage("1234.5678", "parsed")
    first_parsed_at = m.get("1234.5678")["parsed_at"]

    m.upsert_fetched(_record())

    assert m.status_summary()["total"] == 1
    assert m.get("1234.5678")["parsed_at"] == first_parsed_at


def test_all_fetched_ids(tmp_path):
    m = Manifest(tmp_path / "manifest.sqlite3")
    m.upsert_fetched(_record("a"))
    m.upsert_fetched(_record("b"))
    assert set(m.all_fetched_ids()) == {"a", "b"}


def test_get_returns_none_for_unknown_id(tmp_path):
    m = Manifest(tmp_path / "manifest.sqlite3")
    assert m.get("does-not-exist") is None
