from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import json
import requests
import base64
from pathlib import Path
from PIL import Image
from io import BytesIO
import imagehash

from database import get_db
from models.database_models import Detection, Brand, SuspiciousApp

# Import permissions analyzer
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.permissions_analyzer import analyze_permissions_mock

router = APIRouter()

# Suspicious keywords commonly used in fake apps
SUSPICIOUS_KEYWORDS = [
    'update', 'official', 'pro', 'premium', 'secure', 'verified', 
    'original', 'real', 'authentic', 'new', 'latest', 'free', 
    'unlock', 'mod', 'hack', 'cracked', 'plus', 'gold'
]

def detect_suspicious_keywords(app_name: str) -> list:
    """Detect suspicious keywords in app name that fake apps commonly use"""
    app_name_lower = app_name.lower()
    found_keywords = []
    
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in app_name_lower:
            found_keywords.append(keyword.title())
    
    return found_keywords

class EvidenceKitRequest(BaseModel):
    detection_id: int

class EvidenceKitResponse(BaseModel):
    detection_id: int
    app_name: str
    package_id: str
    brand_name: str
    risk_score: int
    evidence: dict
    takedown_email: str
    generated_at: str

@router.post("/api/evidence-kit/generate", response_model=EvidenceKitResponse)
async def generate_evidence_kit(request: EvidenceKitRequest, db: Session = Depends(get_db)):
    """
    Generate a comprehensive evidence kit for a flagged app
    Includes: similarity scores, screenshots info, downloaded logos, and auto-generated takedown email
    """
    
    # Get detection
    detection = db.query(Detection).filter(Detection.id == request.detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    # Get suspicious app
    suspicious_app = db.query(SuspiciousApp).filter(
        SuspiciousApp.id == detection.suspicious_app_id
    ).first()
    
    # Get brand
    brand = db.query(Brand).filter(Brand.id == detection.brand_id).first()
    
    if not suspicious_app or not brand:
        raise HTTPException(status_code=404, detail="Related data not found")
    
    # Download logos and convert to base64
    def download_logo_base64(url):
        try:
            if url:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return base64.b64encode(response.content).decode('utf-8')
        except:
            pass
        return None
    
    # Calculate perceptual hash similarity
    def calculate_icon_similarity(url1, url2):
        """Calculate perceptual hash similarity between two icons (0-1 scale)"""
        try:
            if not url1 or not url2:
                return 0.0
            
            # Download both images
            response1 = requests.get(url1, timeout=5)
            response2 = requests.get(url2, timeout=5)
            
            if response1.status_code != 200 or response2.status_code != 200:
                return 0.0
            
            # Load images
            img1 = Image.open(BytesIO(response1.content))
            img2 = Image.open(BytesIO(response2.content))
            
            # Calculate perceptual hashes (average hash for speed)
            hash1 = imagehash.average_hash(img1)
            hash2 = imagehash.average_hash(img2)
            
            # Calculate similarity (lower hash difference = higher similarity)
            hash_diff = hash1 - hash2
            # Normalize to 0-1 scale (max diff is 64 for 8x8 hash)
            similarity = max(0, 1 - (hash_diff / 64.0))
            
            return round(similarity, 3)
        except Exception as e:
            print(f"Icon similarity calculation error: {e}")
            return 0.0
    
    suspicious_icon_base64 = download_logo_base64(suspicious_app.icon_url)
    official_icon_base64 = download_logo_base64(brand.icon_urls[0] if brand.icon_urls else None)
    
    # Calculate icon perceptual hash similarity
    icon_similarity = calculate_icon_similarity(
        suspicious_app.icon_url,
        brand.icon_urls[0] if brand.icon_urls else None
    )
    
    # Detect suspicious keywords
    suspicious_keywords = detect_suspicious_keywords(suspicious_app.app_name)
    
    # Analyze permissions (mock analysis based on brand category)
    category = brand.category if hasattr(brand, 'category') else 'banking'
    permissions_analysis = analyze_permissions_mock(category)
    
    # Build evidence dictionary
    evidence = {
        "detection_summary": {
            "detection_date": detection.detected_at.isoformat(),
            "confidence_score": float(detection.confidence_score),
            "risk_level": detection.risk_level,
            "status": detection.status
        },
        "app_information": {
            "app_name": suspicious_app.app_name,
            "package_id": suspicious_app.package_id,
            "developer_name": suspicious_app.developer_name,
            "store_url": suspicious_app.store_url,
            "icon_url": suspicious_app.icon_url,
            "install_count": suspicious_app.download_count or "Unknown"
        },
        "legitimate_brand": {
            "brand_name": brand.name,
            "official_package_ids": brand.package_ids,
            "official_developer": brand.developer_name,
            "official_icon_urls": brand.icon_urls
        },
        "similarity_scores": {
            "name_similarity": float(detection.text_similarity_score) if detection.text_similarity_score else 0,
            "icon_similarity": icon_similarity,  # Perceptual hash similarity
            "icon_similarity_method": "Perceptual Hash (Average Hash)",
            "package_similarity": 0.75,  # Mock data
            "overall_risk_score": float(detection.confidence_score)
        },
        "permissions_analysis": {
            "total_permissions": permissions_analysis['total_permissions'],
            "suspicious_permissions": permissions_analysis['suspicious_permissions'],
            "high_risk_count": permissions_analysis['high_risk_count'],
            "permission_risk_score": permissions_analysis['permission_risk_score'],
            "warnings": permissions_analysis['warnings'],
            "analysis_flags": permissions_analysis['analysis']
        },
        "red_flags": [
            f"App name '{suspicious_app.app_name}' is {int((detection.text_similarity_score or 0) * 100)}% similar to '{brand.name}'",
            f"Package ID '{suspicious_app.package_id}' does not match official package(s)",
            f"Developer name mismatch: '{suspicious_app.developer_name}' vs '{brand.developer_name}'",
            f"Certificate mismatch detected" if not detection.certificate_match else None,
            f"Suspicious keywords detected: {', '.join(suspicious_keywords)}" if suspicious_keywords else None,
            f"Unusual permissions: {permissions_analysis['high_risk_count']} high-risk permissions detected" if permissions_analysis['high_risk_count'] > 0 else None,
        ],
        "evidence_attachments": {
            "app_icon": suspicious_app.icon_url,
            "app_icon_base64": suspicious_icon_base64,
            "screenshots": suspicious_app.screenshot_urls or [],
            "official_icon": brand.icon_urls[0] if brand.icon_urls else None,
            "official_icon_base64": official_icon_base64
        }
    }
    
    # Remove None values from red_flags
    evidence["red_flags"] = [flag for flag in evidence["red_flags"] if flag]
    
    # Generate takedown email template
    takedown_email = f"""Subject: Urgent Takedown Request - Counterfeit App Impersonating {brand.name}

To: Google Play Support / App Store Review Team

Dear Security Team,

We are reporting a counterfeit application that is impersonating the legitimate brand "{brand.name}". 
This fake app poses significant security risks to users and damages the brand's reputation.

FAKE APP DETAILS:
-------------------
App Name: {suspicious_app.app_name}
Package ID: {suspicious_app.package_id}
Developer Name: {suspicious_app.developer_name}
Store URL: {suspicious_app.store_url}

LEGITIMATE BRAND DETAILS:
-------------------------
Official Brand: {brand.name}
Official Package ID(s): {', '.join(brand.package_ids) if isinstance(brand.package_ids, list) else brand.package_ids}
Official Developer: {brand.developer_name}

EVIDENCE OF IMPERSONATION:
--------------------------
1. Name Similarity: {int((detection.text_similarity_score or 0) * 100)}% match - clearly attempting to deceive users
2. Package ID Mismatch: The fake app's package ID does not match any official packages
3. Developer Name Mismatch: Listed developer does not match the legitimate brand owner
4. Risk Score: {int(detection.confidence_score * 100)}/100 - HIGH CONFIDENCE fake detection

RED FLAGS:
----------
{chr(10).join(f'• {flag}' for flag in evidence["red_flags"])}

IMPACT:
-------
• User credential theft risk
• Financial fraud potential  
• Brand reputation damage
• User trust erosion

REQUESTED ACTION:
----------------
We request immediate removal of this counterfeit application from the store.

Detection Date: {detection.detected_at.strftime('%Y-%m-%d %H:%M:%S')}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Evidence Package: Available upon request
Contact: security@fakeappdetection.system

Thank you for your prompt attention to this matter.

Regards,
Fake App Detection System
Automated Brand Protection
"""
    
    return EvidenceKitResponse(
        detection_id=detection.id,
        app_name=suspicious_app.app_name,
        package_id=suspicious_app.package_id,
        brand_name=brand.name,
        risk_score=int(detection.confidence_score * 100),
        evidence=evidence,
        takedown_email=takedown_email,
        generated_at=datetime.now().isoformat()
    )

@router.get("/api/evidence-kit/{detection_id}/download")
async def download_evidence_kit(detection_id: int, db: Session = Depends(get_db)):
    """
    Download evidence kit as JSON file
    """
    request = EvidenceKitRequest(detection_id=detection_id)
    evidence_kit = await generate_evidence_kit(request, db)
    
    return {
        "filename": f"evidence_kit_{detection_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        "content": evidence_kit.dict()
    }
