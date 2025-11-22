#!/usr/bin/env python3
"""
Script to send daily messages to all subscribed users
This is called by the scheduler at 4:00 AM GMT
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from bot import BibleVerseBot

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_daily_messages():
    """Send daily messages to all subscribed users"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    bot = BibleVerseBot(bot_token)
    # Initialize the application before sending messages
    await bot.application.initialize()
    try:
        await bot.send_daily_to_all_subscribed()
    finally:
        await bot.shutdown()

if __name__ == "__main__":
    asyncio.run(send_daily_messages())

