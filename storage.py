import config
import db


class MemoryStore:
    def __init__(self):
        self.rows: dict[tuple[int, int], tuple[int, int, str]] = {}

    async def get_user(self, user_id: int, chat_id: int):
        row = self.rows.get((user_id, chat_id))
        if row:
            size, last_used, _ = row
            return (size, last_used)
        return None

    async def create_user(self, user_id: int, chat_id: int, initial_size: int, first_name: str):
        self.rows[(user_id, chat_id)] = (initial_size, 0, first_name)

    async def update_user(self, user_id: int, chat_id: int, size: int, last_used: int, first_name: str):
        self.rows[(user_id, chat_id)] = (size, last_used, first_name)

    async def get_rank(self, chat_id: int, size: int) -> int:
        greater = {
            s
            for (_, cid), (s, _, _) in self.rows.items()
            if cid == chat_id and s > size
        }
        return len(greater) + 1

    async def get_top(self, chat_id: int, limit: int = 10):
        entries = [
            (name, size)
            for (_, cid), (size, _, name) in self.rows.items()
            if cid == chat_id
        ]
        entries.sort(key=lambda x: x[1], reverse=True)
        return entries[:limit]

    async def get_top_global(self, limit: int = 10):
        totals: dict[int, int] = {}
        names: dict[int, str] = {}
        for (user_id, _), (size, _, name) in self.rows.items():
            totals[user_id] = totals.get(user_id, 0) + size
            names[user_id] = name
        entries = sorted(
            ((names[uid], total) for uid, total in totals.items()),
            key=lambda x: x[1],
            reverse=True,
        )
        return entries[:limit]


_memory_store: MemoryStore | None = None


def get_store():
    if config.SAVE_TO_DB:
        return db
    global _memory_store
    if _memory_store is None:
        _memory_store = MemoryStore()
    return _memory_store


async def init():
    if config.SAVE_TO_DB:
        await db.init_db()
