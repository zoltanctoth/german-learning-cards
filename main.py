import csv
import os
import random
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from io import StringIO
from typing import Dict

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

load_dotenv()

DB_FILE = os.getenv("DB_FILE", "learning_progress.db")

# Sheet column headers. Changing the sheet's column names requires updating these.
COL_ID = "id"
COL_GERMAN = "Deutsch"
COL_TRANSLATION = "Bedeutung"
COL_CATEGORY = "Kategorie"

_cards_cache: list[Dict[str, str]] | None = None


class CardAttempt(BaseModel):
    card_id: str
    correct: bool


def init_database():
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
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_card_id ON card_attempts(card_id)")
    conn.commit()
    conn.close()


def save_card_attempt(card_id: str, correct: bool):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO card_attempts (card_id, timestamp, correct) VALUES (?, ?, ?)",
        (card_id, datetime.now().isoformat(), correct),
    )
    conn.commit()
    conn.close()


def get_google_sheet_data() -> list[Dict[str, str]]:
    """Fetch the public sheet as CSV and parse it into card dicts."""
    spreadsheet_url = os.getenv("GOOGLE_SHEET_URL")
    if not spreadsheet_url:
        raise ValueError("GOOGLE_SHEET_URL environment variable is not set")

    if "/d/" not in spreadsheet_url:
        raise ValueError("Invalid Google Sheets URL format")
    sheet_id = spreadsheet_url.split("/d/")[1].split("/")[0]

    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        response.encoding = "utf-8"
    except Exception as e:
        raise ValueError(f"Failed to fetch Google Sheet data: {e}")

    reader = csv.DictReader(StringIO(response.text))
    if reader.fieldnames is None:
        raise ValueError("Spreadsheet must have at least a header row and one data row")

    cards: list[Dict[str, str]] = []
    for row in reader:
        card_id = (row.get(COL_ID) or "").strip()
        german = (row.get(COL_GERMAN) or "").strip()
        translation = (row.get(COL_TRANSLATION) or "").strip()
        if not (card_id and german and translation):
            continue
        card = {"id": card_id, "german": german, "translation": translation}
        category = (row.get(COL_CATEGORY) or "").strip()
        if category:
            card["category"] = category
        cards.append(card)

    if not cards:
        raise ValueError("Spreadsheet must have at least a header row and one data row")
    return cards


def get_cards() -> list[Dict[str, str]]:
    global _cards_cache
    if _cards_cache is None:
        _cards_cache = get_google_sheet_data()
    return _cards_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(title="German Learning Cards API", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Default HTTP metrics (request count, latency histogram, in-progress) at /metrics.
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# TODO(business-metrics): define custom flashcard metrics here.
# See record_attempt() below for where these get incremented.


@app.get("/healthz", include_in_schema=False)
async def healthz():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/api")
async def api_info():
    return {
        "message": "German Learning Cards API",
        "endpoints": {
            "/card": "Get a random learning card",
            "/cards/reload": "Reload cards from Google Sheets",
            "/attempt": "Record a card attempt (POST)",
        },
    }


@app.get("/card")
async def get_random_card() -> Dict[str, str]:
    try:
        cards = get_cards()
        if not cards:
            raise HTTPException(status_code=404, detail="No cards available")
        return random.choice(cards)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cards/reload")
async def reload_cards():
    global _cards_cache
    _cards_cache = None
    try:
        cards = get_cards()
        return {"message": f"Successfully reloaded {len(cards)} cards"}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/attempt")
async def record_attempt(attempt: CardAttempt):
    save_card_attempt(attempt.card_id, attempt.correct)
    # TODO(business-metrics): increment your custom Prometheus counter(s) here.
    return {
        "message": "Attempt recorded successfully",
        "card_id": attempt.card_id,
        "correct": attempt.correct,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
