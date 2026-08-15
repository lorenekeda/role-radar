from fastapi import FastAPI

from app.routes.opportunities import router as opportunities_router

app = FastAPI(
    title="Role Radar API",
    description="API for aggregating and managing job opportunities",
    version="1.0.0",
)

app.include_router(opportunities_router)

@app.get("/")
def root():
    return {"message": "Role Radar API is running!"}