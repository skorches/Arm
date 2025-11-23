#!/usr/bin/env python3
"""
Telegram Bot for Daily Bible Reading Challenge
Handles user interactions, queries, and daily message subscriptions
"""

import os
import logging
import asyncio
import re
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError, Forbidden
from dotenv import load_dotenv
from reading_plan import get_reading_for_day, READING_PLANS
from user_storage import add_user, is_subscribed, get_all_subscribed_users, remove_user
from bible_books import expand_bible_reading, BIBLE_BOOK_ABBREVIATIONS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BibleVerseBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
        
    def _setup_handlers(self):
        """Set up all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("today", self.today_command))
        self.application.add_handler(CommandHandler("day", self.day_command))
        self.application.add_handler(CommandHandler("search", self.search_command))
        
        # Message handler for queries (non-command messages)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_query))
    
    def _ensure_subscribed(self, user_id):
        """Ensure user is subscribed (auto-subscribe on first interaction)"""
        if not is_subscribed(user_id):
            if add_user(user_id):
                logger.info(f"Auto-subscribed user {user_id} on first interaction")
                return True
            else:
                logger.error(f"Failed to auto-subscribe user {user_id}")
                return False
        return True
    
    def get_day_of_year(self):
        """Get the current day of the year (1-365/366)"""
        today = datetime.now()
        day_of_year = today.timetuple().tm_yday
        return day_of_year, today.strftime("%B %d, %Y")
    
    def get_bible_reading(self, day_number):
        """Get the Bible reading assignment for the day from the reading plan."""
        current_year = datetime.now().year
        reading = get_reading_for_day(day_number, current_year)
        
        if not reading:
            logger.warning(f"No reading found for day {day_number}")
            return "Reading not available for this day"
        
        # Convert abbreviations to full names
        reading = expand_bible_reading(reading)
        
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
    
    def format_message(self, day_number, date_str, reading, encouragement, include_encouragement=True):
        """Format the daily message"""
        if include_encouragement:
            message = f"""📖 *Bible in a Year - Day {day_number}*

📅 *Date:* {date_str}
🔢 *Day {day_number} of 365*

📚 *Today's Reading:*
{reading}

💝 *Encouragement:*
{encouragement}

#BibleInAYear #Day{day_number}"""
        else:
            message = f"""📖 *Bible in a Year - Day {day_number}*

📅 *Date:* {date_str}
🔢 *Day {day_number} of 365*

📚 *Reading:*
{reading}

#BibleInAYear #Day{day_number}"""
        return message
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        
        # Auto-subscribe user on first interaction
        is_new = not is_subscribed(user_id)
        self._ensure_subscribed(user_id)
        
        day_number, date_str = self.get_day_of_year()
        
        welcome_message = f"""Welcome to the Bible in a Year Bot, {user.first_name}! 🙏

I'll help you read through the Bible in 365 days.

*Available Commands:*
/start - Show this welcome message
/today - Get today's reading
/day [number] - Get reading for a specific day (1-365)
/search [book] - Search for a Bible book in the reading plan
/help - Show all commands

⏰ *Daily Messages:*
You'll receive a message every day at 4:00 AM GMT with that day's reading.

*Try it now:*
Send /today to see today's reading!"""
        
        try:
            await update.message.reply_text(welcome_message, parse_mode='Markdown')
            logger.info(f"User {user.id} ({user.username}) started the bot")
        except Forbidden:
            # User blocked the bot - remove from subscriptions
            logger.warning(f"User {user_id} blocked the bot, removing from subscriptions")
            remove_user(user_id)
            return
        
        # Send today's reading if this is a new user
        if is_new:
            try:
                reading = self.get_bible_reading(day_number)
                encouragement = self.get_encouragement(day_number)
                message = self.format_message(day_number, date_str, reading, encouragement)
                await update.message.reply_text(message, parse_mode='Markdown')
                logger.info(f"Sent today's reading to new user {user_id}")
            except Forbidden:
                # User blocked the bot - remove from subscriptions
                logger.warning(f"User {user_id} blocked the bot, removing from subscriptions")
                remove_user(user_id)
            except Exception as e:
                logger.error(f"Error sending today's reading to new user {user_id}: {e}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        # Ensure user is subscribed
        self._ensure_subscribed(update.effective_user.id)
        
        help_text = """📖 *Bible in a Year Bot - Help*

*Commands:*
/today - Get today's Bible reading
/day [number] - Get reading for a specific day
  Example: /day 45

/search [book] - Search for a Bible book
  Example: /search Genesis
  Example: /search Matthew
  Example: /search Psalms

*Queries:*
You can also ask questions like:
• "What's today's reading?"
• "Day 45"
• "Show me day 100"

*Daily Messages:*
You'll automatically receive a message every day at 4:00 AM GMT with that day's reading.

*About:*
This bot follows a complete Bible in a Year reading plan, combining Old Testament and New Testament readings each day."""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /today command"""
        # Ensure user is subscribed
        self._ensure_subscribed(update.effective_user.id)
        day_number, date_str = self.get_day_of_year()
        reading = self.get_bible_reading(day_number)
        encouragement = self.get_encouragement(day_number)
        
        message = self.format_message(day_number, date_str, reading, encouragement)
        
        try:
            await update.message.reply_text(message, parse_mode='Markdown')
            logger.info(f"Sent today's reading to user {update.effective_user.id}")
        except TelegramError as e:
            logger.error(f"Error sending message: {e}")
            await update.message.reply_text("Sorry, there was an error sending the message.")
    
    async def day_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /day command with optional day number"""
        # Ensure user is subscribed
        self._ensure_subscribed(update.effective_user.id)
        if context.args:
            try:
                day_number = int(context.args[0])
                if day_number < 1 or day_number > 365:
                    await update.message.reply_text("Please enter a day number between 1 and 365.")
                    return
            except ValueError:
                await update.message.reply_text("Please enter a valid day number (1-365).")
                return
        else:
            day_number, _ = self.get_day_of_year()
        
        # Calculate date for that day (approximate)
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        target_date = start_date + timedelta(days=day_number - 1)
        date_str = target_date.strftime("%B %d, %Y")
        
        reading = self.get_bible_reading(day_number)
        encouragement = self.get_encouragement(day_number)
        
        message = self.format_message(day_number, date_str, reading, encouragement)
        
        try:
            await update.message.reply_text(message, parse_mode='Markdown')
            logger.info(f"Sent day {day_number} reading to user {update.effective_user.id}")
        except TelegramError as e:
            logger.error(f"Error sending message: {e}")
            await update.message.reply_text("Sorry, there was an error sending the message.")
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Ensure user is subscribed
        self._ensure_subscribed(update.effective_user.id)
        """Handle /search command - search for Bible books in the reading plan"""
        if not context.args:
            await update.message.reply_text(
                "🔍 *Search for Bible Books*\n\n"
                "Usage: /search [book name]\n\n"
                "Examples:\n"
                "• /search Genesis\n"
                "• /search Matthew\n"
                "• /search Psalms\n"
                "• /search Revelation\n\n"
                "You can search by full name or abbreviation (e.g., 'Gen', 'Mt', 'Ps').",
                parse_mode='Markdown'
            )
            return
        
        search_term = ' '.join(context.args).lower().strip()
        current_year = datetime.now().year
        plan = READING_PLANS.get(current_year, READING_PLANS[max(READING_PLANS.keys())])
        
        # Find matching books (both full names and abbreviations)
        matching_books = []
        for abbrev, full_name in BIBLE_BOOK_ABBREVIATIONS.items():
            if (search_term in full_name.lower() or 
                search_term in abbrev.lower().replace('.', '') or
                abbrev.lower().replace('.', '') in search_term):
                matching_books.append((abbrev, full_name))
        
        if not matching_books:
            await update.message.reply_text(
                f"❌ No Bible book found matching '{search_term}'.\n\n"
                "Try searching for:\n"
                "• Genesis, Exodus, Leviticus, Numbers, Deuteronomy\n"
                "• Matthew, Mark, Luke, John\n"
                "• Psalms, Proverbs, Revelation\n"
                "• Or use abbreviations like 'Gen', 'Mt', 'Ps'"
            )
            return
        
        # Search for days containing these books
        found_days = []
        for day_num, reading in plan.items():
            reading_lower = reading.lower()
            for abbrev, full_name in matching_books:
                # Check if abbreviation or full name appears in reading
                if abbrev.lower() in reading_lower or full_name.lower() in reading_lower:
                    found_days.append((day_num, reading))
                    break
        
        if not found_days:
            await update.message.reply_text(
                f"❌ No readings found for '{matching_books[0][1]}' in the current reading plan."
            )
            return
        
        # Format results (limit to first 20 to avoid message too long)
        results = found_days[:20]
        book_names = [full_name for _, full_name in matching_books]
        book_display = book_names[0] if len(book_names) == 1 else f"{', '.join(book_names[:3])}"
        
        result_text = f"🔍 *Search Results: {book_display}*\n\n"
        result_text += f"Found in {len(found_days)} day(s):\n\n"
        
        for day_num, reading in results:
            expanded_reading = expand_bible_reading(reading)
            result_text += f"*Day {day_num}:* {expanded_reading}\n"
        
        if len(found_days) > 20:
            result_text += f"\n... and {len(found_days) - 20} more day(s)"
        
        result_text += f"\n\n💡 Use /day [number] to get the full reading for any day."
        
        await update.message.reply_text(result_text, parse_mode='Markdown')
        logger.info(f"User {update.effective_user.id} searched for '{search_term}', found {len(found_days)} results")
    
    async def handle_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text queries (non-command messages)"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        text = update.message.text.lower().strip()
        
        # Check for day number queries
        day_match = re.search(r'\bday\s+(\d+)\b', text)
        if day_match:
            day_number = int(day_match.group(1))
            if 1 <= day_number <= 365:
                # Reuse day_command logic
                current_year = datetime.now().year
                start_date = datetime(current_year, 1, 1)
                target_date = start_date + timedelta(days=day_number - 1)
                date_str = target_date.strftime("%B %d, %Y")
                
                reading = self.get_bible_reading(day_number)
                encouragement = self.get_encouragement(day_number)
                message = self.format_message(day_number, date_str, reading, encouragement)
                
                await update.message.reply_text(message, parse_mode='Markdown')
                return
        
        # Check for "today" queries
        if any(word in text for word in ['today', 'todays', "today's", 'current', 'now']):
            day_number, date_str = self.get_day_of_year()
            reading = self.get_bible_reading(day_number)
            encouragement = self.get_encouragement(day_number)
            message = self.format_message(day_number, date_str, reading, encouragement)
            await update.message.reply_text(message, parse_mode='Markdown')
            return
        
        # Default response for unrecognized queries
        await update.message.reply_text(
            "I can help you with Bible readings! Try:\n\n"
            "• /today - Get today's reading\n"
            "• /day 45 - Get reading for day 45\n"
            "• /search [book] - Find a Bible book\n"
            "• /help - See all commands"
        )
    
    async def send_daily_to_user(self, user_id):
        """Send daily reading to a specific user"""
        try:
            day_number, date_str = self.get_day_of_year()
            reading = self.get_bible_reading(day_number)
            encouragement = self.get_encouragement(day_number)
            
            message = self.format_message(day_number, date_str, reading, encouragement)
            
            await self.application.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Successfully sent daily reading to user {user_id}")
            return True
            
        except Forbidden:
            # User blocked the bot - remove from subscriptions
            logger.warning(f"User {user_id} blocked the bot, removing from subscriptions")
            remove_user(user_id)
            return False
        except TelegramError as e:
            logger.error(f"Telegram error sending to user {user_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending message to user {user_id}: {e}")
            return False
    
    async def send_daily_to_all_subscribed(self):
        """Send daily reading to all subscribed users"""
        users = get_all_subscribed_users()
        
        if not users:
            logger.info("No subscribed users to send messages to")
            return
        
        logger.info(f"Sending daily reading to {len(users)} subscribed users")
        
        success_count = 0
        for user_id in users:
            if await self.send_daily_to_user(user_id):
                success_count += 1
            await asyncio.sleep(0.1)  # Small delay to avoid rate limiting
        
        logger.info(f"Successfully sent to {success_count}/{len(users)} users")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Bible in a Year bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    async def shutdown(self):
        """Shutdown the bot"""
        await self.application.stop()
        await self.application.shutdown()

async def main():
    """Main function to run the bot"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    bot = BibleVerseBot(bot_token)
    bot.run()

if __name__ == "__main__":
    asyncio.run(main())
