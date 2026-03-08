#!/bin/sh

echo "START.SH: Running migrations..."

alembic upgrade head

echo "START.SH: Starting server..."

uvicorn main:app --host 0.0.0.0 --port 8000