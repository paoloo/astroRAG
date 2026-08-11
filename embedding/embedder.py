"""Phase 5: embed chunks via Ollama's embeddings API.

Runs against whatever OLLAMA_HOST is configured (on coyote1, the box's
already-running shared daemon). Vectors are cached per-paper as .npy so a
rerun after an interruption skips papers the manifest already marks
'embedded' instead of recomputing.
"""

from __future__ import annotations

import json
import logging

import numpy as np
import ollama

from config import settings
from state.manifest import Manifest

logger = logging.getLogger(__name__)


def _client() -> ollama.Client:
    return ollama.Client(host=settings.ollama_host)


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = _client()
    return [client.embeddings(model=settings.embedding_model, prompt=text)["embedding"] for text in texts]


def embed_query(text: str) -> list[float]:
    return _client().embeddings(model=settings.embedding_model, prompt=text)["embedding"]


def embed_pending() -> dict[str, int]:
    manifest = Manifest(settings.manifest_path)
    pending = manifest.ids_ready_for("embedded")
    logger.info("embedding %d papers", len(pending))

    for arxiv_id in pending:
        stem = arxiv_id.replace("/", "_")
        chunks_path = settings.chunks_dir / f"{stem}.jsonl"
        vec_path = settings.embeddings_cache_dir / f"{stem}.npy"
        ids_path = settings.embeddings_cache_dir / f"{stem}.ids.json"
        try:
            rows = [json.loads(line) for line in chunks_path.read_text().splitlines() if line]
            texts = [r["text"] for r in rows]
            chunk_ids = [r["chunk_id"] for r in rows]
            vectors = embed_texts(texts)
            np.save(vec_path, np.array(vectors, dtype=np.float32))
            ids_path.write_text(json.dumps(chunk_ids))
            manifest.mark_stage(arxiv_id, "embedded")
            logger.info("embedded %s: %d chunks", arxiv_id, len(texts))
        except Exception as exc:  # noqa: BLE001
            manifest.record_error(arxiv_id, f"embed error: {exc}")
            logger.warning("failed to embed %s: %s", arxiv_id, exc)

    return manifest.status_summary()
