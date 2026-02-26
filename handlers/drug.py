"""Drug browsing handlers."""

import html
from telegram import Update
from telegram.ext import ContextTypes

from states import DRUG_CLASS_SELECT, DRUG_LIST, DRUG_DETAIL, MAIN_MENU
from keyboards.menus import (
    drug_class_keyboard, drug_list_keyboard, drug_detail_keyboard, main_menu_keyboard
)
from data.drugs import DRUG_CLASSES, get_drugs_by_class, get_drug_by_name
from db.queries import update_progress


async def show_drug_classes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_message.reply_text(
        "💊 *Справочник препаратов*\n\nВыберите фармакологический класс:",
        parse_mode="Markdown",
        reply_markup=drug_class_keyboard(DRUG_CLASSES),
    )
    return DRUG_CLASS_SELECT


async def drug_class_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data  # "class:<name>" or "back:main"

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        return MAIN_MENU

    if data.startswith("class:"):
        idx = int(data[len("class:"):])
        drug_class = DRUG_CLASSES[idx]
        drugs = get_drugs_by_class(drug_class)
        context.user_data["current_class"] = drug_class

        if not drugs:
            await query.edit_message_text("Препараты не найдены.")
            return DRUG_CLASS_SELECT

        lines = [f"💊 <b>{html.escape(drug_class)}</b> — {len(drugs)} препарат(ов)\n"]
        for d in drugs:
            lines.append(f"• {html.escape(d['name'])}")
        lines.append("\nВыберите препарат для подробной информации:")

        await query.edit_message_text(
            "\n".join(lines),
            parse_mode="HTML",
            reply_markup=drug_list_keyboard(drugs, drug_class),
        )
        return DRUG_LIST

    return DRUG_CLASS_SELECT


async def drug_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:class_select":
        await query.edit_message_text(
            "💊 Выберите фармакологический класс:",
            reply_markup=drug_class_keyboard(DRUG_CLASSES),
        )
        return DRUG_CLASS_SELECT

    if data.startswith("drug:"):
        idx = int(data[len("drug:"):])
        drug_class = context.user_data.get("current_class", "")
        drugs = get_drugs_by_class(drug_class)

        if not drugs or idx >= len(drugs):
            await query.edit_message_text("Препарат не найден.")
            return DRUG_LIST

        drug = drugs[idx]
        drug_name = drug["name"]
        context.user_data["current_drug"] = drug_name

        text = _format_drug_summary(drug)
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=drug_detail_keyboard(drug_name),
        )

        user_id = query.from_user.id
        await update_progress(user_id, f"drug:{drug_name}")
        return DRUG_DETAIL

    return DRUG_LIST


async def drug_detail_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:drug_list":
        drug_class = context.user_data.get("current_class", "")
        drugs = get_drugs_by_class(drug_class)
        if drugs:
            lines = [f"💊 <b>{html.escape(drug_class)}</b>\n"]
            for d in drugs:
                lines.append(f"• {html.escape(d['name'])}")
            await query.edit_message_text(
                "\n".join(lines),
                parse_mode="HTML",
                reply_markup=drug_list_keyboard(drugs, drug_class),
            )
            return DRUG_LIST
        else:
            await query.edit_message_text(
                "Выберите класс:",
                reply_markup=drug_class_keyboard(DRUG_CLASSES),
            )
            return DRUG_CLASS_SELECT

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        return MAIN_MENU

    return DRUG_DETAIL


def _format_drug_summary(drug: dict) -> str:
    name = html.escape(drug["name"])
    drug_class = html.escape(drug["class"])
    mechanism = html.escape(drug["mechanism"])
    dosage = html.escape(drug["dosage"])

    lines = [f"💊 <b>{name}</b> ({drug_class})\n"]
    lines.append(f"<b>Механизм действия:</b>\n{mechanism}\n")

    indications = "\n".join(f"  • {html.escape(i)}" for i in drug["indications"])
    lines.append(f"<b>Показания:</b>\n{indications}\n")

    side_effects = "\n".join(f"  • {html.escape(s)}" for s in drug["side_effects"])
    lines.append(f"<b>Побочные эффекты:</b>\n{side_effects}\n")

    interactions = "\n".join(f"  • {html.escape(i)}" for i in drug["interactions"])
    lines.append(f"<b>Взаимодействия:</b>\n{interactions}\n")

    lines.append(f"<b>Дозировка:</b>\n  {dosage}")
    return "\n".join(lines)
