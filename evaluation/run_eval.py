"""Phase 8 / test harness: for each question in qa_set.py, generate a
no-context baseline answer and a RAG-augmented answer from the same local
model, score both with a crude keyword check *and* an LLM-judge pass, and
write a comparison report. This is the concrete evidence for "does
retrieval augmentation help" - two independent scoring signals rather than
one, since the keyword check alone was shown to false-negative on
correctly-answered questions (see REPORT.md and evaluation/judge.py).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from config import settings
from evaluation.judge import judge_answer
from evaluation.qa_set import QA_SET
from query.generator import generate_answer, generate_baseline
from query.retriever import hybrid_search

logger = logging.getLogger(__name__)


def _keyword_hit(answer: str, keywords: list[str]) -> bool:
    lowered = answer.lower()
    return any(kw.lower() in lowered for kw in keywords)


def run_eval() -> str:
    rows = []
    baseline_kw_hits = 0
    rag_kw_hits = 0
    baseline_judge_hits = 0
    rag_judge_hits = 0

    for item in QA_SET:
        question = item["question"]
        keywords = item["expected_keywords"]

        baseline = generate_baseline(question)
        chunks = hybrid_search(question)
        rag_answer = generate_answer(question, chunks) if chunks else "(no chunks retrieved)"

        baseline_kw_hit = _keyword_hit(baseline, keywords)
        rag_kw_hit = _keyword_hit(rag_answer, keywords)
        baseline_judge_hit = judge_answer(question, keywords, baseline)
        rag_judge_hit = judge_answer(question, keywords, rag_answer)

        baseline_kw_hits += int(baseline_kw_hit)
        rag_kw_hits += int(rag_kw_hit)
        baseline_judge_hits += int(bool(baseline_judge_hit))
        rag_judge_hits += int(bool(rag_judge_hit))

        rows.append(
            {
                "question": question,
                "keywords": keywords,
                "baseline": baseline,
                "baseline_kw_hit": baseline_kw_hit,
                "baseline_judge_hit": baseline_judge_hit,
                "rag": rag_answer,
                "rag_kw_hit": rag_kw_hit,
                "rag_judge_hit": rag_judge_hit,
                "sources": sorted({c["arxiv_id"] for c in chunks}),
            }
        )
        logger.info(
            "eval: %r -> baseline(kw=%s judge=%s) rag(kw=%s judge=%s)",
            question,
            baseline_kw_hit,
            baseline_judge_hit,
            rag_kw_hit,
            rag_judge_hit,
        )

    report = _render_report(
        rows, baseline_kw_hits, rag_kw_hits, baseline_judge_hits, rag_judge_hits
    )
    out_path = settings.eval_dir / "report.md"
    out_path.write_text(report)
    return str(out_path)


def _mark(hit: bool | None) -> str:
    if hit is None:
        return "judge-error"
    return "hit" if hit else "miss"


def _render_report(
    rows: list[dict],
    baseline_kw_hits: int,
    rag_kw_hits: int,
    baseline_judge_hits: int,
    rag_judge_hits: int,
) -> str:
    n = len(rows)
    lines = [
        "# RAG Evaluation Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Model: `{settings.generation_model}` | Embedding: `{settings.embedding_model}`",
        "",
        f"**Keyword-match score - baseline: {baseline_kw_hits}/{n} | RAG-augmented: {rag_kw_hits}/{n}**",
        f"**LLM-judge score - baseline: {baseline_judge_hits}/{n} | RAG-augmented: {rag_judge_hits}/{n}**",
        "",
        "| # | Question | Baseline (kw / judge) | RAG (kw / judge) | Sources |",
        "|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        sources = ", ".join(r["sources"]) or "-"
        baseline_col = f"{_mark(r['baseline_kw_hit'])} / {_mark(r['baseline_judge_hit'])}"
        rag_col = f"{_mark(r['rag_kw_hit'])} / {_mark(r['rag_judge_hit'])}"
        lines.append(f"| {i} | {r['question']} | {baseline_col} | {rag_col} | {sources} |")

    lines.append("")
    lines.append("## Full transcripts")
    for i, r in enumerate(rows, 1):
        lines += [
            "",
            f"### {i}. {r['question']}",
            f"_expected keywords: {', '.join(r['keywords'])}_",
            "",
            f"**Baseline (no retrieval)** - keyword: {_mark(r['baseline_kw_hit'])}, judge: {_mark(r['baseline_judge_hit'])}",
            "",
            r["baseline"],
            "",
            f"**RAG-augmented** - keyword: {_mark(r['rag_kw_hit'])}, judge: {_mark(r['rag_judge_hit'])}",
            "",
            r["rag"],
            "",
            f"**Retrieved from:** {', '.join(r['sources']) or 'none'}",
        ]

    return "\n".join(lines)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    path = run_eval()
    print(f"wrote {path}")
