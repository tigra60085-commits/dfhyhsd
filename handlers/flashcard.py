"""Flashcard handlers."""

import random
from telegram import Update
from telegram.ext import ContextTypes

from states import FLASHCARD_CATEGORY, FLASHCARD_SHOW, FLASHCARD_RATE, MAIN_MENU
from keyboards.menus import (
    flashcard_category_keyboard, flashcard_show_keyboard,
    flashcard_rate_keyboard, main_menu_keyboard,
)
from data.drugs import DRUG_CLASSES, get_drugs_by_class, DRUGS
from db.queries import rate_flashcard, update_progress


async def show_flashcard_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "🃏 *Карточки*\n\nВыберите класс препаратов для изучения:",
        parse_mode="Markdown",
        reply_markup=flashcard_category_keyboard(DRUG_CLASSES),
    )
    return FLASHCARD_CATEGORY


async def flashcard_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        await query.message.delete()
        return MAIN_MENU

    if data.startswith("fccat:"):
        category = data[len("fccat:"):]
        if category == "all":
            drugs = list(DRUGS)
        else:
            drug_class = DRUG_CLASSES[int(category)]
            drugs = get_drugs_by_class(drug_class)

        if not drugs:
            await query.edit_message_text("Нет препаратов в этой категории.")
            return FLASHCARD_CATEGORY

        random.shuffle(drugs)
        context.user_data["fc_drugs"] = [d["name"] for d in drugs]
        context.user_data["fc_index"] = 0

        return await _show_card_front(query, context)

    return FLASHCARD_CATEGORY


async def flashcard_show_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "fc:reveal":
        return await _show_card_back(query, context)

    if data == "fc:skip":
        context.user_data["fc_index"] = context.user_data.get("fc_index", 0) + 1
        return await _show_card_front(query, context)

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        await query.message.delete()
        return MAIN_MENU

    return FLASHCARD_SHOW


async def flashcard_rate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("fcrate:"):
        rating = data[len("fcrate:"):]
        drugs = context.user_data.get("fc_drugs", [])
        idx = context.user_data.get("fc_index", 0)

        if idx < len(drugs):
            drug_name = drugs[idx]
            await rate_flashcard(query.from_user.id, drug_name, rating)
            await update_progress(query.from_user.id, f"flashcard:{drug_name}")

        context.user_data["fc_index"] = idx + 1
        return await _show_card_front(query, context)

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        await query.message.delete()
        return MAIN_MENU

    return FLASHCARD_RATE


async def _show_card_front(query, context: ContextTypes.DEFAULT_TYPE) -> int:
    from data.drugs import get_drug_by_name
    drugs = context.user_data.get("fc_drugs", [])
    idx = context.user_data.get("fc_index", 0)

    if idx >= len(drugs):
        await query.edit_message_text("🎉 Вы прошли все карточки!\n\nОтличная работа!")
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        return MAIN_MENU

    drug_name = drugs[idx]
    drug = get_drug_by_name(drug_name)
    if not drug:
        context.user_data["fc_index"] = idx + 1
        return await _show_card_front(query, context)

    text = (
        f"🃏 *Карточка {idx + 1}/{len(drugs)}*\n\n"
        f"Препарат: *{drug['name']}*\n"
        f"Класс: {drug['class']}\n\n"
        f"_Что вы знаете об этом препарате? Нажмите «Показать ответ»._"
    )
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=flashcard_show_keyboard(),
    )
    return FLASHCARD_SHOW


async def _show_card_back(query, context: ContextTypes.DEFAULT_TYPE) -> int:
    from data.drugs import get_drug_by_name
    drugs = context.user_data.get("fc_drugs", [])
    idx = context.user_data.get("fc_index", 0)

    if idx >= len(drugs):
        return FLASHCARD_SHOW

    drug_name = drugs[idx]
    drug = get_drug_by_name(drug_name)
    if not drug:
        return FLASHCARD_SHOW

    indications = " / ".join(drug["indications"][:3])
    main_se = " / ".join(drug["side_effects"][:3])

    text = (
        f"🃏 *{drug['name']}* ({drug['class']})\n\n"
        f"*Механизм:*\n{drug['mechanism']}\n\n"
        f"*Ключевые показания:*\n{indications}\n\n"
        f"*Основные побочные эффекты:*\n{main_se}\n\n"
        f"*Дозировка:* {drug['dosage']}\n\n"
        f"_Оцените, насколько хорошо вы знали этот препарат:_"
    )
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=flashcard_rate_keyboard(),
    )
    return FLASHCARD_RATE
