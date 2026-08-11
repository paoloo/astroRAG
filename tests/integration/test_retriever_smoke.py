"""Smoke tests against the real LanceDB table populated on coyote1."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_hybrid_search_returns_k_results_with_required_fields(skip_if_no_ollama, skip_if_no_table):
    from query.retriever import hybrid_search

    results = hybrid_search("exoplanet transit detection method", k=5)

    assert len(results) == 5
    for r in results:
        assert r["text"]
        assert r["arxiv_id"]
        assert r["chunk_id"]


def test_hybrid_search_designation_filter_narrows_results(skip_if_no_ollama, skip_if_no_table):
    from query.retriever import hybrid_search

    results = hybrid_search("planet properties", k=5, designation_filter="TRAPPIST-1")

    for r in results:
        assert "TRAPPIST-1" in r["designations"]


def test_hybrid_search_reranking_can_be_disabled(skip_if_no_ollama, skip_if_no_table):
    """Confirms `settings.rerank_enabled = False` still returns a usable
    (non-reranked, RRF-only) result set - the escape hatch for interactive
    use noted in HANDOFF.md if the extra Ollama call's latency isn't worth it."""
    from config import settings
    from query.retriever import hybrid_search

    original = settings.rerank_enabled
    settings.rerank_enabled = False
    try:
        results = hybrid_search("exoplanet atmosphere characterization", k=5)
        assert len(results) == 5
    finally:
        settings.rerank_enabled = original
