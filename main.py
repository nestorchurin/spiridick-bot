import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

import config
import storage
from handlers import dick_router, help_router, payments_router, start_router, top_router
from utils.throttle import GroupCommandThrottle

dp = Dispatcher()

COMMANDS = [
    BotCommand(command="start", description="Інформація про бота"),
    BotCommand(command="dick", description="Випадковий розмір (тільки в групах)"),
    BotCommand(command="top", description="Топ 10 гравців"),
    BotCommand(command="buy", description="Скинути кулдаун за зірки (приватний чат)"),
    BotCommand(command="help", description="Довідка"),
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(COMMANDS)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                config.LOG_PATH, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
            ),
        ],
    )
    dp.include_router(start_router)
    dp.include_router(dick_router)
    dp.include_router(top_router)
    dp.include_router(payments_router)
    dp.include_router(help_router)
    dp.message.outer_middleware(GroupCommandThrottle(config.GROUP_THROTTLE_SECONDS))
    await storage.init()
    bot = Bot(token=config.BOT_TOKEN)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
