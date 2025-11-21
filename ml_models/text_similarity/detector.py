from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import Levenshtein
import re
from typing import List, Tuple


class TextSimilarityDetector:
    """Detect similar app names and package IDs"""
    
    def __init__(self, threshold=0.80):
        self.threshold = threshold
        
        # Common typosquatting patterns
        self.char_substitutions = {
            'o': ['0', 'ο', 'о'],  # o, zero, greek omicron, cyrillic o
            'a': ['α', 'а'],       # a, alpha, cyrillic a
            'i': ['1', 'l', 'ı'],  # i, one, lowercase L, dotless i
            'e': ['ε', 'е'],       # e, epsilon, cyrillic e
            'm': ['rn'],           # m vs rn
            'w': ['vv'],           # w vs double v
        }
    
    def normalize_text(self, text):
        """Normalize text for comparison"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove common prefixes/suffixes
        text = re.sub(r'^(the|app|official|real|new|pro|plus|lite)\s+', '', text)
        text = re.sub(r'\s+(app|application|apk|free|pro|plus|lite|beta)$', '', text)
        
        # Remove special characters
        text = re.sub(r'[^a-z0-9]', '', text)
        
        return text
    
    def levenshtein_similarity(self, str1, str2):
        """Calculate Levenshtein distance-based similarity"""
        distance = Levenshtein.distance(str1, str2)
        max_len = max(len(str1), len(str2))
        
        if max_len == 0:
            return 1.0
        
        similarity = 1 - (distance / max_len)
        return similarity
    
    def fuzzy_ratio(self, str1, str2):
        """Calculate fuzzy string matching ratio"""
        return fuzz.ratio(str1, str2) / 100.0
    
    def fuzzy_partial_ratio(self, str1, str2):
        """Calculate partial fuzzy matching ratio"""
        return fuzz.partial_ratio(str1, str2) / 100.0
    
    def sequence_matcher_ratio(self, str1, str2):
        """Calculate similarity using SequenceMatcher"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def detect_typosquatting(self, legitimate, suspicious):
        """Detect typosquatting attempts"""
        score = 0
        reasons = []
        
        # Character substitution detection
        for char, substitutes in self.char_substitutions.items():
            if char in legitimate:
                for sub in substitutes:
                    if sub in suspicious:
                        test_str = suspicious.replace(sub, char)
                        if test_str == legitimate:
                            score = 0.95
                            reasons.append(f"Character substitution: '{sub}' → '{char}'")
                            return score, reasons
        
        # Check for single character difference
        if len(legitimate) == len(suspicious):
            diff_count = sum(1 for a, b in zip(legitimate, suspicious) if a != b)
            if diff_count == 1:
                score = 0.90
                reasons.append("Single character difference")
        
        # Check for transposition (swapped adjacent characters)
        if len(legitimate) == len(suspicious):
            for i in range(len(legitimate) - 1):
                if (legitimate[i] == suspicious[i+1] and 
                    legitimate[i+1] == suspicious[i] and
                    legitimate[:i] == suspicious[:i] and
                    legitimate[i+2:] == suspicious[i+2:]):
                    score = 0.88
                    reasons.append(f"Character transposition at position {i}")
                    break
        
        return score, reasons
    
    def compare_names(self, legitimate_name, suspicious_name):
        """
        Compare two app names using multiple algorithms
        Returns (similarity_score, reasons)
        """
        # Normalize both names
        norm_legit = self.normalize_text(legitimate_name)
        norm_susp = self.normalize_text(suspicious_name)
        
        reasons = []
        
        # Exact match after normalization
        if norm_legit == norm_susp:
            return 1.0, ["Exact match after normalization"]
        
        # Check for typosquatting
        typo_score, typo_reasons = self.detect_typosquatting(norm_legit, norm_susp)
        if typo_score > 0:
            return typo_score, typo_reasons
        
        # Calculate various similarity metrics
        levenshtein = self.levenshtein_similarity(norm_legit, norm_susp)
        fuzzy = self.fuzzy_ratio(norm_legit, norm_susp)
        partial_fuzzy = self.fuzzy_partial_ratio(norm_legit, norm_susp)
        sequence = self.sequence_matcher_ratio(norm_legit, norm_susp)
        
        # Weighted average (emphasize exact matching more)
        combined_score = (
            0.30 * levenshtein +
            0.30 * fuzzy +
            0.20 * partial_fuzzy +
            0.20 * sequence
        )
        
        # Add reasons based on scores
        if levenshtein > 0.85:
            reasons.append(f"High Levenshtein similarity: {levenshtein:.2%}")
        if fuzzy > 0.85:
            reasons.append(f"High fuzzy match: {fuzzy:.2%}")
        if partial_fuzzy > 0.90:
            reasons.append(f"Strong partial match: {partial_fuzzy:.2%}")
        
        # Check for substring containment
        if norm_legit in norm_susp or norm_susp in norm_legit:
            combined_score = max(combined_score, 0.80)
            reasons.append("One name contains the other")
        
        return round(combined_score, 4), reasons
    
    def compare_package_ids(self, legitimate_package, suspicious_package):
        """
        Compare package IDs (e.g., com.company.app)
        Package IDs require stricter matching
        """
        # Split into components
        legit_parts = legitimate_package.split('.')
        susp_parts = suspicious_package.split('.')
        
        reasons = []
        
        # Check if same number of components
        if len(legit_parts) != len(susp_parts):
            reasons.append("Different package structure")
        
        # Compare each component
        component_scores = []
        for i, (legit, susp) in enumerate(zip(legit_parts, susp_parts)):
            if legit == susp:
                component_scores.append(1.0)
            else:
                score = self.levenshtein_similarity(legit, susp)
                component_scores.append(score)
                
                if score > 0.8:
                    reasons.append(f"Similar component: {legit} ≈ {susp}")
        
        # Overall package similarity (stricter than name matching)
        if len(component_scores) > 0:
            avg_score = sum(component_scores) / len(component_scores)
        else:
            avg_score = 0.0
        
        return round(avg_score, 4), reasons
    
    def batch_compare(self, legitimate_name, suspicious_names):
        """
        Compare one legitimate name against multiple suspicious names
        Returns list of (name, score, reasons) tuples
        """
        results = []
        
        for susp_name in suspicious_names:
            score, reasons = self.compare_names(legitimate_name, susp_name)
            results.append((susp_name, score, reasons))
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results


# Usage example
if __name__ == "__main__":
    detector = TextSimilarityDetector()
    
    # Example comparisons
    legitimate = "PayPal"
    suspicious_apps = [
        "PayPal",           # Exact match
        "PayPaI",           # I instead of l
        "Pay Pal",          # Space
        "PayPal App",       # Extra word
        "PayPal Pro",       # Extra word
        "РayPal",           # Cyrillic P
        "Pay-Pal",          # Hyphen
        "Paypal Official",  # Different case + extra
        "MyPayPal",         # Prefix
    ]
    
    print(f"Comparing against legitimate app: '{legitimate}'\\n")
    
    results = detector.batch_compare(legitimate, suspicious_apps)
    
    for name, score, reasons in results:
        risk = "🔴 HIGH" if score > 0.85 else "🟡 MEDIUM" if score > 0.70 else "🟢 LOW"
        print(f"{risk} | {name}: {score:.2%}")
        if reasons:
            for reason in reasons:
                print(f"     └─ {reason}")
        print()
