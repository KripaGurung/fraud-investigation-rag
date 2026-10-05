from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
    }

def test_investigation_generation_route_is_registered():
    response = client.post(
        "/investigations/ALERT-DOES-NOT-EXIST/generate",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Fraud alert 'ALERT-DOES-NOT-EXIST' was not found."
    )    