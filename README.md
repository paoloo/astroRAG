# vector — arXiv Exoplanet/Astronomy RAG Pipeline

Retrieval-augmented generation over arXiv `astro-ph.EP` papers: fetch papers,
parse them, extract astronomy entities, chunk, embed, store in LanceDB,
index, then query/evaluate against a local Ollama model.

Runs on `atadev` (GPU + an already-running shared Ollama daemon), not this
laptop — see `Makefile` and `PLAN.md` for why and how.

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
query/       hybrid retrieval + generation (interactive: `python -m query.cli`)
evaluation/  baseline vs. RAG-augmented answer comparison
```

## Quickstart (on atadev)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # defaults already point at localhost:11434

ollama pull nomic-embed-text
ollama pull qwen2.5:14b-instruct

python pipeline.py fetch --seed-set curated-v1 --target-total 400
python pipeline.py run-all
python pipeline.py status

python -m query.cli
python -m evaluation.run_eval   # writes data/eval/report.md
```

## Deploying from this laptop

```bash
make deploy REMOTE=atadev        # rsync source to atadev
make run-remote REMOTE=atadev    # run pipeline.py run-all there
make fetch-report REMOTE=atadev  # pull data/eval/report.md back to reports/
```

See `PLAN.md` for the full architecture and stack rationale.
