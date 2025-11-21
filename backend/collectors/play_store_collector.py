import requests
from typing import List, Dict, Optional
import time
from google_play_scraper import app, search, reviews_all
import logging


class PlayStoreCollector:
    """Collect app data from Google Play Store"""
    
    def __init__(self, delay=2):
        self.delay = delay
        self.logger = logging.getLogger(__name__)
    
    def search_apps(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search for apps by query"""
        try:
            results = search(
                query,
                lang='en',
                country='us',
                n_hits=max_results
            )
            
            apps = []
            for result in results:
                apps.append({
                    'package_id': result.get('appId'),
                    'app_name': result.get('title'),
                    'developer': result.get('developer'),
                    'icon_url': result.get('icon'),
                    'rating': result.get('score'),
                    'installs': result.get('installs'),
                    'source': 'play_store'
                })
                time.sleep(self.delay)
            
            return apps
            
        except Exception as e:
            self.logger.error(f"Error searching Play Store: {e}")
            return []
    
    def get_app_details(self, package_id: str) -> Optional[Dict]:
        """Get detailed information about an app"""
        try:
            details = app(
                package_id,
                lang='en',
                country='us'
            )
            
            return {
                'package_id': details.get('appId'),
                'app_name': details.get('title'),
                'developer_name': details.get('developer'),
                'developer_id': details.get('developerId'),
                'icon_url': details.get('icon'),
                'screenshot_urls': details.get('screenshots', []),
                'rating': details.get('score'),
                'reviews_count': details.get('reviews'),
                'download_count': self._parse_installs(details.get('installs', '0')),
                'version': details.get('version'),
                'last_updated': details.get('updated'),
                'content_rating': details.get('contentRating'),
                'description': details.get('description'),
                'store_url': details.get('url'),
                'source': 'play_store'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting app details for {package_id}: {e}")
            return None
    
    def get_app_reviews(self, package_id: str, max_reviews: int = 100) -> List[Dict]:
        """Get reviews for an app"""
        try:
            result = reviews_all(
                package_id,
                sleep_milliseconds=self.delay * 1000,
                lang='en',
                country='us',
                sort=1,  # Most recent
                count=max_reviews
            )
            
            reviews = []
            for review in result:
                reviews.append({
                    'text': review.get('content'),
                    'rating': review.get('score'),
                    'date': review.get('at').strftime('%Y-%m-%d') if review.get('at') else None,
                    'author': review.get('userName'),
                    'helpful_count': review.get('thumbsUpCount', 0)
                })
            
            return reviews
            
        except Exception as e:
            self.logger.error(f"Error getting reviews for {package_id}: {e}")
            return []
    
    def scan_for_clones(self, legitimate_app_name: str, max_results: int = 50) -> List[Dict]:
        """
        Search for potential clones of a legitimate app
        """
        # Search with various query variations
        queries = [
            legitimate_app_name,
            f"{legitimate_app_name} app",
            f"{legitimate_app_name} official",
            f"{legitimate_app_name} pro",
            f"{legitimate_app_name} plus",
        ]
        
        all_apps = []
        seen_packages = set()
        
        for query in queries:
            apps = self.search_apps(query, max_results=max_results)
            
            for app in apps:
                package_id = app.get('package_id')
                if package_id and package_id not in seen_packages:
                    seen_packages.add(package_id)
                    all_apps.append(app)
            
            time.sleep(self.delay)
        
        return all_apps
    
    def _parse_installs(self, installs_str: str) -> int:
        """Parse install count string (e.g., '1,000,000+') to integer"""
        if not installs_str:
            return 0
        
        # Remove '+' and commas
        installs_str = installs_str.replace('+', '').replace(',', '')
        
        try:
            return int(installs_str)
        except ValueError:
            return 0


# Usage example
if __name__ == "__main__":
    collector = PlayStoreCollector()
    
    # Search for apps
    print("Searching for potential clones of 'PayPal'...")
    apps = collector.scan_for_clones("PayPal", max_results=20)
    
    print(f"\\nFound {len(apps)} apps:")
    for app in apps[:10]:
        print(f"  - {app['app_name']} ({app['package_id']})")
        print(f"    Rating: {app.get('rating', 'N/A')}, Installs: {app.get('installs', 'N/A')}")
    
    # Get details for first app
    if apps:
        print(f"\\nGetting details for {apps[0]['app_name']}...")
        details = collector.get_app_details(apps[0]['package_id'])
        
        if details:
            print(f"  Developer: {details['developer_name']}")
            print(f"  Downloads: {details['download_count']}")
            print(f"  Last Updated: {details['last_updated']}")
