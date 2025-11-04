#!/bin/bash
# Simple start script (alternative, single worker)
# Use this for smaller instances or development

set -e

echo "Starting German Learning Cards (simple mode)..."

exec uvicorn main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000}
