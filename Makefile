##
## vector — arXiv exoplanet/astronomy RAG pipeline
##
## This pipeline runs on atadev (GPU + an already-running shared Ollama
## daemon), not on this laptop. See PLAN.md for why.
##
## Remote targets (require REMOTE=user@hostname):
##   make deploy         — rsync source to the remote (code only, not data/)
##   make venv-remote    — create venv + pip install on the remote
##   make run-remote     — deploy, then `python pipeline.py run-all`
##   make eval-remote    — run the baseline-vs-RAG evaluation harness
##   make status-remote  — print manifest status
##   make fetch-report   — pull data/eval/report.md back into ./reports/
##   make shell-remote   — interactive shell in the remote venv
##
## Example:
##   make run-remote REMOTE=atadev
##

REMOTE     ?= atadev
REMOTE_DIR ?= /home/paolo/vector-rag
# Data lives off /home/paolo (near-full quota) on the 15TB raid1 array -
# see PLAN.md "Execution environment". Only the code is under REMOTE_DIR.
REMOTE_DATA_DIR ?= /mnt/raid1/paolo_tests/vector-rag/data

# Optional local overrides (not committed): create local.mk to point at a
# different host, e.g.
#   REMOTE := lapii
-include local.mk

.PHONY: deploy venv-remote run-remote eval-remote status-remote fetch-report shell-remote _check-remote

_check-remote:
	@[ -n "$(REMOTE)" ] || { \
	    echo ""; \
	    echo "ERROR: REMOTE is not set."; \
	    echo "Usage: make $(MAKECMDGOALS) REMOTE=user@hostname"; \
	    echo ""; \
	    exit 1; \
	}

deploy: _check-remote ## Rsync source to the remote (excludes data/, venv, caches).
	ssh $(REMOTE) "mkdir -p $(REMOTE_DIR)"
	rsync -az --delete \
	    --exclude='.git' \
	    --exclude='.venv' \
	    --exclude='__pycache__' \
	    --exclude='*.pyc' \
	    --exclude='data' \
	    --exclude='reports' \
	    ./ $(REMOTE):$(REMOTE_DIR)/

venv-remote: deploy ## Create the venv and install dependencies on the remote.
	ssh -t $(REMOTE) "cd $(REMOTE_DIR) && \
	    python3 -m venv .venv && \
	    .venv/bin/pip install --upgrade pip && \
	    .venv/bin/pip install -r requirements.txt"

run-remote: deploy ## Run the full pipeline (fetch -> ... -> index) on the remote.
	ssh -t $(REMOTE) "cd $(REMOTE_DIR) && .venv/bin/python pipeline.py run-all"

eval-remote: ## Run the baseline-vs-RAG evaluation harness on the remote.
	ssh -t $(REMOTE) "cd $(REMOTE_DIR) && .venv/bin/python -m evaluation.run_eval"

status-remote: ## Print manifest status from the remote.
	ssh $(REMOTE) "cd $(REMOTE_DIR) && .venv/bin/python pipeline.py status"

fetch-report: _check-remote ## Pull data/eval/report.md back into ./reports/.
	mkdir -p reports
	rsync -az $(REMOTE):$(REMOTE_DATA_DIR)/eval/report.md ./reports/eval-report.md
	@echo "-> reports/eval-report.md"

shell-remote: _check-remote ## Interactive shell in the remote venv.
	ssh -t $(REMOTE) "cd $(REMOTE_DIR) && source .venv/bin/activate && bash"
