"""Central configuration for the arXiv exoplanet/astronomy RAG pipeline.

All paths, model names, and tunables live here so every phase (retrieval,
parsing, extraction, chunking, embedding, storage, indexing, query,
evaluation) reads from one place instead of hardcoding values.
"""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Ollama ---
    ollama_host: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text"
    generation_model: str = "qwen2.5:14b-instruct"

    # --- Storage paths ---
    vector_data_dir: Path = REPO_ROOT / "data"

    # --- arXiv retrieval ---
    arxiv_categories: tuple[str, ...] = ("astro-ph.EP",)
    arxiv_request_delay_seconds: float = 3.0  # arXiv API terms of use minimum

    # --- Chunking ---
    chunk_min_tokens: int = 400
    chunk_max_tokens: int = 800
    chunk_overlap_tokens: int = 80

    # --- Retrieval / RAG ---
    top_k: int = 8
    vector_index_metric: str = "cosine"
    rerank_enabled: bool = True
    rerank_pool_size: int = 30  # candidates pulled via RRF before reranking
    rerank_fetch_limit: int = 160  # per-list (dense/FTS) fetch depth feeding that pool

    @property
    def raw_dir(self) -> Path:
        return self.vector_data_dir / "raw"

    @property
    def parsed_dir(self) -> Path:
        return self.vector_data_dir / "parsed"

    @property
    def chunks_dir(self) -> Path:
        return self.vector_data_dir / "chunks"

    @property
    def embeddings_cache_dir(self) -> Path:
        return self.vector_data_dir / "embeddings_cache"

    @property
    def lancedb_dir(self) -> Path:
        return self.vector_data_dir / "lancedb"

    @property
    def eval_dir(self) -> Path:
        return self.vector_data_dir / "eval"

    @property
    def manifest_path(self) -> Path:
        return self.vector_data_dir / "manifest.sqlite3"

    def ensure_dirs(self) -> None:
        for d in (
            self.raw_dir,
            self.parsed_dir,
            self.chunks_dir,
            self.embeddings_cache_dir,
            self.lancedb_dir,
            self.eval_dir,
        ):
            d.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_dirs()
