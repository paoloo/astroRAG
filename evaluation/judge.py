"""LLM-judge grading, as a second correctness signal alongside the crude
keyword check in run_eval.py.

Keyword matching is cheap and easy to audit, but it's brittle to phrasing:
building the corpus-specific question set surfaced three cases where a
correct, well-cited answer was graded a miss because it used different but
equivalent wording, or because the keyword list itself was written before
checking what the corpus actually says (see REPORT.md). A judge model that
understands "short-wavelength" and "ultraviolet" mean the same thing here
closes that gap without just deleting the keyword check - both scores are
reported so a divergence between them is itself a signal worth reading.
"""

from __future__ import annotations

import logging

import ollama

from config import settings

logger = logging.getLogger(__name__)

_JUDGE_PROMPT = """You are grading whether an answer correctly and substantively addresses a question, as part of evaluating a retrieval-augmented astronomy Q&A system.

Question: {question}

Hint keywords a correct answer often includes (not required verbatim - an \
answer that conveys the same fact with different wording should still \
pass): {keywords}

Answer to grade:
{answer}

Does this answer correctly and substantively address the question? Reply \
with exactly one word: PASS or FAIL."""


def _client() -> ollama.Client:
    return ollama.Client(host=settings.ollama_host)


def judge_answer(question: str, keywords: list[str], answer: str) -> bool | None:
    """Returns True (pass), False (fail), or None if the judge call itself failed."""
    prompt = _JUDGE_PROMPT.format(question=question, keywords=", ".join(keywords), answer=answer)
    try:
        resp = _client().chat(
            model=settings.generation_model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0},
        )
        verdict = resp["message"]["content"].strip().upper()
        if "PASS" in verdict:
            return True
        if "FAIL" in verdict:
            return False
        logger.warning("judge returned an unparseable verdict: %r", verdict)
        return None
    except Exception as exc:  # noqa: BLE001 - a failed judge call shouldn't crash the eval run
        logger.warning("judge call failed: %s", exc)
        return None
