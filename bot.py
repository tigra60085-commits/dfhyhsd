"""Main entry point for the Psychopharmacology Tutor Bot."""

import asyncio
import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)

from config import BOT_TOKEN
from db.schema import create_tables
from states import (
    MAIN_MENU,
    DRUG_CLASS_SELECT, DRUG_LIST, DRUG_DETAIL,
    QUIZ_MENU, QUIZ_CATEGORY, QUIZ_DIFFICULTY, QUIZ_QUESTION, QUIZ_NEXT,
    FLASHCARD_CATEGORY, FLASHCARD_SHOW, FLASHCARD_RATE,
    CASE_LIST, CASE_READ, CASE_QUESTION, CASE_ANSWER,
    INTER_DRUG1, INTER_DRUG2, INTER_RESULT,
    SEARCH_INPUT, SEARCH_RESULT,
    NT_SELECT, GLOSSARY_BROWSE, PROGRESS_VIEW, TIP_VIEW,
    COMPARE_SELECT1, COMPARE_SELECT2,
    PHARMA_COMPARE_INPUT, PHARMA_COMPARE_CONTEXT, PHARMA_COMPARE_FOCUS, PHARMA_COMPARE_AUDIENCE,
    PODCAST_TOPIC, PODCAST_CASE, PODCAST_DURATION,
    CASE_FORMAT_INPUT, CASE_FORMAT_FOCUS, CASE_FORMAT_OPTIONS,
    DOSE_CALC_DRUG, DOSE_CALC_RESULT,
    MONITOR_DRUG, MONITOR_RESULT,
    SCALE_SELECT, SCALE_INPUT, SCALE_RESULT,
    PREG_DRUG, PREG_RESULT,
    WITHDRAW_DRUG, WITHDRAW_RESULT,
)
from handlers.start import start_command, main_menu_handler
from handlers.drug import drug_class_callback, drug_list_callback, drug_detail_callback
from handlers.quiz import (
    quiz_menu_callback, quiz_category_callback, quiz_difficulty_callback,
    quiz_answer_callback, quiz_next_callback,
)
from handlers.flashcard import (
    flashcard_category_callback, flashcard_show_callback, flashcard_rate_callback,
)
from handlers.case import (
    case_list_callback, case_read_callback, case_question_callback, case_answer_callback,
)
from handlers.interaction import inter_drug1_message, inter_drug2_message, inter_result_callback
from handlers.search import search_input_message, search_result_callback
from handlers.progress import progress_back_callback
from handlers.misc import (
    nt_select_callback, glossary_callback, tip_back_callback,
    compare_select1_callback, compare_select2_callback,
)
from handlers.pharma_compare import (
    pharma_compare_drugs_message, pharma_compare_context_message,
    pharma_compare_focus_callback, pharma_compare_audience_callback,
)
from handlers.podcast_dialog import (
    podcast_topic_message, podcast_case_message, podcast_duration_callback,
)
from handlers.case_format import (
    case_format_input_message, case_format_focus_callback, case_format_options_callback,
)
from handlers.dose_calc import (
    dose_calc_drug_message, dose_calc_result_callback,
)
from handlers.monitor_guide import (
    monitor_drug_message, monitor_result_callback,
)
from handlers.scale_calc import (
    scale_select_callback, scale_input_message, scale_result_callback,
)
from handlers.preg_safety import (
    preg_drug_message, preg_result_callback,
)
from handlers.withdraw_guide import (
    withdraw_drug_message, withdraw_result_callback,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def build_conv_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler),
            ],
            # ── Drug browsing ──────────────────────────────────────────────────
            DRUG_CLASS_SELECT: [
                CallbackQueryHandler(drug_class_callback),
            ],
            DRUG_LIST: [
                CallbackQueryHandler(drug_list_callback),
            ],
            DRUG_DETAIL: [
                CallbackQueryHandler(drug_detail_callback),
            ],
            # ── Quiz ───────────────────────────────────────────────────────────
            QUIZ_MENU: [
                CallbackQueryHandler(quiz_menu_callback),
            ],
            QUIZ_CATEGORY: [
                CallbackQueryHandler(quiz_category_callback),
            ],
            QUIZ_DIFFICULTY: [
                CallbackQueryHandler(quiz_difficulty_callback),
            ],
            QUIZ_QUESTION: [
                CallbackQueryHandler(quiz_answer_callback, pattern=r"^qans:"),
            ],
            QUIZ_NEXT: [
                CallbackQueryHandler(quiz_next_callback),
            ],
            # ── Flashcards ─────────────────────────────────────────────────────
            FLASHCARD_CATEGORY: [
                CallbackQueryHandler(flashcard_category_callback),
            ],
            FLASHCARD_SHOW: [
                CallbackQueryHandler(flashcard_show_callback),
            ],
            FLASHCARD_RATE: [
                CallbackQueryHandler(flashcard_rate_callback),
            ],
            # ── Clinical cases ─────────────────────────────────────────────────
            CASE_LIST: [
                CallbackQueryHandler(case_list_callback),
            ],
            CASE_READ: [
                CallbackQueryHandler(case_read_callback),
            ],
            CASE_QUESTION: [
                CallbackQueryHandler(case_question_callback, pattern=r"^caseans:"),
            ],
            CASE_ANSWER: [
                CallbackQueryHandler(case_answer_callback),
            ],
            # ── Drug interactions ──────────────────────────────────────────────
            INTER_DRUG1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, inter_drug1_message),
                CallbackQueryHandler(inter_result_callback, pattern=r"^back:"),
            ],
            INTER_DRUG2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, inter_drug2_message),
                CallbackQueryHandler(inter_result_callback, pattern=r"^back:"),
            ],
            INTER_RESULT: [
                CallbackQueryHandler(inter_result_callback),
            ],
            # ── Search ─────────────────────────────────────────────────────────
            SEARCH_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_input_message),
                CallbackQueryHandler(search_result_callback, pattern=r"^back:"),
            ],
            SEARCH_RESULT: [
                CallbackQueryHandler(search_result_callback),
            ],
            # ── Neurotransmitters ──────────────────────────────────────────────
            NT_SELECT: [
                CallbackQueryHandler(nt_select_callback),
            ],
            # ── Glossary ───────────────────────────────────────────────────────
            GLOSSARY_BROWSE: [
                CallbackQueryHandler(glossary_callback),
            ],
            # ── Progress ───────────────────────────────────────────────────────
            PROGRESS_VIEW: [
                CallbackQueryHandler(progress_back_callback, pattern=r"^back:"),
            ],
            # ── Tip ────────────────────────────────────────────────────────────
            TIP_VIEW: [
                CallbackQueryHandler(tip_back_callback, pattern=r"^back:"),
            ],
            # ── Compare ────────────────────────────────────────────────────────
            COMPARE_SELECT1: [
                CallbackQueryHandler(compare_select1_callback),
            ],
            COMPARE_SELECT2: [
                CallbackQueryHandler(compare_select2_callback),
            ],
            # ── Pharma-compare ─────────────────────────────────────────────────
            PHARMA_COMPARE_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, pharma_compare_drugs_message),
                CallbackQueryHandler(pharma_compare_audience_callback, pattern=r"^back:"),
            ],
            PHARMA_COMPARE_CONTEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, pharma_compare_context_message),
                CallbackQueryHandler(pharma_compare_audience_callback, pattern=r"^back:"),
            ],
            PHARMA_COMPARE_FOCUS: [
                CallbackQueryHandler(pharma_compare_focus_callback),
            ],
            PHARMA_COMPARE_AUDIENCE: [
                CallbackQueryHandler(pharma_compare_audience_callback),
            ],
            # ── Podcast dialog ─────────────────────────────────────────────────
            PODCAST_TOPIC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, podcast_topic_message),
                CallbackQueryHandler(podcast_duration_callback, pattern=r"^back:"),
            ],
            PODCAST_CASE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, podcast_case_message),
                CallbackQueryHandler(podcast_duration_callback, pattern=r"^back:"),
            ],
            PODCAST_DURATION: [
                CallbackQueryHandler(podcast_duration_callback),
            ],
            # ── Case-format ────────────────────────────────────────────────────
            CASE_FORMAT_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, case_format_input_message),
                CallbackQueryHandler(case_format_focus_callback, pattern=r"^back:"),
            ],
            CASE_FORMAT_FOCUS: [
                CallbackQueryHandler(case_format_focus_callback),
            ],
            CASE_FORMAT_OPTIONS: [
                CallbackQueryHandler(case_format_options_callback),
            ],
            # ── Dose calculator ────────────────────────────────────────────────
            DOSE_CALC_DRUG: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, dose_calc_drug_message),
                CallbackQueryHandler(dose_calc_result_callback, pattern=r"^back:"),
            ],
            DOSE_CALC_RESULT: [
                CallbackQueryHandler(dose_calc_result_callback),
            ],
            # ── Monitoring guide ───────────────────────────────────────────────
            MONITOR_DRUG: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_drug_message),
                CallbackQueryHandler(monitor_result_callback, pattern=r"^back:"),
            ],
            MONITOR_RESULT: [
                CallbackQueryHandler(monitor_result_callback),
            ],
            # ── Scale calculator ───────────────────────────────────────────────
            SCALE_SELECT: [
                CallbackQueryHandler(scale_select_callback),
            ],
            SCALE_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, scale_input_message),
                CallbackQueryHandler(scale_result_callback, pattern=r"^(back:|scale:)"),
            ],
            SCALE_RESULT: [
                CallbackQueryHandler(scale_result_callback),
            ],
            # ── Pregnancy safety ───────────────────────────────────────────────
            PREG_DRUG: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, preg_drug_message),
                CallbackQueryHandler(preg_result_callback, pattern=r"^back:"),
            ],
            PREG_RESULT: [
                CallbackQueryHandler(preg_result_callback),
            ],
            # ── Withdrawal guide ───────────────────────────────────────────────
            WITHDRAW_DRUG: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_drug_message),
                CallbackQueryHandler(withdraw_result_callback, pattern=r"^back:"),
            ],
            WITHDRAW_RESULT: [
                CallbackQueryHandler(withdraw_result_callback),
            ],
        },
        fallbacks=[
            CommandHandler("start", start_command),
        ],
        allow_reentry=True,
    )


async def post_init(application: Application) -> None:
    await create_tables()
    logger.info("Database tables created/verified.")


def main() -> None:
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(build_conv_handler())

    logger.info("Bot started. Polling...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
