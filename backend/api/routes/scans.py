from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.database_models import ScanJob, Brand
from models.schemas import ScanJobCreate, ScanJobResponse
from tasks.scan_tasks import run_scan_job

router = APIRouter()


@router.post("/", response_model=ScanJobResponse)
async def create_scan(
    scan: ScanJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start a new scan job for a brand"""
    # Verify brand exists
    brand = db.query(Brand).filter(Brand.id == scan.brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Create scan job
    scan_job = ScanJob(
        brand_id=scan.brand_id,
        sources=scan.sources,
        status="pending"
    )
    db.add(scan_job)
    db.commit()
    db.refresh(scan_job)
    
    # Queue the scan task
    background_tasks.add_task(run_scan_job, scan_job.id)
    
    return scan_job


@router.get("/", response_model=List[ScanJobResponse])
async def list_scans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all scan jobs"""
    scans = db.query(ScanJob).offset(skip).limit(limit).all()
    return scans


@router.get("/{scan_id}", response_model=ScanJobResponse)
async def get_scan(scan_id: int, db: Session = Depends(get_db)):
    """Get scan job details"""
    scan = db.query(ScanJob).filter(ScanJob.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan
