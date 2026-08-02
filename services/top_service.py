import storage


def build_top_text(entries, title: str) -> str:
    if not entries:
        return "Ще ніхто не грав у /dick."

    medals = {0: "🥇", 1: "🥈", 2: "🥉"}
    lines = []
    for i, (name, size) in enumerate(entries, start=1):
        prefix = medals.get(i - 1, f"{i}.")
        lines.append(f"{prefix} {name or 'Гравець'} — {size} см")
    return f"{title}\n\n" + "\n".join(lines)


async def get_top_text(chat_id: int) -> str:
    store = storage.get_store()
    entries = await store.get_top(chat_id, 10)
    return build_top_text(entries, "📊 Топ 10 гравців:")


async def get_global_top_text() -> str:
    store = storage.get_store()
    entries = await store.get_top_global(10)
    return build_top_text(entries, "🌍 Глобальний топ 10:")
