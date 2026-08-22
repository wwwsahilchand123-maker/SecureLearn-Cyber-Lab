# backend/services/url_analyzer.py
"""
URL Analysis Service
Educational Phishing Detection Simulator
"""

import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Tuple
import math
from collections import Counter

class URLAnalyzer:
    """Analyze URLs for phishing indicators"""
    
    SUSPICIOUS_KEYWORDS = [
        'login', 'signin', 'account', 'verify', 'secure', 'update',
        'confirm', 'banking', 'password', 'credential', 'suspended',
        'locked', 'unusual', 'click', 'here', 'now', 'urgent'
    ]
    
    SUSPICIOUS_TLDS = [
        '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work',
        '.date', '.racing', '.download', '.stream', '.loan', '.win'
    ]
    
    COMMON_BRANDS = [
        'paypal', 'amazon', 'google', 'microsoft', 'apple', 'facebook',
        'netflix', 'instagram', 'twitter', 'linkedin', 'ebay', 'yahoo'
    ]
    
    def __init__(self):
        self.indicators = []
        self.risk_score = 0
    
    def analyze(self, url: str) -> Dict:
        """Analyze URL and return results"""
        self.indicators = []
        self.risk_score = 0
        
        # Extract features
        features = self.extract_features(url)
        
        # Calculate risk score
        self.risk_score = self.calculate_risk_score(features, url)
        
        # Determine risk level
        risk_level = self.get_risk_level(self.risk_score)
        
        return {
            'url': url,
            'risk_score': self.risk_score,
            'risk_level': risk_level,
            'features': features,
            'indicators': self.indicators,
            'recommendation': self.get_recommendation(risk_level)
        }
    
    def extract_features(self, url: str) -> Dict:
        """Extract URL features for analysis"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            path = parsed.path
            params = parse_qs(parsed.query)
            
            features = {
                # Length features
                'url_length': len(url),
                'domain_length': len(domain),
                'path_length': len(path),
                
                # Character counts
                'num_dots': url.count('.'),
                'num_hyphens': url.count('-'),
                'num_underscores': url.count('_'),
                'num_slashes': url.count('/'),
                'num_digits': sum(c.isdigit() for c in url),
                'num_params': len(params),
                
                # Binary features
                'has_ip': 1 if self._has_ip(domain) else 0,
                'has_https': 1 if url.startswith('https://') else 0,
                'has_at_symbol': 1 if '@' in url else 0,
                'has_double_slash': 1 if '//' in path else 0,
                'suspicious_tld': 1 if self._has_suspicious_tld(url) else 0,
                
                # Advanced features
                'num_subdomains': len(domain.split('.')) - 2 if '.' in domain else 0,
                'entropy': self._calculate_entropy(url),
                
                # Additional info
                'protocol': parsed.scheme,
                'domain': domain,
                'has_port': 1 if ':' in domain else 0
            }
            
            return features
            
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_risk_score(self, features: Dict, url: str) -> int:
        """Calculate risk score (0-100)"""
        score = 0
        
        # URL length check
        if features.get('url_length', 0) > 75:
            score += 15
            self.indicators.append("Unusually long URL")
        
        # Domain length check
        if features.get('domain_length', 0) > 30:
            score += 10
            self.indicators.append("Long domain name")
        
        # IP address in URL
        if features.get('has_ip', 0):
            score += 25
            self.indicators.append("Uses IP address instead of domain")
        
        # HTTPS missing
        if not features.get('has_https', 0):
            score += 20
            self.indicators.append("Missing HTTPS encryption")
        
        # Excessive dots/subdomains
        if features.get('num_dots', 0) > 4:
            score += 15
            self.indicators.append("Excessive subdomains")
        
        # Suspicious TLD
        if features.get('suspicious_tld', 0):
            score += 20
            self.indicators.append("Suspicious top-level domain")
        
        # @ symbol (redirect technique)
        if features.get('has_at_symbol', 0):
            score += 20
            self.indicators.append("Contains @ symbol (possible redirect)")
        
        # Double slash in path
        if features.get('has_double_slash', 0):
            score += 10
            self.indicators.append("Double slash in path")
        
        # Excessive hyphens
        if features.get('num_hyphens', 0) > 3:
            score += 10
            self.indicators.append("Excessive hyphens")
        
        # High entropy (randomness)
        if features.get('entropy', 0) > 4.5:
            score += 15
            self.indicators.append("High randomness in URL structure")
        
        # Suspicious keywords
        url_lower = url.lower()
        keyword_count = sum(1 for keyword in self.SUSPICIOUS_KEYWORDS if keyword in url_lower)
        if keyword_count > 0:
            score += min(keyword_count * 5, 20)
            self.indicators.append(f"Contains {keyword_count} suspicious keyword(s)")
        
        # Brand impersonation
        for brand in self.COMMON_BRANDS:
            if brand in url_lower and brand not in features.get('domain', '').lower():
                score += 25
                self.indicators.append(f"Possible {brand.title()} impersonation")
                break
        
        # Excessive parameters
        if features.get('num_params', 0) > 5:
            score += 10
            self.indicators.append("Excessive URL parameters")
        
        return min(score, 100)
    
    def get_risk_level(self, score: int) -> str:
        """Determine risk level from score"""
        if score < 30:
            return "LOW"
        elif score < 60:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def get_recommendation(self, risk_level: str) -> str:
        """Get recommendation based on risk level"""
        recommendations = {
            "LOW": "This URL appears relatively safe, but always verify the source.",
            "MEDIUM": "Exercise caution. Verify the sender and don't enter sensitive information.",
            "HIGH": "⚠️ High risk! Do not click this link or enter any credentials."
        }
        return recommendations.get(risk_level, "Unable to determine safety.")
    
    def _has_ip(self, domain: str) -> bool:
        """Check if domain is an IP address"""
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        return bool(re.match(ip_pattern, domain))
    
    def _has_suspicious_tld(self, url: str) -> bool:
        """Check for suspicious TLDs"""
        return any(url.endswith(tld) for tld in self.SUSPICIOUS_TLDS)
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy"""
        if not text:
            return 0.0
        
        counter = Counter(text)
        length = len(text)
        entropy = 0.0
        
        for count in counter.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
        
        return entropy

# Test the analyzer
if __name__ == '__main__':
    analyzer = URLAnalyzer()
    
    # Test URLs
    test_urls = [
        "https://www.google.com",
        "http://paypal-secure-login.tk/verify",
        "https://192.168.1.1/login",
        "http://amaz0n-account-update.xyz/signin?user=test&redirect=malicious"
    ]
    
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"Testing: {url}")
        result = analyzer.analyze(url)
        print(f"Risk Score: {result['risk_score']}/100")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Indicators: {', '.join(result['indicators']) if result['indicators'] else 'None'}")