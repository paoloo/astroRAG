"""Smoke tests against the real Ollama daemon. Requires OLLAMA_HOST reachable
and the embedding model pulled - run on atadev, not locally.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_embed_query_returns_a_real_vector(skip_if_no_ollama):
    from embedding.embedder import embed_query

    vec = embed_query("What is a hot Jupiter?")

    assert isinstance(vec, list)
    assert len(vec) > 0
    assert all(isinstance(x, float) for x in vec)


def test_embed_query_is_deterministic(skip_if_no_ollama):
    from embedding.embedder import embed_query

    v1 = embed_query("habitable zone")
    v2 = embed_query("habitable zone")

    assert v1 == v2
