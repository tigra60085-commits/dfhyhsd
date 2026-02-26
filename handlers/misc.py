"""Miscellaneous handlers: neurotransmitters, glossary, tips, drug class comparison."""

import random
from telegram import Update
from telegram.ext import ContextTypes

from states import (
    NT_SELECT, GLOSSARY_BROWSE, TIP_VIEW, COMPARE_SELECT1, COMPARE_SELECT2, MAIN_MENU
)
from keyboards.menus import (
    nt_select_keyboard, nt_detail_keyboard,
    glossary_keyboard, glossary_term_keyboard,
    compare_select_keyboard, compare_result_keyboard,
    main_menu_keyboard,
)
from data.neurotransmitters import NEUROTRANSMITTERS, NT_NAMES
from data.glossary import GLOSSARY, GLOSSARY_TERMS
from data.tips import TIPS
from data.drugs import DRUG_CLASSES, get_drugs_by_class


# ─── Neurotransmitters ────────────────────────────────────────────────────────

async def show_nt_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.effective_message.reply_text(
        "🧠 *Нейромедиаторные системы*\n\nВыберите систему для изучения:",
        parse_mode="Markdown",
        reply_markup=nt_select_keyboard(NT_NAMES),
    )
    return NT_SELECT


async def nt_select_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())

        return MAIN_MENU

    if data.startswith("nt:"):
        nt_name = data[len("nt:"):]
        nt = NEUROTRANSMITTERS.get(nt_name)
        if not nt:
            await query.edit_message_text("Нейромедиатор не найден.")
            return NT_SELECT

        text = _format_nt(nt_name, nt)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=nt_detail_keyboard(),
        )
        return NT_SELECT

    if data == "back:nt_select":
        await query.edit_message_text(
            "🧠 Выберите нейромедиаторную систему:",
            reply_markup=nt_select_keyboard(NT_NAMES),
        )
        return NT_SELECT

    return NT_SELECT


def _format_nt(name: str, nt: dict) -> str:
    lines = [f"🧠 *{nt['full_name']}*\n"]
    lines.append(f"*Синтез:*\n{nt['synthesis']}\n")
    lines.append(f"*Деградация:*\n{nt['degradation']}\n")
    lines.append(f"*Рецепторы:*\n{nt['receptors']}\n")
    lines.append("*Пути:*")
    for path in nt["pathways"]:
        lines.append(f"  • {path}")
    lines.append(f"\n*Клиническое значение:*\n{nt['clinical_relevance']}\n")
    lines.append("*Связанные препараты:*")
    for drug in nt["related_drugs"]:
        lines.append(f"  • {drug}")
    return "\n".join(lines)


# ─── Glossary ─────────────────────────────────────────────────────────────────

async def show_glossary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["glossary_page"] = 0
    await update.effective_message.reply_text(
        "📖 *Глоссарий психофармакологии*\n\nВыберите термин:",
        parse_mode="Markdown",
        reply_markup=glossary_keyboard(GLOSSARY_TERMS, page=0),
    )
    return GLOSSARY_BROWSE


async def glossary_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())

        return MAIN_MENU

    if data == "back:glossary":
        page = context.user_data.get("glossary_page", 0)
        await query.edit_message_text(
            "📖 *Глоссарий* — выберите термин:",
            parse_mode="Markdown",
            reply_markup=glossary_keyboard(GLOSSARY_TERMS, page=page),
        )
        return GLOSSARY_BROWSE

    if data.startswith("gpage:"):
        page = int(data[len("gpage:"):])
        context.user_data["glossary_page"] = page
        await query.edit_message_text(
            "📖 *Глоссарий* — выберите термин:",
            parse_mode="Markdown",
            reply_markup=glossary_keyboard(GLOSSARY_TERMS, page=page),
        )
        return GLOSSARY_BROWSE

    if data.startswith("gterm:"):
        term = data[len("gterm:"):]
        definition = GLOSSARY.get(term)
        if not definition:
            await query.edit_message_text("Термин не найден.")
            return GLOSSARY_BROWSE

        text = f"📖 *{term}*\n\n{definition}"
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=glossary_term_keyboard(),
        )
        return GLOSSARY_BROWSE

    if data == "noop":
        return GLOSSARY_BROWSE

    return GLOSSARY_BROWSE


# ─── Tips ─────────────────────────────────────────────────────────────────────

async def show_tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    from keyboards.menus import back_keyboard
    tip = random.choice(TIPS)
    await update.effective_message.reply_text(
        f"💡 *Совет дня*\n\n{tip}",
        parse_mode="Markdown",
        reply_markup=back_keyboard("back:main"),
    )
    return TIP_VIEW


async def tip_back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if query.data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())

    return MAIN_MENU


# ─── Drug class comparison ────────────────────────────────────────────────────

async def show_compare_select1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "⚖️ *Сравнение классов*\n\nВыберите *первый* класс препаратов:",
        parse_mode="Markdown",
        reply_markup=compare_select_keyboard(DRUG_CLASSES, step=1),
    )
    return COMPARE_SELECT1


async def compare_select1_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())

        return MAIN_MENU

    if data.startswith("cmp1:"):
        class1 = DRUG_CLASSES[int(data[len("cmp1:"):])]
        context.user_data["compare_class1"] = class1
        await query.edit_message_text(
            f"Первый класс: *{class1}*\n\nВыберите *второй* класс:",
            parse_mode="Markdown",
            reply_markup=compare_select_keyboard(DRUG_CLASSES, step=2),
        )
        return COMPARE_SELECT2

    return COMPARE_SELECT1


async def compare_select2_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())

        return MAIN_MENU

    if data == "cmp:again":
        await query.edit_message_text(
            "⚖️ Выберите *первый* класс препаратов:",
            parse_mode="Markdown",
            reply_markup=compare_select_keyboard(DRUG_CLASSES, step=1),
        )
        return COMPARE_SELECT1

    if data.startswith("cmp2:"):
        class2 = DRUG_CLASSES[int(data[len("cmp2:"):])]
        class1 = context.user_data.get("compare_class1", "")

        drugs1 = get_drugs_by_class(class1)
        drugs2 = get_drugs_by_class(class2)

        text = _format_comparison(class1, drugs1, class2, drugs2)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=compare_result_keyboard(),
        )
        return COMPARE_SELECT2

    return COMPARE_SELECT2


def _format_comparison(class1: str, drugs1: list, class2: str, drugs2: list) -> str:
    lines = [f"⚖️ *{class1}* vs *{class2}*\n"]

    lines.append(f"*── {class1} ──*")
    if drugs1:
        for drug in drugs1:
            lines.append(f"• *{drug['name']}*")
            lines.append(f"  _{drug['mechanism'][:100]}..._" if len(drug['mechanism']) > 100
                         else f"  _{drug['mechanism']}_")
            lines.append(f"  Показания: {', '.join(drug['indications'][:2])}")
    else:
        lines.append("_Нет данных_")

    lines.append(f"\n*── {class2} ──*")
    if drugs2:
        for drug in drugs2:
            lines.append(f"• *{drug['name']}*")
            lines.append(f"  _{drug['mechanism'][:100]}..._" if len(drug['mechanism']) > 100
                         else f"  _{drug['mechanism']}_")
            lines.append(f"  Показания: {', '.join(drug['indications'][:2])}")
    else:
        lines.append("_Нет данных_")

    return "\n".join(lines)
