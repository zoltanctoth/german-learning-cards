# Development Mode Guide

## Quick Start

```bash
./dev.sh
```

Or manually:
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## What Auto-Reloads?

### ✅ Automatically Reloads (No Manual Action Needed)

**Backend Code (Python files)**
- Changes to `main.py` → Server restarts automatically
- Changes to any `.py` file → Server restarts automatically
- Database schema changes → Restart happens automatically

**After server restarts:**
- Just wait ~1-2 seconds
- The page will reconnect automatically (FastAPI handles this)

### 🔄 Requires Browser Refresh

**Frontend (Templates/HTML/CSS/JS)**
- Changes to `templates/index.html` → Press **F5** or **Cmd+R**
- CSS changes in `<style>` tags → Press **F5** or **Cmd+R**
- JavaScript changes in `<script>` tags → Press **F5** or **Cmd+R**
- Changes to files in `static/` → Press **F5** or **Cmd+R**

**Why?** The HTML/CSS/JS are loaded by your browser, not the server. FastAPI serves fresh templates on each request, so a simple refresh gets the latest version.

### 🔴 Requires Full Restart

**Environment Variables**
- Changes to `.env` → Stop server (Ctrl+C) and restart
- Changes to `pyproject.toml` → Stop and restart

**Database Structure**
- If you manually change the database schema, you may need to delete the `.db` file and restart

## Tips for Fast Development

### 1. Keep Browser Developer Tools Open
- **Chrome/Edge**: Press F12 or Cmd+Option+I
- **Disable Cache**: In Network tab, check "Disable cache"
- This ensures you always get fresh CSS/JS

### 2. Use Auto-Refresh Browser Extension (Optional)
Install "Auto Refresh" extension for your browser:
- Chrome: [Auto Refresh Plus](https://chrome.google.com/webstore)
- Firefox: [Auto Refresh](https://addons.mozilla.org/firefox/)

Set it to refresh every 2 seconds while developing.

### 3. Two-Monitor Setup
- **Monitor 1**: Your code editor
- **Monitor 2**: Browser with the app

### 4. Keyboard Shortcuts
- **Save file**: Cmd+S / Ctrl+S
- **Refresh browser**: Cmd+R / Ctrl+R or F5
- **Hard refresh**: Cmd+Shift+R / Ctrl+Shift+R or Ctrl+F5

## Common Development Workflow

### Changing Backend Logic
```
1. Edit main.py
2. Save file (Cmd+S)
3. Wait 1-2 seconds (server auto-restarts)
4. Test in browser (no refresh needed if using API)
```

### Changing Frontend (HTML/CSS)
```
1. Edit templates/index.html
2. Save file (Cmd+S)
3. Refresh browser (F5)
4. See changes immediately
```

### Changing Both
```
1. Edit main.py (backend changes)
2. Edit templates/index.html (frontend changes)
3. Save both files
4. Wait for server restart (~1-2 sec)
5. Refresh browser
```

## Watching File Changes

If you want to see what files trigger reloads, uvicorn shows this in the console:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

When you save a Python file:
```
INFO:     WatchFiles detected changes in 'main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [12346]
INFO:     Started server process [12347]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Alternative: Production Mode

For production (no auto-reload):
```bash
uv run python main.py
```

Or:
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

**Server doesn't restart on save?**
- Make sure you're using `--reload` flag
- Check file is actually saved (look for asterisk in editor tab)
- Some editors save to temp files; try saving explicitly

**Browser shows old version after refresh?**
- Hard refresh: Cmd+Shift+R or Ctrl+Shift+R
- Clear browser cache
- Open DevTools and check "Disable cache"

**Port already in use?**
- Kill existing process: `lsof -ti:8000 | xargs kill`
- Or change port: `--port 8001`

**Changes not appearing?**
- Backend changes: Check server restarted (see console logs)
- Frontend changes: Hard refresh browser
- Database changes: May need to delete `.db` file
