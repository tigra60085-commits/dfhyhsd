"""Keyboard factory functions for the psychopharmacology bot."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton("💊 Препараты"), KeyboardButton("📝 Тест")],
        [KeyboardButton("🃏 Карточки"), KeyboardButton("🏥 Клинические случаи")],
        [KeyboardButton("⚠️ Взаимодействия"), KeyboardButton("🔍 Поиск")],
        [KeyboardButton("🧠 Нейромедиаторы"), KeyboardButton("📊 Мой прогресс")],
        [KeyboardButton("📖 Глоссарий"), KeyboardButton("💡 Совет дня")],
        [KeyboardButton("🔬 Фарма-анализ"), KeyboardButton("🎙️ Подкаст")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def drug_class_keyboard(classes: list) -> InlineKeyboardMarkup:
    buttons = []
    for drug_class in classes:
        buttons.append([InlineKeyboardButton(drug_class, callback_data=f"class:{drug_class}")])
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(buttons)


def drug_list_keyboard(drugs: list, drug_class: str) -> InlineKeyboardMarkup:
    buttons = []
    for drug in drugs:
        buttons.append([InlineKeyboardButton(drug["name"], callback_data=f"drug:{drug['name']}")])
    buttons.append([InlineKeyboardButton("⬅️ Назад к классам", callback_data="back:class_select")])
    return InlineKeyboardMarkup(buttons)


def drug_detail_keyboard(drug_name: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("⬅️ Назад к списку", callback_data="back:drug_list")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def quiz_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("▶️ Начать тест", callback_data="quiz:start")],
        [InlineKeyboardButton("📊 Моя статистика", callback_data="quiz:stats")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def quiz_category_keyboard(categories: list) -> InlineKeyboardMarkup:
    buttons = []
    for cat in categories:
        buttons.append([InlineKeyboardButton(cat, callback_data=f"qcat:{cat}")])
    buttons.append([InlineKeyboardButton("🔀 Все категории", callback_data="qcat:all")])
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="back:quiz_menu")])
    return InlineKeyboardMarkup(buttons)


def quiz_difficulty_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🟢 Лёгкий", callback_data="qdiff:easy")],
        [InlineKeyboardButton("🟡 Средний", callback_data="qdiff:medium")],
        [InlineKeyboardButton("🔴 Сложный", callback_data="qdiff:hard")],
        [InlineKeyboardButton("🔀 Все уровни", callback_data="qdiff:all")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back:quiz_category")],
    ]
    return InlineKeyboardMarkup(buttons)


def quiz_answer_keyboard(options: list) -> InlineKeyboardMarkup:
    labels = ["А", "Б", "В", "Г"]
    buttons = []
    for i, option in enumerate(options):
        label = labels[i] if i < len(labels) else str(i + 1)
        buttons.append([InlineKeyboardButton(f"{label}. {option}", callback_data=f"qans:{i}")])
    return InlineKeyboardMarkup(buttons)


def quiz_next_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("▶️ Следующий вопрос", callback_data="quiz:next")],
        [InlineKeyboardButton("⏹ Завершить тест", callback_data="quiz:finish")],
    ]
    return InlineKeyboardMarkup(buttons)


def flashcard_category_keyboard(classes: list) -> InlineKeyboardMarkup:
    buttons = []
    for drug_class in classes:
        buttons.append([InlineKeyboardButton(drug_class, callback_data=f"fccat:{drug_class}")])
    buttons.append([InlineKeyboardButton("🔀 Все карточки", callback_data="fccat:all")])
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(buttons)


def flashcard_show_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("👁 Показать ответ", callback_data="fc:reveal")],
        [InlineKeyboardButton("⏭ Пропустить", callback_data="fc:skip")],
        [InlineKeyboardButton("⏹ Выйти", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def flashcard_rate_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("😊 Легко", callback_data="fcrate:easy"),
            InlineKeyboardButton("🤔 Средне", callback_data="fcrate:medium"),
            InlineKeyboardButton("😓 Сложно", callback_data="fcrate:hard"),
        ],
        [InlineKeyboardButton("⏹ Выйти", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def case_list_keyboard(cases: list) -> InlineKeyboardMarkup:
    buttons = []
    for case in cases:
        buttons.append([InlineKeyboardButton(
            f"#{case['id']} {case['title']}",
            callback_data=f"case:{case['id']}"
        )])
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(buttons)


def case_start_keyboard(case_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("▶️ Перейти к вопросу", callback_data=f"caseq:{case_id}")],
        [InlineKeyboardButton("⬅️ К списку случаев", callback_data="back:case_list")],
    ]
    return InlineKeyboardMarkup(buttons)


def case_answer_keyboard(options: list) -> InlineKeyboardMarkup:
    labels = ["А", "Б", "В", "Г"]
    buttons = []
    for i, option in enumerate(options):
        label = labels[i] if i < len(labels) else str(i + 1)
        buttons.append([InlineKeyboardButton(f"{label}. {option}", callback_data=f"caseans:{i}")])
    return InlineKeyboardMarkup(buttons)


def case_next_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("📋 К списку случаев", callback_data="back:case_list")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def interaction_result_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🔄 Проверить другую пару", callback_data="inter:again")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def search_result_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🔄 Новый поиск", callback_data="search:again")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def nt_select_keyboard(nt_names: list) -> InlineKeyboardMarkup:
    buttons = []
    for name in nt_names:
        buttons.append([InlineKeyboardButton(name, callback_data=f"nt:{name}")])
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(buttons)


def nt_detail_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("⬅️ К нейромедиаторам", callback_data="back:nt_select")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def glossary_keyboard(terms: list, page: int = 0, page_size: int = 8) -> InlineKeyboardMarkup:
    total_pages = (len(terms) + page_size - 1) // page_size
    page_terms = terms[page * page_size: (page + 1) * page_size]

    buttons = []
    for term in page_terms:
        short = term[:30] + "…" if len(term) > 30 else term
        buttons.append([InlineKeyboardButton(short, callback_data=f"gterm:{term}")])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("◀️", callback_data=f"gpage:{page - 1}"))
    nav.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton("▶️", callback_data=f"gpage:{page + 1}"))
    if nav:
        buttons.append(nav)

    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(buttons)


def glossary_term_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("⬅️ К глоссарию", callback_data="back:glossary")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def compare_select_keyboard(classes: list, step: int = 1) -> InlineKeyboardMarkup:
    buttons = []
    for drug_class in classes:
        buttons.append([InlineKeyboardButton(drug_class, callback_data=f"cmp{step}:{drug_class}")])
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(buttons)


def compare_result_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🔄 Новое сравнение", callback_data="cmp:again")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def back_keyboard(callback_data: str = "back:main") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data=callback_data)]])


# ─── Pharma-compare keyboards ─────────────────────────────────────────────────

PHARMA_FOCUS_OPTIONS = [
    ("🏥 Общий обзор", "Общий обзор"),
    ("👴 Безопасность у пожилых", "Безопасность у пожилых"),
    ("🤰 Беременность и лактация", "Беременность и лактация"),
    ("⚖️ Метаболический профиль", "Метаболический профиль"),
    ("❤️ Кардиологическая безопасность", "Кардиологическая безопасность"),
    ("⚠️ Взаимодействия", "Взаимодействия"),
    ("💊 Комплаентность", "Комплаентность"),
]


def pharma_compare_focus_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(label, callback_data=f"pcfocus:{val}")]
               for label, val in PHARMA_FOCUS_OPTIONS]
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(buttons)


def pharma_compare_audience_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🎓 Ординатор", callback_data="pcaud:resident")],
        [InlineKeyboardButton("🔬 Специалист", callback_data="pcaud:specialist")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def pharma_compare_result_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🔄 Новый анализ", callback_data="pc:again")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ─── Podcast-dialog keyboards ─────────────────────────────────────────────────

def podcast_duration_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("⏱ ~15 мин (short)", callback_data="pdur:short")],
        [InlineKeyboardButton("⏱ ~30 мин (medium)", callback_data="pdur:medium")],
        [InlineKeyboardButton("⏱ ~45 мин (long)", callback_data="pdur:long")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)


def podcast_result_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🎙️ Новый эпизод", callback_data="pd:again")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(buttons)
