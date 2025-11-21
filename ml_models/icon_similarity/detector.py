import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests
from io import BytesIO
import imagehash
import numpy as np


class IconSimilarityDetector:
    """Detect similar app icons using multiple techniques"""
    
    def __init__(self, model_path=None):
        # Use pre-trained ResNet for feature extraction
        self.model = models.resnet50(pretrained=True)
        self.model.eval()
        
        # Remove the final classification layer
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    
    def load_image(self, image_url_or_path):
        """Load image from URL or file path"""
        try:
            if image_url_or_path.startswith('http'):
                response = requests.get(image_url_or_path)
                image = Image.open(BytesIO(response.content)).convert('RGB')
            else:
                image = Image.open(image_url_or_path).convert('RGB')
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def extract_features(self, image):
        """Extract deep learning features from image"""
        if image is None:
            return None
        
        image_tensor = self.transform(image).unsqueeze(0)
        
        with torch.no_grad():
            features = self.model(image_tensor)
        
        return features.squeeze().numpy()
    
    def perceptual_hash_similarity(self, img1, img2):
        """Calculate perceptual hash similarity"""
        hash1 = imagehash.phash(img1)
        hash2 = imagehash.phash(img2)
        
        # Lower difference = more similar (0 = identical)
        difference = hash1 - hash2
        similarity = 1 - (difference / 64.0)  # Normalize to 0-1
        return max(0, similarity)
    
    def deep_feature_similarity(self, features1, features2):
        """Calculate cosine similarity between feature vectors"""
        if features1 is None or features2 is None:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(features1, features2) / (
            np.linalg.norm(features1) * np.linalg.norm(features2)
        )
        return float(similarity)
    
    def compare_icons(self, icon1_url, icon2_url):
        """
        Compare two icons using multiple methods
        Returns combined similarity score (0-1)
        """
        img1 = self.load_image(icon1_url)
        img2 = self.load_image(icon2_url)
        
        if img1 is None or img2 is None:
            return 0.0
        
        # Method 1: Perceptual hash
        phash_score = self.perceptual_hash_similarity(img1, img2)
        
        # Method 2: Deep learning features
        features1 = self.extract_features(img1)
        features2 = self.extract_features(img2)
        deep_score = self.deep_feature_similarity(features1, features2)
        
        # Method 3: Average hash
        avg_hash1 = imagehash.average_hash(img1)
        avg_hash2 = imagehash.average_hash(img2)
        avg_hash_score = 1 - ((avg_hash1 - avg_hash2) / 64.0)
        avg_hash_score = max(0, avg_hash_score)
        
        # Combine scores (weighted average)
        combined_score = (
            0.4 * phash_score +
            0.4 * deep_score +
            0.2 * avg_hash_score
        )
        
        return round(combined_score, 4)
    
    def batch_compare(self, reference_icon, suspicious_icons):
        """
        Compare one reference icon against multiple suspicious icons
        Returns list of (index, similarity_score) tuples
        """
        results = []
        
        for idx, suspicious_icon in enumerate(suspicious_icons):
            score = self.compare_icons(reference_icon, suspicious_icon)
            results.append((idx, score))
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results


# Usage example
if __name__ == "__main__":
    detector = IconSimilarityDetector()
    
    # Example comparison
    legitimate_icon = "path/to/legitimate/icon.png"
    suspicious_icon = "path/to/suspicious/icon.png"
    
    similarity = detector.compare_icons(legitimate_icon, suspicious_icon)
    print(f"Icon similarity: {similarity:.2%}")
    
    if similarity > 0.85:
        print("⚠️ HIGH RISK: Icons are very similar!")
    elif similarity > 0.70:
        print("⚠️ MEDIUM RISK: Icons have notable similarities")
    else:
        print("✓ LOW RISK: Icons are sufficiently different")
