import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from utils.text_utils import format_cooldown, parse_cooldown

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VERSION = os.getenv("BOT_VERSION", "0.0.0")
COOLDOWN_RAW = os.getenv("COOLDOWN", "1d")
MIN_SIZE = int(os.getenv("MIN_SIZE", "-5"))
MAX_SIZE = int(os.getenv("MAX_SIZE", "10"))
INITIAL_SIZE = int(os.getenv("INITIAL_SIZE", "0"))
DB_PATH = os.getenv("DB_PATH", "dick_bot.db")
LOG_PATH = os.getenv("LOG_PATH", "dick_bot.log")
GROUP_THROTTLE_SECONDS = int(os.getenv("GROUP_THROTTLE_SECONDS", "10"))
SAVE_TO_DB = os.getenv("SAVE_TO_DB", "true").strip().lower() in ("1", "true", "yes", "on")
KYIV_TZ = ZoneInfo("Europe/Kyiv")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

if MIN_SIZE >= MAX_SIZE:
    raise ValueError("MIN_SIZE must be less than MAX_SIZE")

COOLDOWN_SECONDS = parse_cooldown(COOLDOWN_RAW)
COOLDOWN_TEXT = format_cooldown(COOLDOWN_SECONDS)
