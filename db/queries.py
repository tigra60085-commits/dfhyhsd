"""Async database query helpers."""

import aiosqlite
from config import DATABASE_PATH


async def get_or_create_user(user_id: int, username: str | None) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username or ""),
        )
        await db.commit()


async def record_quiz_answer(user_id: int, category: str, is_correct: bool) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO quiz_scores (user_id, category, is_correct) VALUES (?, ?, ?)",
            (user_id, category, int(is_correct)),
        )
        await db.commit()


async def get_user_stats(user_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        # Overall quiz stats
        cursor = await db.execute(
            "SELECT COUNT(*) as total, SUM(is_correct) as correct FROM quiz_scores WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        total = row["total"] or 0
        correct = row["correct"] or 0

        # Per-category stats
        cursor = await db.execute(
            """
            SELECT category,
                   COUNT(*) as total,
                   SUM(is_correct) as correct
            FROM quiz_scores
            WHERE user_id = ?
            GROUP BY category
            ORDER BY total DESC
            """,
            (user_id,),
        )
        categories = await cursor.fetchall()

        # Progress sections
        cursor = await db.execute(
            "SELECT section, completed_count FROM progress WHERE user_id = ? ORDER BY last_seen_at DESC",
            (user_id,),
        )
        sections = await cursor.fetchall()

        # Flashcard ratings
        cursor = await db.execute(
            """
            SELECT rating, COUNT(*) as cnt
            FROM flashcard_ratings
            WHERE user_id = ?
            GROUP BY rating
            """,
            (user_id,),
        )
        ratings = await cursor.fetchall()

    return {
        "total_questions": total,
        "correct_answers": correct,
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "categories": [dict(r) for r in categories],
        "sections": [dict(s) for s in sections],
        "flashcard_ratings": {r["rating"]: r["cnt"] for r in ratings},
    }


async def update_progress(user_id: int, section: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO progress (user_id, section, completed_count, last_seen_at)
            VALUES (?, ?, 1, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, section)
            DO UPDATE SET
                completed_count = completed_count + 1,
                last_seen_at = CURRENT_TIMESTAMP
            """,
            (user_id, section),
        )
        await db.commit()


async def rate_flashcard(user_id: int, drug_name: str, rating: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO flashcard_ratings (user_id, drug_name, rating) VALUES (?, ?, ?)",
            (user_id, drug_name, rating),
        )
        await db.commit()
