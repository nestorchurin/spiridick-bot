import random
from datetime import datetime

import config
import storage
from utils.text_utils import format_duration
from utils.time_utils import kyiv_time


def roll() -> int:
    return random.randint(config.MIN_SIZE, config.MAX_SIZE)


def build_cooldown_message(first_name: str, size: int, rank: int, last_used: int) -> str:
    now = int(datetime.now().timestamp())
    remaining = config.COOLDOWN_SECONDS - (now - last_used)
    remaining = ((remaining + 59) // 60) * 60
    return (
        f"{first_name}, Зачекай ще {format_duration(remaining)}.\n"
        f"Твій поточний розмір {size} см.\n"
        f"Ти займаєш {rank}-е місце в групі.\n"
        f"Наступна спроба о {kyiv_time(last_used + config.COOLDOWN_SECONDS)} за Київським часом."
    )


def build_result_text(
    first_name: str, roll: int, new_size: int, rank: int, now: int
) -> str:
    if roll < 0:
        change_line = f"{first_name}, твій пісюн зменшився на {abs(roll)} см 📉"
    elif roll > 0:
        change_line = f"{first_name}, твій пісюн збільшився на {roll} см 📈"
    else:
        change_line = f"{first_name}, твій пісюн не змінився 😶"

    return (
        f"{change_line}\n"
        f"Тепер поточний розмір {new_size} см.\n"
        f"Ти займаєш {rank}-е місце в групі.\n"
        f"Твоя наступна команда буде доступна о {kyiv_time(now + config.COOLDOWN_SECONDS)} за Київським часом."
    )


async def play(user_id: int, chat_id: int, first_name: str) -> str:
    now = int(datetime.now().timestamp())
    store = storage.get_store()

    row = await store.get_user(user_id, chat_id)
    if row is None:
        await store.create_user(user_id, chat_id, config.INITIAL_SIZE, first_name)
        row = await store.get_user(user_id, chat_id)

    size, last_used = row
    if now - last_used < config.COOLDOWN_SECONDS:
        rank = await store.get_rank(chat_id, size)
        return build_cooldown_message(first_name, size, rank, last_used)

    roll_value = roll()
    new_size = size + roll_value
    await store.update_user(user_id, chat_id, new_size, now, first_name)

    rank = await store.get_rank(chat_id, new_size)
    return build_result_text(first_name, roll_value, new_size, rank, now)
