"""Quiz handlers."""

import random
from telegram import Update
from telegram.ext import ContextTypes

from states import QUIZ_MENU, QUIZ_CATEGORY, QUIZ_DIFFICULTY, QUIZ_QUESTION, QUIZ_NEXT, MAIN_MENU
from keyboards.menus import (
    quiz_menu_keyboard, quiz_category_keyboard, quiz_difficulty_keyboard,
    quiz_answer_keyboard, quiz_next_keyboard, main_menu_keyboard,
)
from data.quiz_questions import CATEGORIES, get_filtered_questions
from db.queries import record_quiz_answer, get_user_stats


async def show_quiz_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "📝 *Тест по психофармакологии*\n\nПроверьте свои знания!",
        parse_mode="Markdown",
        reply_markup=quiz_menu_keyboard(),
    )
    return QUIZ_MENU


async def quiz_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "quiz:start":
        await query.edit_message_text(
            "Выберите *категорию* вопросов:",
            parse_mode="Markdown",
            reply_markup=quiz_category_keyboard(CATEGORIES),
        )
        return QUIZ_CATEGORY

    if data == "quiz:stats":
        stats = await get_user_stats(query.from_user.id)
        text = _format_quiz_stats(stats)
        await query.edit_message_text(text, parse_mode="Markdown")
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        return MAIN_MENU

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        await query.message.delete()
        return MAIN_MENU

    return QUIZ_MENU


async def quiz_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("qcat:"):
        category = data[len("qcat:"):]
        context.user_data["quiz_category"] = category if category != "all" else None
        await query.edit_message_text(
            "Выберите *уровень сложности*:",
            parse_mode="Markdown",
            reply_markup=quiz_difficulty_keyboard(),
        )
        return QUIZ_DIFFICULTY

    if data == "back:quiz_menu":
        await query.edit_message_text(
            "📝 *Тест по психофармакологии*",
            parse_mode="Markdown",
            reply_markup=quiz_menu_keyboard(),
        )
        return QUIZ_MENU

    return QUIZ_CATEGORY


async def quiz_difficulty_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("qdiff:"):
        difficulty = data[len("qdiff:"):]
        context.user_data["quiz_difficulty"] = difficulty if difficulty != "all" else None

        category = context.user_data.get("quiz_category")
        diff = context.user_data.get("quiz_difficulty")
        questions = get_filtered_questions(category=category, difficulty=diff)

        if not questions:
            await query.edit_message_text(
                "По выбранным фильтрам нет вопросов. Попробуйте другую комбинацию.",
                reply_markup=quiz_difficulty_keyboard(),
            )
            return QUIZ_DIFFICULTY

        random.shuffle(questions)
        context.user_data["quiz_questions"] = questions
        context.user_data["quiz_index"] = 0
        context.user_data["quiz_score"] = 0

        return await _send_question(query, context)

    if data == "back:quiz_category":
        await query.edit_message_text(
            "Выберите категорию:",
            reply_markup=quiz_category_keyboard(CATEGORIES),
        )
        return QUIZ_CATEGORY

    return QUIZ_DIFFICULTY


async def quiz_answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if not data.startswith("qans:"):
        return QUIZ_QUESTION

    answer_idx = int(data[len("qans:"):])
    questions = context.user_data.get("quiz_questions", [])
    idx = context.user_data.get("quiz_index", 0)

    if idx >= len(questions):
        return QUIZ_NEXT

    question = questions[idx]
    correct = question["correct"]
    is_correct = (answer_idx == correct)

    if is_correct:
        context.user_data["quiz_score"] = context.user_data.get("quiz_score", 0) + 1
        result_emoji = "✅"
        result_text = "Правильно!"
    else:
        result_emoji = "❌"
        correct_option = question["options"][correct]
        result_text = f"Неправильно. Правильный ответ: *{correct_option}*"

    await record_quiz_answer(query.from_user.id, question["category"], is_correct)

    text = (
        f"{result_emoji} {result_text}\n\n"
        f"💬 *Пояснение:*\n{question['explanation']}\n\n"
        f"📊 Счёт: {context.user_data['quiz_score']}/{idx + 1}"
    )
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=quiz_next_keyboard(),
    )

    context.user_data["quiz_index"] = idx + 1
    return QUIZ_NEXT


async def quiz_next_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "quiz:next":
        return await _send_question(query, context)

    if data == "quiz:finish":
        return await _finish_quiz(query, context)

    return QUIZ_NEXT


async def _send_question(query, context: ContextTypes.DEFAULT_TYPE) -> int:
    questions = context.user_data.get("quiz_questions", [])
    idx = context.user_data.get("quiz_index", 0)

    if idx >= len(questions):
        return await _finish_quiz(query, context)

    question = questions[idx]
    diff_map = {"easy": "🟢 Лёгкий", "medium": "🟡 Средний", "hard": "🔴 Сложный"}
    difficulty_label = diff_map.get(question["difficulty"], question["difficulty"])

    text = (
        f"❓ *Вопрос {idx + 1}/{len(questions)}*\n"
        f"Категория: {question['category']} | {difficulty_label}\n\n"
        f"{question['question']}"
    )

    edit_fn = getattr(query, "edit_message_text", None)
    if edit_fn:
        await edit_fn(
            text,
            parse_mode="Markdown",
            reply_markup=quiz_answer_keyboard(question["options"]),
        )
    else:
        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=quiz_answer_keyboard(question["options"]),
        )

    return QUIZ_QUESTION


async def _finish_quiz(query, context: ContextTypes.DEFAULT_TYPE) -> int:
    questions = context.user_data.get("quiz_questions", [])
    score = context.user_data.get("quiz_score", 0)
    total = context.user_data.get("quiz_index", len(questions))

    pct = round(score / total * 100) if total > 0 else 0
    if pct >= 80:
        grade = "🏆 Отлично!"
    elif pct >= 60:
        grade = "👍 Хороший результат"
    elif pct >= 40:
        grade = "📚 Нужно повторить"
    else:
        grade = "💪 Продолжайте учиться!"

    text = (
        f"🏁 *Тест завершён!*\n\n"
        f"Правильных ответов: *{score}/{total}* ({pct}%)\n"
        f"{grade}"
    )
    await query.edit_message_text(text, parse_mode="Markdown")
    await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())

    context.user_data.pop("quiz_questions", None)
    context.user_data.pop("quiz_index", None)
    context.user_data.pop("quiz_score", None)
    return MAIN_MENU


def _format_quiz_stats(stats: dict) -> str:
    lines = [
        "📊 *Ваша статистика*\n",
        f"Всего ответов: *{stats['total_questions']}*",
        f"Правильных: *{stats['correct_answers']}* ({stats['accuracy']}%)\n",
    ]
    if stats["categories"]:
        lines.append("*По категориям:*")
        for cat in stats["categories"]:
            cat_pct = round(cat["correct"] / cat["total"] * 100) if cat["total"] else 0
            lines.append(f"  • {cat['category']}: {cat['correct']}/{cat['total']} ({cat_pct}%)")
    else:
        lines.append("Вы ещё не проходили тесты.")
    return "\n".join(lines)
