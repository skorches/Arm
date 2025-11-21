# Deployment Guide for VPS

## Prerequisites

- Docker and Docker Compose installed on your VPS
- Telegram Bot Token (already configured: `8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE`)
- Your Telegram Chat ID

## Step-by-Step Deployment

### 1. Get Your Chat ID

1. Message your bot on Telegram
2. Visit: `https://api.telegram.org/bot8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE/getUpdates`
3. Find your chat ID in the response (look for `"chat":{"id":123456789}`)

### 2. Configure Environment Variables

Create or edit the `.env` file in the telegram directory:

```bash
cd /home/wars09/Cursor/Arm/telegram
nano .env
```

Add:
```
TELEGRAM_BOT_TOKEN=8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. Build and Start the Container

```bash
docker-compose up -d --build
```

### 4. Verify It's Running

```bash
docker-compose ps
docker-compose logs -f
```

### 5. Test the Bot

You can manually trigger a message to test:

```bash
docker-compose exec bible-bot python3 bot.py
```

## Managing the Bot

### View Logs
```bash
docker-compose logs -f
```

### Stop the Bot
```bash
docker-compose down
```

### Restart the Bot
```bash
docker-compose restart
```

### Update the Bot
```bash
docker-compose down
git pull  # if using git
docker-compose up -d --build
```

## Schedule

The bot is configured to send messages daily at **4:00 AM GMT**. The scheduler runs continuously inside the Docker container.

## Updating Reading Plan for 2026

When the 2026 reading plan is ready:

1. Edit `reading_plan.py`
2. Add `READING_PLAN_2026` dictionary with all 365 days
3. Add it to `READING_PLANS` dictionary
4. Rebuild the container:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

The bot automatically detects the current year and uses the appropriate reading plan.

