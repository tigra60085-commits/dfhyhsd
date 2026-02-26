# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Telegram bot for learning psychopharmacology. Features: drug reference (browsing by class), quizzes, flashcards, clinical cases, drug interaction checker, search, neurotransmitter system info, glossary, and user progress tracking.

## Setup & Running

```bash
pip install -r requirements.txt
cp .env.example .env
# Set BOT_TOKEN in .env (get from @BotFather on Telegram)
python bot.py
```

The bot requires a valid `BOT_TOKEN` in `.env` — `config.py` will raise a `ValueError` on startup if it's missing.

## Architecture

**Stack:** Python + `python-telegram-bot==20.7` (async) + `aiosqlite` + SQLite

**Entry point:** `bot.py` — registers all handlers and starts polling.

**Conversation flow** is driven by a single `ConversationHandler` with 28 states defined in `states.py` (integers 0–27 via `range(28)`).

**Module layout:**

| Directory | Purpose |
|-----------|---------|
| `config.py` | Loads `BOT_TOKEN` and `DATABASE_PATH` from `.env` |
| `states.py` | All conversation state integer constants |
| `data/` | Static data: drug database, quiz questions, clinical cases, drug interactions, neurotransmitter systems, glossary, tips |
| `db/` | SQLite schema creation and async query helpers (user progress, quiz scores) |
| `keyboards/` | `InlineKeyboardMarkup` / `ReplyKeyboardMarkup` factory functions |
| `handlers/` | One module per feature (start, drug, quiz, flashcard, case, interaction, search, progress, misc) |
| `services/` | Business logic layer (drug service, quiz service, etc.) |

**State groups in `states.py`:**
- `MAIN_MENU` (0)
- Drug browsing: `DRUG_CLASS_SELECT`→`DRUG_LIST`→`DRUG_INFO`→`DRUG_DETAIL`
- Quiz: `QUIZ_MENU`→`QUIZ_CATEGORY`→`QUIZ_DIFFICULTY`→`QUIZ_QUESTION`→`QUIZ_NEXT`
- Flashcards: `FLASHCARD_CATEGORY`→`FLASHCARD_SHOW`→`FLASHCARD_RATE`
- Cases: `CASE_LIST`→`CASE_READ`→`CASE_QUESTION`→`CASE_ANSWER`
- Interactions: `INTER_DRUG1`→`INTER_DRUG2`→`INTER_RESULT`
- Search: `SEARCH_INPUT`→`SEARCH_RESULT`
- Misc: `NT_SELECT`, `GLOSSARY_BROWSE`, `PROGRESS_VIEW`, `TIP_VIEW`, `COMPARE_SELECT1`, `COMPARE_SELECT2`

## Key Conventions

- All handler functions are `async def` (python-telegram-bot v20 async API).
- Database access uses `aiosqlite`; the DB file path comes from `config.DATABASE_PATH`.
- Static content (drugs, quiz questions, etc.) lives in `data/` as plain Python dicts/lists — no external CMS.
- Keyboards are built in `keyboards/menus.py` and imported by handlers; never construct `InlineKeyboardMarkup` inline inside handlers.
- Each handler module returns a state constant from `states.py` to drive the conversation forward.
- Business logic is encapsulated in service classes in `services/` to separate concerns from handlers.
- Custom exceptions are defined in `exceptions.py` for better error handling.
- Caching is implemented using `functools.lru_cache` for static data to improve performance.
