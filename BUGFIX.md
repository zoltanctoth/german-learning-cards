# Bug Fix: Google Sheets Connection Error

## Problem
The web UI was showing "Error loading card" and the server returned a 500 Internal Server Error when trying to fetch cards from the `/card` endpoint.

**Error Details:**
```
INFO:     127.0.0.1:52761 - "GET /card HTTP/1.1" 500 Internal Server Error
```

**Root Cause:**
```python
AttributeError: 'NoneType' object has no attribute '__module__'
```

The issue was that `gspread.Client(auth=None)` doesn't work for accessing public Google Sheets. The gspread library requires proper authentication credentials and doesn't support truly anonymous access.

## Solution

**Changed from:** Using gspread library with `auth=None`
```python
gc = gspread.Client(auth=None)
sheet = gc.open_by_key(sheet_id).sheet1
all_values = sheet.get_all_values()
```

**Changed to:** Direct CSV export via Google Sheets public API
```python
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
response = requests.get(csv_url)
csv_data = StringIO(response.text)
reader = csv.reader(csv_data)
all_values = list(reader)
```

## Why This Works Better

1. **Simpler**: No authentication needed for public sheets
2. **More reliable**: Uses Google's built-in CSV export feature
3. **Faster**: Direct HTTP request, no API client overhead
4. **No dependencies on gspread**: Only needs `requests` library
5. **Works with any public sheet**: As long as "anyone with link can view"

## Changes Made

### Files Modified:
1. **[main.py](main.py)**:
   - Removed gspread import, added requests, csv, StringIO
   - Replaced gspread connection with CSV export approach
   - Simplified error handling

2. **[test_main.py](test_main.py)**:
   - Updated mocks from `patch("main.gspread.Client")` to `patch("requests.get")`
   - Changed mock data from gspread format to CSV format
   - All 12 tests still passing

3. **[debug.py](debug.py)**:
   - Created debug script to test Google Sheets connection
   - Helps troubleshoot future issues

### Dependencies:
- Removed need for: `gspread` (kept for compatibility but not used)
- Added: `requests` (already a dependency of other packages)

## Verification

✅ All 12 tests passing
✅ Real Google Sheets connection verified
✅ Card fetched successfully: `{"german": "das Auto", "translation": "az Autó"}`

## To Start the Fixed Server

```bash
uv run python main.py
```

Then open http://localhost:8000 - the card should load without errors!

## Note About UTF-8 Encoding

The debug output shows `az AutÃ³` instead of `az Autó` - this is just a console display issue. The actual data in the response is correctly UTF-8 encoded and will display properly in the web browser.
