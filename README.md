import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен прямо здесь (на free тарифе env не работает)
TOKEN = '8688223526:AAGEyn58kTxRgXhS1KHJj-c5WjT7gGQjtJ0'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я эхо-бот. Пиши что угодно — повторю!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main():
    print("Бот запущен успешно!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
