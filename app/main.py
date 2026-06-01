from fastapi import FastAPI

from app.api.tenders import router as tenders_router

app = FastAPI(
    title="SmartTender Analytics",
    description="AI-ready system for tender monitoring, filtering and analytics.",
    version="0.1.0",
)

app.include_router(tenders_router)


@app.get("/")
def root():
    return {
        "message": "SmartTender Analytics API is running"
    }