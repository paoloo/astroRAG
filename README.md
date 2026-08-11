# arXiv Exoplanet/Astronomy RAG Pipeline Experiment

Retrieval-augmented generation over arXiv `astro-ph.EP` papers: fetch papers,
parse them, extract astronomy entities, chunk, embed, store in LanceDB,
index, then query/evaluate against a local Ollama model.

Runs entirely on your own hardware and your own local Ollama daemon - a
GPU speeds up embedding, reranking, and generation, but nothing here
requires one. See `reports/design-choices.md` for why it's built this way.

## Layout

Each pipeline phase is its own directory; `pipeline.py` orchestrates them
via a manifest (`state/manifest.py`, backed by `data/manifest.sqlite3`) that
makes every stage idempotent and reruns cheap.

```
retrieval/   arXiv fetch
parsing/     PDF -> markdown
extraction/  exoplanet/star designation + detection-method tagging
chunking/    section+token aware chunking
embedding/   Ollama embeddings
storage/     LanceDB persistence
indexing/    ANN + full-text index build
query/       hybrid retrieval + reranking + generation (interactive: `python -m query.cli`)
evaluation/  baseline vs. RAG-augmented answer comparison, keyword + LLM-judge scoring
```

## Quickstart

Requires Python 3.10+ and a running [Ollama](https://ollama.com) daemon.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # defaults already point at localhost:11434

ollama pull nomic-embed-text
ollama pull qwen2.5:14b-instruct   # or any other Ollama chat model - see .env.example

python pipeline.py fetch --seed-set curated-v1 --target-total 400
python pipeline.py run-all
python pipeline.py status

python -m query.cli
python -m evaluation.run_eval   # writes data/eval/report.md
```

## Running the tests

```bash
python -m pytest tests/unit -v          # fast, offline, no live services
python -m pytest tests/integration -v   # requires Ollama + a populated LanceDB table; several minutes
```

## Deploying to a remote GPU host

The `Makefile` targets are optional, for running the pipeline on a
separate machine (e.g. a shared lab GPU server) over SSH instead of
locally:

```bash
make deploy REMOTE=user@host        # rsync source to the remote
make run-remote REMOTE=user@host    # run pipeline.py run-all there
make fetch-report REMOTE=user@host  # pull data/eval/report.md back to reports/
```

See `reports/design-choices.md` for the full architecture and stack
rationale, and `REPORT.md` for evaluation methodology and results.

## License

MIT - see `LICENSE`.
