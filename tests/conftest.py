"""Shared pytest fixtures for the psychopharmacology bot test suite."""

import os

import pytest

# Ensure BOT_TOKEN is set before any module imports config.py
os.environ.setdefault("BOT_TOKEN", "test_bot_token_for_ci")


@pytest.fixture
async def db_path(tmp_path, monkeypatch):
    """Create an isolated SQLite DB in a temp directory for each test."""
    path = str(tmp_path / "test.db")
    monkeypatch.setattr("db.schema.DATABASE_PATH", path)
    monkeypatch.setattr("db.queries.DATABASE_PATH", path)
    from db.schema import create_tables
    await create_tables()
    return path
