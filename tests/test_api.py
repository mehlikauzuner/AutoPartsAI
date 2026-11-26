from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_vehicle():
    response = client.post("/vehicles", json={
        "vin": "WVWZZZ1JZXW000001",
        "brand": "Volkswagen",
        "model": "Golf",
        "year": 2020
    })
    assert response.status_code == 200  # Basarili istek
    assert response.json()["brand"] == "Volkswagen"  # Dogru arac


def test_create_part_request():
    response = client.post("/part-requests", json={
        "part_name": "Fren Balatasi",
        "quantity": 2
    })
    assert response.status_code == 200  # Basarili istek
    assert response.json()["quantity"] == 2  # Dogru miktar


def test_chat_page():
    response = client.get("/chat")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "AutoPartsAI" in response.text
    assert 'id="fileInput"' in response.text
    assert "/vehicles/upload-registration" in response.text
