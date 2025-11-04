# Project Checkpoint - German Learning Cards App

**Date**: 2025-10-18
**Status**: Backend Complete, Frontend Pending

## What We've Built

### Backend (COMPLETED ✓)

A Python 3.13 FastAPI backend that serves German learning flashcards from a Google Spreadsheet.

**Key Files**:
- [main.py](main.py) - FastAPI application with card endpoints
- [test_main.py](test_main.py) - Pytest test suite (11 tests, all passing)
- [.env](.env) - Environment configuration with Google Sheets URL
- [pyproject.toml](pyproject.toml) - uv project dependencies

**API Endpoints**:
1. `GET /` - API information
2. `GET /card` - Returns random card: `{"german": "...", "translation": "..."}`
3. `POST /cards/reload` - Reloads cards from Google Sheets

**Google Sheets Integration**:
- Source: https://docs.google.com/spreadsheets/d/1CP_2dqL2AdOguQd4BClfuEM66SakoH0HgrQCSjkJ8kA/edit?usp=sharing
- Format: Column 1 = German, Column 2 = Translation (Hungarian/English)
- First row is header (skipped)
- Uses public access (no authentication required)
- Cards are cached in memory for performance

**Tech Stack**:
- Python 3.13
- FastAPI + uvicorn
- gspread (Google Sheets API)
- python-dotenv
- pytest + httpx (testing)
- uv (package manager)

### How to Run the Backend

```bash
# Activate virtual environment (optional)
source .venv/bin/activate

# Start the server
uv run python main.py
# OR
uv run uvicorn main:app --reload

# Run tests
uv run pytest test_main.py -v
```

Server runs at: http://localhost:8000

## What's Next - Frontend

### User Requirements
- Keep it as simple as possible (user doesn't know JavaScript/TypeScript)
- Display learning cards from the backend
- Minimal complexity

### Recommended Frontend Options

**Option 1: Jinja2 Templates + FastAPI (RECOMMENDED)**
- Pure Python-based HTML templates
- Served directly by FastAPI
- Minimal to no JavaScript needed
- Simple button to get next card
- Good for server-side rendering

**Option 2: Streamlit**
- 100% Python, zero JavaScript
- Quick to build UI
- Runs as separate app
- Very beginner-friendly

**Option 3: HTMX + Jinja2**
- Uses HTML attributes instead of JavaScript
- Still simple, but adds dynamic updates
- Good middle ground

**Option 4: Simple HTML File**
- Single HTML file with minimal vanilla JS
- Just use fetch() API to call backend
- Can open directly in browser

### Questions to Answer in Next Session

1. Which frontend approach do you prefer?
2. Do you want to run frontend and backend together or separately?
3. Any specific UI requirements (show answer immediately, flip card effect, etc.)?

## Project Structure

```
german-learning-cards/
├── .venv/                  # Virtual environment (Python 3.13)
├── main.py                 # FastAPI backend ✓
├── test_main.py            # Tests ✓
├── .env                    # Environment config ✓
├── .env.example            # Template ✓
├── .gitignore             # Git ignore rules ✓
├── pyproject.toml         # Dependencies ✓
├── README.md              # Documentation ✓
└── CHECKPOINT.md          # This file ✓
```

## Environment Variables

Located in `.env`:
```
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/1CP_2dqL2AdOguQd4BClfuEM66SakoH0HgrQCSjkJ8kA/edit?usp=sharing
```

## Dependencies Installed

**Main**:
- fastapi==0.119.0
- uvicorn==0.37.0
- gspread==6.2.1
- python-dotenv==1.1.1

**Dev**:
- pytest==8.4.2
- httpx==0.28.1

## Test Results

All 11 tests passing:
- Root endpoint test
- Card endpoint tests (single, multiple calls, validation)
- Google Sheets data extraction tests
- Caching mechanism tests
- Error handling tests
- Empty row handling tests

## Important Notes

1. **Virtual Environment**: Always use `uv run` or activate `.venv` - never install to global Python
2. **Google Sheets**: Must be public (anyone with link can view) for current implementation
3. **Caching**: Cards are cached after first load; use `/cards/reload` endpoint to refresh
4. **Git**: `.env` is gitignored (contains configuration, but could have secrets in future)

## To Resume in Next Session

Say something like:
> "I want to continue with the German learning cards app. I prefer [Option X] for the frontend."

Or:
> "Let's continue. Show me the checkpoint and let's implement the frontend with [your preference]."

The assistant should:
1. Read this CHECKPOINT.md file
2. Verify the backend is working
3. Implement the chosen frontend approach
4. Help with deployment if needed
