def plural_ua(n: int, one: str, few: str, many: str) -> str:
    n10 = n % 10
    n100 = n % 100
    if n100 in (11, 12, 13, 14):
        return many
    if n10 == 1:
        return one
    if n10 in (2, 3, 4):
        return few
    return many


def parse_cooldown(value: str) -> int:
    value = value.strip().lower()
    multipliers = {
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
    }
    suffix = value[-1]
    if suffix in multipliers:
        return int(value[:-1]) * multipliers[suffix]
    return int(value) * 60


def format_cooldown(seconds: int) -> str:
    if seconds % 604800 == 0:
        n = seconds // 604800
        return f"{n} {plural_ua(n, 'тиждень', 'тижні', 'тижнів')}"
    if seconds % 86400 == 0:
        n = seconds // 86400
        return f"{n} {plural_ua(n, 'день', 'дні', 'днів')}"
    if seconds % 3600 == 0:
        n = seconds // 3600
        return f"{n} {plural_ua(n, 'година', 'години', 'годин')}"
    n = seconds // 60
    return f"{n} {plural_ua(n, 'хвилина', 'хвилини', 'хвилин')}"


def format_duration(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    parts = []
    if days:
        parts.append(f"{days} {plural_ua(days, 'день', 'дні', 'днів')}")
    if hours:
        parts.append(f"{hours} {plural_ua(hours, 'година', 'години', 'годин')}")
    if minutes or not parts:
        parts.append(f"{minutes} {plural_ua(minutes, 'хвилина', 'хвилини', 'хвилин')}")
    return " ".join(parts)
