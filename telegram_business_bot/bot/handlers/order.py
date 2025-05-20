import os
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database import save_order
import re
from bot.config import ADMIN_ID

router = Router()


class OrderStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    choosing_service = State()
    confirming_order = State()


@router.message(F.text == "📝 Оформить заказ")
async def start_order(message: Message, state: FSMContext):
    print("[FSM] Старт оформления заказа")
    await message.answer("Введите ваше имя:")
    await state.set_state(OrderStates.waiting_for_name)


@router.message(OrderStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    print(f"[FSM] Ввод имени: {message.text}")
    await state.update_data(name=message.text)
    await message.answer("Теперь введите ваш номер телефона:")
    await state.set_state(OrderStates.waiting_for_phone)


@router.message(OrderStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    print(f"[FSM] Ввод телефона: {message.text}")
    phone = message.text.strip()

    # Простой паттерн: от 10 до 15 цифр
    if not re.fullmatch(r"\+?\d{10,15}", phone):
        await message.answer("❗ Номер телефона должен содержать от 10 до 15 цифр. Попробуйте снова.")
        return

    await state.update_data(phone=phone)

    service_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔧 Ремонт", callback_data="service_repair")],
        [InlineKeyboardButton(text="🧹 Уборка", callback_data="service_cleaning")],
        [InlineKeyboardButton(text="🚚 Доставка", callback_data="service_delivery")]
    ])

    await message.answer("Выберите услугу:", reply_markup=service_keyboard)
    await state.set_state(OrderStates.choosing_service)


@router.callback_query(F.data.startswith("service_"), OrderStates.choosing_service)
async def process_service(callback: CallbackQuery, state: FSMContext):
    service = callback.data.replace("service_", "")
    print(f"[FSM] Выбор услуги: {service}")
    await state.update_data(service=service)

    data = await state.get_data()
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ])

    await callback.message.answer(
        f"<b>Проверьте данные:</b>\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Услуга: {service.capitalize()}",
        reply_markup=confirm_keyboard
    )
    await state.set_state(OrderStates.confirming_order)
    await callback.answer()


@router.callback_query(F.data == "confirm", OrderStates.confirming_order)
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # ✅ Проверка на наличие всех ключей
    if not all(k in data for k in ['name', 'phone', 'service']):
        await callback.message.answer("❌ Ошибка: данные заказа неполны. Попробуйте начать заново.")
        await state.clear()
        return
    print(f"[FSM] Подтверждение: {data}")
    # Сохраняем в базу
    save_order(
        name=data.get("name"),
        phone=data.get("phone"),
        service=data.get("service")
    )
    await callback.message.answer("Ваш заказ принят! Мы свяжемся с вами.")
    await state.clear()
    await callback.answer()

    # Отправка уведомления админу
    bot: Bot = callback.bot
    await bot.send_message(
        ADMIN_ID,
        f"📬 Новый заказ:\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Услуга: {data['service']}"
    )


@router.callback_query(F.data == "cancel", OrderStates.confirming_order)
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    print("[FSM] Заказ отменён")
    await callback.message.answer("Заказ отменён. Вы можете начать заново.")
    await state.clear()
    await callback.answer()
