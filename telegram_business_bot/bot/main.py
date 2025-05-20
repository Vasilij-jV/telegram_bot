import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import BOT_TOKEN
from bot.handlers import order
from bot.database import init_db
import logging


async def main():
    logging.basicConfig(level=logging.INFO)

    print("📦 Инициализация базы данных...")
    init_db()

    print("🔄 main.py запущен")
    print("Token:", BOT_TOKEN)

    # Инициализация бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Только один dispatcher с FSM-хранилищем
    dp = Dispatcher(storage=MemoryStorage())

    # Основной router
    router = Router()

    # Reply-клавиатура
    main_reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Оформить заказ")],
            [KeyboardButton(text="📞 Контакты")],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )

    # Обработчики
    @router.message(Command("start"))
    async def cmd_start(message: Message):
        await message.answer("Привет! Я бизнес-бот. Чем могу помочь?",
                             reply_markup=main_reply_keyboard)

    # Inline-клавиатура
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

    # Подключаем роутеры один раз
    dp.include_router(router)
    dp.include_router(order.router)

    print("✅ Бот запущен. Ожидаю сообщений...")

    # Точка входа
    print("🚀 Запускаю бота через polling...")

    await dp.start_polling(bot)
    print('asfd')


if __name__ == "__main__":
    try:
        print("🔁 Запуск asyncio")
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
