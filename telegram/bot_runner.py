#!/usr/bin/env python3
"""
Main bot runner - handles incoming messages and keeps bot running
This should run continuously to handle user queries
"""

import os
import logging
from dotenv import load_dotenv
from bot import BibleVerseBot

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the interactive bot"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    bot = BibleVerseBot(bot_token)
    logger.info("Starting interactive bot (handles user queries)...")
    bot.run()

if __name__ == "__main__":
    main()

