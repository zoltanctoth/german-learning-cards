# Project Checkpoint v2 - German Learning Cards App

**Date**: 2025-10-18
**Status**: ✅ FULLY WORKING - Backend + Frontend Complete

## Current State

### ✅ What's Working
1. **Backend API** - FastAPI serving cards from Google Sheets
2. **Web UI** - Beautiful flip card interface (mobile + desktop)
3. **Google Sheets Integration** - CSV export method with UTF-8 support
4. **All Tests Passing** - 12/12 tests green

### 🎯 Quick Start

```bash
# Start the server
uv run python main.py

# Open browser
http://localhost:8000

# Run tests
uv run pytest test_main.py -v
```

## Tech Stack

**Backend:**
- Python 3.13 + uv
- FastAPI + Jinja2 templates
- requests (for Google Sheets CSV export)

**Frontend:**
- HTML + Tailwind CSS (via CDN)
- Vanilla JavaScript (~80 lines)
- CSS 3D transforms for card flip

**Data Source:**
- Google Sheets (public, CSV export)
- Example: https://docs.google.com/spreadsheets/d/1CP_2dqL2AdOguQd4BClfuEM66SakoH0HgrQCSjkJ8kA

## Recent Bug Fixes

### Issue 1: Google Sheets Connection Error (500)
**Fixed:** Switched from gspread to direct CSV export
- Before: `gspread.Client(auth=None)` → AttributeError
- After: `requests.get(csv_url)` → Works perfectly

### Issue 2: UTF-8 Encoding (ó showing as Ã³)
**Fixed:** Explicit encoding declaration
```python
response.encoding = 'utf-8'
```

## File Structure

```
german-learning-cards/
├── main.py                 # FastAPI backend ✓
├── test_main.py            # 12 tests (all passing) ✓
├── templates/
│   └── index.html         # Flip card UI ✓
├── static/                 # Static files (empty for now)
├── debug.py               # Debug script for testing
├── test_api.py            # API UTF-8 test script
├── .env                   # Configuration ✓
├── .env.example           # Template ✓
├── pyproject.toml         # Dependencies ✓
├── README.md              # Documentation ✓
├── USAGE.md               # How to use & customize ✓
├── BUGFIX.md              # Bug fix documentation ✓
├── CHECKPOINT.md          # Original checkpoint ✓
└── CHECKPOINT_v2.md       # This file ✓
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI (HTML) |
| `/api` | GET | API info (JSON) |
| `/card` | GET | Random card (JSON) |
| `/cards/reload` | POST | Reload from sheets |

## Dependencies

**Production:**
- fastapi==0.119.0
- uvicorn==0.37.0
- jinja2==3.1.6
- python-dotenv==1.1.1
- requests==2.32.5

**Development:**
- pytest==8.4.2
- httpx==0.28.1

## UI Features

**Card Interaction:**
1. Click once → Flip to show translation
2. Click again → Load next card

**Buttons:**
- Skip Card → Get new card without revealing
- Reload Deck → Refresh from Google Sheets

**Responsive Design:**
- Mobile: 300px card height
- Desktop: 400px card height
- Touch-friendly tap targets

## Configuration

**Environment Variables (.env):**
```
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_ID/edit
```

**Google Sheets Format:**
- Row 1: Headers (ignored)
- Column A: German expression
- Column B: Translation
- Must be public (anyone with link can view)

## Testing

```bash
# Run all tests
uv run pytest test_main.py -v

# Test Google Sheets connection
uv run python debug.py

# Test UTF-8 encoding
uv run python test_api.py
```

## Known Working State

- ✅ Server starts without errors
- ✅ UI loads correctly
- ✅ Cards fetch from Google Sheets
- ✅ UTF-8 characters display properly (ó, ü, ß, etc.)
- ✅ Flip animation works smoothly
- ✅ Mobile responsive
- ✅ All tests pass

## Next Steps (If Needed)

### Potential Enhancements:
1. **Add more cards to spreadsheet** - Just edit the Google Sheet
2. **Track progress** - Add counter showing cards reviewed
3. **Mark cards as learned** - Store state (would need backend storage)
4. **Add multiple decks** - Support multiple spreadsheet URLs
5. **Keyboard shortcuts** - Space to flip, Enter for next
6. **Sound effects** - Audio feedback on flip
7. **Dark mode** - Toggle between light/dark themes
8. **Statistics** - Track learning progress over time

### Deployment Options:
- **Heroku**: Easy Python deployment
- **Railway**: Modern alternative to Heroku
- **Render**: Free tier available
- **Fly.io**: Edge deployment
- **VPS**: Digital Ocean, Linode, etc.

## How to Resume

Just say:
> "Let's continue with the German learning cards app. I want to [add feature/fix issue/deploy]."

Or:
> "Read CHECKPOINT_v2.md and let's [do something]."

## Troubleshooting

**Cards not loading?**
```bash
uv run python debug.py  # Test connection
```

**Special characters broken?**
- Check that UTF-8 encoding line is present in main.py:51

**Tests failing?**
```bash
uv run pytest test_main.py -v  # See which test fails
```

## Context Summary for Claude

When resuming:
1. App is fully functional
2. All bugs fixed (connection + encoding)
3. 12 tests passing
4. Ready for enhancements or deployment
5. User is a developer, wants readable code
6. Using HTMX + Tailwind (simple, no build step)
