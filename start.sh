#!/bin/sh
set -e

echo "START.SH: Running migrations..."
echo "START.SH: Migrations disabled for now..."

# alembic upgrade head

echo "START.SH: Starting server..."

exec uvicorn main:app --reload --host ${APP_HOST} --port ${APP_PORT}
