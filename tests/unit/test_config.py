"""Tests for config.py's Settings - mostly guarding against tunables drifting
into nonsensical relationships (e.g. min chunk size larger than max).
"""

from __future__ import annotations

from config import Settings, settings


def test_default_settings_are_internally_consistent():
    assert settings.chunk_min_tokens < settings.chunk_max_tokens
    assert settings.top_k > 0
    assert settings.rerank_pool_size >= settings.top_k
    assert settings.arxiv_request_delay_seconds >= 3.0  # arXiv API terms of use minimum


def test_ensure_dirs_creates_expected_subdirs(tmp_path):
    s = Settings(vector_data_dir=tmp_path / "data")
    s.ensure_dirs()

    for sub in ("raw", "parsed", "chunks", "embeddings_cache", "lancedb", "eval"):
        assert (tmp_path / "data" / sub).is_dir()


def test_derived_paths_are_under_vector_data_dir(tmp_path):
    s = Settings(vector_data_dir=tmp_path / "data")
    assert s.manifest_path == tmp_path / "data" / "manifest.sqlite3"
    assert s.lancedb_dir == tmp_path / "data" / "lancedb"
