"""Simple in-memory per-user rate limiter."""

import time
from collections import defaultdict
from functools import wraps

# Sliding-window counters: {user_id: [timestamp, ...]}
_WINDOWS: dict[int, list[float]] = defaultdict(list)

# Default: 30 actions per 60 seconds per user
_LIMIT = 30
_WINDOW = 60.0


def rate_limited(func):
    """Decorator: silently drop the update if the user exceeds the rate limit."""
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        if user is None:
            return await func(update, context, *args, **kwargs)

        uid = user.id
        now = time.monotonic()
        window = _WINDOWS[uid]

        # Remove timestamps outside the sliding window
        _WINDOWS[uid] = [t for t in window if now - t < _WINDOW]
        window = _WINDOWS[uid]

        if len(window) >= _LIMIT:
            # Silently ignore the request; optionally warn the user once
            if update.callback_query:
                await update.callback_query.answer(
                    "Слишком много запросов — пожалуйста, подождите немного.", show_alert=False
                )
            elif update.message:
                await update.message.reply_text(
                    "Слишком много запросов за короткое время. Пожалуйста, подождите."
                )
            return None

        _WINDOWS[uid].append(now)
        return await func(update, context, *args, **kwargs)

    return wrapper
