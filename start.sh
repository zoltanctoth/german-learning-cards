#!/bin/bash
# Start script for German Learning Cards app
# Compatible with render.com and other hosting platforms

# Exit on error
set -e

echo "Starting German Learning Cards application..."

# Clear any conflicting VIRTUAL_ENV variable
unset VIRTUAL_ENV

# Install dependencies if needed (render.com does this automatically, but good to have)
if [ ! -d ".venv" ]; then
    echo "Installing dependencies..."
    uv sync
fi

# Start the FastAPI application with uvicorn
# - host 0.0.0.0 allows external connections
# - port ${PORT:-8000} uses PORT env var if set, otherwise defaults to 8000
# - workers 4 for production (adjust based on your render.com instance size)
exec uv run python -m uvicorn main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --workers 4
