from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Додати статтю витрат")],
        [KeyboardButton(text="📊 Отримати звіт витрат за вказаний період")],
        [KeyboardButton(text="📝 Відредагувати статтю у списку витрат"), KeyboardButton(text="❌ Видалити статтю у списку витрат")]
    ],
    resize_keyboard=True
)
