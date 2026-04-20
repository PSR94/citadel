#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT_DIR"

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

python3 -m pip install --upgrade pip
(cd apps/api && python3 -m pip install -e ".[dev]")
npm install

echo "Bootstrap complete."
echo "Next steps:"
echo "  1. docker compose up --build"
echo "  2. Open http://localhost:3000"

