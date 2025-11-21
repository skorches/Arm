# Bible in a Year Telegram Bot

A Telegram bot that sends daily Bible reading assignments for a year-long challenge. The bot is **publicly accessible** - anyone can find it and use it!

## Features

- ✅ **Public Bot**: Anyone can find and use the bot
- ✅ **Interactive Queries**: Users can ask questions and get readings
- ✅ **Daily Subscriptions**: Users can subscribe to receive daily messages at 4:00 AM GMT
- ✅ **Complete Reading Plan**: Full 365-day Bible in a Year plan
- ✅ **Commands & Queries**: Multiple ways to interact with the bot
- ✅ **Docker Support**: Easy deployment on VPS

## Bot Commands

- `/start` - Welcome message and introduction
- `/help` - Show all available commands
- `/today` - Get today's Bible reading
- `/day [number]` - Get reading for a specific day (1-365)
  - Example: `/day 45`
- `/subscribe` - Subscribe to daily messages (sent at 4:00 AM GMT)
- `/unsubscribe` - Stop receiving daily messages
- `/status` - Check your subscription status

## Query Examples

Users can also ask questions naturally:
- "What's today's reading?"
- "Day 45"
- "Show me day 100"
- "today"

## Quick Start with Docker (Recommended for VPS)

### 1. Configure Environment Variables

Edit the `.env` file:
```bash
TELEGRAM_BOT_TOKEN=8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE
TELEGRAM_CHAT_ID=not_needed_anymore
```

**Note**: `TELEGRAM_CHAT_ID` is no longer required since the bot handles multiple users!

### 2. Build and Run with Docker

```bash
cd telegram
docker-compose up -d --build
```

The bot will now:
- Handle incoming messages from any user
- Send daily readings to subscribed users at 4:00 AM GMT

### 3. Check Logs

```bash
docker-compose logs -f
```

### 4. Stop the Bot

```bash
docker-compose down
```

## How It Works

### Two Components Running:

1. **Interactive Bot** (`bot_runner.py`)
   - Handles all user queries and commands
   - Responds to messages in real-time
   - Manages subscriptions

2. **Scheduler** (`scheduler.py`)
   - Runs daily at 4:00 AM GMT
   - Sends messages to all subscribed users
   - Uses `daily_sender.py` to send to everyone

### User Storage

- Subscribed users are stored in `subscribed_users.json`
- This file persists in Docker via volume mount
- No database required - simple JSON file storage

## Testing the Bot

1. Find your bot on Telegram (search for the bot username you created with @BotFather)
2. Send `/start` to begin
3. Try `/today` to see today's reading
4. Use `/subscribe` to get daily messages

## Updating the Reading Plan for 2026

When the 2026 reading plan is ready:

1. Open `reading_plan.py`
2. Add a new dictionary `READING_PLAN_2026` with all 365 days
3. Add it to the `READING_PLANS` dictionary:
   ```python
   READING_PLANS = {
       2025: READING_PLAN_2025,
       2026: READING_PLAN_2026,
   }
   ```
4. Rebuild: `docker-compose up -d --build`

The bot automatically uses the correct year's plan based on the current date.

## Customization

### Change the Send Time

Edit `scheduler.py` and modify:
```python
schedule.every().day.at("04:00").do(run_bot)  # 4:00 AM GMT
```

### Add More Encouragements

Edit `bot.py` and add more encouragements to the `encouragements` list in the `get_encouragement` method.

## Troubleshooting

- **Bot not responding**: Check logs with `docker-compose logs -f`
- **Users not receiving daily messages**: Verify they used `/subscribe`
- **Import errors**: Make sure all dependencies are installed
- **Permission errors**: Ensure scripts have execute permissions

## File Structure

```
telegram/
├── bot.py              # Main bot logic with handlers
├── bot_runner.py       # Runs interactive bot (handles queries)
├── daily_sender.py     # Sends daily messages to all subscribers
├── scheduler.py        # Schedules daily messages at 4 AM GMT
├── user_storage.py     # Manages user subscriptions
├── reading_plan.py     # Complete 365-day reading plan
├── start.sh            # Startup script for Docker
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
└── .env                # Environment variables (not in git)
```

## License

This project is open source and available for personal use.
