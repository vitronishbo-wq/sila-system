import os
from urllib.parse import urlparse

import pytest

from scripts.force_delete_users import check_safety, get_target_emails


def test_get_target_emails_from_cli():
    assert get_target_emails("a@x,b@x") == ["a@x", "b@x"]


def test_get_target_emails_from_env(monkeypatch):
    monkeypatch.setenv("FORCE_DELETE_EMAILS", "c@x,d@x")
    assert get_target_emails() == ["c@x", "d@x"]


def test_get_target_emails_default(monkeypatch):
    monkeypatch.delenv("FORCE_DELETE_EMAILS", raising=False)
    emails = get_target_emails()
    assert "admin@sila.co.ao" in emails


def test_check_safety_local(monkeypatch):
    # simulate settings.ENVIRONMENT not production and local DB
    monkeypatch.setattr(
        "app.core.config.settings.ENVIRONMENT", "development", raising=False
    )
    local_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/sila_db"
    # Should not raise
    check_safety(local_url)


def test_check_safety_block_remote(monkeypatch):
    monkeypatch.setattr(
        "app.core.config.settings.ENVIRONMENT", "development", raising=False
    )
    remote_url = "postgresql+asyncpg://postgres:postgres@db.example.com:5432/sila_db"
    with pytest.raises(SystemExit):
        check_safety(remote_url)


def test_check_safety_block_prod(monkeypatch):
    monkeypatch.setattr(
        "app.core.config.settings.ENVIRONMENT", "production", raising=False
    )
    local_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/sila_db"
    with pytest.raises(SystemExit):
        check_safety(local_url)
