import asyncio
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN
from database import init_db, add_user, get_user


# База данных
init_db()


# Тренировки
workouts = [
    "💪 Сделай 20 отжиманий",
    "🔥 Сделай 50 приседаний",
    "🏃 Пробеги 1 километр",
    "🧘 Сделай растяжку 10 минут",
    "💪 Сделай планку 1 минуту",
    "🥊 Сделай 30 ударов в воздух",
    "🚶 Пройди 5000 шагов"
]


# Цитаты
quotes = [
    "🔥 Успех начинается там, где заканчиваются оправдания.",
    "💪 Каждый день становись лучше, чем вчера.",
    "⚡ Дисциплина сильнее мотивации.",
    "🏆 Маленькие победы создают большие результаты.",
    "🔥 Никто не сделает это за тебя.",
    "💯 Твой главный соперник — ты вчерашний."
]


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Старт
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

Привет, {message.from_user.first_name}! 👋

🎯 Твоя тренировка сегодня:

{workout}

💬 Цитата дня:

{quote}

Не ищи оправданий. Делай. 💪
""",
        parse_mode="HTML"
    )


# Профиль
@dp.message()
async def profile(message: Message):

    user = get_user(message.from_user.id)

    if user:
        await message.answer(
            f"""
👤 Профиль

Имя: {user[2]}

🏆 Уровень: {user[4]}
⭐ XP: {user[3]}
🔥 Серия: {user[5]} дней
🎯 Выполнено: {user[6]}
"""
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
