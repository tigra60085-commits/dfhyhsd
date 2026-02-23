"""Shared pytest fixtures for the psychopharmacology bot test suite."""

import os

import pytest
import aiosqlite

# Ensure BOT_TOKEN is set before any module imports config.py
os.environ.setdefault("BOT_TOKEN", "test_bot_token_for_ci")


@pytest.fixture
async def db_conn():
    """Create an in-memory SQLite DB for each test with all tables initialized."""
    from db.schema import create_tables
    async with aiosqlite.connect(":memory:") as conn:
        # Manually execute the table creation statements since create_tables()
        # doesn't take a connection parameter
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                section TEXT NOT NULL,
                completed_count INTEGER DEFAULT 1,
                last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, section),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS flashcard_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                drug_name TEXT NOT NULL,
                rating TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_prefs (
                user_id INTEGER PRIMARY KEY,
                quiz_difficulty TEXT NOT NULL DEFAULT 'all',
                daily_reminder INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS streaks (
                user_id INTEGER PRIMARY KEY,
                current_streak INTEGER NOT NULL DEFAULT 0,
                longest_streak INTEGER NOT NULL DEFAULT 0,
                last_active_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await conn.commit()
        yield conn
