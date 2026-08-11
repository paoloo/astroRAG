"""Smoke tests for query/generator.py against the real generation model."""

from __future__ import annotations

import re

import pytest

pytestmark = pytest.mark.integration


def test_generate_answer_cites_a_retrieved_paper(skip_if_no_ollama, skip_if_no_table):
    from query.generator import generate_answer
    from query.retriever import hybrid_search

    chunks = hybrid_search("what is a hot Jupiter", k=5)
    answer = generate_answer("What is a hot Jupiter?", chunks)

    assert len(answer) > 0
    assert re.search(r"arXiv:\d{4,7}\.\d+", answer), f"no inline citation found in: {answer!r}"


def test_generate_baseline_runs_without_retrieved_context(skip_if_no_ollama):
    from query.generator import generate_baseline

    answer = generate_baseline("What is a hot Jupiter?")

    assert len(answer) > 0
