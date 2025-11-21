from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import get_db
from models.database_models import Detection, SuspiciousApp, Brand
from models.schemas import DetectionResponse

router = APIRouter()


@router.get("/", response_model=List[DetectionResponse])
async def list_detections(
    skip: int = 0,
    limit: int = 100,
    min_confidence: float = Query(0.0, ge=0.0, le=1.0),
    risk_level: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all detections with filters"""
    query = db.query(Detection).options(
        joinedload(Detection.suspicious_app),
        joinedload(Detection.brand)
    )
    
    if min_confidence > 0:
        query = query.filter(Detection.confidence_score >= min_confidence)
    
    if risk_level:
        query = query.filter(Detection.risk_level == risk_level)
    
    if status:
        query = query.filter(Detection.status == status)
    
    detections = query.offset(skip).limit(limit).all()
    return detections


@router.get("/{detection_id}", response_model=DetectionResponse)
async def get_detection(detection_id: int, db: Session = Depends(get_db)):
    """Get detection details"""
    detection = db.query(Detection).filter(Detection.id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection


@router.post("/{detection_id}/confirm")
async def confirm_detection(detection_id: int, db: Session = Depends(get_db)):
    """Confirm a detection as true positive"""
    detection = db.query(Detection).filter(Detection.id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    detection.status = "confirmed"
    db.commit()
    
    return {"message": "Detection confirmed", "detection_id": detection_id}


@router.post("/{detection_id}/false-positive")
async def mark_false_positive(detection_id: int, db: Session = Depends(get_db)):
    """Mark a detection as false positive"""
    detection = db.query(Detection).filter(Detection.id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    detection.status = "false_positive"
    db.commit()
    
    return {"message": "Marked as false positive", "detection_id": detection_id}
