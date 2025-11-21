from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    package_ids = Column(JSON)  # List of legitimate package IDs
    icon_urls = Column(JSON)  # List of official icon URLs
    developer_name = Column(String)
    certificates = Column(JSON)  # List of valid certificate fingerprints
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    detections = relationship("Detection", back_populates="brand")


class SuspiciousApp(Base):
    __tablename__ = "suspicious_apps"

    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(String, unique=True, index=True)
    app_name = Column(String)
    developer_name = Column(String)
    icon_url = Column(String)
    screenshot_urls = Column(JSON)
    store_url = Column(String)
    source = Column(String)  # play_store, app_store, apk_mirror, etc.
    download_count = Column(Integer, default=0)
    rating = Column(Float)
    reviews_count = Column(Integer, default=0)
    certificate_fingerprint = Column(String)
    sdk_list = Column(JSON)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, default=datetime.utcnow)

    detections = relationship("Detection", back_populates="suspicious_app")


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    suspicious_app_id = Column(Integer, ForeignKey("suspicious_apps.id"))
    
    # Detection scores
    icon_similarity_score = Column(Float)
    text_similarity_score = Column(Float)
    certificate_match = Column(Boolean)
    review_fraud_score = Column(Float)
    sdk_anomaly_score = Column(Float)
    
    # Combined score
    confidence_score = Column(Float)
    risk_level = Column(String)  # LOW, MEDIUM, HIGH, CRITICAL
    
    # Evidence
    evidence_path = Column(String)
    detection_reasons = Column(JSON)
    
    # Status
    status = Column(String, default="pending")  # pending, confirmed, false_positive, reported
    detected_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    
    brand = relationship("Brand", back_populates="detections")
    suspicious_app = relationship("SuspiciousApp", back_populates="detections")
    takedowns = relationship("Takedown", back_populates="detection")


class Takedown(Base):
    __tablename__ = "takedowns"

    id = Column(Integer, primary_key=True, index=True)
    detection_id = Column(Integer, ForeignKey("detections.id"))
    store = Column(String)  # play_store, app_store, etc.
    request_id = Column(String)
    request_body = Column(Text)
    evidence_kit_path = Column(String)
    
    status = Column(String, default="submitted")  # submitted, acknowledged, taken_down, rejected
    submitted_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Metrics
    time_to_takedown = Column(Integer, nullable=True)  # in hours
    
    detection = relationship("Detection", back_populates="takedowns")


class ScanJob(Base):
    __tablename__ = "scan_jobs"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    sources = Column(JSON)  # List of sources to scan
    status = Column(String, default="pending")  # pending, running, completed, failed
    
    apps_scanned = Column(Integer, default=0)
    detections_found = Column(Integer, default=0)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    error_message = Column(Text, nullable=True)


class Metrics(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    total_apps_scanned = Column(Integer, default=0)
    fake_apps_detected = Column(Integer, default=0)
    takedowns_submitted = Column(Integer, default=0)
    takedowns_successful = Column(Integer, default=0)
    
    avg_detection_time = Column(Float, default=0.0)  # seconds
    avg_time_to_takedown = Column(Float, default=0.0)  # hours
    
    user_exposure_prevented = Column(Integer, default=0)  # estimated downloads prevented
