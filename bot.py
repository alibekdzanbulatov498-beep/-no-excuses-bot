ADMIN_ID = 5933655039

import asyncio
import random
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN
from database import init_db, add_user, get_user, add_xp, count_users


logging.basicConfig(level=logging.INFO)


init_db()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


workouts = [
    "💪 20 отжиманий",
    "🔥 50 приседаний",
    "🏃 Пробежка 1 км",
    "🧘 Растяжка 10 минут",
    "💪 Планка 1 минута",
    "🥊 30 ударов в воздух"
]


quotes = [
    "🔥 Не ищи оправдания — ищи результат.",
    "💪 Каждый день становись лучше.",
    "⚡ Дисциплина побеждает мотивацию.",
    "🏆 Маленькие шаги создают большие победы.",
    "🔥 Работай молча — результат всё покажет."
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

    await message.answer(
        f"""
🔥 <b>NO EXCUSES</b>

Привет, {message.from_user.first_name}! 👋

👥 Нас уже: {count_users()} человек

🎯 Твоя тренировка:

{random.choice(workouts)}

💬 Цитата:

{random.choice(quotes)}

Делай без оправданий 💪
""",
        parse_mode="HTML",
        reply_markup=menu
    )


@dp.message(lambda m: m.text == "🎯 Тренировка")
async def workout(message: Message):

    await message.answer(
        f"""
🎯 Новая тренировка:

{random.choice(workouts)}

🔥 Сделай это сегодня!
"""
    )


@dp.message(lambda m: m.text == "✅ Выполнил")
async def done(message: Message):

    add_xp(message.from_user.id, 20)

    await message.answer(
        """
🎉 Красавчик!

⭐ +20 XP

Продолжай идти к цели 🔥
"""
    )


@dp.message(lambda m: m.text == "👤 Профиль")
async def profile(message: Message):

    user = get_user(message.from_user.id)

    if user:
        await message.answer(
            f"""
👤 Профиль

Имя: {user[2]}

⭐ XP: {user[3]}
🏆 Уровень: {user[4]}
🔥 Серия: {user[5]}
🎯 Выполнено: {user[6]}
"""
        )
    else:
        await message.answer("Сначала напиши /start")



from aiohttp import web


async def health(request):
    return web.Response(text="Bot is running")


async def web_server():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        10000
    )

    await site.start()


async def main():

    print("🔥 BOT STARTED")
    
me = await bot.get_me()
print(f"Запущен бот: @{me.username}")

    await bot.delete_webhook(drop_pending_updates=True)

    await web_server()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
