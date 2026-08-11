"""Regression tests pinning the two retrieval bugs found and fixed while
building the corpus-specific evaluation (see REPORT.md). Both bugs were
silent - retrieval just returned slightly-wrong-but-plausible results with
no error - so these exist to catch a silent reintroduction, not to catch a
crash.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_tess_first_planet_chunk_is_retrieved(skip_if_no_ollama, skip_if_no_table):
    """Pins the RRF-fusion fix: the answer chunk (arXiv:2607.12088's
    abstract) used to rank 22nd of 258 RRF-fused candidates - well outside
    an 8-result cutoff - despite containing an almost verbatim answer.
    Fixed by widening the candidate pool and reranking it (query/reranker.py).
    """
    from query.retriever import hybrid_search

    results = hybrid_search(
        "What type of planet was the first exoplanet discovered by TESS "
        "(the Transiting Exoplanet Survey Satellite)?",
        k=8,
    )

    assert any(r["arxiv_id"] == "2607.12088" for r in results)


def test_ogle_saturn_chunk_is_retrieved_and_used(skip_if_no_ollama, skip_if_no_table):
    """Pins the reranker-truncation fix: the answer sentence ("an orbit
    longer than Saturn's") sat at character 2012 of its chunk, past the
    reranker's original 400-char truncation, so the model was judging
    relevance without ever reading the relevant text. Fixed by removing the
    truncation (query/reranker.py).
    """
    from query.generator import generate_answer
    from query.retriever import hybrid_search

    question = (
        "The microlensing event OGLE-2016-BLG-0007 revealed a super-Earth "
        "on an orbit wider than which planet's orbit in our solar system?"
    )
    results = hybrid_search(question, k=8)
    assert any(r["arxiv_id"] == "2504.20158" and r["chunk_index"] == 4 for r in results), (
        "the chunk containing the Saturn comparison was not retrieved"
    )

    answer = generate_answer(question, results)
    assert "saturn" in answer.lower()
