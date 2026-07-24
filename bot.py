import asyncio
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN
from database import init_db, add_user, get_user, add_xp


init_db()


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


workouts = [
    "💪 Сделай 20 отжиманий",
    "🔥 Сделай 50 приседаний",
    "🏃 Пробеги 1 километр",
    "🧘 Сделай растяжку 10 минут",
    "💪 Стой в планке 1 минуту",
    "🥊 Сделай 30 ударов"
]


quotes = [
    "🔥 Успех начинается там, где заканчиваются оправдания.",
    "💪 Каждый день становись сильнее.",
    "⚡ Дисциплина важнее мотивации.",
    "🏆 Маленькие шаги дают большие результаты.",
    "🔥 Работай молча, результат скажет всё."
]


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎯 Тренировка"),
            KeyboardButton(text="👤 Профиль")
        ],
        [
            KeyboardButton(text="✅ Выполнил")
        ]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: Message):

    add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )

    workout = random.choice(workouts)
    quote = random.choice(quotes)

    await message.answer(
        f"""
🔥 <b>NO EXCUSES</b>

Привет, {message.from_user.first_name}! 

🎯 Твоя тренировка:

{workout}

💬 Цитата:

{quote}

Делай без оправданий 💪
""",
        parse_mode="HTML",
        reply_markup=menu
    )


@dp.message(lambda message: message.text == "🎯 Тренировка")
async def training(message: Message):

    await message.answer(
        f"""
🎯 Новая тренировка:

{random.choice(workouts)}

🔥 Не сдавайся!
"""
    )


@dp.message(lambda message: message.text == "✅ Выполнил")
async def complete(message: Message):

    add_xp(message.from_user.id, 20)

    await message.answer(
        """
🎉 Отлично!

⭐ +20 XP

Продолжай двигаться вперёд 🔥
"""
    )


@dp.message(lambda message: message.text == "👤 Профиль")
async def profile(message: Message):

    user = get_user(message.from_user.id)

    await message.answer(
        f"""
👤 Профиль

Имя: {user[2]}

🏆 Уровень: {user[4]}
⭐ XP: {user[3]}
🔥 Серия: {user[5]}
🎯 Выполнено: {user[6]}
"""
    )


async def main():
    await dp.start_polling(bot)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
