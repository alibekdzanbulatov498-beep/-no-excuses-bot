import asyncio

import random

from aiogram import Bot, Dispatcher, F

from aiogram.filters import CommandStart

from aiogram.types import Message

TOKEN = "8870694306:AAFmVW4WSXgjoz2H2KIPlApPPkYGD5rcFsY"

bot = Bot(token=TOKEN)

dp = Dispatcher()

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

        f"""🔥 Добро пожаловать в NO EXCUSES!

Сегодня твоя миссия:

{mission}

Каждый день ты будешь получать новое задание.

Скоро появятся XP, ранги и достижения. 🚀"""

    )

async def main():

    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
