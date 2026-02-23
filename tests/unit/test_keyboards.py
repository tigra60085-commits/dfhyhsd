"""Unit tests for keyboard factory functions."""

from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

from keyboards.menus import (
    main_menu_keyboard, drug_class_keyboard, quiz_category_keyboard,
    quiz_difficulty_keyboard, quiz_answer_keyboard, flashcard_rate_keyboard,
    case_list_keyboard, search_result_keyboard, glossary_keyboard, back_keyboard,
)


class TestKeyboards:
    """Tests for keyboard factory return types and structures."""

    def test_main_menu_keyboard_type(self):
        """Main menu should return ReplyKeyboardMarkup."""
        kb = main_menu_keyboard()
        assert isinstance(kb, ReplyKeyboardMarkup)
        assert len(kb.keyboard) >= 9

    def test_drug_class_keyboard_type(self):
        """Drug class keyboard should return InlineKeyboardMarkup."""
        classes = ["SSRI", "SNRI", "TCA"]
        kb = drug_class_keyboard(classes)
        assert isinstance(kb, InlineKeyboardMarkup)
        assert len(kb.inline_keyboard) > 0

    def test_quiz_category_keyboard_type(self):
        """Quiz category keyboard should return InlineKeyboardMarkup."""
        kb = quiz_category_keyboard(["SSRI", "SNRI"])
        assert isinstance(kb, InlineKeyboardMarkup)

    def test_quiz_difficulty_keyboard_type(self):
        """Quiz difficulty keyboard should return InlineKeyboardMarkup."""
        kb = quiz_difficulty_keyboard()
        assert isinstance(kb, InlineKeyboardMarkup)
        assert len(kb.inline_keyboard) > 0

    def test_quiz_answer_keyboard_structure(self):
        """Quiz answer keyboard should have buttons."""
        options = ["A) SSRI", "B) SNRI", "C) TCA", "D) MAOI"]
        kb = quiz_answer_keyboard(options)
        assert isinstance(kb, InlineKeyboardMarkup)
        assert len(kb.inline_keyboard) > 0

    def test_flashcard_rate_keyboard_type(self):
        """Flashcard rate keyboard should return InlineKeyboardMarkup."""
        kb = flashcard_rate_keyboard()
        assert isinstance(kb, InlineKeyboardMarkup)
        assert len(kb.inline_keyboard) > 0

    def test_case_list_keyboard_type(self):
        """Case list keyboard should return InlineKeyboardMarkup."""
        from data.clinical_cases import CASES
        kb = case_list_keyboard(CASES)
        assert isinstance(kb, InlineKeyboardMarkup)

    def test_search_result_keyboard_type(self):
        """Search result keyboard should return InlineKeyboardMarkup."""
        kb = search_result_keyboard()
        assert isinstance(kb, InlineKeyboardMarkup)

    def test_glossary_keyboard_type(self):
        """Glossary keyboard should return InlineKeyboardMarkup."""
        terms = ["Term1", "Term2", "Term3", "Term4", "Term5"]
        kb = glossary_keyboard(terms, page=0)
        assert isinstance(kb, InlineKeyboardMarkup)

    def test_back_keyboard_structure(self):
        """Back button keyboard should have correct structure."""
        kb = back_keyboard("back:main")
        assert isinstance(kb, InlineKeyboardMarkup)
        assert len(kb.inline_keyboard) == 1
        assert kb.inline_keyboard[0][0].callback_data == "back:main"
