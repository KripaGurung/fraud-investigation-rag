from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.db.session import get_db

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Fraud Investigation API is running"}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "healthy",
        "database": "connected",
    }
