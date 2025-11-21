#!/usr/bin/env python3
"""
Telegram Bot for Daily Bible Verse Challenge
Sends daily Bible verses with day of year, verse, and encouragement
"""

import os
import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from telegram.error import TelegramError
import requests
from dotenv import load_dotenv
from reading_plan import get_reading_for_day

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bible API endpoint (using Bible Gateway API alternative - ESV API)
BIBLE_API_URL = "https://api.esv.org/v3/passage/text/"

class BibleVerseBot:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.bible_api_key = os.getenv('BIBLE_API_KEY', '')
        
    def get_day_of_year(self):
        """Get the current day of the year (1-365/366)"""
        today = datetime.now()
        day_of_year = today.timetuple().tm_yday
        return day_of_year, today.strftime("%B %d, %Y")
    
    def get_bible_reading(self, day_number):
        """
        Get the Bible reading assignment for the day from the reading plan.
        """
        current_year = datetime.now().year
        reading = get_reading_for_day(day_number, current_year)
        
        if not reading:
            logger.warning(f"No reading found for day {day_number}")
            return "Reading not available for this day"
        
        return reading
    
    def get_encouragement(self, day_number):
        """Get a word of encouragement based on the day"""
        encouragements = [
            "Remember, God's love for you is unchanging and eternal. Trust in His plan for your life today!",
            "You are never alone. God is with you every step of the way, guiding and protecting you.",
            "Each new day is a gift from God. Embrace it with gratitude and faith!",
            "Your strength comes from the Lord. Lean on Him when you feel weak.",
            "God's grace is sufficient for you. His power is made perfect in weakness.",
            "Keep your eyes fixed on Jesus. He is the author and perfecter of your faith.",
            "Don't worry about tomorrow. God is already there, preparing the way for you.",
            "You are fearfully and wonderfully made. God has a unique purpose for your life.",
            "In every situation, give thanks. God is working all things together for your good.",
            "Stand firm in your faith. The Lord is your shield and your strength.",
            "Let your light shine today. You are a reflection of God's love to others.",
            "God's mercies are new every morning. Receive His fresh grace today!",
            "Cast all your anxiety on Him because He cares for you.",
            "The Lord will fight for you; you need only to be still.",
            "Seek first His kingdom and His righteousness, and all these things will be given to you.",
        ]
        
        encouragement_index = (day_number - 1) % len(encouragements)
        return encouragements[encouragement_index]
    
    def format_message(self, day_number, date_str, reading, encouragement):
        """Format the daily message"""
        message = f"""📖 *Bible in a Year - Day {day_number}*

📅 *Date:* {date_str}
🔢 *Day {day_number} of 365*

📚 *Today's Reading:*
{reading}

💝 *Encouragement:*
{encouragement}

#BibleInAYear #Day{day_number}"""
        return message
    
    async def send_daily_verse(self):
        """Send the daily Bible reading to the chat"""
        try:
            day_number, date_str = self.get_day_of_year()
            reading = self.get_bible_reading(day_number)
            encouragement = self.get_encouragement(day_number)
            
            message = self.format_message(day_number, date_str, reading, encouragement)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Successfully sent daily reading for day {day_number}")
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

async def main():
    """Main function to run the bot"""
    # Get configuration from environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    if not chat_id:
        logger.error("TELEGRAM_CHAT_ID not found in environment variables")
        return
    
    # Create bot instance
    bot = BibleVerseBot(bot_token, chat_id)
    
    # Send daily verse
    await bot.send_daily_verse()

if __name__ == "__main__":
    asyncio.run(main())

