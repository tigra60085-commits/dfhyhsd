"""Unit tests for keyboard factory functions in keyboards/menus.py.

We duck-type the returned keyboard objects (type(kb).__name__) instead of
importing telegram types directly, to stay compatible with environments where
the cryptography/cffi backend is unavailable.

If the telegram package itself cannot be imported (broken cffi), the entire
module is skipped via pytest.importorskip.
"""

import pytest

pytest.importorskip("telegram", reason="python-telegram-bot not importable (cffi backend missing)")

from keyboards.menus import (
    back_keyboard,
    case_answer_keyboard,
    case_format_focus_keyboard,
    case_format_options_keyboard,
    case_format_result_keyboard,
    case_list_keyboard,
    case_next_keyboard,
    compare_result_keyboard,
    dose_calc_result_keyboard,
    drug_class_keyboard,
    drug_detail_keyboard,
    drug_list_keyboard,
    flashcard_category_keyboard,
    flashcard_rate_keyboard,
    flashcard_show_keyboard,
    glossary_keyboard,
    interaction_result_keyboard,
    main_menu_keyboard,
    monitor_result_keyboard,
    pharma_compare_focus_keyboard,
    preg_result_keyboard,
    quiz_answer_keyboard,
    quiz_category_keyboard,
    quiz_difficulty_keyboard,
    quiz_menu_keyboard,
    quiz_next_keyboard,
    scale_result_keyboard,
    scale_select_keyboard,
    search_result_keyboard,
    withdraw_result_keyboard,
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _all_callbacks(keyboard) -> list:
    """Flatten all callback_data strings from an inline keyboard."""
    return [btn.callback_data for row in keyboard.inline_keyboard for btn in row]


def _button_texts(keyboard) -> list:
    return [btn.text for row in keyboard.inline_keyboard for btn in row]


# ─── Main menu ────────────────────────────────────────────────────────────────


def test_main_menu_is_reply_keyboard():
    kb = main_menu_keyboard()
    assert type(kb).__name__ == "ReplyKeyboardMarkup"


def test_main_menu_has_at_least_nine_rows():
    kb = main_menu_keyboard()
    assert len(kb.keyboard) >= 9


def test_main_menu_resize_keyboard():
    kb = main_menu_keyboard()
    assert kb.resize_keyboard is True


# ─── Drug keyboards ───────────────────────────────────────────────────────────


def test_drug_class_keyboard_callback_prefix():
    kb = drug_class_keyboard(["SSRI", "SNRI"])
    callbacks = _all_callbacks(kb)
    assert "class:SSRI" in callbacks
    assert "class:SNRI" in callbacks


def test_drug_class_keyboard_has_back_button():
    kb = drug_class_keyboard(["SSRI"])
    callbacks = _all_callbacks(kb)
    assert any("back:" in cb for cb in callbacks)


def test_drug_list_keyboard_callback_prefix():
    drugs = [{"name": "Флуоксетин"}, {"name": "Сертралин"}]
    kb = drug_list_keyboard(drugs, "SSRI")
    callbacks = _all_callbacks(kb)
    assert "drug:Флуоксетин" in callbacks
    assert "drug:Сертралин" in callbacks


def test_drug_detail_keyboard_is_inline():
    kb = drug_detail_keyboard("Флуоксетин")
    assert type(kb).__name__ == "InlineKeyboardMarkup"
    assert len(kb.inline_keyboard) > 0


# ─── Quiz keyboards ───────────────────────────────────────────────────────────


def test_quiz_answer_keyboard_four_options():
    kb = quiz_answer_keyboard(["А", "Б", "В", "Г"])
    callbacks = _all_callbacks(kb)
    assert len(callbacks) == 4
    for i in range(4):
        assert f"qans:{i}" in callbacks


def test_quiz_answer_keyboard_two_options():
    kb = quiz_answer_keyboard(["Да", "Нет"])
    callbacks = _all_callbacks(kb)
    assert "qans:0" in callbacks
    assert "qans:1" in callbacks


def test_quiz_category_keyboard_has_all_option():
    kb = quiz_category_keyboard(["SSRI", "SNRI"])
    callbacks = _all_callbacks(kb)
    assert "qcat:all" in callbacks


def test_quiz_difficulty_keyboard_has_all_levels():
    kb = quiz_difficulty_keyboard()
    callbacks = _all_callbacks(kb)
    assert "qdiff:easy" in callbacks
    assert "qdiff:medium" in callbacks
    assert "qdiff:hard" in callbacks
    assert "qdiff:all" in callbacks


def test_quiz_next_keyboard_callbacks():
    kb = quiz_next_keyboard()
    callbacks = _all_callbacks(kb)
    assert "quiz:next" in callbacks
    assert "quiz:finish" in callbacks


# ─── Case-format keyboards ────────────────────────────────────────────────────


def test_case_format_focus_keyboard_prefixes():
    kb = case_format_focus_keyboard()
    callbacks = _all_callbacks(kb)
    focus_callbacks = [cb for cb in callbacks if cb.startswith("cff:")]
    assert len(focus_callbacks) == 7  # 7 focus options defined


def test_case_format_options_keyboard_has_four_options():
    kb = case_format_options_keyboard()
    callbacks = _all_callbacks(kb)
    cfopt_callbacks = [cb for cb in callbacks if cb.startswith("cfopt:")]
    assert len(cfopt_callbacks) == 4


def test_case_format_result_keyboard_has_again():
    kb = case_format_result_keyboard()
    callbacks = _all_callbacks(kb)
    assert "cf:again" in callbacks


# ─── Scale keyboards ──────────────────────────────────────────────────────────


def test_scale_select_keyboard_has_ten_scales():
    kb = scale_select_keyboard()
    callbacks = _all_callbacks(kb)
    scale_callbacks = [cb for cb in callbacks if cb.startswith("scale:")]
    assert len(scale_callbacks) == 10


def test_scale_result_keyboard_has_again():
    kb = scale_result_keyboard()
    callbacks = _all_callbacks(kb)
    assert "scale:again" in callbacks


# ─── Glossary keyboard (pagination) ───────────────────────────────────────────


def test_glossary_keyboard_page_zero_no_prev():
    terms = [f"term_{i}" for i in range(20)]
    kb = glossary_keyboard(terms, page=0)
    callbacks = _all_callbacks(kb)
    assert not any(cb == "gpage:0" for cb in callbacks)  # no prev on page 0 (prev would be gpage:-1)
    # But there should be a next button
    assert any(cb.startswith("gpage:") for cb in callbacks)


def test_glossary_keyboard_middle_page_has_both_nav():
    terms = [f"term_{i}" for i in range(30)]
    kb = glossary_keyboard(terms, page=1)
    callbacks = _all_callbacks(kb)
    # Should have both prev (gpage:0) and next (gpage:2)
    assert "gpage:0" in callbacks
    assert "gpage:2" in callbacks


def test_glossary_keyboard_terms_as_buttons():
    terms = ["Агорафобия", "Анксиолитик", "Атаракс"]
    kb = glossary_keyboard(terms, page=0)
    callbacks = _all_callbacks(kb)
    assert any(cb.startswith("gterm:") for cb in callbacks)


# ─── Utility keyboards ────────────────────────────────────────────────────────


def test_back_keyboard_default():
    kb = back_keyboard()
    callbacks = _all_callbacks(kb)
    assert "back:main" in callbacks


def test_back_keyboard_custom():
    kb = back_keyboard("back:quiz_menu")
    callbacks = _all_callbacks(kb)
    assert "back:quiz_menu" in callbacks


def test_dose_calc_result_keyboard_has_again():
    kb = dose_calc_result_keyboard()
    callbacks = _all_callbacks(kb)
    assert "dc:again" in callbacks


def test_monitor_result_keyboard_has_again():
    kb = monitor_result_keyboard()
    callbacks = _all_callbacks(kb)
    assert "mon:again" in callbacks


def test_preg_result_keyboard_has_again():
    kb = preg_result_keyboard()
    callbacks = _all_callbacks(kb)
    assert "preg:again" in callbacks


def test_withdraw_result_keyboard_has_again():
    kb = withdraw_result_keyboard()
    callbacks = _all_callbacks(kb)
    assert "wd:again" in callbacks


def test_interaction_result_keyboard():
    kb = interaction_result_keyboard()
    callbacks = _all_callbacks(kb)
    assert "inter:again" in callbacks


def test_search_result_keyboard():
    kb = search_result_keyboard()
    callbacks = _all_callbacks(kb)
    assert "search:again" in callbacks


def test_pharma_compare_focus_keyboard_has_back():
    kb = pharma_compare_focus_keyboard()
    callbacks = _all_callbacks(kb)
    assert any(cb.startswith("pcfocus:") for cb in callbacks)
    assert "back:main" in callbacks
