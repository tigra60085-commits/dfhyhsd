import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot_data.db")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан! Укажите токен в файле .env")
