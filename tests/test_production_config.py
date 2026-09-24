from backend.config import ProductionConfig


def test_production_disables_debug():
    assert ProductionConfig.DEBUG is False


def test_production_session_cookie_hardening():
    assert ProductionConfig.SESSION_COOKIE_HTTPONLY is True
    assert ProductionConfig.SESSION_COOKIE_SAMESITE == "Lax"
    assert ProductionConfig.PERMANENT_SESSION_LIFETIME.total_seconds() == 24 * 60 * 60


def test_production_cors_is_local_by_default():
    assert ProductionConfig.CORS_ORIGINS == [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
    ]
