from datetime import datetime
from database import SessionLocal
from models.database_models import Takedown, Detection, SuspiciousApp, Brand
from evidence.generator import EvidenceGenerator
import logging


logger = logging.getLogger(__name__)


def generate_takedown_request(takedown_id: int):
    """Generate evidence kit and takedown request"""
    db = SessionLocal()
    
    try:
        # Get takedown
        takedown = db.query(Takedown).filter(Takedown.id == takedown_id).first()
        if not takedown:
            logger.error(f"Takedown {takedown_id} not found")
            return
        
        # Get detection details
        detection = db.query(Detection).filter(Detection.id == takedown.detection_id).first()
        if not detection:
            logger.error(f"Detection not found for takedown {takedown_id}")
            return
        
        # Get brand and suspicious app
        brand = db.query(Brand).filter(Brand.id == detection.brand_id).first()
        suspicious_app = db.query(SuspiciousApp).filter(
            SuspiciousApp.id == detection.suspicious_app_id
        ).first()
        
        # Initialize evidence generator
        generator = EvidenceGenerator()
        
        # Generate evidence kit
        logger.info(f"Generating evidence kit for takedown {takedown_id}")
        evidence_path = generator.create_evidence_kit(
            brand=brand,
            suspicious_app=suspicious_app,
            detection=detection
        )
        
        # Generate takedown request
        logger.info(f"Generating takedown request for {takedown.store}")
        request_body = generator.create_takedown_request(
            brand=brand,
            suspicious_app=suspicious_app,
            detection=detection,
            store=takedown.store
        )
        
        # Update takedown record
        takedown.evidence_kit_path = evidence_path
        takedown.request_body = request_body
        takedown.status = "submitted"
        db.commit()
        
        logger.info(f"Takedown request generated successfully: {takedown_id}")
        
    except Exception as e:
        logger.error(f"Error generating takedown request: {e}")
        takedown.status = "failed"
        db.commit()
    
    finally:
        db.close()
