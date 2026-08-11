# Design Choices

Why this pipeline is built the way it is. This covers architecture and
technology decisions only, nothing tied to any particular machine - the
goal is that another astronomer can read this, stand the pipeline up on
their own hardware, and understand every choice without needing access to
the environment it was originally built on. See `README.md` for setup and
usage; `REPORT.md` for evaluation methodology and results.

## Environment and dependencies

Plain `python3 -m venv` plus a pinned `requirements.txt`, rather than
conda or a lockfile-based tool. This keeps the dependency footprint small
and the setup reproducible with nothing beyond a standard Python install.

A local [Ollama](https://ollama.com) daemon provides both the embedding
model and the chat model, so there's exactly one runtime to install for
all model inference, no separate torch/sentence-transformers stack to
manage. Model names are configurable via `.env` (`EMBEDDING_MODEL`,
`GENERATION_MODEL`), so this scales from a laptop running a small model to
a GPU server running a much larger one without any code changes - pick a
model sized to whatever hardware is available.

## arXiv retrieval

The `arxiv` PyPI package wraps arXiv's Atom API and enforces the mandatory
rate limit. In practice, `export.arxiv.org`'s API is intermittently flaky:
503s, 429s, and bare timeouts were observed even under correctly
rate-limited, non-abusive use. `retrieval/arxiv_client.py` sets
`num_retries=10` (the library only sleeps `delay_seconds` between retries,
no backoff, so a generous retry count is needed to ride out a transient
blip), and `retrieval/fetch.py` wraps each seed query in its own
try/except so one query exhausting its retries doesn't abort the whole
fetch run.

### Incremental-ingestion design

`retrieval/fetch.py` has two entry points that share all the same
downstream code:

- `fetch_curated(seed_set, ...)` - runs a fixed list of seed queries
  (`retrieval/seeds.py`), used to build an initial corpus in one pass.
- `fetch_incremental(since_date)` - filters by category and arXiv's
  `submittedDate`, pulling only what's new since a given date.

Both funnel into the same manifest-tracked save path, so nothing about
downstream processing (parsing, chunking, embedding, ...) needs to know
which mode fetched a given paper. Moving from a one-time curated pull to
an ongoing weekly/incremental ingestion is a matter of calling
`fetch_incremental` on a schedule (cron, or any job scheduler) instead of
`fetch_curated` once - no pipeline rework required. The main thing to plan
for before turning that on is storage growth, since an ongoing crawl has
no natural stopping point the way a curated seed list does.

## PDF parsing

`pymupdf4llm` converts each PDF to structured markdown, preserving
headings so chunking can split on document structure. It was chosen over
heavier layout-aware ML parsers (e.g. `marker-pdf`) because it has no
GPU/torch dependency and is fast enough to run entirely on CPU - a
deliberate tradeoff of some fidelity on complex layouts (multi-column
author/affiliation blocks in particular; see `REPORT.md`'s account of a
chunk that mixed affiliation footnotes with abstract text) for keeping the
whole pipeline runnable without a GPU if needed.

## Entity and metadata extraction

Planet and star designations (`Kepler-452b`, `TOI-700 d`, `WASP-12b`,
`TRAPPIST-1e`, `HD 209458`, ...) follow regular enough naming conventions
that hand-written regex (`extraction/patterns.py`) catches the great
majority of real mentions without needing to train or run an NER model.
Detection-method mentions (transit, radial velocity, direct imaging,
microlensing, TTV, astrometry) are tagged the same way. This is
deliberately a heuristic, not a source of truth: it exists to enrich chunk
metadata for filtered retrieval, not to extract precise planet parameters.

## Chunking

`semantic-text-splitter`'s `MarkdownSplitter` splits on markdown structure
(headings, paragraphs, sentences) within a token-count target (400-800
tokens, 80 token overlap), rather than cutting at a fixed character
offset. This keeps chunks semantically coherent - a chunk is much less
likely to end mid-sentence or split a claim from its citation - at the
cost of some chunk-size variance.

## Vector storage and retrieval

**LanceDB** (embedded, on-disk, Arrow-native) holds chunk text, metadata,
and embeddings in one table. It was chosen over alternatives like Chroma
or a standalone FAISS index because it supports hybrid search - dense
vector similarity and full-text/BM25 search over the same table - without
running a separate server process. Hybrid search matters here because
exact designations ("TOI-700 d") need lexical matching that dense
embedding similarity alone tends to miss, while paraphrased or conceptual
questions ("planets in the habitable zone") need the reverse. The two
result sets are merged with reciprocal rank fusion (RRF) in
`query/retriever.py`, computed manually rather than via LanceDB's built-in
hybrid search, which requires registering an embedding function with the
table - keeping embedding entirely under this project's own control
(`embedding/embedder.py`) instead was simpler to reason about.

### Reranking

RRF fusion alone can still bury a genuinely relevant chunk if it only
scores well on one signal. This was diagnosed concretely while building
the evaluation set (see `REPORT.md`): a chunk containing an
almost-verbatim answer to a test question ranked 22nd out of 258 RRF-fused
candidates - well outside a top-8 cutoff - because it had a strong
full-text match (rank 16) but a mediocre dense-vector rank (68), and RRF's
averaging punished that mismatch.

The standard fix is a cross-encoder reranker (e.g. `bge-reranker-v2-m3`),
but that pulls in `sentence-transformers`/torch as a new, fairly heavy
dependency for a single pipeline stage. `query/reranker.py` instead reuses
the chat model already running for generation: given the question and a
wider RRF candidate pool (30, configurable via `settings.rerank_pool_size`),
it asks the model to return the most relevant ones in order, with a
fallback to the plain RRF ordering if the model's response can't be
parsed. This fixed the diagnosed case with no new dependency, at the cost
of one extra model call per query - worth it for answer quality, though
latency-sensitive interactive use may want `rerank_enabled = False`.

## Generation and grounding

The RAG prompt (`query/generator.py`) instructs the model to answer only
from the provided excerpts, cite sources inline as `[arXiv:<id>]`, and say
so explicitly if the excerpts don't contain enough information rather than
guessing. That last instruction is deliberate: a retrieval gap should
produce an honest "I don't know" rather than a confident, uncited guess,
even though it costs a point on a strict correctness check when the base
model happens to know the answer from its own training. See `REPORT.md`
for a concrete example of this tradeoff.

## State tracking and idempotency

A SQLite manifest (`state/manifest.py`) tracks, per paper, whether each
pipeline stage (fetch, parse, extract, chunk, embed, store, index) has
completed. Every phase only processes papers that finished the previous
stage but not the current one (`ids_ready_for(stage)`), which makes the
whole pipeline safe to interrupt and rerun at any point, and is what makes
incremental ingestion (above) cheap: a rerun only ever touches what's
actually new or unfinished.

## Evaluation methodology

Two independent scoring signals, not one: a keyword-match check (cheap,
fast, fully auditable, but brittle to phrasing) and an LLM-judge pass
(`evaluation/judge.py`, semantic, more robust to paraphrasing, but not a
ground-truth oracle). Building the eval set surfaced concrete cases where
each one mattered - keyword matching for catching a fabricated wrong
answer verbatim, the judge for recognizing "did not find a significant
trend" and "no significant trend" as the same claim. Reporting both scores
together, rather than collapsing to one number, is itself a design choice:
a divergence between them is a signal worth reading, not noise to average
away. Full methodology and results are in `REPORT.md`.
