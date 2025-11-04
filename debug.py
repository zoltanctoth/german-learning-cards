"""Debug script to test Google Sheets connection."""
import os
from dotenv import load_dotenv
import requests
import csv
from io import StringIO

load_dotenv()

spreadsheet_url = os.getenv("GOOGLE_SHEET_URL")
print(f"Spreadsheet URL: {spreadsheet_url}")

# Extract spreadsheet ID
if "/d/" in spreadsheet_url:
    sheet_id = spreadsheet_url.split("/d/")[1].split("/")[0]
    print(f"Extracted Sheet ID: {sheet_id}")
else:
    print("ERROR: Invalid URL format")
    exit(1)

# Try to connect using CSV export
try:
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    print(f"\nCSV Export URL: {csv_url}")

    print("\nFetching data via CSV export...")
    response = requests.get(csv_url)
    print(f"Response status: {response.status_code}")
    response.raise_for_status()

    # Ensure proper UTF-8 encoding
    response.encoding = 'utf-8'

    print(f"\nResponse length: {len(response.text)} characters")
    print(f"Response encoding: {response.encoding}")

    # Parse CSV data
    csv_data = StringIO(response.text)
    reader = csv.reader(csv_data)
    all_values = list(reader)

    print(f"Retrieved {len(all_values)} rows")

    print("\nAll rows:")
    for i, row in enumerate(all_values):
        print(f"Row {i}: {row}")

    # Build cards
    print("\n--- Building Cards ---")
    cards = []
    for row in all_values[1:]:  # Skip header
        if len(row) >= 2 and row[0].strip() and row[1].strip():
            card = {
                "german": row[0].strip(),
                "translation": row[1].strip()
            }
            cards.append(card)
            print(f"Card: {card}")

    print(f"\n✓ Successfully parsed {len(cards)} cards")

except Exception as e:
    print(f"\nERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
