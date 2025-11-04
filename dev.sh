#!/bin/bash
# Development server with auto-reload

echo "🚀 Starting German Learning Cards in development mode..."
echo ""
echo "Features:"
echo "  ✓ Auto-reload on Python file changes"
echo "  ✓ Auto-reload on template changes (Jinja2)"
echo "  ✓ Server: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
