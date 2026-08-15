from fastapi import FastAPI

from app.routes.opportunities import router as opportunities_router
from app.routes.ingestion import router as ingestion_router


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

app = FastAPI(
    title="Role Radar API",
    description="API for aggregating and managing job opportunities",
    version="1.0.0",
)

app.include_router(opportunities_router)
app.include_router(ingestion_router)

@app.get("/")
def root():
    return {"message": "Role Radar API is running!"}