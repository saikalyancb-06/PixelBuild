from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.database_models import Takedown, Detection
from models.schemas import TakedownCreate, TakedownResponse
from tasks.takedown_tasks import generate_takedown_request

router = APIRouter()


@router.post("/", response_model=TakedownResponse)
async def create_takedown(
    takedown: TakedownCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Submit a takedown request"""
    # Verify detection exists
    detection = db.query(Detection).filter(Detection.id == takedown.detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    # Create takedown
    db_takedown = Takedown(
        detection_id=takedown.detection_id,
        store=takedown.store,
        status="submitted"
    )
    db.add(db_takedown)
    db.commit()
    db.refresh(db_takedown)
    
    # Queue evidence generation and submission
    background_tasks.add_task(generate_takedown_request, db_takedown.id)
    
    return db_takedown


@router.get("/", response_model=List[TakedownResponse])
async def list_takedowns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all takedown requests"""
    takedowns = db.query(Takedown).offset(skip).limit(limit).all()
    return takedowns


@router.get("/{takedown_id}", response_model=TakedownResponse)
async def get_takedown(takedown_id: int, db: Session = Depends(get_db)):
    """Get takedown details"""
    takedown = db.query(Takedown).filter(Takedown.id == takedown_id).first()
    if not takedown:
        raise HTTPException(status_code=404, detail="Takedown not found")
    return takedown


@router.post("/{takedown_id}/acknowledge")
async def acknowledge_takedown(takedown_id: int, db: Session = Depends(get_db)):
    """Mark takedown as acknowledged by store"""
    takedown = db.query(Takedown).filter(Takedown.id == takedown_id).first()
    if not takedown:
        raise HTTPException(status_code=404, detail="Takedown not found")
    
    from datetime import datetime
    takedown.status = "acknowledged"
    takedown.acknowledged_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Takedown acknowledged", "takedown_id": takedown_id}
