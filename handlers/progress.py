"""User progress handler."""

from telegram import Update
from telegram.ext import ContextTypes

from states import PROGRESS_VIEW, MAIN_MENU
from keyboards.menus import main_menu_keyboard, back_keyboard
from db.queries import get_user_stats, get_streak, touch_streak


async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    stats = await get_user_stats(user_id)
    streak = await touch_streak(user_id)

    lines = ["📊 *Ваш прогресс*\n"]

    # Streak block
    current = streak["current_streak"]
    longest = streak["longest_streak"]
    fire = "🔥" * min(current, 5) if current > 0 else ""
    lines.append(f"*Стрик активности:* {fire} {current} {'день' if current == 1 else 'дней'}")
    if longest > current:
        lines.append(f"  _Рекорд: {longest} дней_")
    lines.append("")

    # Quiz statistics
    total = stats["total_questions"]
    correct = stats["correct_answers"]
    accuracy = stats["accuracy"]

    if total > 0:
        lines.append(f"*📝 Тесты:*")
        lines.append(f"  Всего ответов: {total}")
        lines.append(f"  Правильных: {correct} ({accuracy}%)")

        if stats["categories"]:
            lines.append("\n  *По категориям:*")
            for cat in stats["categories"]:
                cat_pct = round(cat["correct"] / cat["total"] * 100) if cat["total"] else 0
                lines.append(f"    • {cat['category']}: {cat['correct']}/{cat['total']} ({cat_pct}%)")
    else:
        lines.append("*📝 Тесты:* _ещё не проходили_")

    # Flashcard ratings
    ratings = stats.get("flashcard_ratings", {})
    if ratings:
        total_fc = sum(ratings.values())
        lines.append(f"\n*🃏 Карточки:*")
        lines.append(f"  Оценено карточек: {total_fc}")
        if "easy" in ratings:
            lines.append(f"  😊 Легко: {ratings['easy']}")
        if "medium" in ratings:
            lines.append(f"  🤔 Средне: {ratings['medium']}")
        if "hard" in ratings:
            lines.append(f"  😓 Сложно: {ratings['hard']}")
    else:
        lines.append("\n*🃏 Карточки:* _ещё не изучали_")

    # Sections visited
    sections = stats.get("sections", [])
    if sections:
        lines.append(f"\n*📚 Изученные разделы:*")
        for s in sections[:5]:
            section_name = s["section"].replace("drug:", "Препарат: ").replace(
                "case:", "Случай #").replace("flashcard:", "Карточка: ")
            lines.append(f"  • {section_name} (×{s['completed_count']})")
        if len(sections) > 5:
            lines.append(f"  _...и ещё {len(sections) - 5} разделов_")
    else:
        lines.append("\n*📚 Разделы:* _ещё не изучали_")

    text = "\n".join(lines)
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=back_keyboard("back:main"),
    )
    return PROGRESS_VIEW


async def progress_back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if query.data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        await query.message.delete()
    return MAIN_MENU
