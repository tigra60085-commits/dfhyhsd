"""Database schema creation."""

import aiosqlite
from config import DATABASE_PATH


CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    user_id    INTEGER PRIMARY KEY,
    username   TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_QUIZ_SCORES = """
CREATE TABLE IF NOT EXISTS quiz_scores (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    category   TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
"""

CREATE_PROGRESS = """
CREATE TABLE IF NOT EXISTS progress (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    section         TEXT NOT NULL,
    completed_count INTEGER NOT NULL DEFAULT 1,
    last_seen_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, section),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
"""

CREATE_FLASHCARD_RATINGS = """
CREATE TABLE IF NOT EXISTS flashcard_ratings (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    drug_name  TEXT NOT NULL,
    rating     TEXT NOT NULL,
    rated_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
"""


CREATE_USER_PREFS = """
CREATE TABLE IF NOT EXISTS user_prefs (
    user_id        INTEGER PRIMARY KEY,
    quiz_difficulty TEXT NOT NULL DEFAULT 'all',
    daily_reminder INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
"""

CREATE_STREAKS = """
CREATE TABLE IF NOT EXISTS streaks (
    user_id         INTEGER PRIMARY KEY,
    current_streak  INTEGER NOT NULL DEFAULT 0,
    longest_streak  INTEGER NOT NULL DEFAULT 0,
    last_active_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
"""


async def create_tables() -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(CREATE_USERS)
        await db.execute(CREATE_QUIZ_SCORES)
        await db.execute(CREATE_PROGRESS)
        await db.execute(CREATE_FLASHCARD_RATINGS)
        await db.execute(CREATE_USER_PREFS)
        await db.execute(CREATE_STREAKS)
        await db.commit()
