"""
Initialize the database and create all tables
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import Base, engine
from models.database_models import (
    Brand, SuspiciousApp, Detection, ScanJob, Takedown, Metrics
)

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("  - brands")
        print("  - suspicious_apps")
        print("  - detections")
        print("  - scan_jobs")
        print("  - takedowns")
        print("  - metrics")
        print("\nNext step: Run 'python data/create_demo_data.py' to populate with demo data")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        raise

if __name__ == "__main__":
    init_database()
