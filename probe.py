"""
telegram_business_bot/
├── bot/

│   ├── __init__.py
│   ├── main.py         ← основной файл с запуском бота
│   ├── handlers.py     ← тут будут обрабатываться команды
│   └── config.py       ← настройки (токен и т.д.)
├── requirements.txt    ← зависимости
└── README.md           ← описание проекта
ADMIN_ID=6352026332
"""

from pathlib import Path

# Загрузка .env
# env_path = Path(__file__).resolve().parent.parent / '.env'
# print(env_path)
# print(Path(__file__))
# print(Path(__file__).resolve().parent)

current = Path(__file__).resolve()
print([current] + list(current.parents))

from pathlib import Path


def find_project_root(marker_files=('orders.db', '.git')):
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    raise RuntimeError("Не удалось найти корень проекта")


# Использование:
project_root = find_project_root()
file_path = project_root / 'some_folder' / 'file.txt'
print(file_path)



#
    #
    # @router.message(F.text == '📝 Оформить заказ')
    # async def reply_order(message: Message):
    #     await message.answer('Вы выбрали оформить заказ через Reply-клавиатуру!')
    #
    #
    # @router.message(F.text == '📞 Контакты')
    # async def reply_contacts(message: Message):
    #     await message.answer('Наши контакты: +7 900 123 45 67')
    #
    #
    # @router.message(F.text == '❓ Помощь')
    # async def reply_help(message: Message):
    #     await message.answer('Напишите, что вас интересует, или выберите из меню.')


# def find_project_root(marker=".env"):
#     current = Path(__file__).resolve().parent
#     for parent in [current] + list(current.parents):
#         if (parent / marker).exists():
#             return parent
#     raise RuntimeError("Не удалось найти корень проекта")
