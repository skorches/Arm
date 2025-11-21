# Bible in a Year Telegram Bot

A Telegram bot that sends daily Bible reading assignments for a year-long challenge. Each message includes:
- Day of the year (1-365)
- Current date
- Bible reading assignment (Old Testament and New Testament)
- Word of encouragement

The bot uses the complete Bible in a Year reading plan and runs in Docker on your VPS, posting daily at 4:00 AM GMT.

## Quick Start with Docker (Recommended for VPS)

### 1. Get Your Chat ID

1. Start a conversation with your bot on Telegram
2. Send any message to your bot
3. Visit: `https://api.telegram.org/bot8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE/getUpdates`
4. Look for `"chat":{"id":123456789}` in the response - that's your chat ID

Alternatively, you can use [@userinfobot](https://t.me/userinfobot) to get your user ID.

### 2. Configure Environment Variables

Edit the `.env` file and add your chat ID:
```bash
TELEGRAM_BOT_TOKEN=8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. Build and Run with Docker

```bash
cd telegram
docker-compose up -d
```

The bot will now run in the background and send daily Bible readings at 4:00 AM GMT.

### 4. Check Logs

```bash
docker-compose logs -f
```

### 5. Stop the Bot

```bash
docker-compose down
```

## Manual Setup (Alternative)

### 1. Install Dependencies

```bash
cd telegram
pip3 install -r requirements.txt
```

### 2. Configure Environment Variables

Edit `.env` and add your credentials:
```
TELEGRAM_BOT_TOKEN=8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. Test the Bot

Run the bot manually to test:
```bash
python3 bot.py
```

### 4. Set Up Daily Scheduling

#### Option A: Using the Scheduler Script (Recommended for testing)

Run the scheduler:
```bash
python3 scheduler.py
```

This will send messages daily at 4:00 AM GMT. The time is set in `scheduler.py`.

#### Option B: Using systemd (Linux - Recommended for production)

1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/telegram-bible-bot.service
   ```

2. Add the following content:
   ```ini
   [Unit]
   Description=Telegram Bible Verse Bot
   After=network.target

   [Service]
   Type=simple
   User=wars09
   WorkingDirectory=/home/wars09/Cursor/Arm/telegram
   ExecStart=/usr/bin/python3 /home/wars09/Cursor/Arm/telegram/bot.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Create a systemd timer for daily execution:
   ```bash
   sudo nano /etc/systemd/system/telegram-bible-bot.timer
   ```

4. Add the following content:
   ```ini
   [Unit]
   Description=Run Telegram Bible Bot Daily
   Requires=telegram-bible-bot.service

   [Timer]
   OnCalendar=daily
   OnCalendar=08:00
   Persistent=true

   [Install]
   WantedBy=timers.target
   ```

5. Enable and start the timer:
   ```bash
   sudo systemctl enable telegram-bible-bot.timer
   sudo systemctl start telegram-bible-bot.timer
   ```

#### Option C: Using Cron (Alternative)

Add to crontab:
```bash
crontab -e
```

Add this line (runs daily at 4:00 AM GMT):
```
0 4 * * * cd /home/wars09/Cursor/Arm/telegram && /usr/bin/python3 bot.py
```

## Features

- **Complete Bible in a Year Plan**: Uses the full 365-day reading plan
- **Daily Reading Assignments**: Sends Old Testament and New Testament readings each day
- **Day Counter**: Tracks progress through the 365-day challenge
- **Encouragement**: Includes a daily word of encouragement
- **Year-Aware**: Automatically uses the correct reading plan for the current year
- **Docker Support**: Easy deployment on VPS with Docker
- **Automatic Scheduling**: Runs daily at 4:00 AM GMT

## Updating the Reading Plan for 2026

When the 2026 reading plan is ready:

1. Open `reading_plan.py`
2. Add a new dictionary `READING_PLAN_2026` with all 365 days (same format as `READING_PLAN_2025`)
3. Add it to the `READING_PLANS` dictionary:
   ```python
   READING_PLANS = {
       2025: READING_PLAN_2025,
       2026: READING_PLAN_2026,  # Add this line
   }
   ```
4. The bot will automatically use the correct year's plan based on the current date

## Customization

### Change the Send Time

Edit `scheduler.py` and modify:
```python
schedule.every().day.at("04:00").do(run_bot)  # 4:00 AM GMT
```

### Add More Encouragements

Edit `bot.py` and add more encouragements to the `encouragements` list in the `get_encouragement` method.

## Troubleshooting

- **Bot not sending messages**: Check that your bot token and chat ID are correct
- **Import errors**: Make sure all dependencies are installed: `pip3 install -r requirements.txt`
- **Permission errors**: Ensure the bot script has execute permissions: `chmod +x bot.py`

## License

This project is open source and available for personal use.

