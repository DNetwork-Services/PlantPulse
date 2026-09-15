from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api import assets, maintenance, work_orders


app = FastAPI(
    title="PlantPulse API",
    description="Ethanol Plant Operations & Asset Management Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router)
app.include_router(maintenance.router)
app.include_router(work_orders.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "plantpulse-backend"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "reachable"}


@app.get("/")
def root():
    return {"message": "PlantPulse API is running"}