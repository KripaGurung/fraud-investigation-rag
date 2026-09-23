from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)
from api.routes.investigations import (
    get_investigation_generator_factory,
    router,
)

class FakeInvestigationGenerator:
    def generate(
        self,
        alert_id: str,
        context,
    ) -> InvestigationCase:
        return InvestigationCase(
            alert_id=alert_id,
            executive_summary="Generated summary.",
            risk_narrative="Generated risk narrative.",
            recommended_follow_up=["Review transaction history."],
        )

class InvalidCitationInvestigationGenerator:
    def generate(
        self,
        alert_id: str,
        context,
    ) -> InvestigationCase:
        return InvestigationCase(
            alert_id=alert_id,
            executive_summary="Generated summary.",
            risk_narrative="Generated risk narrative.",
            supporting_findings=[
                InvestigationFinding(
                    statement="Generated unsupported finding.",
                    evidence_ids=["FAKE-999"],
                )
            ],
        )    

def create_test_app(db: Session) -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[
    get_investigation_generator_factory
    ] = lambda: lambda: FakeInvestigationGenerator()

    return app


def test_generate_investigation_route_returns_case(db: Session) -> None:
    app = create_test_app(db)

    response = TestClient(app).post(
        "/investigations/ALERT-001/generate",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["alert_id"] == "ALERT-001"
    assert body["executive_summary"] == "Generated summary."
    assert body["risk_narrative"] == "Generated risk narrative."
    assert body["recommended_follow_up"] == [
        "Review transaction history."
    ]


def test_generate_investigation_route_returns_404_for_unknown_alert(db: Session,) -> None:
    app = create_test_app(db)

    response = TestClient(app).post(
        "/investigations/ALERT-DOES-NOT-EXIST/generate",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Fraud alert 'ALERT-DOES-NOT-EXIST' was not found."
    )

def test_generate_investigation_route_returns_502_for_invalid_citations(
    db: Session,
) -> None:
    app = create_test_app(db)

    app.dependency_overrides[
        get_investigation_generator_factory
    ] = lambda: lambda: InvalidCitationInvestigationGenerator()

    response = TestClient(app).post(
        "/investigations/ALERT-001/generate",
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Generated investigation contains invalid evidence citations: "
        "FAKE-999"
    )    