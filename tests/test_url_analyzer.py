from backend.services.url_analyzer import URLAnalyzer


def test_valid_ip_address_is_flagged_as_high_risk():
    result = URLAnalyzer().analyze("http://192.168.1.10/login")

    assert result["features"]["has_ip"] == 1
    assert result["risk_level"] == "HIGH"
    assert any("IP address" in indicator for indicator in result["indicators"])


def test_https_domain_without_obvious_signals_stays_low_risk():
    result = URLAnalyzer().analyze("https://example.com")

    assert result["features"]["has_https"] == 1
    assert result["features"]["has_ip"] == 0
    assert result["risk_level"] == "LOW"


def test_brand_impersonation_signal_is_recorded():
    result = URLAnalyzer().analyze("https://paypal-login.example.com/verify")

    assert any("Paypal impersonation" in indicator for indicator in result["indicators"])
    assert result["risk_score"] >= 25
