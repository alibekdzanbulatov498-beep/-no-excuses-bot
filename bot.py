import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN
from database import init_db, add_user, get_user

# Создаем базу данных
init_db()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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

Добро пожаловать, <b>{message.from_user.first_name}</b>!

Это только начало.

Скоро здесь появятся:

🎯 Ежедневные задания
🏆 Уровни
⭐ XP
🔥 Серия дней
🥇 Рейтинг
🎖 Достижения

Пока напиши любое сообщение 😊
""",
        parse_mode="HTML"
    )


@dp.message()
async def echo(message: Message):
    user = get_user(message.from_user.id)

    await message.answer(
        f"""
👤 Ты зарегистрирован!

ID: {user[0]}
Имя: {user[2]}

🏆 Уровень: {user[4]}
⭐ XP: {user[3]}
🔥 Серия: {user[5]}
🎯 Выполнено: {user[6]}
"""
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
