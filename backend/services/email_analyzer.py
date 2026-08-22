# backend/services/email_analyzer.py
"""
Email/Message Analysis Service
Educational Phishing Detection Simulator
"""

import re
from typing import Dict, List, Tuple

class EmailAnalyzer:
    """Analyze emails for phishing indicators"""
    
    URGENCY_KEYWORDS = [
        'urgent', 'immediate', 'action required', 'suspend', 'verify now',
        'click here', 'within 24 hours', 'expire', 'limited time',
        'act now', 'don\'t delay', 'hurry', 'final notice'
    ]
    
    THREAT_KEYWORDS = [
        'account closed', 'suspended', 'locked', 'unauthorized',
        'unusual activity', 'security alert', 'verify identity',
        'confirm identity', 'blocked', 'terminated'
    ]
    
    FINANCIAL_KEYWORDS = [
        'refund', 'payment', 'invoice', 'wire transfer', 'bank account',
        'credit card', 'ssn', 'social security', 'tax return',
        'prize', 'lottery', 'inheritance', 'million dollars'
    ]
    
    CREDENTIAL_KEYWORDS = [
        'password', 'username', 'login', 'signin', 'credential',
        'verify account', 'update information', 'confirm details',
        'personal information', 'security question'
    ]
    
    POOR_GRAMMAR_PATTERNS = [
        r'\b(your|you\'re)\s+(account|password)\s+has\s+been\s+compromise\b',
        r'\bDear\s+Customer\b',
        r'\bDear\s+User\b',
        r'\bkindly\s+',
        r'\bdo\s+the\s+needful\b',
    ]
    
    def __init__(self):
        self.indicators = []
        self.risk_score = 0
    
    def analyze(self, sender: str, subject: str, body: str) -> Dict:
        """Analyze email for phishing indicators"""
        self.indicators = []
        self.risk_score = 0
        
        # Check sender
        self._check_sender(sender)
        
        # Check subject
        self._check_subject(subject)
        
        # Check body
        self._check_body(body)
        
        # Check links
        self._check_links(body)
        
        # Determine risk level
        risk_level = self._get_risk_level(self.risk_score)
        
        return {
            'sender': sender,
            'subject': subject,
            'risk_score': min(self.risk_score, 100),
            'risk_level': risk_level,
            'indicators': self.indicators,
            'phishing_techniques': self._identify_techniques(),
            'recommendation': self._get_recommendation(risk_level)
        }
    
    def _check_sender(self, sender: str):
        """Check sender email address"""
        sender_lower = sender.lower()
        
        # Check for suspicious domain
        if '@' in sender:
            domain = sender.split('@')[1]
            
            # Free email providers for business
            free_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
            if any(provider in domain for provider in free_providers):
                if any(word in sender_lower for word in ['paypal', 'amazon', 'bank', 'irs', 'support']):
                    self.risk_score += 20
                    self.indicators.append("Business using free email provider")
            
            # Suspicious TLDs
            if domain.endswith(('.tk', '.ml', '.ga', '.cf', '.gq')):
                self.risk_score += 15
                self.indicators.append("Suspicious email domain")
            
            # Misspelled domains
            common_brands = ['paypal', 'amazon', 'google', 'microsoft', 'apple']
            for brand in common_brands:
                if brand in domain and brand not in domain.split('.')[0]:
                    self.risk_score += 25
                    self.indicators.append(f"Possible {brand.title()} domain spoofing")
        
        # Display name vs email mismatch
        if '<' in sender and '>' in sender:
            display_name = sender.split('<')[0].strip().lower()
            email_part = sender.split('<')[1].split('>')[0].lower()
            
            if display_name and display_name not in email_part:
                self.risk_score += 15
                self.indicators.append("Display name doesn't match email address")
    
    def _check_subject(self, subject: str):
        """Check email subject line"""
        subject_lower = subject.lower()
        
        # Urgency in subject
        urgency_count = sum(1 for keyword in self.URGENCY_KEYWORDS if keyword in subject_lower)
        if urgency_count > 0:
            self.risk_score += min(urgency_count * 10, 20)
            self.indicators.append("Urgent language in subject")
        
        # Threats in subject
        threat_count = sum(1 for keyword in self.THREAT_KEYWORDS if keyword in subject_lower)
        if threat_count > 0:
            self.risk_score += min(threat_count * 15, 25)
            self.indicators.append("Threatening language in subject")
        
        # All caps
        if subject.isupper() and len(subject) > 10:
            self.risk_score += 10
            self.indicators.append("ALL CAPS subject line")
        
        # Excessive punctuation
        if subject.count('!') > 1 or subject.count('?') > 1:
            self.risk_score += 5
            self.indicators.append("Excessive punctuation")
    
    def _check_body(self, body: str):
        """Check email body content"""
        body_lower = body.lower()
        
        # Generic greetings
        generic_greetings = ['dear customer', 'dear user', 'dear member', 'dear account holder']
        if any(greeting in body_lower for greeting in generic_greetings):
            self.risk_score += 15
            self.indicators.append("Generic greeting (not personalized)")
        
        # Urgency
        urgency_count = sum(1 for keyword in self.URGENCY_KEYWORDS if keyword in body_lower)
        if urgency_count > 2:
            self.risk_score += 20
            self.indicators.append("Multiple urgency indicators")
        
        # Threats
        threat_count = sum(1 for keyword in self.THREAT_KEYWORDS if keyword in body_lower)
        if threat_count > 0:
            self.risk_score += 20
            self.indicators.append("Contains threats or warnings")
        
        # Credential requests
        credential_count = sum(1 for keyword in self.CREDENTIAL_KEYWORDS if keyword in body_lower)
        if credential_count > 0:
            self.risk_score += 30
            self.indicators.append("Requests credentials or personal information")
        
        # Financial requests
        financial_count = sum(1 for keyword in self.FINANCIAL_KEYWORDS if keyword in body_lower)
        if financial_count > 0:
            self.risk_score += 25
            self.indicators.append("Requests financial information")
        
        # Poor grammar patterns
        grammar_issues = sum(1 for pattern in self.POOR_GRAMMAR_PATTERNS if re.search(pattern, body_lower))
        if grammar_issues > 0:
            self.risk_score += min(grammar_issues * 10, 20)
            self.indicators.append("Poor grammar or spelling")
        
        # Suspicious attachments mentioned
        if re.search(r'\b(open|view|download)\s+(attachment|file|document)\b', body_lower):
            self.risk_score += 15
            self.indicators.append("Requests to open attachments")
    
    def _check_links(self, body: str):
        """Check links in email body"""
        # Find URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, body)
        
        if len(urls) > 5:
            self.risk_score += 10
            self.indicators.append("Contains many links")
        
        # Check for mismatched display text and URL
        html_link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
        html_links = re.findall(html_link_pattern, body, re.IGNORECASE)
        
        for url, display_text in html_links:
            if 'click here' in display_text.lower() or 'here' == display_text.lower():
                self.risk_score += 10
                self.indicators.append("Generic 'click here' links")
            
            # Check if display text suggests different domain
            if 'http' in display_text and url != display_text:
                self.risk_score += 20
                self.indicators.append("Link URL doesn't match displayed text")
        
        # Shortened URLs
        url_shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly']
        if any(shortener in body.lower() for shortener in url_shorteners):
            self.risk_score += 15
            self.indicators.append("Contains shortened URLs")
    
    def _identify_techniques(self) -> List[str]:
        """Identify phishing techniques used"""
        techniques = []
        
        indicators_text = ' '.join(self.indicators).lower()
        
        if 'urgent' in indicators_text or 'threat' in indicators_text:
            techniques.append("Social Engineering: Creating urgency/fear")
        
        if 'credential' in indicators_text or 'personal information' in indicators_text:
            techniques.append("Credential Harvesting")
        
        if 'spoofing' in indicators_text or 'mismatch' in indicators_text:
            techniques.append("Domain Spoofing")
        
        if 'generic greeting' in indicators_text:
            techniques.append("Mass Phishing Campaign")
        
        if 'financial' in indicators_text:
            techniques.append("Financial Fraud")
        
        return techniques
    
    def _get_risk_level(self, score: int) -> str:
        """Determine risk level"""
        if score < 30:
            return "LOW"
        elif score < 60:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _get_recommendation(self, risk_level: str) -> str:
        """Get recommendation"""
        recommendations = {
            "LOW": "Email appears relatively safe, but always verify sender before clicking links.",
            "MEDIUM": "⚠️ Exercise caution. Verify the sender directly before taking any action.",
            "HIGH": "🚨 High phishing risk! Do not click links or provide any information. Report as spam."
        }
        return recommendations.get(risk_level, "Unable to determine safety.")

# Test the analyzer
if __name__ == '__main__':
    analyzer = EmailAnalyzer()
    
    # Test phishing email
    result = analyzer.analyze(
        sender="PayPal Security <noreply@paypa1-secure.tk>",
        subject="URGENT: Your Account Will Be Suspended!",
        body="""
        Dear Customer,
        
        We have detected unusual activity on your account. Your account will be 
        suspended within 24 hours unless you verify your identity immediately.
        
        Click here to verify: http://paypal-verify.tk/login
        
        Failure to verify will result in permanent account closure.
        
        PayPal Security Team
        """
    )
    
    print(f"\nRisk Score: {result['risk_score']}/100")
    print(f"Risk Level: {result['risk_level']}")
    print(f"\nIndicators:")
    for indicator in result['indicators']:
        print(f"  - {indicator}")
    print(f"\nPhishing Techniques:")
    for technique in result['phishing_techniques']:
        print(f"  - {technique}")
    print(f"\nRecommendation: {result['recommendation']}")