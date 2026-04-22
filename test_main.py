from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_educate_endpoint():
    response = client.post("/api/educate", json={"query": "How do I vote?"})
    assert response.status_code == 200
    assert response.json() == {"message": "This is a mocked response for the chatbot query.", "sanitized_query": "How do I vote?"}

def test_locate_endpoint():
    response = client.post("/api/locate", json={"zip_code": "12345"})
    assert response.status_code == 200
    assert response.json() == {"polling_place": "Mocked Polling Place at 123 Main St", "zip_code": "12345"}

def test_locate_endpoint_invalid_zip():
    response = client.post("/api/locate", json={"zip_code": "1234"})
    assert response.status_code == 422
