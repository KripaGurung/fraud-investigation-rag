import pytest
from sqlalchemy.orm import Session

from api.db.session import SessionLocal


@pytest.fixture
def db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()