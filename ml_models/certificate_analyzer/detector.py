import hashlib
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class CertificateAnalyzer:
    """Analyze APK certificates and signatures"""
    
    def __init__(self, legitimate_certificates: List[str] = None):
        """
        Initialize with list of known legitimate certificate fingerprints
        """
        self.legitimate_certs = legitimate_certificates or []
    
    def extract_certificate_info(self, apk_path: str) -> Dict:
        """
        Extract certificate information from APK
        In production, use androguard for actual APK analysis
        """
        try:
            from androguard.core.bytecodes.apk import APK
            
            apk = APK(apk_path)
            
            # Get certificate information
            cert = apk.get_certificate_der(apk.get_signature_names()[0])
            
            # Calculate fingerprints
            md5 = hashlib.md5(cert).hexdigest()
            sha1 = hashlib.sha1(cert).hexdigest()
            sha256 = hashlib.sha256(cert).hexdigest()
            
            # Get certificate details
            cert_info = {
                'md5': md5,
                'sha1': sha1,
                'sha256': sha256,
                'issuer': apk.get_certificate(apk.get_signature_names()[0]).get('issuer', 'Unknown'),
                'subject': apk.get_certificate(apk.get_signature_names()[0]).get('subject', 'Unknown'),
                'valid_from': None,  # Extract from cert
                'valid_to': None,    # Extract from cert
                'serial_number': None,
            }
            
            return cert_info
            
        except ImportError:
            # Fallback for demo purposes
            return self._mock_certificate_info(apk_path)
        except Exception as e:
            print(f"Error extracting certificate: {e}")
            return None
    
    def _mock_certificate_info(self, apk_path: str) -> Dict:
        """Mock certificate info for demo"""
        # This is just for demonstration
        app_hash = hashlib.md5(apk_path.encode()).hexdigest()
        
        return {
            'md5': app_hash[:32],
            'sha1': hashlib.sha1(app_hash.encode()).hexdigest(),
            'sha256': hashlib.sha256(app_hash.encode()).hexdigest(),
            'issuer': 'CN=Unknown Developer',
            'subject': 'CN=Unknown App',
            'valid_from': '2023-01-01',
            'valid_to': '2025-01-01',
            'serial_number': '12345678',
        }
    
    def verify_certificate(self, suspicious_cert: Dict) -> Tuple[bool, List[str]]:
        """
        Verify if certificate matches legitimate ones
        Returns (is_match, reasons)
        """
        reasons = []
        
        if not suspicious_cert:
            return False, ["No certificate information available"]
        
        # Check against known legitimate certificates
        for legit_cert in self.legitimate_certs:
            if suspicious_cert['sha256'] == legit_cert:
                return True, ["Certificate matches legitimate app"]
            
            if suspicious_cert['sha1'] == legit_cert:
                return True, ["Certificate matches legitimate app (SHA1)"]
        
        # If no match found
        reasons.append("Certificate does not match any known legitimate certificates")
        
        # Additional checks
        if self._is_debug_certificate(suspicious_cert):
            reasons.append("⚠️ Using debug/development certificate")
        
        if self._is_self_signed(suspicious_cert):
            reasons.append("Self-signed certificate detected")
        
        if self._has_suspicious_issuer(suspicious_cert):
            reasons.append("⚠️ Suspicious certificate issuer")
        
        return False, reasons
    
    def _is_debug_certificate(self, cert_info: Dict) -> bool:
        """Check if using Android debug certificate"""
        debug_patterns = [
            'CN=Android Debug',
            'O=Android',
            'androiddebugkey',
        ]
        
        issuer = cert_info.get('issuer', '').lower()
        subject = cert_info.get('subject', '').lower()
        
        for pattern in debug_patterns:
            if pattern.lower() in issuer or pattern.lower() in subject:
                return True
        
        return False
    
    def _is_self_signed(self, cert_info: Dict) -> bool:
        """Check if certificate is self-signed"""
        issuer = cert_info.get('issuer', '')
        subject = cert_info.get('subject', '')
        
        # Self-signed if issuer == subject
        return issuer == subject
    
    def _has_suspicious_issuer(self, cert_info: Dict) -> bool:
        """Check for suspicious certificate issuers"""
        suspicious_patterns = [
            'unknown',
            'test',
            'temp',
            'fake',
            'copy',
            'clone',
        ]
        
        issuer = cert_info.get('issuer', '').lower()
        
        for pattern in suspicious_patterns:
            if pattern in issuer:
                return True
        
        return False
    
    def compare_certificates(self, cert1: Dict, cert2: Dict) -> float:
        """
        Compare two certificates and return similarity score
        """
        if not cert1 or not cert2:
            return 0.0
        
        # Exact match on SHA256
        if cert1.get('sha256') == cert2.get('sha256'):
            return 1.0
        
        # Exact match on SHA1
        if cert1.get('sha1') == cert2.get('sha1'):
            return 1.0
        
        # Different certificates
        return 0.0
    
    def analyze_signing_pattern(self, cert_info: Dict) -> Dict:
        """
        Analyze certificate for suspicious patterns
        Returns risk assessment
        """
        risk_score = 0.0
        flags = []
        
        # Check for debug certificate
        if self._is_debug_certificate(cert_info):
            risk_score += 0.4
            flags.append("DEBUG_CERTIFICATE")
        
        # Check for suspicious issuer
        if self._has_suspicious_issuer(cert_info):
            risk_score += 0.3
            flags.append("SUSPICIOUS_ISSUER")
        
        # Check certificate validity
        valid_to = cert_info.get('valid_to')
        if valid_to:
            # Check if certificate is expired or expiring soon
            # (This would need proper date parsing in production)
            pass
        
        # Short validity period (< 1 year) is suspicious for production apps
        # This would require proper date calculation
        
        return {
            'risk_score': min(risk_score, 1.0),
            'flags': flags,
            'is_legitimate': risk_score < 0.3,
        }


# Usage example
if __name__ == "__main__":
    # Known legitimate certificates (SHA256)
    legitimate_certs = [
        "a1b2c3d4e5f6...",  # PayPal legitimate cert
        "1234567890ab...",  # WhatsApp legitimate cert
    ]
    
    analyzer = CertificateAnalyzer(legitimate_certs)
    
    # Analyze a suspicious APK
    apk_path = "suspicious_app.apk"
    cert_info = analyzer.extract_certificate_info(apk_path)
    
    if cert_info:
        print(f"Certificate Info:")
        print(f"  SHA256: {cert_info['sha256']}")
        print(f"  Issuer: {cert_info['issuer']}")
        print(f"  Subject: {cert_info['subject']}")
        print()
        
        # Verify certificate
        is_match, reasons = analyzer.verify_certificate(cert_info)
        
        if is_match:
            print("✅ Certificate matches legitimate app")
        else:
            print("❌ Certificate DOES NOT match legitimate app")
            print("Reasons:")
            for reason in reasons:
                print(f"  - {reason}")
        
        # Analyze signing pattern
        analysis = analyzer.analyze_signing_pattern(cert_info)
        print(f"\\nRisk Score: {analysis['risk_score']:.2%}")
        print(f"Flags: {', '.join(analysis['flags']) if analysis['flags'] else 'None'}")
        print(f"Legitimate: {analysis['is_legitimate']}")
