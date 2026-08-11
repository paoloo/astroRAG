"""Quality gate: reruns the full corpus-specific evaluation set
(evaluation/qa_set.py) and asserts the RAG-augmented score hasn't regressed
below a floor set under the last known-good result (15/18, see REPORT.md).
The threshold is intentionally a few points below 15 to leave room for the
generation model's normal run-to-run variance rather than flaking on noise.

This is the slowest test in the suite by far: ~18 questions, each doing an
embedding call, a hybrid search, an LLM reranking call, and a generation
call. Expect several minutes.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration

_LAST_KNOWN_GOOD = 16  # keyword score; see REPORT.md (LLM-judge score is 18/18)
_REGRESSION_FLOOR = 14


def test_rag_score_has_not_regressed(skip_if_no_ollama, skip_if_no_table):
    from evaluation.qa_set import QA_SET
    from query.generator import generate_answer
    from query.retriever import hybrid_search

    hits = 0
    misses: list[str] = []

    for item in QA_SET:
        chunks = hybrid_search(item["question"])
        answer = generate_answer(item["question"], chunks) if chunks else ""
        lowered = answer.lower()
        if any(kw.lower() in lowered for kw in item["expected_keywords"]):
            hits += 1
        else:
            misses.append(item["question"])

    assert hits >= _REGRESSION_FLOOR, (
        f"RAG score regressed to {hits}/{len(QA_SET)} "
        f"(floor {_REGRESSION_FLOOR}, last known-good {_LAST_KNOWN_GOOD}). "
        f"Missed: {misses}"
    )
