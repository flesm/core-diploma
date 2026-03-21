#!/bin/bash
set -e

echo "Applying migrations to alembic..."
alembic upgrade head

echo "Starting FastAPI server..."
exec uvicorn src.app.presentation.rest.main:app --host 0.0.0.0 --port 8000
