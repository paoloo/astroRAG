"""Phase 4: split parsed markdown into RAG chunks.

Uses `semantic-text-splitter`'s MarkdownSplitter, which splits on markdown
structure (headings, paragraphs, sentences) while respecting a token-count
capacity range — so chunks stay coherent instead of being cut mid-sentence
at a fixed character offset. Each chunk gets paper-level metadata plus
chunk-local entity tags (which designations/detection methods actually
appear in *this* chunk, not just anywhere in the paper) for filtered
retrieval later.
"""

from __future__ import annotations

import json
import logging

from semantic_text_splitter import MarkdownSplitter

from config import settings
from extraction.patterns import ALL_DESIGNATION_PATTERNS, DETECTION_METHODS
from state.manifest import Manifest

logger = logging.getLogger(__name__)

_TIKTOKEN_MODEL = "gpt-3.5-turbo"


def _splitter() -> MarkdownSplitter:
    capacity = (settings.chunk_min_tokens, settings.chunk_max_tokens)
    try:
        return MarkdownSplitter.from_tiktoken_model(
            _TIKTOKEN_MODEL, capacity, overlap=settings.chunk_overlap_tokens
        )
    except TypeError:
        # Older/newer library versions may take a single max-capacity int
        # instead of a (min, max) tuple, or may not support `overlap`.
        return MarkdownSplitter.from_tiktoken_model(_TIKTOKEN_MODEL, settings.chunk_max_tokens)


def _local_entities(text: str) -> dict[str, list[str]]:
    designations: set[str] = set()
    for pattern in ALL_DESIGNATION_PATTERNS:
        for match in pattern.findall(text):
            cleaned = " ".join(match.split())
            if cleaned:
                designations.add(cleaned)
    methods = [name for name, pattern in DETECTION_METHODS.items() if pattern.search(text)]
    return {"designations": sorted(designations), "detection_methods": sorted(methods)}


def chunk_pending() -> dict[str, int]:
    manifest = Manifest(settings.manifest_path)
    pending = manifest.ids_ready_for("chunked")
    logger.info("chunking %d papers", len(pending))
    splitter = _splitter()

    for arxiv_id in pending:
        record = manifest.get(arxiv_id)
        stem = arxiv_id.replace("/", "_")
        parsed_path = settings.parsed_dir / f"{stem}.md"
        out_path = settings.chunks_dir / f"{stem}.jsonl"
        try:
            text = parsed_path.read_text()
            pieces = splitter.chunks(text)
            with out_path.open("w") as f:
                for i, piece in enumerate(pieces):
                    ents = _local_entities(piece)
                    row = {
                        "chunk_id": f"{arxiv_id}::{i}",
                        "arxiv_id": arxiv_id,
                        "chunk_index": i,
                        "title": record["title"],
                        "published": record["published"],
                        "categories": record["categories"],
                        "text": piece,
                        "designations": ents["designations"],
                        "detection_methods": ents["detection_methods"],
                    }
                    f.write(json.dumps(row) + "\n")
            manifest.mark_stage(arxiv_id, "chunked")
            logger.info("chunked %s into %d chunks", arxiv_id, len(pieces))
        except Exception as exc:  # noqa: BLE001
            manifest.record_error(arxiv_id, f"chunk error: {exc}")
            logger.warning("failed to chunk %s: %s", arxiv_id, exc)

    return manifest.status_summary()
