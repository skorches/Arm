# Quick Start Guide

## Your Bot Token
Already configured: `8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE`

## Step 1: Get Your Chat ID

1. Send a message to your bot on Telegram
2. Visit this URL in your browser:
   ```
   https://api.telegram.org/bot8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE/getUpdates
   ```
3. Look for `"chat":{"id":123456789}` - that's your chat ID

## Step 2: Create .env File

Create a file named `.env` in the telegram directory:

```bash
cd /home/wars09/Cursor/Arm/telegram
nano .env
```

Add these lines (replace with your actual chat ID):
```
TELEGRAM_BOT_TOKEN=8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE
TELEGRAM_CHAT_ID=your_chat_id_here
```

Save and exit (Ctrl+X, then Y, then Enter).

## Step 3: Deploy with Docker

```bash
docker-compose up -d --build
```

## Step 4: Check Logs

```bash
docker-compose logs -f
```

The bot will send daily Bible readings at 4:00 AM GMT!

## Testing

To test immediately:
```bash
docker-compose exec bible-bot python3 bot.py
```

## Updating for 2026

When you have the 2026 reading plan:
1. Edit `reading_plan.py`
2. Add `READING_PLAN_2026 = {...}` with all 365 days
3. Add `2026: READING_PLAN_2026` to the `READING_PLANS` dictionary
4. Rebuild: `docker-compose up -d --build`

