from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Fraud Investigation API is running"}