# Bot Features Overview

## What's New

The bot has been completely redesigned to be **publicly accessible** and **interactive**!

### ✅ Public Access
- Anyone can find your bot on Telegram and use it
- No need to configure a specific chat ID
- Users interact with the bot directly

### ✅ Interactive Queries
Users can:
- Ask questions naturally: "What's today's reading?"
- Use commands: `/today`, `/day 45`
- Query specific days: "Day 100", "Show me day 45"

### ✅ Subscription System
- Users can `/subscribe` to get daily messages
- Users can `/unsubscribe` anytime
- Daily messages sent at 4:00 AM GMT to all subscribers
- Subscriptions stored in `subscribed_users.json`

## Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and bot introduction |
| `/help` | Show all available commands |
| `/today` | Get today's Bible reading |
| `/day [number]` | Get reading for specific day (1-365) |
| `/subscribe` | Subscribe to daily messages |
| `/unsubscribe` | Stop receiving daily messages |
| `/status` | Check subscription status |

## Example Interactions

**User:** `/start`
**Bot:** Welcome message with instructions

**User:** `/today`
**Bot:** Today's reading with encouragement

**User:** `/day 45`
**Bot:** Reading for day 45

**User:** "What's today's reading?"
**Bot:** Today's reading (natural language query)

**User:** "Day 100"
**Bot:** Reading for day 100

**User:** `/subscribe`
**Bot:** "✅ You've been subscribed to daily Bible readings!"

## How It Works

### Two Processes Running:

1. **Interactive Bot** (`bot_runner.py`)
   - Listens for incoming messages
   - Handles all commands and queries
   - Manages user subscriptions
   - Runs continuously

2. **Scheduler** (`scheduler.py`)
   - Checks time every minute
   - At 4:00 AM GMT, runs `daily_sender.py`
   - Sends messages to ALL subscribed users
   - Runs continuously

### User Storage

- File: `subscribed_users.json`
- Format: Simple JSON with list of user IDs
- Persists across Docker restarts (via volume mount)
- No database needed!

## Deployment

The bot runs in Docker with both processes:
- Interactive bot handles queries 24/7
- Scheduler sends daily messages at 4 AM GMT

No configuration needed - just deploy and users can start using it!

