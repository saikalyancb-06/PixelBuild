from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class BrandCreate(BaseModel):
    name: str
    package_ids: List[str]
    icon_urls: List[str]
    developer_name: str
    certificates: Optional[List[str]] = []


class BrandResponse(BaseModel):
    id: int
    name: str
    package_ids: List[str]
    icon_urls: List[str]
    developer_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class SuspiciousAppResponse(BaseModel):
    id: int
    package_id: str
    app_name: str
    developer_name: str
    icon_url: str
    store_url: str
    source: str
    download_count: int
    rating: Optional[float]

    class Config:
        from_attributes = True


class DetectionResponse(BaseModel):
    id: int
    brand_id: int
    suspicious_app_id: int
    icon_similarity_score: float
    text_similarity_score: float
    certificate_match: bool
    confidence_score: float
    risk_level: str
    detection_reasons: List[str]
    status: str
    detected_at: datetime

    class Config:
        from_attributes = True


class ScanJobCreate(BaseModel):
    brand_id: int
    sources: List[str] = ["play_store", "app_store", "apk_mirror"]


class ScanJobResponse(BaseModel):
    id: int
    brand_id: int
    sources: List[str]
    status: str
    apps_scanned: int
    detections_found: int
    created_at: datetime

    class Config:
        from_attributes = True


class TakedownCreate(BaseModel):
    detection_id: int
    store: str


class TakedownResponse(BaseModel):
    id: int
    detection_id: int
    store: str
    status: str
    submitted_at: datetime
    time_to_takedown: Optional[int]

    class Config:
        from_attributes = True


class MetricsResponse(BaseModel):
    total_apps_scanned: int
    fake_apps_detected: int
    detection_rate: float
    takedowns_submitted: int
    takedowns_successful: int
    success_rate: float
    avg_detection_time: float
    avg_time_to_takedown: float
    user_exposure_prevented: int
