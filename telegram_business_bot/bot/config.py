from dotenv import load_dotenv
import os
from pathlib import Path

# Загрузка .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv("ADMIN_ID"))

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден. Убедись, что файл .env существует и содержит правильный токен.")

if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID не найден. Убедись, что файл .env существует и содержит правильный токен.")



