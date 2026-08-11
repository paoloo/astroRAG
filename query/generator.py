"""Builds the RAG prompt from retrieved chunks and calls the local Ollama
chat model. Also exposes a no-context baseline call, used by the evaluation
harness to show what retrieval augmentation actually changes.
"""

from __future__ import annotations

import ollama

from config import settings

RAG_SYSTEM_PROMPT = (
    "You are an astronomy research assistant specializing in exoplanets. "
    "Answer the question using ONLY the provided excerpts from arXiv papers. "
    "Cite sources inline as [arXiv:<id>]. If the excerpts don't contain enough "
    "information to answer, say so explicitly rather than guessing."
)

BASELINE_SYSTEM_PROMPT = "You are an astronomy research assistant."


def _client() -> ollama.Client:
    return ollama.Client(host=settings.ollama_host)


def build_context(chunks: list[dict]) -> str:
    return "\n\n---\n\n".join(f"[arXiv:{c['arxiv_id']}] {c['title']}\n{c['text']}" for c in chunks)


def generate_answer(question: str, chunks: list[dict]) -> str:
    context = build_context(chunks)
    prompt = f"Context excerpts:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
    resp = _client().chat(
        model=settings.generation_model,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return resp["message"]["content"]


def generate_baseline(question: str) -> str:
    resp = _client().chat(
        model=settings.generation_model,
        messages=[
            {"role": "system", "content": BASELINE_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
    )
    return resp["message"]["content"]
