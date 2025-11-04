import os
import random
import csv
import sqlite3
from datetime import datetime
from io import StringIO
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = FastAPI(title="German Learning Cards API")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global cache for cards
_cards_cache = None

# Database file
DB_FILE = "learning_progress.db"


# Pydantic models for request validation
class CardAttempt(BaseModel):
    card_id: str
    correct: bool


def init_database():
    """Initialize SQLite database with card_attempts table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS card_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            correct BOOLEAN NOT NULL
        )
    """)

    # Create index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_card_id
        ON card_attempts(card_id)
    """)

    conn.commit()
    conn.close()


def save_card_attempt(card_id: str, correct: bool):
    """Save a card attempt to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO card_attempts (card_id, timestamp, correct)
        VALUES (?, ?, ?)
    """, (card_id, datetime.now().isoformat(), correct))

    conn.commit()
    conn.close()


def get_google_sheet_data() -> list[Dict[str, str]]:
    """
    Fetch data from Google Sheets and return as a list of card dictionaries.
    Works with public Google Sheets (anyone with the link can view).
    """
    spreadsheet_url = os.getenv("GOOGLE_SHEET_URL")

    if not spreadsheet_url:
        raise ValueError("GOOGLE_SHEET_URL environment variable is not set")

    # Extract spreadsheet ID from URL
    if "/d/" in spreadsheet_url:
        sheet_id = spreadsheet_url.split("/d/")[1].split("/")[0]
    else:
        raise ValueError("Invalid Google Sheets URL format")

    # Use Google Sheets CSV export for public sheets (simplest approach)
    try:
        # Export as CSV is the simplest way to access public sheets
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

        response = requests.get(csv_url)
        response.raise_for_status()

        # Ensure proper UTF-8 encoding
        response.encoding = 'utf-8'

        # Parse CSV data
        csv_data = StringIO(response.text)
        reader = csv.reader(csv_data)
        all_values = list(reader)

    except Exception as e:
        raise ValueError(f"Failed to fetch Google Sheet data: {str(e)}")

    if len(all_values) < 2:
        raise ValueError("Spreadsheet must have at least a header row and one data row")

    # Skip header row (first row)
    # Expected columns: id, german, translation
    cards = []
    for row in all_values[1:]:
        if len(row) >= 3 and row[0].strip() and row[1].strip() and row[2].strip():
            cards.append({
                "id": row[0].strip(),
                "german": row[1].strip(),
                "translation": row[2].strip()
            })

    return cards


def get_cards() -> list[Dict[str, str]]:
    """
    Get cards from cache or fetch from Google Sheets if cache is empty.
    """
    global _cards_cache

    if _cards_cache is None:
        _cards_cache = get_google_sheet_data()

    return _cards_cache


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_database()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main HTML page."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/api")
async def api_info():
    """API endpoint with information."""
    return {
        "message": "German Learning Cards API",
        "endpoints": {
            "/card": "Get a random learning card",
            "/cards/reload": "Reload cards from Google Sheets"
        }
    }


@app.get("/card")
async def get_random_card() -> Dict[str, str]:
    """
    Get a random learning card from the Google Spreadsheet.

    Returns:
        A dictionary with 'german' and 'translation' keys
    """
    try:
        cards = get_cards()

        if not cards:
            raise HTTPException(status_code=404, detail="No cards available")

        # Return a random card
        return random.choice(cards)

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching card: {str(e)}")


@app.post("/cards/reload")
async def reload_cards():
    """
    Reload cards from Google Sheets (clear cache).
    """
    global _cards_cache
    _cards_cache = None

    try:
        cards = get_cards()
        return {"message": f"Successfully reloaded {len(cards)} cards"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading cards: {str(e)}")


@app.post("/attempt")
async def record_attempt(attempt: CardAttempt):
    """
    Record a card attempt (whether user got it right or wrong).
    """
    try:
        save_card_attempt(attempt.card_id, attempt.correct)
        return {
            "message": "Attempt recorded successfully",
            "card_id": attempt.card_id,
            "correct": attempt.correct
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording attempt: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
