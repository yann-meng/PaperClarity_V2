#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Ensure backend source root is on PYTHONPATH so absolute imports like `api.*` resolve.
export PYTHONPATH="$(pwd)/app/backend${PYTHONPATH:+:$PYTHONPATH}"

uvicorn app.backend.main:app --reload --host 0.0.0.0 --port 8000
