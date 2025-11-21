import re
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from collections import Counter
import numpy as np


class ReviewFraudDetector:
    """Detect fake/fraudulent reviews on app stores"""
    
    def __init__(self):
        # Suspicious review patterns
        self.spam_keywords = [
            'best app ever', 'amazing app', 'must download', 'five stars',
            'highly recommend', 'download now', 'great app', 'perfect app',
            'best app', 'awesome app', 'fantastic', 'wonderful'
        ]
        
        # Patterns of bot-generated reviews
        self.bot_patterns = [
            r'^(great|good|best|nice|cool)\s+(app|application)',
            r'(five|5)\s+star',
            r'highly\s+recommend',
        ]
    
    def analyze_reviews(self, reviews: List[Dict]) -> Dict:
        """
        Analyze a list of reviews for fraud patterns
        
        reviews format: [
            {
                'text': 'Review text',
                'rating': 5,
                'date': '2024-01-01',
                'author': 'username',
                'helpful_count': 0
            },
            ...
        ]
        """
        if not reviews:
            return self._create_empty_analysis()
        
        total_reviews = len(reviews)
        
        # Various fraud indicators
        duplicate_count = self._detect_duplicate_reviews(reviews)
        bot_like_count = self._detect_bot_reviews(reviews)
        suspicious_timing = self._detect_suspicious_timing(reviews)
        rating_manipulation = self._detect_rating_manipulation(reviews)
        low_effort_count = self._detect_low_effort_reviews(reviews)
        template_count = self._detect_template_reviews(reviews)
        
        # Calculate overall fraud score
        fraud_score = self._calculate_fraud_score(
            total_reviews,
            duplicate_count,
            bot_like_count,
            suspicious_timing,
            rating_manipulation,
            low_effort_count,
            template_count
        )
        
        return {
            'total_reviews': total_reviews,
            'fraud_score': fraud_score,
            'risk_level': self._get_risk_level(fraud_score),
            'indicators': {
                'duplicate_reviews': duplicate_count,
                'bot_like_reviews': bot_like_count,
                'suspicious_timing': suspicious_timing,
                'rating_manipulation_score': rating_manipulation,
                'low_effort_reviews': low_effort_count,
                'template_reviews': template_count,
            },
            'flags': self._get_fraud_flags(
                duplicate_count, bot_like_count, suspicious_timing,
                rating_manipulation, low_effort_count, template_count
            )
        }
    
    def _detect_duplicate_reviews(self, reviews: List[Dict]) -> int:
        """Detect duplicate or near-duplicate reviews"""
        review_texts = [r['text'].lower().strip() for r in reviews]
        
        # Count exact duplicates
        text_counts = Counter(review_texts)
        duplicates = sum(count - 1 for count in text_counts.values() if count > 1)
        
        return duplicates
    
    def _detect_bot_reviews(self, reviews: List[Dict]) -> int:
        """Detect bot-generated reviews"""
        bot_count = 0
        
        for review in reviews:
            text = review['text'].lower()
            
            # Check for spam keywords
            if any(keyword in text for keyword in self.spam_keywords):
                bot_count += 1
                continue
            
            # Check for bot patterns
            if any(re.search(pattern, text) for pattern in self.bot_patterns):
                bot_count += 1
                continue
            
            # Very short reviews with max rating
            if len(text.split()) <= 3 and review.get('rating', 0) == 5:
                bot_count += 1
        
        return bot_count
    
    def _detect_suspicious_timing(self, reviews: List[Dict]) -> float:
        """Detect suspicious review timing patterns"""
        if len(reviews) < 10:
            return 0.0
        
        # Parse dates
        dates = []
        for review in reviews:
            try:
                date = datetime.strptime(review['date'], '%Y-%m-%d')
                dates.append(date)
            except:
                continue
        
        if len(dates) < 10:
            return 0.0
        
        dates.sort()
        
        # Check for sudden spikes
        # Count reviews in 24-hour windows
        spike_count = 0
        for i in range(len(dates) - 5):
            window_start = dates[i]
            window_end = window_start + timedelta(days=1)
            
            reviews_in_window = sum(
                1 for date in dates[i:] if window_start <= date <= window_end
            )
            
            # If more than 20% of reviews in a single day
            if reviews_in_window > len(dates) * 0.2:
                spike_count += 1
        
        # Normalize spike score
        spike_score = min(spike_count / 5, 1.0)
        
        return spike_score
    
    def _detect_rating_manipulation(self, reviews: List[Dict]) -> float:
        """Detect rating manipulation patterns"""
        ratings = [r.get('rating', 0) for r in reviews if r.get('rating')]
        
        if not ratings:
            return 0.0
        
        # Calculate rating distribution
        rating_counts = Counter(ratings)
        
        # Suspicious if too many 5-star ratings
        five_star_ratio = rating_counts.get(5, 0) / len(ratings)
        
        # Suspicious if bimodal distribution (many 5s and 1s, few in between)
        if len(ratings) > 20:
            middle_ratings = rating_counts.get(2, 0) + rating_counts.get(3, 0) + rating_counts.get(4, 0)
            middle_ratio = middle_ratings / len(ratings)
            
            # If < 20% middle ratings and > 70% extreme ratings
            if middle_ratio < 0.2 and (five_star_ratio > 0.7 or rating_counts.get(1, 0) / len(ratings) > 0.3):
                return 0.8
        
        # High concentration of 5-star reviews is suspicious
        if five_star_ratio > 0.9:
            return 0.9
        elif five_star_ratio > 0.8:
            return 0.7
        elif five_star_ratio > 0.7:
            return 0.5
        
        return 0.0
    
    def _detect_low_effort_reviews(self, reviews: List[Dict]) -> int:
        """Detect low-effort reviews (very short, generic)"""
        low_effort_count = 0
        
        generic_phrases = [
            'good', 'great', 'nice', 'cool', 'ok', 'okay', 'fine',
            'good app', 'nice app', 'love it', 'like it'
        ]
        
        for review in reviews:
            text = review['text'].lower().strip()
            
            # Very short reviews
            if len(text.split()) <= 2:
                low_effort_count += 1
            # Generic single-phrase reviews
            elif text in generic_phrases:
                low_effort_count += 1
        
        return low_effort_count
    
    def _detect_template_reviews(self, reviews: List[Dict]) -> int:
        """Detect reviews following templates"""
        # Find common patterns in reviews
        review_texts = [r['text'].lower() for r in reviews]
        
        # Simple template detection: find reviews with similar structure
        template_count = 0
        
        # Look for reviews starting with same phrases
        first_words = [' '.join(text.split()[:3]) for text in review_texts if len(text.split()) >= 3]
        word_counts = Counter(first_words)
        
        # If many reviews start the same way
        for phrase, count in word_counts.items():
            if count > max(len(reviews) * 0.1, 3):  # More than 10% or 3+ reviews
                template_count += count
        
        return template_count
    
    def _calculate_fraud_score(self, total, duplicates, bots, timing, 
                                rating, low_effort, templates) -> float:
        """Calculate overall fraud score (0-1)"""
        if total == 0:
            return 0.0
        
        # Weight different indicators
        scores = []
        
        # Duplicate ratio
        if total > 0:
            scores.append(min(duplicates / total, 1.0) * 0.25)
        
        # Bot ratio
        if total > 0:
            scores.append(min(bots / total, 1.0) * 0.25)
        
        # Timing suspiciousness
        scores.append(timing * 0.15)
        
        # Rating manipulation
        scores.append(rating * 0.20)
        
        # Low effort ratio
        if total > 0:
            scores.append(min(low_effort / total, 1.0) * 0.10)
        
        # Template ratio
        if total > 0:
            scores.append(min(templates / total, 1.0) * 0.05)
        
        return round(sum(scores), 4)
    
    def _get_risk_level(self, fraud_score: float) -> str:
        """Convert fraud score to risk level"""
        if fraud_score >= 0.75:
            return "CRITICAL"
        elif fraud_score >= 0.60:
            return "HIGH"
        elif fraud_score >= 0.40:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_fraud_flags(self, duplicates, bots, timing, rating, 
                         low_effort, templates) -> List[str]:
        """Generate list of fraud flags"""
        flags = []
        
        if duplicates > 5:
            flags.append("HIGH_DUPLICATE_COUNT")
        if bots > 10:
            flags.append("BOT_LIKE_REVIEWS")
        if timing > 0.5:
            flags.append("SUSPICIOUS_TIMING_PATTERN")
        if rating > 0.7:
            flags.append("RATING_MANIPULATION")
        if low_effort > 15:
            flags.append("MANY_LOW_EFFORT_REVIEWS")
        if templates > 10:
            flags.append("TEMPLATE_REVIEWS")
        
        return flags
    
    def _create_empty_analysis(self) -> Dict:
        """Create empty analysis result"""
        return {
            'total_reviews': 0,
            'fraud_score': 0.0,
            'risk_level': 'UNKNOWN',
            'indicators': {},
            'flags': []
        }


# Usage example
if __name__ == "__main__":
    detector = ReviewFraudDetector()
    
    # Example reviews (simulated)
    reviews = [
        {'text': 'Best app ever! Highly recommend!', 'rating': 5, 'date': '2024-01-01', 'author': 'user1'},
        {'text': 'Great app! Five stars!', 'rating': 5, 'date': '2024-01-01', 'author': 'user2'},
        {'text': 'Amazing! Must download!', 'rating': 5, 'date': '2024-01-01', 'author': 'user3'},
        {'text': 'Perfect app', 'rating': 5, 'date': '2024-01-02', 'author': 'user4'},
        {'text': 'Great', 'rating': 5, 'date': '2024-01-02', 'author': 'user5'},
        # ... more reviews
    ]
    
    analysis = detector.analyze_reviews(reviews)
    
    print(f"Review Fraud Analysis")
    print(f"=====================")
    print(f"Total Reviews: {analysis['total_reviews']}")
    print(f"Fraud Score: {analysis['fraud_score']:.2%}")
    print(f"Risk Level: {analysis['risk_level']}")
    print(f"\\nIndicators:")
    for key, value in analysis['indicators'].items():
        print(f"  {key}: {value}")
    print(f"\\nFlags: {', '.join(analysis['flags']) if analysis['flags'] else 'None'}")
