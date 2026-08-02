from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from services import top_service

router = Router()


@router.message(Command("top"), F.chat.type.in_({"group", "supergroup"}))
async def cmd_top(message: Message):
    text = await top_service.get_top_text(message.chat.id)
    await message.answer(text)


@router.message(Command("top"), F.chat.type == "private")
async def cmd_top_private(message: Message):
    text = await top_service.get_global_top_text()
    await message.answer(text)
