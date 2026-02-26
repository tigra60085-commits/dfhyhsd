"""Admin command handlers (/admin_stats, /admin_reload)."""

import logging
import os

from telegram import Update
from telegram.ext import ContextTypes

from db.queries import get_admin_stats

logger = logging.getLogger(__name__)

# Comma-separated admin user IDs from environment (optional)
_ADMIN_IDS_RAW = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: set[int] = set()
for _part in _ADMIN_IDS_RAW.split(","):
    _part = _part.strip()
    if _part.isdigit():
        ADMIN_IDS.add(int(_part))


def _is_admin(user_id: int) -> bool:
    """Return True only if user_id is explicitly listed in ADMIN_IDS."""
    return bool(ADMIN_IDS) and user_id in ADMIN_IDS


async def admin_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send bot usage statistics to admins."""
    user = update.effective_user
    if not _is_admin(user.id):
        await update.message.reply_text("Нет доступа.")
        return

    try:
        stats = await get_admin_stats()
        text = (
            "📊 *Статистика бота*\n\n"
            f"👥 Пользователей всего: *{stats['total_users']}*\n"
            f"🆕 Новых за 7 дней: *{stats['new_users_7d']}*\n"
            f"🔥 Активны сегодня: *{stats['active_today']}*\n"
            f"📝 Вопросов отвечено: *{stats['total_questions']}*\n"
        )
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        logger.error("admin_stats error: %s", e)
        await update.message.reply_text(f"Ошибка при получении статистики: {e}")


async def admin_reload_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Placeholder reload command — confirms data is loaded fresh on each request."""
    user = update.effective_user
    if not _is_admin(user.id):
        await update.message.reply_text("Нет доступа.")
        return

    # Data is loaded from module-level dicts, so a 'reload' means nothing at runtime
    # without a full restart. We confirm the current state instead.
    from data.drugs import DRUGS, DRUG_CLASSES
    from data.clinical_cases import CASES
    from data.interactions import INTERACTIONS

    text = (
        "✅ *Данные актуальны*\n\n"
        f"💊 Препаратов: *{len(DRUGS)}*\n"
        f"🗂 Классов: *{len(DRUG_CLASSES)}*\n"
        f"⚠️ Взаимодействий: *{len(INTERACTIONS)}*\n"
        f"🏥 Клинических случаев: *{len(CASES)}*\n\n"
        "_(Для применения изменений данных требуется перезапуск бота)_"
    )
    await update.message.reply_text(text, parse_mode="Markdown")
