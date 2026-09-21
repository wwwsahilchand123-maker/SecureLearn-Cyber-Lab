import os

import pytest

from backend.config import Config


def test_development_allows_default_secret(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setattr(Config, "SECRET_KEY", "dev-secret-key-change-in-production")
    Config.validate()


def test_production_rejects_default_secret(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setattr(Config, "SECRET_KEY", "dev-secret-key-change-in-production")
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        Config.validate()


def test_production_requires_long_secret(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setattr(Config, "SECRET_KEY", "too-short")
    with pytest.raises(RuntimeError, match="32 characters"):
        Config.validate()
