"""Curated seed queries for the initial ~300-500 paper corpus (astro-ph.EP).

Each query is run independently against the arXiv API (scoped to
`config.settings.arxiv_categories`) and results are deduplicated by arXiv ID
in `fetch.py`. This is the "curated-v1" seed set; broader/weekly ingestion
later uses `arxiv_client.search_since` instead of this list.
"""

CURATED_V1: list[str] = [
    "exoplanet atmosphere characterization",
    "transit photometry exoplanet",
    "radial velocity survey exoplanet",
    "habitable zone terrestrial planet",
    "exoplanet detection method review",
    "hot Jupiter formation migration",
    "TESS exoplanet discovery",
    "Kepler exoplanet catalog occurrence rate",
    "exoplanet biosignature spectroscopy",
    "planet formation protoplanetary disk",
    "exomoon detection",
    "direct imaging exoplanet young planet",
    "microlensing exoplanet survey",
    "exoplanet interior structure composition",
    "brown dwarf companion",
    "super-Earth mini-Neptune population",
    "JWST exoplanet transmission spectrum",
    "exoplanet host star metallicity",
    "circumbinary planet",
    "exoplanet atmospheric escape",
]

SEED_SETS: dict[str, list[str]] = {
    "curated-v1": CURATED_V1,
}
