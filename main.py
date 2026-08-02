import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VERSION = os.getenv("BOT_VERSION", "1.0.0")
COOLDOWN = os.getenv("COOLDOWN", "10 хвилин")
MIN_SIZE = int(os.getenv("MIN_SIZE", "5"))
MAX_SIZE = int(os.getenv("MAX_SIZE", "30"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

dp = Dispatcher()


@dp.message(Command("start"), F.chat.type == "private")
async def cmd_start_private(message: Message):
    text = (
        f"*Dick Bot | {VERSION}*\n"
        f"Команда /dick працює лише в групових чатах. Раз в {COOLDOWN} гравець може прописати цю команду, щоб отримати випадковий розмір.\n"
        f"Наразі розмір від {MIN_SIZE} до {MAX_SIZE} см.\n"
        f"Якщо у тебе є питання — пиши /help."
    )
    await message.answer(text, parse_mode="Markdown")


@dp.message(Command("start"), F.chat.type.in_({"group", "supergroup"}))
async def cmd_start_group(message: Message):
    await message.answer("Ця команда доступна лише в @spiridick_bot")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
