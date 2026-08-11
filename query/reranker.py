"""LLM-based listwise reranking of retrieved chunks.

The RRF fusion in `retriever.py` picks a good candidate pool but can bury a
genuinely relevant chunk if it only scored well on one signal (e.g. a
strong FTS/BM25 match but a mediocre dense-vector rank) - diagnosed
concretely on this corpus: a chunk containing the exact answer to a test
question ranked 22nd out of 258 RRF-fused candidates, well outside the
top-8 cutoff, despite an FTS rank of 16.

A cross-encoder reranker (e.g. bge-reranker-v2-m3) is the standard fix, but
it needs sentence-transformers/torch, which risks the tight `/home/paolo`
disk quota on atadev (see PLAN.md). This reuses the local Ollama chat model
already running for generation instead: given the question and a batch of
candidate chunks, ask it to return the most relevant ones in order. No new
dependency, no new disk footprint.
"""

from __future__ import annotations

import json
import logging

import ollama

from config import settings

logger = logging.getLogger(__name__)

_PROMPT = """You are ranking search results by relevance to a question.

Question: {question}

Candidates:
{candidates}

Return ONLY a JSON array of the candidate numbers, ordered from most to \
least relevant to the question, listing at most {top_k} numbers. \
Example: [3, 1, 7]"""


def _client() -> ollama.Client:
    return ollama.Client(host=settings.ollama_host)


def rerank(question: str, chunks: list[dict], top_k: int) -> list[dict]:
    if len(chunks) <= top_k:
        return chunks

    # No truncation: chunks are already capped by chunking config (~800
    # tokens, max observed ~5.6k chars) and the daemon's 64k context easily
    # covers a 30-candidate pool at that size. An earlier 400-char cutoff
    # here silently hid the answer-bearing sentence in a real test case
    # (it sat past character 2000 in an otherwise-relevant chunk).
    candidates = "\n".join(f"{i + 1}. [{c['arxiv_id']}] {c['text']}" for i, c in enumerate(chunks))
    prompt = _PROMPT.format(question=question, candidates=candidates, top_k=top_k)

    try:
        resp = _client().chat(
            model=settings.generation_model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0},
        )
        text = resp["message"]["content"]
        indices = json.loads(text[text.index("[") : text.rindex("]") + 1])

        ranked: list[dict] = []
        seen_ids: set[str] = set()
        for i in indices:
            if not (isinstance(i, int) and 1 <= i <= len(chunks)):
                continue
            c = chunks[i - 1]
            if c["chunk_id"] in seen_ids:
                continue
            ranked.append(c)
            seen_ids.add(c["chunk_id"])
        for c in chunks:
            if len(ranked) >= top_k:
                break
            if c["chunk_id"] not in seen_ids:
                ranked.append(c)
                seen_ids.add(c["chunk_id"])
        return ranked[:top_k]
    except Exception as exc:  # noqa: BLE001 - fall back rather than break retrieval
        logger.warning("rerank failed, falling back to RRF order: %s", exc)
        return chunks[:top_k]
