import os
import asyncio
import random
from threading import Thread

from flask import Flask
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("8870694306:AAFmVW4WSXgjoz2H2KIPlApPPkYGD5rcFsY")
print("TOKEN CHECK:", TOKEN is not None)

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask(__name__)


@app.route("/")
def home():
    return "NO EXCUSES bot is running!"


def run_web():
    app.run(host="0.0.0.0", port=10000)


missions = [
    "💪 Сделай 20 отжиманий",
    "🏃 Пройди 5000 шагов",
    "💧 Выпей 2 литра воды",
    "📚 Прочитай 10 страниц книги",
    "🧠 Не заходи в соцсети 1 час",
    "🔥 Сделай планку 1 минуту",
    "🥗 Не ешь сладкое сегодня",
    "😴 Ложись спать до 23:00"
]


@dp.message(CommandStart())
async def start(message: Message):
    mission = random.choice(missions)

    await message.answer(
        f"🔥 NO EXCUSES\n\n"
        f"Твоя миссия сегодня:\n\n"
        f"{mission}\n\n"
        f"Скоро добавим XP, уровни и достижения 🚀"
    )


async def main():
    Thread(target=run_web).start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
