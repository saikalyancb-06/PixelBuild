from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sys
import os
import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

# Use simple relative imports
from database import get_db
from models.database_models import Brand, SuspiciousApp, Detection

# Simple text similarity without ML dependencies
def simple_text_similarity(str1, str2):
    """Simple text similarity without external dependencies"""
    str1 = str1.lower().replace(' ', '').replace('-', '').replace('_', '')
    str2 = str2.lower().replace(' ', '').replace('-', '').replace('_', '')
    
    if str1 == str2:
        return 1.0
    
    # Levenshtein distance
    if len(str1) < len(str2):
        str1, str2 = str2, str1
    
    if len(str2) == 0:
        return 0.0
    
    previous_row = range(len(str2) + 1)
    for i, c1 in enumerate(str1):
        current_row = [i + 1]
        for j, c2 in enumerate(str2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    distance = previous_row[-1]
    max_len = max(len(str1), len(str2))
    return 1 - (distance / max_len)

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

router = APIRouter()

class QuickCheckRequest(BaseModel):
    url: str

class QuickCheckResponse(BaseModel):
    is_fake: bool
    app_name: str
    package_id: str
    developer: str
    store: str
    risk_score: int
    reasons: list[str]
    matched_brand: Optional[str] = None

def extract_package_id(url: str) -> tuple[str, str]:
    """Extract package ID and store from URL"""
    
    # Google Play Store - more flexible regex
    play_store_match = re.search(r'id=([a-zA-Z0-9._\-]+)', url)
    if 'play.google.com' in url.lower() and play_store_match:
        return play_store_match.group(1), "Google Play Store"
    
    # App Store
    app_store_match = re.search(r'apps\.apple\.com/.*?/app/([^/]+)/id(\d+)', url)
    if app_store_match:
        app_name = app_store_match.group(1).replace('-', ' ').title()
        return f"apple.{app_store_match.group(2)}", "Apple App Store"
    
    # If URL looks like a package ID itself
    if re.match(r'^[a-zA-Z0-9._\-]+$', url):
        return url, "Unknown"
    
    # Try to extract any package-like pattern
    package_match = re.search(r'([a-z]+\.[a-z]+\.[a-zA-Z0-9._\-]+)', url.lower())
    if package_match:
        return package_match.group(1), "Google Play Store"
    
    raise HTTPException(status_code=400, detail=f"Could not extract package ID from URL: {url}")

def scrape_play_store_app(package_id: str) -> dict:
    """Scrape app details from Google Play Store"""
    url = f"https://play.google.com/store/apps/details?id={package_id}&hl=en&gl=US"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract app name
        app_name_tag = soup.find('h1', {'itemprop': 'name'})
        app_name = app_name_tag.text.strip() if app_name_tag else None
        
        # Extract developer name
        developer_tag = soup.find('a', {'class': 'Si6A0c'}) or soup.find('div', {'class': 'Vbfug'})
        developer = developer_tag.text.strip() if developer_tag else None
        
        # Extract rating
        rating_tag = soup.find('div', {'class': 'TT9eCd'})
        rating = None
        if rating_tag:
            try:
                # Remove any non-numeric characters except decimal point
                rating_text = re.sub(r'[^\d.]', '', rating_tag.text.strip())
                rating = float(rating_text) if rating_text else None
            except ValueError:
                rating = None
        
        # Extract download count (approximate)
        downloads_tag = soup.find('div', {'class': 'ClM7O'})
        downloads = downloads_tag.text.strip() if downloads_tag else None
        
        # Check if app exists
        not_found = soup.find('div', string=re.compile('not found|couldn\'t find', re.IGNORECASE))
        
        return {
            'exists': not not_found is None,
            'app_name': app_name,
            'developer': developer,
            'rating': rating,
            'downloads': downloads,
            'package_id': package_id
        }
        
    except requests.RequestException as e:
        return {
            'exists': False,
            'app_name': None,
            'developer': None,
            'error': str(e)
        }

def extract_app_name_from_package(package_id: str) -> str:
    """Extract likely app name from package ID"""
    parts = package_id.split('.')
    # Usually the last part is the app name
    app_name = parts[-1] if parts else package_id
    # Capitalize it
    return app_name.replace('_', ' ').title()

@router.post("/api/quick-check", response_model=QuickCheckResponse)
async def quick_check(request: QuickCheckRequest, db: Session = Depends(get_db)):
    """
    Quick check if an app URL is fake or real
    - Scrapes real-time data from Play Store
    - Compares against known legitimate brands
    - Returns risk assessment
    """
    
    try:
        package_id, store = extract_package_id(request.url)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse URL: {str(e)}")
    
    # Default values
    is_fake = False
    risk_score = 0
    reasons = []
    matched_brand = None
    developer = "Unknown"
    app_name = extract_app_name_from_package(package_id)
    
    # Check if this package is already in our suspicious apps database
    existing_suspicious = db.query(SuspiciousApp).filter(
        SuspiciousApp.package_id == package_id
    ).first()
    
    if existing_suspicious:
        is_fake = True
        risk_score = 95
        reasons.append(f"This app is flagged in our database as fake")
        reasons.append(f"Impersonating: {existing_suspicious.legitimate_brand}")
        
        brand = db.query(Brand).filter(Brand.id == existing_suspicious.brand_id).first()
        if brand:
            matched_brand = brand.name
        
        return QuickCheckResponse(
            is_fake=is_fake,
            app_name=app_name,
            package_id=package_id,
            developer=developer,
            store=store,
            risk_score=risk_score,
            reasons=reasons,
            matched_brand=matched_brand
        )
    
    # Get all legitimate brands FIRST
    brands = db.query(Brand).all()
    
    # Check if this package ID is in our database as legitimate
    for brand in brands:
        brand_pkg_ids = brand.package_ids if isinstance(brand.package_ids, list) else []
        if package_id in brand_pkg_ids:
            # This is a known legitimate app!
            return QuickCheckResponse(
                is_fake=False,
                app_name=brand.name,
                package_id=package_id,
                developer=brand.developer_name if brand.developer_name else brand.name,
                store=store,
                risk_score=0,
                reasons=[
                    f"✓ This is the official {brand.name} app",
                    f"✓ Package ID verified: {package_id}",
                    f"✓ Developer: {brand.developer_name if brand.developer_name else 'Verified'}"
                ],
                matched_brand=brand.name
            )
    
    # Scrape real-time data from Play Store ONLY if not in database
    if store == "Google Play Store":
        scraped_data = scrape_play_store_app(package_id)
        
        # Use scraped data
        if scraped_data.get('app_name'):
            app_name = scraped_data['app_name']
        if scraped_data.get('developer'):
            developer = scraped_data['developer']
        
        # Check if app exists - only flag as fake if we're SURE it doesn't exist
        if scraped_data.get('exists') is False:
            return QuickCheckResponse(
                is_fake=True,
                app_name=app_name,
                package_id=package_id,
                developer="Unknown",
                store=store,
                risk_score=100,
                reasons=["App does not exist on Google Play Store", "This could be a phishing link or malicious URL"],
                matched_brand=None
            )
    
    # Get all legitimate brands
    brands = db.query(Brand).all()
    
    max_similarity = 0
    best_match_brand = None
    
    # Detect suspicious keywords in app name
    suspicious_keywords = detect_suspicious_keywords(app_name)
    
    # Check against all brands
    for brand in brands:
        # Compare app name with brand name
        name_similarity = simple_text_similarity(brand.name, app_name)
        
        # Compare with developer name too
        dev_similarity = 0
        if developer and developer != "Unknown":
            dev_similarity = simple_text_similarity(brand.name, developer)
        
        # Use the higher similarity
        similarity = max(name_similarity, dev_similarity)
        
        if similarity > max_similarity:
            max_similarity = similarity
            best_match_brand = brand
    
    # Determine if it's fake based on similarity AND package ID verification
    if max_similarity > 0.75:  # High similarity - potential impersonation
        if best_match_brand:
            # Check if package ID matches the legitimate brand
            brand_pkg_ids = best_match_brand.package_ids if isinstance(best_match_brand.package_ids, list) else []
            is_exact_match = any(package_id == pkg for pkg in brand_pkg_ids)
            
            # Check developer name match
            dev_match = False
            if best_match_brand.developer_name and developer != "Unknown":
                dev_similarity = simple_text_similarity(best_match_brand.developer_name, developer)
                dev_match = dev_similarity > 0.80
            
            if is_exact_match:
                # Package ID matches - legitimate app
                is_fake = False
                risk_score = 0
                reasons = [f"✓ This is the official {best_match_brand.name} app"]
                reasons.append(f"✓ Package ID verified: {package_id}")
                if best_match_brand.developer_name:
                    reasons.append(f"✓ Developer: {best_match_brand.developer_name}")
                matched_brand = best_match_brand.name
            else:
                # Name is very similar but package ID doesn't match = FAKE
                is_fake = True
                risk_score = int(max_similarity * 100)
                
                # Add suspicious keyword boost to risk
                if suspicious_keywords:
                    risk_score = min(100, risk_score + len(suspicious_keywords) * 5)
                
                reasons.append(f"⚠️ WARNING: App name very similar to {best_match_brand.name}")
                reasons.append(f"✗ Package ID does NOT match official app!")
                if brand_pkg_ids:
                    reasons.append(f"Official package: {', '.join(brand_pkg_ids[:2])}")
                reasons.append(f"This package: {package_id}")
                if developer != "Unknown":
                    reasons.append(f"Developer: {developer}")
                
                # Add suspicious keywords warning
                if suspicious_keywords:
                    reasons.append(f"⚠️ Suspicious keywords found: {', '.join(suspicious_keywords)}")
                
                matched_brand = best_match_brand.name
    
    elif max_similarity > 0.50:
        # Medium similarity - possible impersonation
        if best_match_brand:
            risk_score = int(max_similarity * 100)
            reasons.append(f"⚠️ App name has moderate similarity to {best_match_brand.name}")
            reasons.append("This could be a legitimate app or potential impersonation")
            reasons.append("Verify the developer and reviews before installing")
            matched_brand = best_match_brand.name
    
    else:
        # Low similarity - app doesn't match known brands (likely legitimate unknown app)
        is_fake = False
        risk_score = 10
        reasons.append("✓ App does not match any known fake app patterns")
        reasons.append("This app is not in our database of known brands")
        if developer != "Unknown":
            reasons.append(f"Developer: {developer}")
        reasons.append("Always check reviews and permissions before installing")
    
    return QuickCheckResponse(
        is_fake=is_fake,
        app_name=app_name,
        package_id=package_id,
        developer=developer,
        store=store,
        risk_score=risk_score,
        reasons=reasons if reasons else ["No specific threats detected"],
        matched_brand=matched_brand
    )
