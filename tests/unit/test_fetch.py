"""Tests for retrieval/fetch.py - specifically fetch_incremental's resilience
to arXiv API failures mid-pagination. All mocked, no live network calls.
"""

from __future__ import annotations

from unittest.mock import patch

from config import settings
from retrieval import fetch
from retrieval.arxiv_client import ArxivPaper
from state.manifest import Manifest


def _paper(arxiv_id: str) -> ArxivPaper:
    return ArxivPaper(
        arxiv_id=arxiv_id,
        versioned_id=f"{arxiv_id}v1",
        title=f"Paper {arxiv_id}",
        abstract="abstract",
        published="2026-01-01",
        updated="2026-01-01",
        categories=["astro-ph.EP"],
        pdf_url="https://example.invalid/x.pdf",
        entry_id="https://arxiv.org/abs/x",
    )


def _use_tmp_data_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "vector_data_dir", tmp_path)
    settings.ensure_dirs()


def _search_since_raises_after(papers, exc):
    def _gen(*args, **kwargs):
        yield from papers
        raise exc

    return _gen()


@patch("retrieval.fetch.arxiv_client.download_pdf")
@patch("retrieval.fetch.arxiv_client.search_since")
def test_fetch_incremental_keeps_papers_fetched_before_a_pagination_failure(
    mock_search_since, mock_download_pdf, tmp_path, monkeypatch
):
    """Regression test: fetch_incremental used to have no exception handling
    around its search_since loop, unlike fetch_curated's per-query guard. A
    live run hit sustained HTTP 429s from arXiv on page 2 of results, the
    client exhausted its retries, and the raised exception propagated
    straight up and killed the whole process - losing papers already fetched
    in the same run. Fixed by wrapping the loop the same way fetch_curated
    wraps its per-query loop: log and stop, don't crash."""
    _use_tmp_data_dir(tmp_path, monkeypatch)
    mock_search_since.return_value = _search_since_raises_after(
        [_paper("1111.1111"), _paper("2222.2222")], RuntimeError("HTTP 429")
    )

    summary = fetch.fetch_incremental("20260711")

    assert summary["fetched"] == 2
    manifest = Manifest(settings.manifest_path)
    assert set(manifest.all_fetched_ids()) == {"1111.1111", "2222.2222"}


@patch("retrieval.fetch.arxiv_client.download_pdf")
@patch("retrieval.fetch.arxiv_client.search_since")
def test_fetch_incremental_skips_already_seen_papers(
    mock_search_since, mock_download_pdf, tmp_path, monkeypatch
):
    _use_tmp_data_dir(tmp_path, monkeypatch)
    manifest = Manifest(settings.manifest_path)
    fetch._save_paper(_paper("1111.1111"), manifest)
    mock_download_pdf.reset_mock()

    mock_search_since.return_value = iter([_paper("1111.1111"), _paper("3333.3333")])

    summary = fetch.fetch_incremental("20260711")

    assert summary["fetched"] == 2
    assert mock_download_pdf.call_count == 1  # only the new paper triggered a download
