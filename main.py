import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен берём из переменных окружения (Bothost позволит задать)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не задан! Укажи его в переменных окружения на Bothost.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я эхо-бот. Напиши мне что-нибудь — я повторю.")

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
