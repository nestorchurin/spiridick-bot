import aiosqlite

import config


async def init_db():
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL,
                size INTEGER NOT NULL DEFAULT 0,
                last_used INTEGER NOT NULL DEFAULT 0,
                first_name TEXT NOT NULL DEFAULT '',
                PRIMARY KEY (user_id, chat_id)
            )
            """
        )
        cursor = await db.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in await cursor.fetchall()]
        if "first_name" not in columns:
            await db.execute(
                "ALTER TABLE users ADD COLUMN first_name TEXT NOT NULL DEFAULT ''"
            )
        await db.commit()


async def get_user(user_id: int, chat_id: int):
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute(
            "SELECT size, last_used FROM users WHERE user_id=? AND chat_id=?",
            (user_id, chat_id),
        ) as cursor:
            return await cursor.fetchone()


async def create_user(user_id: int, chat_id: int, initial_size: int, first_name: str):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, chat_id, size, last_used, first_name) "
            "VALUES (?, ?, ?, 0, ?)",
            (user_id, chat_id, initial_size, first_name),
        )
        await db.commit()


async def update_user(user_id: int, chat_id: int, size: int, last_used: int, first_name: str):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "UPDATE users SET size=?, last_used=?, first_name=? WHERE user_id=? AND chat_id=?",
            (size, last_used, first_name, user_id, chat_id),
        )
        await db.commit()


async def get_rank(chat_id: int, size: int) -> int:
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(DISTINCT size) FROM users WHERE chat_id=? AND size > ?",
            (chat_id, size),
        ) as cursor:
            row = await cursor.fetchone()
            return (row[0] or 0) + 1


async def get_top(chat_id: int, limit: int = 10):
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute(
            "SELECT first_name, size FROM users WHERE chat_id=? "
            "ORDER BY size DESC, user_id ASC LIMIT ?",
            (chat_id, limit),
        ) as cursor:
            return await cursor.fetchall()


async def get_top_global(limit: int = 10):
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute(
            """
            SELECT first_name, SUM(size) AS total FROM users
            GROUP BY user_id
            ORDER BY total DESC, user_id ASC
            LIMIT ?
            """,
            (limit,),
        ) as cursor:
            return await cursor.fetchall()
