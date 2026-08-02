from datetime import datetime

import config


def kyiv_time(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=config.KYIV_TZ).strftime("%H:%M")
