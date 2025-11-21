from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from api.routes import brands, detections, scans, takedowns, metrics, quick_check, evidence_kit
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fake App Detection API",
    description="API for detecting and reporting counterfeit mobile applications",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://10.17.233.15:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(brands.router, prefix="/api/brands", tags=["Brands"])
app.include_router(scans.router, prefix="/api/scans", tags=["Scans"])
app.include_router(detections.router, prefix="/api/detections", tags=["Detections"])
app.include_router(takedowns.router, prefix="/api/takedowns", tags=["Takedowns"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])
app.include_router(quick_check.router, tags=["Quick Check"])
app.include_router(evidence_kit.router, tags=["Evidence Kit"])


@app.get("/")
async def root():
    return {
        "message": "Fake App Detection API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fake-app-detection"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
