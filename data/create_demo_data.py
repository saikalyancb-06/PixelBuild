"""
Sample data for demo purposes
Run this script to populate the database with demo data
"""
from datetime import datetime, timedelta
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import SessionLocal
from models.database_models import Brand, SuspiciousApp, Detection, ScanJob, Takedown, Metrics


def create_demo_data():
    db = SessionLocal()
    
    try:
        # Create sample brands
        brands_data = [
            {
                'name': 'PayPal',
                'developer_name': 'PayPal, Inc.',
                'package_ids': ['com.paypal.android.p2pmobile'],
                'icon_urls': ['https://play-lh.googleusercontent.com/paypal-icon'],
                'certificates': ['a1b2c3d4e5f6...']
            },
            {
                'name': 'WhatsApp',
                'developer_name': 'WhatsApp LLC',
                'package_ids': ['com.whatsapp'],
                'icon_urls': ['https://play-lh.googleusercontent.com/whatsapp-icon'],
                'certificates': ['1234567890ab...']
            },
            {
                'name': 'PhonePe',
                'developer_name': 'PhonePe Private Limited',
                'package_ids': ['com.phonepe.app'],
                'icon_urls': ['https://play-lh.googleusercontent.com/phonepe-icon'],
                'certificates': ['xyz123abc456...']
            },
            {
                'name': 'Google Pay',
                'developer_name': 'Google LLC',
                'package_ids': ['com.google.android.apps.nbu.paisa.user'],
                'icon_urls': ['https://play-lh.googleusercontent.com/gpay-icon'],
                'certificates': ['google789xyz...']
            },
            {
                'name': 'Amazon',
                'developer_name': 'Amazon Mobile LLC',
                'package_ids': ['com.amazon.mShop.android.shopping'],
                'icon_urls': ['https://play-lh.googleusercontent.com/amazon-icon'],
                'certificates': ['amazon123...']
            },
        ]
        
        brands = []
        for brand_data in brands_data:
            brand = Brand(**brand_data)
            db.add(brand)
            brands.append(brand)
        
        db.commit()
        print(f"Created {len(brands)} brands")
        
        # Create suspicious apps
        suspicious_apps_data = [
            # PayPal fakes
            {'app_name': 'PayPaI', 'package_id': 'com.paypal.fake1', 'developer_name': 'Unknown Dev', 'source': 'play_store', 'download_count': 50000, 'rating': 4.2},
            {'app_name': 'РayPal', 'package_id': 'com.paypal.fake2', 'developer_name': 'Fake Corp', 'source': 'apk_mirror', 'download_count': 30000, 'rating': 4.5},
            {'app_name': 'PayPal Pro', 'package_id': 'com.paypal.pro.fake', 'developer_name': 'PayPaI Inc', 'source': 'play_store', 'download_count': 100000, 'rating': 4.7},
            
            # WhatsApp fakes
            {'app_name': 'WhatApp', 'package_id': 'com.whatapp.fake', 'developer_name': 'Messaging Inc', 'source': 'play_store', 'download_count': 200000, 'rating': 4.3},
            {'app_name': 'WhatsApp Plus', 'package_id': 'com.whatsapp.plus.fake', 'developer_name': 'Plus Dev', 'source': 'apk_mirror', 'download_count': 500000, 'rating': 4.6},
            
            # PhonePe fakes
            {'app_name': 'PhonePay', 'package_id': 'com.phonepay.fake', 'developer_name': 'Payment Solutions', 'source': 'play_store', 'download_count': 75000, 'rating': 4.1},
            {'app_name': 'Phone Pe', 'package_id': 'com.phone.pe.fake', 'developer_name': 'UPI Services', 'source': 'apk_mirror', 'download_count': 40000, 'rating': 4.4},
            
            # Google Pay fakes
            {'app_name': 'GooglePay', 'package_id': 'com.googlepay.fake', 'developer_name': 'Google Inc.', 'source': 'play_store', 'download_count': 150000, 'rating': 4.5},
            {'app_name': 'G Pay', 'package_id': 'com.gpay.fake', 'developer_name': 'Payment Tech', 'source': 'apk_mirror', 'download_count': 80000, 'rating': 4.2},
            
            # Amazon fakes
            {'app_name': 'Amaz0n', 'package_id': 'com.amazon.fake1', 'developer_name': 'Shopping Ltd', 'source': 'play_store', 'download_count': 120000, 'rating': 4.3},
        ]
        
        suspicious_apps = []
        for app_data in suspicious_apps_data:
            app_data['icon_url'] = f"https://example.com/icons/{app_data['package_id']}.png"
            app_data['screenshot_urls'] = [f"https://example.com/screenshots/{app_data['package_id']}_1.png"]
            app_data['store_url'] = f"https://play.google.com/store/apps/details?id={app_data['package_id']}"
            
            app = SuspiciousApp(**app_data)
            db.add(app)
            suspicious_apps.append(app)
        
        db.commit()
        print(f"Created {len(suspicious_apps)} suspicious apps")
        
        # Create detections
        detections = []
        for i, app in enumerate(suspicious_apps):
            # Determine which brand this fake targets
            if 'paypal' in app.app_name.lower():
                brand = brands[0]
            elif 'whats' in app.app_name.lower():
                brand = brands[1]
            elif 'phone' in app.app_name.lower():
                brand = brands[2]
            elif 'pay' in app.app_name.lower() or 'gpay' in app.app_name.lower():
                brand = brands[3]
            else:
                brand = brands[4]
            
            # Generate random but realistic detection scores
            icon_sim = random.uniform(0.82, 0.98)
            text_sim = random.uniform(0.78, 0.96)
            review_fraud = random.uniform(0.65, 0.88)
            
            confidence = (0.35 * icon_sim + 0.35 * text_sim + 0.15 * review_fraud + 0.15)
            
            if confidence >= 0.90:
                risk_level = "CRITICAL"
            elif confidence >= 0.80:
                risk_level = "HIGH"
            elif confidence >= 0.70:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
            
            detection = Detection(
                brand_id=brand.id,
                suspicious_app_id=app.id,
                icon_similarity_score=icon_sim,
                text_similarity_score=text_sim,
                certificate_match=False,
                review_fraud_score=review_fraud,
                confidence_score=confidence,
                risk_level=risk_level,
                detection_reasons=[
                    f"Icon similarity: {icon_sim:.2%}",
                    f"Name similarity: {text_sim:.2%}",
                    "Certificate mismatch detected",
                    f"Review fraud score: {review_fraud:.2%}"
                ],
                status='pending' if i < 5 else 'confirmed',
                detected_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.add(detection)
            detections.append(detection)
        
        db.commit()
        print(f"Created {len(detections)} detections")
        
        # Create scan jobs
        for brand in brands[:3]:
            scan = ScanJob(
                brand_id=brand.id,
                sources=['play_store', 'apk_mirror'],
                status='completed',
                apps_scanned=random.randint(100, 500),
                detections_found=random.randint(1, 5),
                started_at=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
                completed_at=datetime.utcnow() - timedelta(days=random.randint(0, 9)),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
            )
            db.add(scan)
        
        db.commit()
        print("Created scan jobs")
        
        # Create takedowns for some detections
        for detection in detections[:5]:
            takedown = Takedown(
                detection_id=detection.id,
                store='play_store',
                request_id=f"REQ-{random.randint(10000, 99999)}",
                request_body="Automated takedown request generated",
                evidence_kit_path=f"./evidence_kits/detection_{detection.id}.pdf",
                status=random.choice(['submitted', 'acknowledged', 'taken_down']),
                submitted_at=datetime.utcnow() - timedelta(days=random.randint(0, 5)),
                time_to_takedown=random.randint(6, 48) if random.random() > 0.3 else None
            )
            db.add(takedown)
        
        db.commit()
        print("Created takedowns")
        
        # Create metrics
        metrics = Metrics(
            date=datetime.utcnow(),
            total_apps_scanned=10000,
            fake_apps_detected=127,
            takedowns_submitted=95,
            takedowns_successful=89,
            avg_detection_time=3.2,
            avg_time_to_takedown=18.5,
            user_exposure_prevented=2500000
        )
        db.add(metrics)
        db.commit()
        print("Created metrics")
        
        print("\\n✅ Demo data created successfully!")
        print(f"   - {len(brands)} brands")
        print(f"   - {len(suspicious_apps)} suspicious apps")
        print(f"   - {len(detections)} detections")
        print(f"   - Scan jobs and takedowns")
        
    except Exception as e:
        print(f"Error creating demo data: {e}")
        db.rollback()
    
    finally:
        db.close()


if __name__ == "__main__":
    print("Creating demo data...")
    create_demo_data()
