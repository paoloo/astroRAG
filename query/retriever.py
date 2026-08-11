"""Query-time hybrid retrieval: dense vector search + full-text (BM25) search
over the LanceDB `chunks` table, merged by reciprocal rank fusion, then
optionally reranked.

Dense search alone tends to miss exact catalog designations ("TOI-700 d");
FTS alone misses paraphrased semantic queries ("planets in the habitable
zone"). Combining both (rather than relying on LanceDB's built-in hybrid
search, which needs a registered embedding function) keeps embedding fully
under our control via `embedding/embedder.py`.

RRF alone can still bury a genuinely relevant chunk that only scored well
on one signal - confirmed on this corpus (see `query/reranker.py`'s
docstring) - so by default a wider candidate pool is pulled via RRF
(`settings.rerank_pool_size`) and cut down to `k` by `reranker.rerank`
rather than truncating to `k` directly off the RRF ranking.
"""

from __future__ import annotations

from config import settings
from embedding.embedder import embed_query
from query.reranker import rerank
from storage.vector_store import get_table

_RRF_K = 60


def hybrid_search(
    query: str,
    k: int = settings.top_k,
    designation_filter: str | None = None,
    fetch_multiplier: int = 4,
) -> list[dict]:
    table = get_table()
    query_vector = embed_query(query)
    fetch_k = max(k * fetch_multiplier, settings.rerank_fetch_limit if settings.rerank_enabled else 0)

    vec_search = table.search(query_vector, vector_column_name="vector").limit(fetch_k)
    fts_search = table.search(query, query_type="fts").limit(fetch_k)

    if designation_filter:
        escaped = designation_filter.replace("'", "''")
        clause = f"designations LIKE '%{escaped}%'"
        vec_search = vec_search.where(clause)
        fts_search = fts_search.where(clause)

    vec_rows = vec_search.to_list()
    fts_rows = fts_search.to_list()

    scores: dict[str, float] = {}
    rows_by_id: dict[str, dict] = {}
    for rank, row in enumerate(vec_rows):
        cid = row["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (_RRF_K + rank)
        rows_by_id[cid] = row
    for rank, row in enumerate(fts_rows):
        cid = row["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (_RRF_K + rank)
        rows_by_id.setdefault(cid, row)

    pool_size = settings.rerank_pool_size if settings.rerank_enabled else k
    ranked_ids = sorted(scores, key=lambda cid: scores[cid], reverse=True)[:pool_size]
    pool = [rows_by_id[cid] for cid in ranked_ids]

    return rerank(query, pool, k) if settings.rerank_enabled else pool[:k]
