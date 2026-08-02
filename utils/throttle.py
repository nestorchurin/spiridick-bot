import time

from aiogram import BaseMiddleware
from aiogram.types import Message

GROUP_TYPES = {"group", "supergroup"}

_last: dict[tuple[int, int, str], float] = {}


def is_throttled(chat_id: int, user_id: int, command: str, seconds: float = 1) -> bool:
    now = time.monotonic()
    key = (chat_id, user_id, command)
    last = _last.get(key, 0.0)
    if now - last < seconds:
        return True
    _last[key] = now
    return False


class GroupCommandThrottle(BaseMiddleware):
    def __init__(self, seconds: float = 1):
        self.seconds = seconds

    async def __call__(self, handler, event: Message, data: dict):
        if (
            event.chat
            and event.chat.type in GROUP_TYPES
            and event.text
            and event.text.startswith("/")
            and event.from_user
        ):
            command = event.text.split()[0].split("@")[0].lower()
            if is_throttled(event.chat.id, event.from_user.id, command, self.seconds):
                return
        return await handler(event, data)
