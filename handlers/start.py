"""Start handler and main menu routing."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from states import (
    MAIN_MENU, DRUG_CLASS_SELECT, QUIZ_MENU, FLASHCARD_CATEGORY,
    CASE_LIST, INTER_DRUG1, SEARCH_INPUT, NT_SELECT, PROGRESS_VIEW,
    GLOSSARY_BROWSE, TIP_VIEW, COMPARE_SELECT1,
    PHARMA_COMPARE_INPUT, PODCAST_TOPIC, CASE_FORMAT_INPUT,
    DOSE_CALC_DRUG, MONITOR_DRUG, SCALE_SELECT, PREG_DRUG, WITHDRAW_DRUG,
)
from keyboards.menus import main_menu_keyboard
from db.queries import get_or_create_user, touch_streak

logger = logging.getLogger(__name__)


WELCOME_TEXT = (
    "👋 Добро пожаловать в *Психофармакологический тьютор*!\n\n"
    "Я помогу вам изучить:\n"
    "• 💊 Справочник препаратов по классам\n"
    "• 📝 Тесты и карточки для самопроверки\n"
    "• 🏥 Клинические случаи\n"
    "• ⚠️ Взаимодействия лекарств\n"
    "• 🧠 Нейромедиаторные системы\n"
    "• 📖 Глоссарий терминов\n"
    "• 🔬 Детальный сравнительный анализ препаратов (.docx)\n"
    "• 🎙️ Генератор подкаст-эпизода (.docx)\n"
    "• 📋 Форматирование клинического кейса (.docx)\n"
    "• 💉 Дозирование препаратов\n"
    "• 🔭 Протоколы мониторинга\n"
    "• 📊 Психометрические шкалы\n"
    "• 🤰 Безопасность при беременности/лактации\n"
    "• 🚫 Протоколы отмены препаратов\n\n"
    "Выберите раздел:"
)


HELP_TEXT = (
    "ℹ️ *Справка — Психофармакологический тьютор*\n\n"
    "*Доступные разделы:*\n"
    "• 💊 Препараты — справочник по 50+ препаратам\n"
    "• 📝 Тест — квизы с адаптивной сложностью\n"
    "• 🃏 Карточки — флеш-карточки для запоминания\n"
    "• 🏥 Клинические случаи — 25 разборов\n"
    "• ⚠️ Взаимодействия — 50+ пар взаимодействий\n"
    "• 🔍 Поиск — нечёткий поиск по базе препаратов\n"
    "• 🧠 Нейромедиаторы — DA, 5-HT, NE, ГАМК, Глу, АЦХ\n"
    "• 📊 Мой прогресс — статистика + стрик\n"
    "• 📖 Глоссарий — термины психофармакологии\n"
    "• 🔬 Фарма-анализ — детальное сравнение препаратов (.docx)\n"
    "• 💉 Дозы — дозирование и фармакокинетика\n"
    "• 🔭 Мониторинг — протоколы мониторинга\n"
    "• 📊 Шкалы — PHQ-9, GAD-7, HAMD, PANSS и др.\n"
    "• 🤰 Беременность — безопасность при беременности/лактации\n"
    "• 🚫 Отмена — протоколы отмены препаратов\n\n"
    "*Команды:*\n"
    "/start — перезапустить бот\n"
    "/help — эта справка\n\n"
    "_По вопросам и предложениям: обратитесь к администратору._"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    try:
        await get_or_create_user(user.id, user.username)
        await touch_streak(user.id)
    except Exception as e:
        logger.warning("DB error in start_command for user %s: %s", user.id, e)
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )
    return MAIN_MENU


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command — works outside conversation too."""
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler — logs the error and notifies the user."""
    logger.error(f"[ERROR_HANDLER] Unhandled exception: {type(context.error).__name__}: {context.error}", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "Произошла ошибка. Попробуйте снова или нажмите /start для перезапуска."
            )
        except Exception:
            pass


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    logger.info(f"[MAIN_MENU] User {update.effective_user.id} sent: {text!r}")

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
        "🔬 Фарма-анализ": PHARMA_COMPARE_INPUT,
        "🎙️ Подкаст": PODCAST_TOPIC,
        "📋 Кейс": CASE_FORMAT_INPUT,
        "💉 Дозы": DOSE_CALC_DRUG,
        "🔭 Мониторинг": MONITOR_DRUG,
        "📊 Шкалы": SCALE_SELECT,
        "🤰 Беременность": PREG_DRUG,
        "🚫 Отмена": WITHDRAW_DRUG,
    }

    next_state = routing.get(text)
    if next_state is None:
        logger.warning(f"[MAIN_MENU] Unknown text from user {update.effective_user.id}: {text!r}")
        await update.message.reply_text(
            "Пожалуйста, воспользуйтесь кнопками меню.",
            reply_markup=main_menu_keyboard(),
        )
        return MAIN_MENU

    logger.info(f"[MAIN_MENU] Routing {text!r} to state {next_state}")

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
    elif next_state == PHARMA_COMPARE_INPUT:
        from handlers.pharma_compare import start_pharma_compare
        return await start_pharma_compare(update, context)
    elif next_state == PODCAST_TOPIC:
        from handlers.podcast_dialog import start_podcast
        return await start_podcast(update, context)
    elif next_state == CASE_FORMAT_INPUT:
        from handlers.case_format import start_case_format
        return await start_case_format(update, context)
    elif next_state == DOSE_CALC_DRUG:
        from handlers.dose_calc import start_dose_calc
        return await start_dose_calc(update, context)
    elif next_state == MONITOR_DRUG:
        from handlers.monitor_guide import start_monitor_guide
        return await start_monitor_guide(update, context)
    elif next_state == SCALE_SELECT:
        from handlers.scale_calc import start_scale_calc
        return await start_scale_calc(update, context)
    elif next_state == PREG_DRUG:
        from handlers.preg_safety import start_preg_safety
        return await start_preg_safety(update, context)
    elif next_state == WITHDRAW_DRUG:
        from handlers.withdraw_guide import start_withdraw_guide
        return await start_withdraw_guide(update, context)

    return MAIN_MENU
