from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_investigate_alert_returns_investigation_result() -> None:
    response = client.post(
        "/api/v1/investigations/ALERT-001",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["alert_id"] == "ALERT-001"
    assert data["summary"]

    assert "supporting_evidence" in data
    assert "contradicting_evidence" in data
    assert "missing_evidence" in data

    assert isinstance(data["supporting_evidence"], list)
    assert isinstance(data["contradicting_evidence"], list)
    assert isinstance(data["missing_evidence"], list)


def test_investigate_unknown_alert_returns_404() -> None:
    response = client.post(
        "/api/v1/investigations/ALERT-DOES-NOT-EXIST",
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data
    assert "ALERT-DOES-NOT-EXIST" in data["detail"]