from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.routes.alerts import router


def create_test_app(db: Session) -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_db] = lambda: db

    return app


def test_list_alerts_route_returns_alerts(db: Session) -> None:
    app = create_test_app(db)

    response = TestClient(app).get("/alerts")

    assert response.status_code == 200

    body = response.json()

    assert len(body) >= 1
    assert any(
        alert["alert_reference"] == "ALERT-001"
        for alert in body
    )

def test_get_alert_detail_route_returns_alert(db: Session) -> None:
    app = create_test_app(db)

    response = TestClient(app).get("/alerts/ALERT-001")

    assert response.status_code == 200

    body = response.json()

    assert body["alert_reference"] == "ALERT-001"
    assert body["transaction"]["transaction_reference"]
    assert body["account"]["account_number"]
    assert body["customer"]["customer_number"]    

def test_get_alert_detail_route_returns_404_for_unknown_alert(
    db: Session,
) -> None:
    app = create_test_app(db)

    response = TestClient(app).get(
        "/alerts/ALERT-DOES-NOT-EXIST",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Fraud alert 'ALERT-DOES-NOT-EXIST' was not found."
    )    