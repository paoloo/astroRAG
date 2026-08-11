"""Phase 3: tag each parsed paper with the astronomy entities/metadata it mentions
(planet/star designations, detection methods). Output is a sidecar JSON next to
the parsed markdown; chunking attaches the relevant subset to each chunk's metadata
so query-time retrieval can filter by entity (e.g. "only chunks mentioning TOI-700").
"""

from __future__ import annotations

import json
import logging

from config import settings
from extraction.patterns import ALL_DESIGNATION_PATTERNS, DETECTION_METHODS
from state.manifest import Manifest

logger = logging.getLogger(__name__)


def extract_entities(text: str) -> dict[str, list[str]]:
    designations: set[str] = set()
    for pattern in ALL_DESIGNATION_PATTERNS:
        for match in pattern.findall(text):
            cleaned = " ".join(match.split())
            if cleaned:
                designations.add(cleaned)

    methods = [name for name, pattern in DETECTION_METHODS.items() if pattern.search(text)]

    return {
        "designations": sorted(designations),
        "detection_methods": sorted(methods),
    }


def extract_pending() -> dict[str, int]:
    manifest = Manifest(settings.manifest_path)
    pending = manifest.ids_ready_for("extracted")
    logger.info("extracting entities for %d papers", len(pending))

    for arxiv_id in pending:
        stem = arxiv_id.replace("/", "_")
        parsed_path = settings.parsed_dir / f"{stem}.md"
        out_path = settings.parsed_dir / f"{stem}.entities.json"
        try:
            text = parsed_path.read_text()
            entities = extract_entities(text)
            out_path.write_text(json.dumps(entities, indent=2))
            manifest.mark_stage(arxiv_id, "extracted")
            logger.info(
                "extracted %s: %d designations, %d methods",
                arxiv_id,
                len(entities["designations"]),
                len(entities["detection_methods"]),
            )
        except Exception as exc:  # noqa: BLE001
            manifest.record_error(arxiv_id, f"extraction error: {exc}")
            logger.warning("failed to extract entities for %s: %s", arxiv_id, exc)

    return manifest.status_summary()
