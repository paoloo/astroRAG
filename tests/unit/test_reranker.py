"""Tests for query/reranker.py - all mocked, no live Ollama call. Covers the
non-happy paths that never got exercised by manual testing: malformed LLM
output, a dead Ollama client, and duplicate/out-of-range indices.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from query.reranker import rerank


def _chunks(n: int) -> list[dict]:
    return [{"chunk_id": f"c{i}", "arxiv_id": "0000.0000", "text": f"chunk {i} text"} for i in range(n)]


def test_rerank_is_noop_when_pool_not_larger_than_top_k():
    chunks = _chunks(5)
    assert rerank("question", chunks, top_k=8) == chunks


@patch("query.reranker._client")
def test_rerank_reorders_by_llm_response(mock_client_fn):
    chunks = _chunks(10)
    mock_client = MagicMock()
    mock_client.chat.return_value = {"message": {"content": "[5, 2, 9]"}}
    mock_client_fn.return_value = mock_client

    result = rerank("question", chunks, top_k=3)

    assert [c["chunk_id"] for c in result] == ["c4", "c1", "c8"]  # 1-indexed -> 0-indexed


@patch("query.reranker._client")
def test_rerank_falls_back_on_malformed_json(mock_client_fn):
    chunks = _chunks(10)
    mock_client = MagicMock()
    mock_client.chat.return_value = {"message": {"content": "not valid json at all"}}
    mock_client_fn.return_value = mock_client

    result = rerank("question", chunks, top_k=3)

    assert [c["chunk_id"] for c in result] == ["c0", "c1", "c2"]


@patch("query.reranker._client")
def test_rerank_falls_back_when_ollama_unreachable(mock_client_fn):
    chunks = _chunks(10)
    mock_client_fn.side_effect = RuntimeError("connection refused")

    result = rerank("question", chunks, top_k=3)

    assert [c["chunk_id"] for c in result] == ["c0", "c1", "c2"]


@patch("query.reranker._client")
def test_rerank_ignores_out_of_range_indices(mock_client_fn):
    chunks = _chunks(5)
    mock_client = MagicMock()
    mock_client.chat.return_value = {"message": {"content": "[2, 99, 4]"}}
    mock_client_fn.return_value = mock_client

    result = rerank("question", chunks, top_k=3)

    assert [c["chunk_id"] for c in result] == ["c1", "c3", "c0"]


@patch("query.reranker._client")
def test_rerank_dedupes_repeated_indices(mock_client_fn):
    """Regression test: a duplicate index in the LLM's response used to slip
    through and return the same chunk twice, wasting a context slot in the
    final answer prompt. Fixed by deduping while building `ranked` instead of
    only deduping the fill-up loop afterward."""
    chunks = _chunks(5)
    mock_client = MagicMock()
    mock_client.chat.return_value = {"message": {"content": "[2, 2, 4]"}}
    mock_client_fn.return_value = mock_client

    result = rerank("question", chunks, top_k=3)
    ids = [c["chunk_id"] for c in result]

    assert len(ids) == len(set(ids)), f"duplicate chunk in reranked result: {ids}"
    assert ids == ["c1", "c3", "c0"]  # c1, c3 from the response, c0 fills the remaining slot
