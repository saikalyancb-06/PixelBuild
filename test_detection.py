"""
Test script to demonstrate fake app detection
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_models.text_similarity.detector import TextSimilarityDetector
from ml_models.icon_similarity.detector import IconSimilarityDetector

def test_text_detection():
    """Test text similarity detection"""
    print("=" * 60)
    print("TEXT SIMILARITY DETECTION TEST")
    print("=" * 60)
    
    detector = TextSimilarityDetector()
    
    # Test cases: (legitimate app, suspicious app)
    test_cases = [
        ("PayPal", "PayPaI"),  # Typosquatting with I instead of l
        ("WhatsApp", "WhatApp"),  # Missing letter
        ("Google Pay", "Googl Pay"),  # Typo
        ("PhonePe", "Phone Pe"),  # Space added
        ("Amazon", "Amazom"),  # Letter swap
    ]
    
    print("\nDetecting typosquatting and name similarity...\n")
    
    for legitimate, suspicious in test_cases:
        similarity_score, reasons = detector.compare_names(legitimate, suspicious)
        is_suspicious = similarity_score > 0.80
        
        status = "🚨 SUSPICIOUS" if is_suspicious else "✅ SAFE"
        
        print(f"{status}")
        print(f"  Legitimate:  {legitimate}")
        print(f"  Suspicious:  {suspicious}")
        print(f"  Similarity:  {similarity_score:.2%}")
        print(f"  Reasons:     {', '.join(reasons) if reasons else 'N/A'}")
        print()

def test_api_endpoints():
    """Test API endpoints"""
    import requests
    
    print("=" * 60)
    print("API ENDPOINTS TEST")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test endpoints
    endpoints = [
        "/metrics",
        "/brands",
        "/detections",
        "/scans",
        "/takedowns",
    ]
    
    print("\nTesting all API endpoints...\n")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 1
                print(f"✅ {endpoint:20} Status: {response.status_code}  Records: {count}")
            else:
                print(f"❌ {endpoint:20} Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint:20} Error: {str(e)}")
    
    print()

def test_detection_thresholds():
    """Test different similarity thresholds"""
    print("=" * 60)
    print("DETECTION THRESHOLD ANALYSIS")
    print("=" * 60)
    
    detector = TextSimilarityDetector()
    
    test_pairs = [
        ("PayPal", "PayPal"),      # Exact match
        ("PayPal", "PayPaI"),      # Very similar (typosquatting)
        ("PayPal", "Paypal"),      # Case difference
        ("PayPal", "Pay Pal"),     # Space added
        ("PayPal", "PaiPal"),      # Letter swap
        ("PayPal", "Amazon"),      # Completely different
    ]
    
    print("\nAnalyzing detection at different similarity levels...\n")
    
    for app1, app2 in test_pairs:
        score, reasons = detector.compare_names(app1, app2)
        is_suspicious = score > 0.80
        
        # Visual similarity bar
        bar_length = int(score * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        
        print(f"{app1:15} vs {app2:15}")
        print(f"  {bar} {score:.1%}")
        print(f"  {'🚨 DETECTED' if is_suspicious else '✅ SAFE':12}")
        print()

if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " FAKE APP DETECTION SYSTEM - TEST SUITE ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Run all tests
    test_text_detection()
    input("Press Enter to continue to API tests...")
    
    test_api_endpoints()
    input("Press Enter to continue to threshold analysis...")
    
    test_detection_thresholds()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)
    print("\nNow open http://localhost:3001 to see the dashboard!")
    print()
