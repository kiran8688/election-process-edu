from fastapi.testclient import TestClient
from main import app
from schemas import ChatbotQuery, PollingLocator
from pydantic import ValidationError
import pytest

client = TestClient(app)

# Schema Validation Tests
def test_chatbot_query_schema_valid():
    query = ChatbotQuery(query="Valid query")
    assert query.query == "Valid query"

def test_chatbot_query_schema_invalid():
    with pytest.raises(ValidationError):
        ChatbotQuery(query="") # Empty query violates min_length=1

def test_polling_locator_schema_valid():
    locator = PollingLocator(zip_code="12345")
    assert locator.zip_code == "12345"

def test_polling_locator_schema_invalid_length():
    with pytest.raises(ValidationError):
        PollingLocator(zip_code="1234") # Not 5 digits

def test_polling_locator_schema_invalid_chars():
    with pytest.raises(ValidationError):
        PollingLocator(zip_code="12abc") # Contains letters

# Endpoint Tests
def test_educate_endpoint_mocked():
    response = client.post("/api/educate", json={"query": "How do I vote?"})
    assert response.status_code == 200
    json_resp = response.json()
    assert "AI Simulation" in json_resp["message"]
    assert json_resp["sanitized_query"] == "How do I vote?"

def test_educate_endpoint_sanitization():
    response = client.post("/api/educate", json={"query": "<script>alert('xss')</script>"})
    assert response.status_code == 200
    assert response.json()["sanitized_query"] == "&lt;script&gt;alert('xss')&lt;/script&gt;"

def test_locate_endpoint():
    response = client.post("/api/locate", json={"zip_code": "12345"})
    assert response.status_code == 200
    assert response.json() == {
        "polling_place": "Mocked Polling Place for ZIP 12345",
        "zip_code": "12345",
        "lat": 38.8977,
        "lng": -77.0365
    }

def test_locate_endpoint_invalid_zip():
    response = client.post("/api/locate", json={"zip_code": "1234"})
    assert response.status_code == 422

def test_config_endpoint():
    response = client.get("/api/config")
    assert response.status_code == 200
    assert "maps_api_key" in response.json()

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
