import asyncio
import signal
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения Bothost! Добавь его в панели Env.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

ADMIN_ID = 1051261597  # твой ID — сюда приходят все заявки

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оставить заявку")],
        [KeyboardButton(text="Написать в личку")],
        [KeyboardButton(text="Что такое Candor Candle?")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Я помощник Натали. Чем могу помочь?\n\n"
        "Нажми на кнопку ниже ✨",
        reply_markup=keyboard
    )

@dp.message(F.text == "Что такое Candor Candle?")
async def about_candor(message: types.Message):
    await message.answer(
        "Каждый месяц 13-го числа мы выпускаем ровно 13 свечей с уникальным эксклюзивным ароматом. "
        "Каждой свече присваивается свой собственный номер — это твой личный билет в Candor Community\n\n"
        "Каждая свеча создана вручную из натуральных премиум-материалов и несёт в себе особую силу и намерение.\n"
        "Становясь обладателем Candor Candle, ты не просто покупаешь свечу — ты становишься частью сообщества"
    )

@dp.message(F.text == "Оставить заявку")
@dp.message(F.text == "Написать в личку")
@dp.message()
async def forward_to_admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Это ты сама себе пишешь 😊")
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else f"ID {user.id}"

    await bot.send_message(
        ADMIN_ID,
        f"НОВАЯ ЗАЯВКА!\n"
        f"От: {user.full_name} ({username})\n"
        f"Сообщение:\n\n{message.text}\n\n"
        f"Ответить: t.me/{user.username if user.username else user.id}"
    )
    
    await message.answer(
        "Спасибо, что написал(а) мне! ❤️\n"
        "Я уже передала твою заявку Натали — она точно увидит и очень скоро ответит.\n\n"
        "Обычно Натали отвечает в течение 1–2 часов, но если вдруг чуть задержится — это только потому, "
        "что она хочет ответить максимально тепло и по-настоящему полезно 🌸\n\n"
        "Жду тебя здесь, обнимаю 🤗✨"
    )

async def on_shutdown():
    print("Получен SIGTERM — graceful shutdown")
    await bot.session.close()
    print("Сессия закрыта, бот остановлен корректно")

async def main():
    print("Бот запущен!")
    
    await dp.start_polling(bot, handle_signals=True)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, lambda: loop.create_task(on_shutdown()))
    loop.add_signal_handler(signal.SIGINT, lambda: loop.create_task(on_shutdown()))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        asyncio.run(on_shutdown())
