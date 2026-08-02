from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

import config

router = Router()


@router.message(Command("start"), F.chat.type == "private")
async def cmd_start_private(message: Message):
    text = (
        f"*Dick Bot | {config.VERSION}*\n"
        f"Команда /dick працює лише в групових чатах. Раз в {config.COOLDOWN_TEXT} гравець може прописати цю команду, щоб отримати випадковий розмір.\n"
        f"Наразі розмір від {config.MIN_SIZE} до {config.MAX_SIZE} см.\n"
        f"Не хочеш чекати? Скинь кулдаун за {config.ATTEMPT_COST} ⭐ через /buy.\n"
        f"Якщо у тебе є питання — пиши /help."
    )
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("start"), F.chat.type.in_({"group", "supergroup"}))
async def cmd_start_group(message: Message):
    await message.answer("Ця команда доступна лише в @spiridick_bot")
