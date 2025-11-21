from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.database_models import Detection, ScanJob, Takedown, Metrics
from models.schemas import MetricsResponse

router = APIRouter()


@router.get("/", response_model=MetricsResponse)
async def get_metrics(db: Session = Depends(get_db)):
    """Get overall system metrics"""
    
    # Total apps scanned
    total_scanned = db.query(func.sum(ScanJob.apps_scanned)).scalar() or 0
    
    # Fake apps detected
    fake_apps = db.query(Detection).count()
    
    # Takedowns
    takedowns_submitted = db.query(Takedown).count()
    takedowns_successful = db.query(Takedown).filter(
        Takedown.status == "taken_down"
    ).count()
    
    # Calculate rates
    detection_rate = (fake_apps / total_scanned * 100) if total_scanned > 0 else 0
    success_rate = (takedowns_successful / takedowns_submitted * 100) if takedowns_submitted > 0 else 0
    
    # Average time to takedown
    avg_ttd = db.query(func.avg(Takedown.time_to_takedown)).scalar() or 0
    
    # User exposure prevented (estimated)
    user_exposure = db.query(func.sum(Metrics.user_exposure_prevented)).scalar() or 0
    
    return MetricsResponse(
        total_apps_scanned=total_scanned,
        fake_apps_detected=fake_apps,
        detection_rate=round(detection_rate, 2),
        takedowns_submitted=takedowns_submitted,
        takedowns_successful=takedowns_successful,
        success_rate=round(success_rate, 2),
        avg_detection_time=3.2,  # Mock value
        avg_time_to_takedown=round(avg_ttd, 2),
        user_exposure_prevented=user_exposure
    )


@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    
    # Detections by risk level
    risk_distribution = db.query(
        Detection.risk_level,
        func.count(Detection.id)
    ).group_by(Detection.risk_level).all()
    
    # Detections by status
    status_distribution = db.query(
        Detection.status,
        func.count(Detection.id)
    ).group_by(Detection.status).all()
    
    # Recent detections
    recent_detections = db.query(Detection).order_by(
        Detection.detected_at.desc()
    ).limit(10).all()
    
    return {
        "risk_distribution": dict(risk_distribution),
        "status_distribution": dict(status_distribution),
        "recent_detections_count": len(recent_detections),
        "high_confidence_detections": db.query(Detection).filter(
            Detection.confidence_score >= 0.95
        ).count()
    }
