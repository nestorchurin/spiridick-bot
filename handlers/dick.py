from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from services import dick_service

router = Router()


@router.message(Command("dick"), F.chat.type.in_({"group", "supergroup"}))
async def cmd_dick(message: Message):
    first_name = message.from_user.first_name or "Гравець"
    text = await dick_service.play(message.from_user.id, message.chat.id, first_name)
    await message.answer(text)


@router.message(Command("dick"), F.chat.type == "private")
async def cmd_dick_private(message: Message):
    await message.answer("Команда /dick доступна лише в групових чатах.")
