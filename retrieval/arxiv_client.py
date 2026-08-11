"""Thin, rate-limited wrapper over the `arxiv` package.

arXiv's API terms of use require staying under ~1 request per 3 seconds;
`arxiv.Client(delay_seconds=...)` already enforces that between page fetches,
so callers just iterate results normally.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

import arxiv

from config import settings

_VERSION_SUFFIX = re.compile(r"v\d+$")


def normalize_id(short_id: str) -> str:
    """Strip the trailing version (e.g. '2301.01234v2' -> '2301.01234')."""
    return _VERSION_SUFFIX.sub("", short_id)


@dataclass
class ArxivPaper:
    arxiv_id: str  # version-stripped, used as the manifest/storage key
    versioned_id: str
    title: str
    abstract: str
    published: str
    updated: str
    categories: list[str]
    pdf_url: str
    entry_id: str


def _to_paper(result: arxiv.Result) -> ArxivPaper:
    short_id = result.get_short_id()
    return ArxivPaper(
        arxiv_id=normalize_id(short_id),
        versioned_id=short_id,
        title=result.title.strip(),
        abstract=result.summary.strip(),
        published=result.published.isoformat() if result.published else "",
        updated=result.updated.isoformat() if result.updated else "",
        categories=list(result.categories),
        pdf_url=result.pdf_url,
        entry_id=result.entry_id,
    )


def _client() -> arxiv.Client:
    # export.arxiv.org's API is intermittently flaky (obsered 503/429/timeouts
    # even under normal use) - the client only sleeps `delay_seconds` between
    # retries with no backoff, so a generous retry count is needed to ride out
    # a transient blip instead of failing the whole query.
    return arxiv.Client(
        page_size=100,
        delay_seconds=settings.arxiv_request_delay_seconds,
        num_retries=10,
    )


def search(
    query: str,
    max_results: int = 50,
    sort_by: arxiv.SortCriterion = arxiv.SortCriterion.Relevance,
) -> Iterator[ArxivPaper]:
    """Search arXiv, scoped to the configured categories, for `query`."""
    category_filter = " OR ".join(f"cat:{c}" for c in settings.arxiv_categories)
    full_query = f"({category_filter}) AND ({query})"
    search_obj = arxiv.Search(query=full_query, max_results=max_results, sort_by=sort_by)
    for result in _client().results(search_obj):
        yield _to_paper(result)


def search_since(
    since_date: str,
    max_results: int = 1000,
) -> Iterator[ArxivPaper]:
    """Incremental mode: everything in the configured categories submitted since `since_date`
    (format YYYYMMDD). Used by the later broad/weekly ingestion mode, not the initial curated pull.
    """
    category_filter = " OR ".join(f"cat:{c}" for c in settings.arxiv_categories)
    full_query = f"({category_filter}) AND submittedDate:[{since_date}0000 TO 99991231]"
    search_obj = arxiv.Search(
        query=full_query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate
    )
    for result in _client().results(search_obj):
        yield _to_paper(result)


def download_pdf(paper: ArxivPaper, dest_path: str) -> None:
    import urllib.request

    req = urllib.request.Request(paper.pdf_url, headers={"User-Agent": "vector-rag/0.1"})
    with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())
