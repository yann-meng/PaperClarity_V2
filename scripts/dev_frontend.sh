#!/usr/bin/env bash
set -euo pipefail

# Load nvm when available so node/npm are discoverable in non-interactive shells.
if ! command -v npm >/dev/null 2>&1 && [ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]; then
  # shellcheck disable=SC1090
  . "${NVM_DIR:-$HOME/.nvm}/nvm.sh"
fi

cd "$(dirname "$0")/../app/frontend"

if command -v npm >/dev/null 2>&1; then
  npm install
  npm run dev -- --host 0.0.0.0 --port 5173
elif command -v pnpm >/dev/null 2>&1; then
  pnpm install
  pnpm dev --host 0.0.0.0 --port 5173
elif command -v yarn >/dev/null 2>&1; then
  yarn install
  yarn dev --host 0.0.0.0 --port 5173
else
  echo "No supported package manager found (npm/pnpm/yarn)." >&2
  echo "Install Node.js and ensure your shell can access it, then retry." >&2
  exit 127
fi
