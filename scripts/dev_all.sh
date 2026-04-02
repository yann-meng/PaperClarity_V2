#!/usr/bin/env bash
set -euo pipefail
ROOT="$(dirname "$0")/.."
(
  cd "$ROOT/app/frontend"
  npm install
  npm run dev -- --host 0.0.0.0 --port 5173
) &
(
  cd "$ROOT"
  uvicorn app.backend.main:app --reload --host 0.0.0.0 --port 8000
)

./scripts/dev_backend.sh

