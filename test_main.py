import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app, get_google_sheet_data, get_cards


# Test client for FastAPI
client = TestClient(app)


# Mock card data for testing
MOCK_CARDS = [
    {"id": "1", "german": "Hallo", "translation": "Hello"},
    {"id": "2", "german": "Danke", "translation": "Thank you"},
    {"id": "3", "german": "Guten Tag", "translation": "Good day"},
]


@pytest.fixture
def mock_env_var(monkeypatch):
    """Set up mock environment variable for tests."""
    monkeypatch.setenv("GOOGLE_SHEET_URL", "https://docs.google.com/spreadsheets/d/1CP_2dqL2AdOguQd4BClfuEM66SakoH0HgrQCSjkJ8kA/edit")


@pytest.fixture
def mock_google_sheets():
    """Mock Google Sheets CSV export calls."""
    csv_data = """id,German,Translation
1,Hallo,Hello
2,Danke,Thank you
3,Guten Tag,Good day"""

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = csv_data
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture(autouse=True)
def reset_cache():
    """Reset the global cache before each test."""
    import main
    main._cards_cache = None
    yield
    main._cards_cache = None


@pytest.fixture(autouse=True)
def cleanup_database():
    """Clean up test database before and after each test."""
    import os
    from main import DB_FILE, init_database

    # Remove database if it exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    # Initialize fresh database
    init_database()

    yield

    # Clean up after test
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)


def test_root_endpoint():
    """Test the root endpoint returns HTML page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert b"German Learning Cards" in response.content


def test_api_endpoint():
    """Test the /api endpoint returns API information."""
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert "/card" in data["endpoints"]


def test_get_card_endpoint(mock_env_var, mock_google_sheets):
    """Test the /card endpoint returns a random card."""
    response = client.get("/card")
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "german" in data
    assert "translation" in data
    assert isinstance(data["id"], str)
    assert isinstance(data["german"], str)
    assert isinstance(data["translation"], str)


def test_get_card_endpoint_returns_valid_card(mock_env_var, mock_google_sheets):
    """Test that /card endpoint returns one of the expected cards."""
    response = client.get("/card")
    assert response.status_code == 200

    data = response.json()
    # The card should be one of our mock cards
    assert data in MOCK_CARDS


def test_get_card_endpoint_multiple_calls(mock_env_var, mock_google_sheets):
    """Test that multiple calls to /card work correctly."""
    cards_received = []

    for _ in range(10):
        response = client.get("/card")
        assert response.status_code == 200
        cards_received.append(response.json())

    # All cards should be valid
    for card in cards_received:
        assert card in MOCK_CARDS


def test_get_google_sheet_data_no_env_var():
    """Test that get_google_sheet_data raises error when GOOGLE_SHEET_URL is not set."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GOOGLE_SHEET_URL environment variable is not set"):
            get_google_sheet_data()


def test_get_google_sheet_data_invalid_url(mock_env_var):
    """Test that get_google_sheet_data raises error with invalid URL format."""
    with patch.dict(os.environ, {"GOOGLE_SHEET_URL": "https://invalid-url.com"}):
        with pytest.raises(ValueError, match="Invalid Google Sheets URL format"):
            get_google_sheet_data()


def test_get_google_sheet_data_success(mock_env_var, mock_google_sheets):
    """Test successful data extraction from Google Sheets."""
    cards = get_google_sheet_data()

    assert len(cards) == 3
    assert cards[0] == {"id": "1", "german": "Hallo", "translation": "Hello"}
    assert cards[1] == {"id": "2", "german": "Danke", "translation": "Thank you"}
    assert cards[2] == {"id": "3", "german": "Guten Tag", "translation": "Good day"}


def test_get_cards_caching(mock_env_var, mock_google_sheets):
    """Test that get_cards() uses caching."""
    import main

    # First call should fetch from Google Sheets
    cards1 = get_cards()
    assert len(cards1) == 3

    # Cache should be populated
    assert main._cards_cache is not None

    # Second call should use cache (not call Google Sheets again)
    cards2 = get_cards()
    assert cards1 == cards2


def test_reload_cards_endpoint(mock_env_var, mock_google_sheets):
    """Test the /cards/reload endpoint."""
    # First, get a card to populate cache
    client.get("/card")

    # Reload cards
    response = client.post("/cards/reload")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "3 cards" in data["message"]


def test_get_google_sheet_data_empty_rows(mock_env_var):
    """Test that empty rows are skipped."""
    csv_data = """id,German,Translation
1,Hallo,Hello
2,,
3,Danke,Thank you
4,   ,   """

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = csv_data
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        cards = get_google_sheet_data()

        # Should only have 2 valid cards (empty rows skipped)
        assert len(cards) == 2
        assert cards[0] == {"id": "1", "german": "Hallo", "translation": "Hello"}
        assert cards[1] == {"id": "3", "german": "Danke", "translation": "Thank you"}


def test_get_google_sheet_data_no_data_rows(mock_env_var):
    """Test error when spreadsheet has only header row."""
    csv_data = """id,German,Translation"""

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = csv_data
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Spreadsheet must have at least a header row and one data row"):
            get_google_sheet_data()


def test_record_attempt_endpoint(mock_env_var, mock_google_sheets):
    """Test the /attempt endpoint records card attempts."""
    response = client.post("/attempt", json={
        "card_id": "1",
        "correct": True
    })
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["card_id"] == "1"
    assert data["correct"] is True


def test_record_attempt_incorrect(mock_env_var, mock_google_sheets):
    """Test recording an incorrect attempt."""
    response = client.post("/attempt", json={
        "card_id": "2",
        "correct": False
    })
    assert response.status_code == 200

    data = response.json()
    assert data["card_id"] == "2"
    assert data["correct"] is False
