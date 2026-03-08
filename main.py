import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = '8688223526:AAGEyn58kTxRgXhS1KHJj-c5WjT7gGQjtJ0'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Твой ID — сюда приходят все заявки
ADMIN_ID = 1051261597   # ← твой ID, не меняй

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n"
        "Я помощник. Напиши, что тебе нужно (заявка, вопрос, заказ), "
        "и я сразу передам это Натали."
    )

@dp.message()
async def forward_request(message: types.Message):
    # Если пишешь ты сама — не пересылаем себе же
    if message.from_user.id == ADMIN_ID:
        await message.answer("Это ты сама себе пишешь 😊")
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else f"ID {user.id}"
    
    # Пересылаем тебе сообщение + информацию
    await bot.send_message(
        ADMIN_ID,
        f"Новая заявка!\n"
        f"От: {user.full_name} ({username})\n"
        f"Сообщение:\n\n{message.text}\n\n"
        f"Ответить: t.me/{user.username if user.username else user.id}"
    )
    
    # Ответ пользователю
    await message.answer(
        "Заявка отправлена! ✨\n"
        "Натали скоро с тобой свяжется."
    )

async def main():
    print("Бот-помощник запущен! Заявки идут в личку Натали.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
