"""Clinical case handlers."""

from telegram import Update
from telegram.ext import ContextTypes

from states import CASE_LIST, CASE_READ, CASE_QUESTION, CASE_ANSWER, MAIN_MENU
from keyboards.menus import (
    case_list_keyboard, case_start_keyboard,
    case_answer_keyboard, case_next_keyboard, main_menu_keyboard,
)
from data.clinical_cases import CASES, get_case_by_id
from db.queries import update_progress


async def show_case_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_message.reply_text(
        "🏥 *Клинические случаи*\n\nВыберите случай для разбора:",
        parse_mode="Markdown",
        reply_markup=case_list_keyboard(CASES),
    )
    return CASE_LIST


async def case_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        return MAIN_MENU

    if data.startswith("case:"):
        case_id = int(data[len("case:"):])
        case = get_case_by_id(case_id)
        if not case:
            await query.edit_message_text("Случай не найден.")
            return CASE_LIST

        context.user_data["current_case_id"] = case_id
        text = (
            f"🏥 *Случай #{case['id']}: {case['title']}*\n\n"
            f"{case['presentation']}"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=case_start_keyboard(case_id),
        )
        return CASE_READ

    return CASE_LIST


async def case_read_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:case_list":
        await query.edit_message_text(
            "🏥 Выберите клинический случай:",
            reply_markup=case_list_keyboard(CASES),
        )
        return CASE_LIST

    if data.startswith("caseq:"):
        case_id = int(data[len("caseq:"):])
        case = get_case_by_id(case_id)
        if not case:
            return CASE_READ

        labels = ["А", "Б", "В", "Г"]
        options_text = "\n".join(
            f"{labels[i] if i < len(labels) else i+1}. {opt}"
            for i, opt in enumerate(case["options"])
        )
        text = (
            f"❓ *Вопрос:*\n{case['question']}\n\n"
            f"{options_text}"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=case_answer_keyboard(case["options"]),
        )
        return CASE_QUESTION

    return CASE_READ


async def case_question_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if not data.startswith("caseans:"):
        return CASE_QUESTION

    answer_idx = int(data[len("caseans:"):])
    case_id = context.user_data.get("current_case_id")
    case = get_case_by_id(case_id)

    if not case:
        return CASE_QUESTION

    correct = case["correct"]
    is_correct = (answer_idx == correct)

    if is_correct:
        result = "✅ *Правильно!*"
    else:
        correct_option = case["options"][correct]
        result = f"❌ *Неправильно.* Правильный ответ: *{correct_option}*"

    text = (
        f"{result}\n\n"
        f"💬 *Разбор:*\n{case['explanation']}"
    )
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=case_next_keyboard(),
    )

    await update_progress(query.from_user.id, f"case:{case_id}")
    return CASE_ANSWER


async def case_answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:case_list":
        await query.edit_message_text(
            "🏥 Выберите клинический случай:",
            reply_markup=case_list_keyboard(CASES),
        )
        return CASE_LIST

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        return MAIN_MENU

    return CASE_ANSWER
