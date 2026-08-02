from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "*Доступні команди:*\n"
        "/dick — випадковий розмір (тільки в групах)\n"
        "/top — топ 10 гравців (у групі) або глобальний топ (у приватному чаті)\n"
        "/start — інформація про бота\n"
        "/help — ця довідка"
    )
    await message.answer(text, parse_mode="Markdown")
