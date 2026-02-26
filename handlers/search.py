"""Search handler."""

from telegram import Update
from telegram.ext import ContextTypes

from states import SEARCH_INPUT, SEARCH_RESULT, MAIN_MENU
from keyboards.menus import search_result_keyboard, main_menu_keyboard, back_keyboard
from handlers.rate_limiter import rate_limited
from data.drugs import search_drugs, fuzzy_suggest
from data.glossary import GLOSSARY


async def ask_search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "🔍 *Поиск*\n\nВведите название препарата, класс, показание или термин:",
        parse_mode="Markdown",
        reply_markup=back_keyboard("back:main"),
    )
    return SEARCH_INPUT


@rate_limited
async def search_input_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query_text = update.message.text.strip()
    if not query_text:
        await update.message.reply_text("Введите поисковый запрос.")
        return SEARCH_INPUT

    # Search drugs
    drug_results = search_drugs(query_text)

    # Search glossary
    q_lower = query_text.lower()
    glossary_results = [
        (term, definition)
        for term, definition in GLOSSARY.items()
        if q_lower in term.lower() or q_lower in definition.lower()
    ]

    if not drug_results and not glossary_results:
        suggestions = fuzzy_suggest(query_text)
        if suggestions:
            sugg_str = ", ".join(f"*{s}*" for s in suggestions)
            text = (
                f"🔍 По запросу *«{query_text}»* ничего не найдено.\n\n"
                f"Возможно, вы имели в виду: {sugg_str}?"
            )
        else:
            text = (
                f"🔍 По запросу *«{query_text}»* ничего не найдено.\n\n"
                f"Попробуйте другой запрос (например: «флуоксетин», «SSRI», «депрессия»)."
            )
    else:
        lines = [f"🔍 Результаты по запросу *«{query_text}»*\n"]

        if drug_results:
            lines.append(f"*💊 Препараты ({len(drug_results)}):*")
            for drug in drug_results[:5]:
                lines.append(f"  • *{drug['name']}* ({drug['class']})")
                lines.append(f"    _{drug['mechanism'][:80]}..._" if len(drug['mechanism']) > 80
                              else f"    _{drug['mechanism']}_")
            if len(drug_results) > 5:
                lines.append(f"  _...и ещё {len(drug_results) - 5} препарат(ов)_")

        if glossary_results:
            lines.append(f"\n*📖 Глоссарий ({len(glossary_results)}):*")
            for term, definition in glossary_results[:3]:
                short_def = definition[:100] + "..." if len(definition) > 100 else definition
                lines.append(f"  • *{term}*: {short_def}")
            if len(glossary_results) > 3:
                lines.append(f"  _...и ещё {len(glossary_results) - 3} термин(ов)_")

        text = "\n".join(lines)

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=search_result_keyboard(),
    )
    return SEARCH_RESULT


async def search_result_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "search:again":
        await query.edit_message_text(
            "Введите поисковый запрос:",
        )
        return SEARCH_INPUT

    if data == "back:main":
        await query.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard())
        return MAIN_MENU

    return SEARCH_RESULT
