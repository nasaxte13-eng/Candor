import asyncio
import signal
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = '8688223526:AAGEyn58kTxRgXhS1KHJj-c5WjT7gGQjtJ0'

bot = Bot(token=TOKEN)
dp = Dispatcher()

ADMIN_ID = 1051261597  # твой ID

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n"
        "Я помощник. Напиши, что тебе нужно (заявка, вопрос, запись и т.д.), "
        "и я сразу передам это Натали."
    )

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
    
    await message.answer("Заявка отправлена! ✨ Натали скоро свяжется с тобой.")

async def on_shutdown():
    print("Получен SIGTERM — graceful shutdown")
    await bot.session.close()
    print("Сессия закрыта, бот остановлен корректно")

async def main():
    print("Бот запущен!")
    
    # Запускаем polling с обработкой сигналов
    await dp.start_polling(bot, handle_signals=True)

    # Регистрируем shutdown-хук (на случай, если polling завершится)
    asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(on_shutdown()))
    asyncio.get_event_loop().add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(on_shutdown()))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        asyncio.run(on_shutdown())
