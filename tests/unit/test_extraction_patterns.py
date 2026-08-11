"""Tests for extraction/patterns.py and extraction/entities.py - the regex
heuristics used to tag chunks with planet/star designations and detection
methods for filtered retrieval (`query/retriever.py`'s designation_filter).
"""

from __future__ import annotations

from extraction.entities import extract_entities
from extraction.patterns import ALL_DESIGNATION_PATTERNS, DETECTION_METHODS


def _designations(text: str) -> set[str]:
    found: set[str] = set()
    for pattern in ALL_DESIGNATION_PATTERNS:
        found.update(" ".join(m.split()) for m in pattern.findall(text))
    return found


def test_kepler_style_designations():
    assert "Kepler-452b" in _designations("The planet Kepler-452b is Earth-sized.")
    assert any(m.startswith("KOI-") for m in _designations("KOI-7016.01 is a candidate."))


def test_tess_style_designations():
    matches = _designations("TOI-700 d orbits in the habitable zone.")
    assert any("TOI-700" in m for m in matches)


def test_survey_style_designations():
    for name in ("WASP-12b", "HAT-P-7b", "TrES-2b", "CoRoT-7b"):
        assert _designations(f"The planet {name} was studied."), f"no match for {name}"


def test_catalog_star_designations():
    assert _designations("The host star HD 209458 hosts a hot Jupiter.")


def test_trappist_designations():
    matches = _designations("TRAPPIST-1e is a rocky planet in the TRAPPIST-1 system.")
    assert any("TRAPPIST-1" in m for m in matches)


def test_proxima_designation():
    assert _designations("Proxima Centauri b orbits our nearest neighbor star.")


def test_no_false_positive_on_unrelated_text():
    assert _designations("The weather today is sunny with a chance of rain.") == set()


def test_detection_methods_matched():
    text = "This planet was found using radial velocity and confirmed via transit photometry."
    hits = {name for name, pattern in DETECTION_METHODS.items() if pattern.search(text)}
    assert "radial velocity" in hits
    assert "transit photometry" in hits


def test_detection_methods_no_false_positive():
    hits = {name for name, pattern in DETECTION_METHODS.items() if pattern.search("A story about a cat.")}
    assert hits == set()


def test_extract_entities_combines_designations_and_methods():
    text = "WASP-12b was detected via transit photometry around its host star."
    result = extract_entities(text)
    assert any("WASP-12" in d for d in result["designations"])
    assert "transit photometry" in result["detection_methods"]
    assert result["designations"] == sorted(result["designations"])
    assert result["detection_methods"] == sorted(result["detection_methods"])
