# CLAUDE.md

Guidance for AI agents working in this repo. Keep this short and current.

## What this is

A single-file FastAPI app ([main.py](main.py)) serving a German flashcard UI. Cards are loaded from a public Google Sheet via CSV export; attempt history is stored in a local SQLite DB.

## Architecture (one paragraph)

`GET /` renders [templates/index.html](templates/index.html) (Jinja2 + HTMX + Tailwind CDN, no build step). The page calls `GET /card`, which returns a random row from an in-memory cache populated lazily from the Google Sheet. `POST /attempt` writes a row to `card_attempts` in `learning_progress.db`. `POST /cards/reload` clears the cache. The DB is initialized in the FastAPI `lifespan` handler. No auth, no users — single-user local-first design.

## Commands

| Task            | Command                            |
|-----------------|------------------------------------|
| Install deps    | `uv sync`                          |
| Dev server      | `./dev.sh`                         |
| Production      | `./start.sh`                       |
| Tests           | `uv run pytest test_main.py -v`    |
| Add a dep       | edit `pyproject.toml` then `uv sync` |

Never `pip install` — this project uses `uv` exclusively. The global rule in `~/CLAUDE.md` about the `~/.venv/` virtualenv does **not** apply here; this project has its own `.venv/` managed by `uv sync`.

## Sheet contract (load-bearing)

`get_google_sheet_data()` parses the CSV with `csv.DictReader` keyed on these header names:

- `id` — card identifier (required)
- `Deutsch` — German word (required)
- `Bedeutung` — translation (required)
- `Kategorie` — optional category
- `Fertig?` — ignored

Header constants live at the top of [main.py](main.py) (`COL_ID`, `COL_GERMAN`, etc.). If you rename a column in the sheet, update the constant. Column **order** doesn't matter (DictReader uses names).

## Conventions

- Single file ([main.py](main.py)); don't split into packages unless it grows past ~400 lines.
- Tests mock `requests.get` to avoid hitting the real sheet (see `mock_google_sheets` fixture).
- The DB file is local-only and gitignored; never commit it.
- Frontend uses CDN scripts on purpose — no bundler, no `node_modules`. Don't introduce a build step.

## Things not to do

- Don't recreate `CHECKPOINT.md`, `BUGFIX.md`, `USAGE.md`, or similar working-notes files. They were intentionally removed; use git history / PR descriptions instead.
- Don't add `pip` or `pipenv` workflows. `Pipfile` was removed; uv is the only package manager.
- Don't put a real `GOOGLE_SHEET_URL` in `.env.example` — it must remain a placeholder.
