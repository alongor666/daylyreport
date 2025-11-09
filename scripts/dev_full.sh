#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -d ".venv" && -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

if [[ -n "${PYTHON_CMD:-}" ]]; then
  if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
    echo "PYTHON_CMD is set to '$PYTHON_CMD' but the command was not found."
    exit 1
  fi
else
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
  else
    echo "Python 3 is required. Install python3 or set PYTHON_CMD to a valid interpreter."
    exit 1
  fi
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required. Install Node.js (>= 18) before running this script."
  exit 1
fi

if [[ ! -d "frontend/node_modules" ]]; then
  echo "frontend/node_modules is missing. Run 'cd frontend && npm install' first."
  exit 1
fi

BACKEND_PID=""

cleanup() {
  if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    echo "Stopping backend (PID: $BACKEND_PID)..."
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
    wait "$BACKEND_PID" >/dev/null 2>&1 || true
  fi
}

handle_signal() {
  echo ""
  echo "Received interrupt. Shutting down services..."
  cleanup
  exit 130
}

trap handle_signal INT TERM

echo "Starting backend API server..."
(
  cd backend
  "$PYTHON_CMD" api_server.py
) &
BACKEND_PID=$!
echo "Backend is running on http://localhost:${API_PORT:-5001} (PID: $BACKEND_PID)"

echo "Starting Vite dev server..."
cd frontend
npm run dev
FRONTEND_EXIT=$?

cleanup
exit $FRONTEND_EXIT
