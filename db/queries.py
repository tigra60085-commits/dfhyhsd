"""Async database query helpers."""

import aiosqlite
from datetime import date
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


# ── User preferences ───────────────────────────────────────────────────────────

async def get_user_prefs(user_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT quiz_difficulty, daily_reminder FROM user_prefs WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        if row:
            return dict(row)
        return {"quiz_difficulty": "all", "daily_reminder": 0}


async def set_user_pref(user_id: int, key: str, value) -> None:
    """Update a single user preference by key."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO user_prefs (user_id) VALUES (?) ON CONFLICT(user_id) DO NOTHING",
            (user_id,),
        )
        await db.execute(
            f"UPDATE user_prefs SET {key} = ? WHERE user_id = ?",  # noqa: S608 – key is internal
            (value, user_id),
        )
        await db.commit()


# ── Streaks ────────────────────────────────────────────────────────────────────

async def touch_streak(user_id: int) -> dict:
    """Update the daily activity streak and return current/longest values."""
    today = date.today().isoformat()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        # Ensure row exists
        await db.execute(
            "INSERT OR IGNORE INTO streaks (user_id, current_streak, longest_streak, last_active_date) "
            "VALUES (?, 0, 0, NULL)",
            (user_id,),
        )
        cursor = await db.execute(
            "SELECT current_streak, longest_streak, last_active_date FROM streaks WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        current = row["current_streak"]
        longest = row["longest_streak"]
        last = row["last_active_date"]

        if last == today:
            # Already counted today
            pass
        else:
            from datetime import timedelta
            yesterday = (date.today() - timedelta(days=1)).isoformat()
            if last == yesterday:
                current += 1
            else:
                current = 1
            longest = max(longest, current)
            await db.execute(
                "UPDATE streaks SET current_streak=?, longest_streak=?, last_active_date=? WHERE user_id=?",
                (current, longest, today, user_id),
            )
        await db.commit()
    return {"current_streak": current, "longest_streak": longest}


async def get_streak(user_id: int) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT current_streak, longest_streak FROM streaks WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        if row:
            return dict(row)
        return {"current_streak": 0, "longest_streak": 0}


# ── Admin ──────────────────────────────────────────────────────────────────────

async def get_admin_stats() -> dict:
    """Aggregate statistics for admin dashboard."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM users")
        row = await cursor.fetchone()
        total_users = row["cnt"]

        cursor = await db.execute("SELECT COUNT(*) as cnt FROM quiz_scores")
        row = await cursor.fetchone()
        total_questions = row["cnt"]

        cursor = await db.execute(
            "SELECT COUNT(*) as cnt FROM users WHERE created_at >= date('now', '-7 days')"
        )
        row = await cursor.fetchone()
        new_users_7d = row["cnt"]

        cursor = await db.execute(
            "SELECT COUNT(DISTINCT user_id) as cnt FROM quiz_scores "
            "WHERE created_at >= date('now', '-1 days')"
        )
        row = await cursor.fetchone()
        active_today = row["cnt"]

    return {
        "total_users": total_users,
        "total_questions": total_questions,
        "new_users_7d": new_users_7d,
        "active_today": active_today,
    }
