"""Drug interaction checker handlers."""

from telegram import Update
from telegram.ext import ContextTypes

from states import INTER_DRUG1, INTER_DRUG2, INTER_RESULT, MAIN_MENU
from keyboards.menus import interaction_result_keyboard, main_menu_keyboard, back_keyboard
from handlers.rate_limiter import rate_limited
from data.interactions import find_interaction


SEVERITY_LABELS = {
    "severe": "🔴 Серьёзное",
    "moderate": "🟡 Умеренное",
    "mild": "🟢 Незначительное",
}


async def ask_drug1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_message.reply_text(
        "⚠️ *Проверка взаимодействий*\n\n"
        "Введите название *первого препарата* (на русском или латинском):",
        parse_mode="Markdown",
        reply_markup=back_keyboard("back:main"),
    )
    return INTER_DRUG1


@rate_limited
async def inter_drug1_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    drug1 = update.message.text.strip()
    if not drug1:
        await update.message.reply_text("Пожалуйста, введите название препарата.")
        return INTER_DRUG1

    context.user_data["inter_drug1"] = drug1
    await update.message.reply_text(
        f"Первый препарат: *{drug1}*\n\n"
        f"Теперь введите название *второго препарата*:",
        parse_mode="Markdown",
        reply_markup=back_keyboard("back:main"),
    )
    return INTER_DRUG2


@rate_limited
async def inter_drug2_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    drug2 = update.message.text.strip()
    if not drug2:
        await update.message.reply_text("Пожалуйста, введите название препарата.")
        return INTER_DRUG2

    drug1 = context.user_data.get("inter_drug1", "")
    interactions = find_interaction(drug1, drug2)

    if not interactions:
        text = (
            f"✅ *Взаимодействия не найдены*\n\n"
            f"Между *{drug1}* и *{drug2}* нет зарегистрированных взаимодействий в базе.\n\n"
            f"⚠️ _База данных неполная — всегда консультируйтесь с актуальными источниками._"
        )
    else:
        lines = [f"⚠️ *Взаимодействия: {drug1} + {drug2}*\n"]
        for inter in interactions:
            severity = SEVERITY_LABELS.get(inter["severity"], inter["severity"])
            lines.append(f"*{severity}*")
            lines.append(inter["description"])
            lines.append("")
        text = "\n".join(lines)

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=interaction_result_keyboard(),
    )
    return INTER_RESULT


async def inter_result_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "inter:again":
        await query.edit_message_text(
            "Введите название *первого препарата*:",
            parse_mode="Markdown",
        )
        return INTER_DRUG1

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        return MAIN_MENU

    return INTER_RESULT
