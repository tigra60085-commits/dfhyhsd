"""Start handler and main menu routing."""

from telegram import Update
from telegram.ext import ContextTypes

from states import (
    MAIN_MENU, DRUG_CLASS_SELECT, QUIZ_MENU, FLASHCARD_CATEGORY,
    CASE_LIST, INTER_DRUG1, SEARCH_INPUT, NT_SELECT, PROGRESS_VIEW,
    GLOSSARY_BROWSE, TIP_VIEW, COMPARE_SELECT1,
)
from keyboards.menus import main_menu_keyboard
from db.queries import get_or_create_user


WELCOME_TEXT = (
    "👋 Добро пожаловать в *Психофармакологический тьютор*!\n\n"
    "Я помогу вам изучить:\n"
    "• 💊 Справочник препаратов по классам\n"
    "• 📝 Тесты и карточки для самопроверки\n"
    "• 🏥 Клинические случаи\n"
    "• ⚠️ Взаимодействия лекарств\n"
    "• 🧠 Нейромедиаторные системы\n"
    "• 📖 Глоссарий терминов\n\n"
    "Выберите раздел:"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await get_or_create_user(user.id, user.username)
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )
    return MAIN_MENU


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text

    routing = {
        "💊 Препараты": DRUG_CLASS_SELECT,
        "📝 Тест": QUIZ_MENU,
        "🃏 Карточки": FLASHCARD_CATEGORY,
        "🏥 Клинические случаи": CASE_LIST,
        "⚠️ Взаимодействия": INTER_DRUG1,
        "🔍 Поиск": SEARCH_INPUT,
        "🧠 Нейромедиаторы": NT_SELECT,
        "📊 Мой прогресс": PROGRESS_VIEW,
        "📖 Глоссарий": GLOSSARY_BROWSE,
        "💡 Совет дня": TIP_VIEW,
        "⚖️ Сравнить классы": COMPARE_SELECT1,
    }

    next_state = routing.get(text)
    if next_state is None:
        await update.message.reply_text(
            "Пожалуйста, воспользуйтесь кнопками меню.",
            reply_markup=main_menu_keyboard(),
        )
        return MAIN_MENU

    # Import handler entry points lazily to avoid circular imports
    if next_state == DRUG_CLASS_SELECT:
        from handlers.drug import show_drug_classes
        return await show_drug_classes(update, context)
    elif next_state == QUIZ_MENU:
        from handlers.quiz import show_quiz_menu
        return await show_quiz_menu(update, context)
    elif next_state == FLASHCARD_CATEGORY:
        from handlers.flashcard import show_flashcard_categories
        return await show_flashcard_categories(update, context)
    elif next_state == CASE_LIST:
        from handlers.case import show_case_list
        return await show_case_list(update, context)
    elif next_state == INTER_DRUG1:
        from handlers.interaction import ask_drug1
        return await ask_drug1(update, context)
    elif next_state == SEARCH_INPUT:
        from handlers.search import ask_search_query
        return await ask_search_query(update, context)
    elif next_state == NT_SELECT:
        from handlers.misc import show_nt_select
        return await show_nt_select(update, context)
    elif next_state == PROGRESS_VIEW:
        from handlers.progress import show_progress
        return await show_progress(update, context)
    elif next_state == GLOSSARY_BROWSE:
        from handlers.misc import show_glossary
        return await show_glossary(update, context)
    elif next_state == TIP_VIEW:
        from handlers.misc import show_tip
        return await show_tip(update, context)
    elif next_state == COMPARE_SELECT1:
        from handlers.misc import show_compare_select1
        return await show_compare_select1(update, context)

    return MAIN_MENU
