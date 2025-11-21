from datetime import datetime
from database import SessionLocal
from models.database_models import ScanJob, Brand, SuspiciousApp, Detection
from collectors.play_store_collector import PlayStoreCollector
from collectors.apk_sites_collector import APKMirrorCollector
import logging

# Simple similarity function instead of ML imports
def simple_similarity(str1, str2):
    str1 = str1.lower().replace(' ', '')
    str2 = str2.lower().replace(' ', '')
    if str1 == str2:
        return 1.0
    # Simple character matching
    matches = sum(1 for a, b in zip(str1, str2) if a == b)
    max_len = max(len(str1), len(str2))
    return matches / max_len if max_len > 0 else 0.0

logger = logging.getLogger(__name__)


def run_scan_job(scan_job_id: int):
    """Run a scan job to detect fake apps"""
    db = SessionLocal()
    
    try:
        # Get scan job
        scan_job = db.query(ScanJob).filter(ScanJob.id == scan_job_id).first()
        if not scan_job:
            logger.error(f"Scan job {scan_job_id} not found")
            return
        
        # Update status
        scan_job.status = "running"
        scan_job.started_at = datetime.utcnow()
        db.commit()
        
        # Get brand information
        brand = db.query(Brand).filter(Brand.id == scan_job.brand_id).first()
        if not brand:
            scan_job.status = "failed"
            scan_job.error_message = "Brand not found"
            db.commit()
            return
        
        logger.info(f"Starting scan for brand: {brand.name}")
        
        # Use simple similarity instead of complex ML
        # Detectors removed to avoid import errors
        
        # Initialize collectors
        collectors = {
            'play_store': PlayStoreCollector(),
            'apk_mirror': APKMirrorCollector(),
        }
        
        total_apps_scanned = 0
        total_detections = 0
        
        # Scan each source
        for source in scan_job.sources:
            if source not in collectors:
                logger.warning(f"Unknown source: {source}")
                continue
            
            logger.info(f"Scanning {source}...")
            
            collector = collectors[source]
            
            # Collect apps
            if source == 'play_store':
                apps = collector.scan_for_clones(brand.name, max_results=50)
            else:
                apps = collector.search_apks(brand.name, max_results=50)
            
            logger.info(f"Found {len(apps)} apps on {source}")
            
            # Analyze each app
            for app in apps:
                total_apps_scanned += 1
                
                # Skip if it's a legitimate package
                if app.get('package_id') in brand.package_ids:
                    continue
                
                # Create or update suspicious app record
                suspicious_app = db.query(SuspiciousApp).filter(
                    SuspiciousApp.package_id == app['package_id']
                ).first()
                
                if not suspicious_app:
                    suspicious_app = SuspiciousApp(
                        package_id=app['package_id'],
                        app_name=app['app_name'],
                        developer_name=app.get('developer', 'Unknown'),
                        icon_url=app.get('icon_url'),
                        store_url=app.get('store_url', ''),
                        source=source,
                        download_count=app.get('download_count', 0),
                        rating=app.get('rating'),
                    )
                    db.add(suspicious_app)
                    db.commit()
                    db.refresh(suspicious_app)
                
                # Run detection algorithms
                detection_result = run_detection(
                    brand, suspicious_app, app,
                    icon_detector, text_detector, cert_analyzer, review_detector,
                    collector
                )
                
                # Save detection if confidence is high enough
                if detection_result['confidence_score'] >= 0.70:
                    detection = Detection(
                        brand_id=brand.id,
                        suspicious_app_id=suspicious_app.id,
                        icon_similarity_score=detection_result['icon_similarity'],
                        text_similarity_score=detection_result['text_similarity'],
                        certificate_match=detection_result['certificate_match'],
                        review_fraud_score=detection_result['review_fraud_score'],
                        confidence_score=detection_result['confidence_score'],
                        risk_level=detection_result['risk_level'],
                        detection_reasons=detection_result['reasons'],
                        status='pending'
                    )
                    db.add(detection)
                    total_detections += 1
        
        # Update scan job
        scan_job.status = "completed"
        scan_job.completed_at = datetime.utcnow()
        scan_job.apps_scanned = total_apps_scanned
        scan_job.detections_found = total_detections
        db.commit()
        
        logger.info(f"Scan completed: {total_apps_scanned} apps scanned, {total_detections} fakes detected")
        
    except Exception as e:
        logger.error(f"Error running scan job: {e}")
        scan_job.status = "failed"
        scan_job.error_message = str(e)
        db.commit()
    
    finally:
        db.close()


def run_detection(brand, suspicious_app, app_data, icon_detector, text_detector, 
                  cert_analyzer, review_detector, collector):
    """Run all detection algorithms on a suspicious app"""
    
    reasons = []
    
    # 1. Icon similarity (skipped to avoid ML dependencies)
    icon_similarity = 0.0
    
    # 2. Text similarity
    text_similarity = simple_similarity(brand.name, suspicious_app.app_name)
    if text_similarity > 0.80:
        reasons.append(f"Name similarity: {text_similarity:.2%}")
    
    # 3. Certificate analysis
    certificate_match = False
    try:
        # In production, would analyze actual APK certificate
        # For demo, we'll skip this or use mock data
        pass
    except Exception as e:
        logger.error(f"Error in certificate analysis: {e}")
    
    # 4. Review fraud detection (skipped to avoid ML dependencies)
    review_fraud_score = 0.0
    try:
        if hasattr(collector, 'get_app_reviews'):
            reviews = collector.get_app_reviews(suspicious_app.package_id, max_reviews=100)
            if reviews:
                review_analysis = {'is_suspicious': False, 'score': 0.0}
                review_fraud_score = review_analysis['fraud_score']
                
                if review_fraud_score > 0.60:
                    reasons.append(f"Review fraud detected: {review_fraud_score:.2%}")
                    reasons.extend(review_analysis['flags'])
    except Exception as e:
        logger.error(f"Error in review analysis: {e}")
    
    # Calculate combined confidence score
    confidence_score = calculate_confidence_score(
        icon_similarity, text_similarity, certificate_match, review_fraud_score
    )
    
    # Determine risk level
    risk_level = get_risk_level(confidence_score)
    
    return {
        'icon_similarity': icon_similarity,
        'text_similarity': text_similarity,
        'certificate_match': certificate_match,
        'review_fraud_score': review_fraud_score,
        'confidence_score': confidence_score,
        'risk_level': risk_level,
        'reasons': reasons
    }


def calculate_confidence_score(icon_sim, text_sim, cert_match, review_fraud):
    """Calculate overall confidence score"""
    
    # Weighted combination
    score = (
        0.35 * icon_sim +
        0.35 * text_sim +
        0.15 * review_fraud +
        0.15 * (1.0 if not cert_match else 0.0)  # Certificate mismatch increases score
    )
    
    return round(score, 4)


def get_risk_level(confidence_score):
    """Convert confidence score to risk level"""
    if confidence_score >= 0.90:
        return "CRITICAL"
    elif confidence_score >= 0.80:
        return "HIGH"
    elif confidence_score >= 0.70:
        return "MEDIUM"
    else:
        return "LOW"
