import asyncio
import nest_asyncio
nest_asyncio.apply()

import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

from bot.config import BOT_TOKEN
from bot.handlers import order
from bot.database import init_db

# 🔐 Настройки webhook
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "v3ryS3cur3T0k3n"  # ⚠️ Только символы [a-zA-Z0-9_-] допустимы!
DOMAIN = "https://vtagsboortj.ru"  # ЗАМЕНИ на свой настоящий домен!
WEBHOOK_URL = f"{DOMAIN}{WEBHOOK_PATH}"

# ⚙️ Настройки сервера
HOST = "0.0.0.0"
PORT = 8000


async def main():
    logging.basicConfig(level=logging.INFO)

    init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    router = Router()

    main_reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Оформить заказ")],
            [KeyboardButton(text="📞 Контакты")],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )

    @router.message(Command("start"))
    async def cmd_start(message: Message):
        await message.answer("Привет! Я бизнес-бот. Чем могу помочь?",
                             reply_markup=main_reply_keyboard)

    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Заказать", callback_data="order")],
        [InlineKeyboardButton(text="📞 Связаться", callback_data="contact")],
        [InlineKeyboardButton(text="❓ Справка", callback_data="help")],
        [InlineKeyboardButton(text="💬 Отзывы", callback_data='reviews')]
    ])

    @router.message(Command("menu"))
    async def cmd_menu(message: Message):
        await message.answer("Выберите действие:", reply_markup=menu_keyboard)

    @router.callback_query(F.data.in_({"order", "contact", "help", "reviews"}))
    async def process_callback(callback: CallbackQuery):
        if callback.data == "order":
            await callback.message.answer("Вы выбрали заказ. Сейчас оформим!")
        elif callback.data == "contact":
            await callback.message.answer("Наш менеджер свяжется с вами.")
        elif callback.data == "help":
            await callback.message.answer("Это тестовый бот. Команды: /start, /menu")
        elif callback.data == 'reviews':
            await callback.message.answer('Вы можете оставить свой отзыв!')
        await callback.answer("Спасибо!", show_alert=True)

    dp.include_router(router)
    dp.include_router(order.router)

    # Удалим старый webhook (если был)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

    # Создаем aiohttp-приложение
    app = web.Application()

    @dp.startup.register
    async def on_startup(dispatcher: Dispatcher):
        print("✅ Бот запущен")

    @dp.shutdown.register
    async def on_shutdown(dispatcher: Dispatcher):
        print("❌ Бот остановлен")

    # Подключаем webhook
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    print(f"🌐 Webhook установлен: {WEBHOOK_URL}")
    print(f"🚀 Сервер запущен на http://{HOST}:{PORT}")

    # Запускаем сервер
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
