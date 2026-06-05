from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_returns_response():
    response = client.post(
        "/api/chat",
        json={"message": "What should I improve next?", "mode": "trainer"},
    )

    assert response.status_code == 200
    assert response.json()["response"]
    assert response.json()["session_id"]


def test_training_example_and_export():
    example_response = client.post(
        "/api/training/examples",
        json={
            "prompt": "Say hello",
            "completion": "Hello. I am KAYA.",
            "tags": ["test"],
            "rating": 5,
        },
    )

    assert example_response.status_code == 200
    assert example_response.json()["example"]["rating"] == 5

    status_response = client.get("/api/training/status")
    assert status_response.status_code == 200
    assert status_response.json()["stats"]["examples"] >= 1

    export_response = client.post("/api/training/export")
    assert export_response.status_code == 200
    assert export_response.json()["examples"] >= 1


def test_calculator_endpoint():
    response = client.post(
        "/api/calculator",
        json={"expression": "sqrt(144)+sin(pi/2)+2^5"},
    )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["result"] == "45"


def test_chat_uses_calculator():
    response = client.post(
        "/api/chat",
        json={"message": "calculate sqrt(144)+sin(pi/2)+2^5"},
    )

    assert response.status_code == 200
    assert "Answer: 45" in response.json()["response"]
