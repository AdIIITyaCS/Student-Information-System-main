#!/usr/bin/env bash
set -euo pipefail

# Use Render's $PYTHON if set, otherwise fall back to python3
PYTHON_BIN="${PYTHON:-python3}"

echo "Using python: ${PYTHON_BIN}"

"${PYTHON_BIN}" -m pip install -r requirements.txt
"${PYTHON_BIN}" manage.py migrate --noinput
"${PYTHON_BIN}" manage.py collectstatic --noinput
# after collectstatic
"${PYTHON_BIN}" scripts/sync_mongo_to_sqlite.py
"${PYTHON_BIN}" scripts/create_admin.py

echo "Build script finished"
