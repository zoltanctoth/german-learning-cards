"""Quick test to verify API returns correct UTF-8 data."""
from main import get_google_sheet_data
import json

print("Testing Google Sheets data fetch with UTF-8 encoding...\n")

try:
    cards = get_google_sheet_data()
    print(f"✓ Fetched {len(cards)} card(s)\n")

    for i, card in enumerate(cards, 1):
        print(f"Card {i}:")
        print(f"  German: {card['german']}")
        print(f"  Translation: {card['translation']}")
        print()

    # Test JSON serialization (what the API will return)
    print("JSON serialization test:")
    json_str = json.dumps(cards[0], ensure_ascii=False, indent=2)
    print(json_str)
    print()

    # Verify special characters are preserved
    if 'ó' in cards[0]['translation']:
        print("✓ UTF-8 special characters (ó) correctly preserved!")
    else:
        print("✗ UTF-8 encoding issue detected")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
