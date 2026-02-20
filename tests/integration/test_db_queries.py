"""Integration tests for db/queries.py using an isolated SQLite file."""

import pytest

from db.queries import (
    get_or_create_user,
    get_user_stats,
    rate_flashcard,
    record_quiz_answer,
    update_progress,
)


# All tests receive db_path from conftest.py, which patches DATABASE_PATH
# for both db.schema and db.queries and runs create_tables().


class TestGetOrCreateUser:
    async def test_creates_user(self, db_path):
        # Should not raise
        await get_or_create_user(1, "alice")

    async def test_idempotent_second_call(self, db_path):
        await get_or_create_user(1, "alice")
        await get_or_create_user(1, "alice")  # INSERT OR IGNORE — must not raise

    async def test_none_username_accepted(self, db_path):
        await get_or_create_user(2, None)

    async def test_multiple_users(self, db_path):
        await get_or_create_user(10, "user_a")
        await get_or_create_user(11, "user_b")


class TestRecordQuizAnswer:
    async def test_records_correct_answer(self, db_path):
        await get_or_create_user(1, "alice")
        await record_quiz_answer(1, "SSRI", True)

    async def test_records_incorrect_answer(self, db_path):
        await get_or_create_user(1, "alice")
        await record_quiz_answer(1, "SSRI", False)

    async def test_multiple_answers(self, db_path):
        await get_or_create_user(1, "alice")
        for _ in range(5):
            await record_quiz_answer(1, "Механизмы действия", True)


class TestGetUserStats:
    async def test_unknown_user_returns_zero_stats(self, db_path):
        stats = await get_user_stats(99999)
        assert stats["total_questions"] == 0
        assert stats["correct_answers"] == 0
        assert stats["accuracy"] == 0

    async def test_accuracy_calculation(self, db_path):
        await get_or_create_user(1, "alice")
        # 3 correct, 1 wrong → 75.0%
        for _ in range(3):
            await record_quiz_answer(1, "SSRI", True)
        await record_quiz_answer(1, "SSRI", False)

        stats = await get_user_stats(1)
        assert stats["total_questions"] == 4
        assert stats["correct_answers"] == 3
        assert stats["accuracy"] == 75.0

    async def test_perfect_score(self, db_path):
        await get_or_create_user(2, "bob")
        await record_quiz_answer(2, "SNRI", True)
        stats = await get_user_stats(2)
        assert stats["accuracy"] == 100.0

    async def test_zero_score(self, db_path):
        await get_or_create_user(3, "carol")
        await record_quiz_answer(3, "TCA", False)
        stats = await get_user_stats(3)
        assert stats["accuracy"] == 0.0
        assert stats["total_questions"] == 1
        assert stats["correct_answers"] == 0

    async def test_stats_has_required_keys(self, db_path):
        await get_or_create_user(4, "dave")
        stats = await get_user_stats(4)
        for key in ("total_questions", "correct_answers", "accuracy", "categories", "sections", "flashcard_ratings"):
            assert key in stats, f"Missing key: {key}"

    async def test_per_category_breakdown(self, db_path):
        await get_or_create_user(5, "eve")
        await record_quiz_answer(5, "SSRI", True)
        await record_quiz_answer(5, "SNRI", False)
        stats = await get_user_stats(5)
        categories = {c["category"] for c in stats["categories"]}
        assert "SSRI" in categories
        assert "SNRI" in categories


class TestUpdateProgress:
    async def test_creates_progress_entry(self, db_path):
        await get_or_create_user(1, "alice")
        await update_progress(1, "quiz")

    async def test_increments_on_second_call(self, db_path):
        await get_or_create_user(1, "alice")
        await update_progress(1, "flashcard")
        await update_progress(1, "flashcard")

        stats = await get_user_stats(1)
        section_counts = {s["section"]: s["completed_count"] for s in stats["sections"]}
        assert section_counts.get("flashcard", 0) == 2

    async def test_different_sections_tracked_separately(self, db_path):
        await get_or_create_user(1, "alice")
        await update_progress(1, "quiz")
        await update_progress(1, "drug")

        stats = await get_user_stats(1)
        sections = {s["section"] for s in stats["sections"]}
        assert "quiz" in sections
        assert "drug" in sections


class TestRateFlashcard:
    async def test_rates_flashcard(self, db_path):
        await get_or_create_user(1, "alice")
        await rate_flashcard(1, "Флуоксетин", "easy")

    async def test_multiple_ratings_same_drug(self, db_path):
        await get_or_create_user(1, "alice")
        # Same drug can be rated multiple times (no unique constraint)
        await rate_flashcard(1, "Сертралин", "easy")
        await rate_flashcard(1, "Сертралин", "hard")

    async def test_all_rating_values(self, db_path):
        await get_or_create_user(1, "alice")
        for rating in ("easy", "medium", "hard"):
            await rate_flashcard(1, "Эсциталопрам", rating)

    async def test_ratings_appear_in_user_stats(self, db_path):
        await get_or_create_user(1, "alice")
        await rate_flashcard(1, "Литий", "easy")
        await rate_flashcard(1, "Литий", "easy")
        await rate_flashcard(1, "Вальпроат", "hard")

        stats = await get_user_stats(1)
        ratings = stats["flashcard_ratings"]
        assert ratings.get("easy", 0) == 2
        assert ratings.get("hard", 0) == 1
