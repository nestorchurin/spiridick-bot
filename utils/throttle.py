import time

from aiogram import BaseMiddleware
from aiogram.types import Message

GROUP_TYPES = {"group", "supergroup"}

_last: dict[int, float] = {}


def is_throttled(chat_id: int, seconds: float = 10) -> bool:
    now = time.monotonic()
    last = _last.get(chat_id, 0.0)
    if now - last < seconds:
        return True
    _last[chat_id] = now
    return False


class GroupCommandThrottle(BaseMiddleware):
    def __init__(self, seconds: float = 10):
        self.seconds = seconds

    async def __call__(self, handler, event: Message, data: dict):
        if (
            event.chat
            and event.chat.type in GROUP_TYPES
            and event.text
            and event.text.startswith("/")
        ):
            if is_throttled(event.chat.id, self.seconds):
                return
        return await handler(event, data)
