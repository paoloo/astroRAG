"""Regex patterns for astronomy/exoplanet designations.

These are heuristic, not exhaustive — astronomy catalog naming is regular
enough (survey prefix + number + lowercase letter for the planet) that regex
gets most real mentions without needing an ML NER model. False
positives/negatives are acceptable here since this only enriches chunk
metadata for filtering, it isn't the source of truth for planet parameters.
"""

from __future__ import annotations

import re

# Kepler/K2/KOI: "Kepler-452b", "Kepler-22 b", "K2-18 b", "KOI-7016.01"
KEPLER_STYLE = re.compile(r"\b(?:Kepler|K2|KOI)-\d+\.?\d*\s?[b-z]?\b")

# TESS: "TOI-700 d", "TOI-700.01", "TIC 150428135"
TESS_STYLE = re.compile(r"\b(?:TOI|TIC)-?\s?\d+\.?\d*\s?[b-z]?\b")

# Ground-based transit surveys: "WASP-12b", "HAT-P-7b", "HATS-2b", "TrES-2b",
# "CoRoT-7b", "XO-1b", "Qatar-1b", "NGTS-1b", "WTS-2b"
SURVEY_STYLE = re.compile(
    r"\b(?:WASP|HAT-P|HATS|TrES|CoRoT|XO|Qatar|NGTS|WTS)-\d+\s?[b-z]?\b"
)

# Catalog host stars: "HD 209458", "HD 209458 b", "HIP 65426", "GJ 1214 b",
# "LHS 1140 b", "HR 8799"
CATALOG_STAR = re.compile(r"\b(?:HD|HIP|GJ|GI|LHS|HR)\s?\d+\s?[b-z]?\b")

# TRAPPIST-1 system: "TRAPPIST-1e", "TRAPPIST-1 b"
TRAPPIST = re.compile(r"\bTRAPPIST-1\s?[b-h]?\b")

# Proxima Centauri b / Proxima b
PROXIMA = re.compile(r"\bProxima(?:\s+Centauri)?\s?b\b", re.IGNORECASE)

ALL_DESIGNATION_PATTERNS = (
    KEPLER_STYLE,
    TESS_STYLE,
    SURVEY_STYLE,
    CATALOG_STAR,
    TRAPPIST,
    PROXIMA,
)

DETECTION_METHODS = {
    "transit photometry": re.compile(r"\btransit(?:ing)?\s+photometry\b", re.IGNORECASE),
    "radial velocity": re.compile(r"\bradial[\s-]velocity\b", re.IGNORECASE),
    "direct imaging": re.compile(r"\bdirect(?:ly)?\s+imag(?:ing|ed)\b", re.IGNORECASE),
    "microlensing": re.compile(r"\bmicro-?lensing\b", re.IGNORECASE),
    "transit timing variation": re.compile(r"\btransit[\s-]timing\s+variation", re.IGNORECASE),
    "astrometry": re.compile(r"\bastrometr(?:y|ic)\b", re.IGNORECASE),
}
