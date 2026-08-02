# SpiriDick Bot

A Telegram bot where players roll a random size in group chats. Each roll changes your stored size, and you can compete for the top spot.

**Note:** The bot's interface and messages are in **Ukrainian** (the bot was built for Ukrainian-speaking groups).

## Features

- `/dick` — roll a random size (group/supergroup only). Your size is updated by the roll value and saved. Runs on a per-player cooldown.
- `/top` — show the top 10 players:
  - in a group → leaderboard for that group
  - in a private chat → **global** leaderboard (sizes summed across all groups)
- `/buy` — reset your cooldown for Telegram Stars (private chat only), so you can `/dick` again immediately
- `/help` — command reference
- `/start` — bot info (private chat only)
- Auto-registered command menu (`set_my_commands`)
- Per-user, per-command throttling in groups (silent rate limit, default 1s)
- Monetization via **Telegram Stars** (`XTR` invoices, `pre_checkout_query` + `successful_payment` flow, payments stored for refunds)
- Two storage backends: SQLite or in-memory
- File logging with rotation

## Requirements

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   git clone https://github.com/nestorchurin/spiridick-bot.git
   cd spiridick-bot
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure the environment:

   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and set your bot token:

   ```env
   BOT_TOKEN=your_bot_token_here
   ```

## Configuration (.env)

| Variable | Default | Description |
|---|---|---|
| `BOT_TOKEN` | — | Bot token from BotFather (required) |
| `BOT_VERSION` | `0.0.0` | Version shown in `/start` |
| `COOLDOWN` | `1d` | Per-player cooldown: `10m`, `1h`, `1d`, `1w` |
| `MIN_SIZE` | `-5` | Minimum roll value |
| `MAX_SIZE` | `10` | Maximum roll value |
| `INITIAL_SIZE` | `0` | Starting size for new players |
| `DB_PATH` | `dick_bot.db` | SQLite database file path |
| `SAVE_TO_DB` | `true` | `true` = persist to SQLite, `false` = keep data in memory only (resets on restart) |
| `GROUP_THROTTLE_SECONDS` | `1` | Seconds of silent throttling per user **and** per command in groups (`0` = off) |
| `ATTEMPT_COST` | `25` | Price in ⭐ (Telegram Stars) to reset the `/dick` cooldown via `/buy` |
| `LOG_PATH` | `dick_bot.log` | Log file path |

## Running

```bash
source venv/bin/activate
python main.py
```

## Docker (Alpine)

The image is based on `python:3.12-alpine`. The database and logs are stored on a named volume, so data survives container restarts.

```bash
cp .env.example .env
# set BOT_TOKEN in .env

docker compose up -d --build
```

Stop the bot:

```bash
docker compose down
```

Run manually without compose:

```bash
docker build -t spiridick-bot .
docker run -d --name spiridick-bot \
  --env-file .env \
  -e DB_PATH=/app/data/dick_bot.db \
  -e LOG_PATH=/app/data/dick_bot.log \
  -v spiridick-data:/app/data \
  --restart unless-stopped \
  spiridick-bot
```

## Bot setup in Telegram

To make plain commands like `/dick` work in groups, either:

1. Disable privacy mode: `@BotFather` → `/mybots` → your bot → `Bot Settings` → `Group Privacy` → `Turn off`
2. Or add the bot as a group admin.

## How the game works

1. A player sends `/dick` in a group (if the cooldown has passed).
2. A random value is rolled between `MIN_SIZE` and `MAX_SIZE` (e.g. `-5` to `10`).
3. The value is added to the player's stored size (e.g. `100 + (-4) = 96 cm`).
4. The bot replies with the change, the new size, the player's rank in the group, and the next available attempt time (Kyiv time).
5. If the cooldown is still active, the player can reset it by paying `ATTEMPT_COST` ⭐ via `/buy` in the bot's private chat and immediately `/dick` again.

## Project structure

```
main.py                       # entry point: dispatcher, command menu, polling
config.py                     # .env loading + validation
db.py                         # SQLite layer (aiosqlite)
storage.py                    # storage switch: SQLite or in-memory
Dockerfile                    # Alpine-based Docker image
docker-compose.yml            # compose service with persistent volume
handlers/
  start.py                    # /start
  dick.py                     # /dick
  top.py                      # /top (group + global)
  payments.py                 # /buy, Telegram Stars invoices + successful payment
  help.py                     # /help
services/
  dick_service.py             # game logic: roll, cooldown, rank, message
  top_service.py              # leaderboard text
utils/
  text_utils.py               # pluralization, cooldown parsing/formatting
  time_utils.py               # Kyiv time formatting
  throttle.py                 # group command throttling middleware
```

## License

MIT
