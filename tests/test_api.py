from fastapi.testclient import TestClient

from api.main import app


def test_create_workflow_endpoint() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/workflows",
        json={"request_id": "req-42", "goal": "Research LangGraph operations"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["state"]["request_id"] == "req-42"
    assert payload["state"]["approval_status"] == "pending"
