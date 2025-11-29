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
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.error import TelegramError, Forbidden, BadRequest
from dotenv import load_dotenv
from reading_plan import get_reading_for_day, READING_PLANS
from user_storage import add_user, is_subscribed, get_all_subscribed_users, remove_user
from bible_books import expand_bible_reading, BIBLE_BOOK_ABBREVIATIONS
from quiz_questions import (
    get_random_question, get_total_questions, get_stats,
    CATEGORIES, DIFFICULTIES
)
from bible_qa import find_answer, get_all_topics
from quiz_storage import (
    get_user_score, update_user_score, start_quiz_session,
    get_quiz_session, update_quiz_session, end_quiz_session,
    load_active_quizzes, save_active_quizzes, get_leaderboard,
    get_user_rank, update_user_info, save_quiz_to_history, get_quiz_history
)
from reading_progress import (
    mark_day_completed, get_user_progress, get_current_streak,
    get_longest_streak, is_day_completed
)
from daily_quiz import (
    get_today_quiz_question, mark_daily_quiz_completed,
    has_completed_daily_quiz, get_daily_quiz_stats, get_daily_quiz_leaderboard
)
from verses import (
    get_verse_of_the_day, search_verses, get_verse_by_reference
)
from achievements import (
    check_and_award_achievements, get_user_achievements,
    get_achievement_display, ACHIEVEMENTS
)
from reminders import (
    set_reminder, remove_reminder, disable_reminders, enable_reminders,
    get_user_reminders, parse_time_string
)
from config import (
    MAX_RECENT_QUESTIONS, DAYS_IN_YEAR, DAYS_IN_LEAP_YEAR,
    PROGRESS_BAR_LENGTH, LEADERBOARD_TOP_N, ENCOURAGEMENT_MESSAGES,
    MESSAGE_SEPARATOR, ERROR_MESSAGE_GENERIC, ERROR_MESSAGE_QUIZ_ACTIVE,
    ERROR_MESSAGE_INVALID_DAY, TOTAL_QUIZ_QUESTIONS
)

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
        # In-memory fallback for quiz sessions if file storage fails
        self._in_memory_quizzes = {}
        # Track recently asked questions per user to avoid repeats
        self._recent_questions = {}  # {user_id: [question_indices]}
        
    def _setup_handlers(self):
        """Set up all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("today", self.today_command))
        self.application.add_handler(CommandHandler("day", self.day_command))
        self.application.add_handler(CommandHandler("search", self.search_command))
        self.application.add_handler(CommandHandler("quiz", self.quiz_command))
        self.application.add_handler(CommandHandler("quiz_start", self.quiz_command))
        self.application.add_handler(CommandHandler("quiz_easy", self.quiz_easy_command))
        self.application.add_handler(CommandHandler("quiz_medium", self.quiz_medium_command))
        self.application.add_handler(CommandHandler("quiz_hard", self.quiz_hard_command))
        self.application.add_handler(CommandHandler("score", self.score_command))
        self.application.add_handler(CommandHandler("leaderboard", self.leaderboard_command))
        self.application.add_handler(CommandHandler("rankings", self.leaderboard_command))
        self.application.add_handler(CommandHandler("quiz_stop", self.quiz_stop_command))
        self.application.add_handler(CommandHandler("ask", self.ask_command))
        self.application.add_handler(CommandHandler("question", self.ask_command))
        self.application.add_handler(CommandHandler("test_daily", self.test_daily_command))
        self.application.add_handler(CommandHandler("progress", self.progress_command))
        self.application.add_handler(CommandHandler("streak", self.streak_command))
        self.application.add_handler(CommandHandler("completed", self.completed_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CommandHandler("daily_quiz", self.daily_quiz_command))
        self.application.add_handler(CommandHandler("challenge", self.daily_quiz_command))
        self.application.add_handler(CommandHandler("verse", self.verse_command))
        self.application.add_handler(CommandHandler("achievements", self.achievements_command))
        self.application.add_handler(CommandHandler("badges", self.achievements_command))
        self.application.add_handler(CommandHandler("remind", self.remind_command))
        self.application.add_handler(CommandHandler("remind_off", self.remind_off_command))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
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
    
    # ==================== Input Validation Methods ====================
    
    def _validate_day_number(self, day_str: str) -> tuple[bool, int | None, str]:
        """
        Validate day number input
        Returns: (is_valid, day_number, error_message)
        """
        try:
            day_number = int(day_str)
            current_year = datetime.now().year
            is_leap_year = current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0)
            max_days = DAYS_IN_LEAP_YEAR if is_leap_year else DAYS_IN_YEAR
            
            if day_number < 1:
                return (False, None, f"❌ Day number must be at least 1. Please enter a number between 1 and {max_days}.")
            elif day_number > max_days:
                return (False, None, f"❌ Day number cannot exceed {max_days}. Please enter a number between 1 and {max_days}.")
            else:
                return (True, day_number, "")
        except ValueError:
            return (False, None, ERROR_MESSAGE_INVALID_DAY)
    
    def _validate_search_term(self, search_term: str) -> tuple[bool, str]:
        """
        Validate search term input
        Returns: (is_valid, error_message)
        """
        if not search_term or not search_term.strip():
            return (False, "❌ Please provide a book name to search for.\n\nExample: /search Genesis")
        
        if len(search_term) > 50:
            return (False, "❌ Search term is too long. Please use a shorter book name (max 50 characters).")
        
        # Check for potentially harmful characters (basic sanitization)
        if any(char in search_term for char in ['<', '>', '{', '}', '[', ']', '`']):
            return (False, "❌ Invalid characters in search term. Please use only letters, numbers, and spaces.")
        
        return (True, "")
    
    def _validate_question(self, question: str) -> tuple[bool, str]:
        """
        Validate question input for /ask command
        Returns: (is_valid, error_message)
        """
        if not question or not question.strip():
            return (False, "❌ Please provide a question.\n\nExample: /ask How can I be saved?")
        
        if len(question) < 3:
            return (False, "❌ Question is too short. Please ask a more detailed question.")
        
        if len(question) > 500:
            return (False, "❌ Question is too long. Please keep it under 500 characters.")
        
        return (True, "")
    
    def _validate_verse_reference(self, reference: str) -> tuple[bool, str]:
        """
        Validate verse reference input
        Returns: (is_valid, error_message)
        """
        if not reference or not reference.strip():
            return (True, "")  # Empty is valid (will show verse of the day)
        
        if len(reference) > 100:
            return (False, "❌ Verse reference is too long. Please use a shorter reference (max 100 characters).")
        
        return (True, "")
    
    def _validate_time_string(self, time_str: str) -> tuple[bool, str]:
        """
        Validate time string for reminders
        Returns: (is_valid, error_message)
        """
        if not time_str or not time_str.strip():
            return (False, "❌ Please provide a time.\n\nExample: /remind 8am")
        
        # The parse_time_string function will handle actual parsing
        # This just validates the input format
        if len(time_str) > 20:
            return (False, "❌ Time string is too long. Please use a format like '8am' or '14:30'.")
        
        return (True, "")
    
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
        encouragement_index = (day_number - 1) % len(ENCOURAGEMENT_MESSAGES)
        return ENCOURAGEMENT_MESSAGES[encouragement_index]
    
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
    
    def get_quiz_answer_keyboard(self, question_data):
        """Create inline keyboard with quiz answer options as buttons"""
        options = question_data['options']
        keyboard = []
        for i, option in enumerate(options):
            keyboard.append([InlineKeyboardButton(f"{i+1}. {option}", callback_data=f"quiz_answer_{i}")])
        keyboard.append([InlineKeyboardButton("⏹️ Stop Quiz", callback_data="quiz_stop")])
        return InlineKeyboardMarkup(keyboard)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        
        # Auto-subscribe user on first interaction
        is_new = not is_subscribed(user_id)
        self._ensure_subscribed(user_id)
        
        day_number, date_str = self.get_day_of_year()
        
        welcome_message = f"""📖 *Welcome to Bible in a Year Bot, {user.first_name}!* 🙏

*Everything is button-based - no typing needed!*

Just tap the buttons below to:
• 📖 Read today's Bible passage
• 🎯 Test your knowledge with quizzes
• 📊 Track your reading progress
• ❓ Ask Bible questions
• 🏆 Compete on the leaderboard

*Use the buttons below to get started!* 👇"""
        
        try:
            await update.message.reply_text(
                welcome_message, 
                parse_mode='Markdown',
                reply_markup=self.get_main_menu_keyboard()
            )
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
                mark_day_completed(user_id, day_number)
                await update.message.reply_text(
                    message, 
                    parse_mode='Markdown',
                    reply_markup=self.get_quick_actions_keyboard()
                )
                logger.info(f"Sent today's reading to new user {user_id}")
            except Forbidden:
                # User blocked the bot - remove from subscriptions
                logger.warning(f"User {user_id} blocked the bot, removing from subscriptions")
                remove_user(user_id)
            except Exception as e:
                logger.error(f"Error sending today's reading to new user {user_id}: {e}")
    
    def get_main_menu_keyboard(self):
        """Create comprehensive main menu inline keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📖 Today's Reading", callback_data="menu_today"),
                InlineKeyboardButton("📊 My Progress", callback_data="menu_progress")
            ],
            [
                InlineKeyboardButton("🎯 Start Quiz", callback_data="menu_quiz"),
                InlineKeyboardButton("⭐ Daily Challenge", callback_data="menu_daily_quiz")
            ],
            [
                InlineKeyboardButton("📖 Verse of Day", callback_data="menu_verse"),
                InlineKeyboardButton("🏆 Achievements", callback_data="menu_achievements")
            ],
            [
                InlineKeyboardButton("📈 Leaderboard", callback_data="menu_leaderboard"),
                InlineKeyboardButton("🔥 My Streak", callback_data="menu_streak")
            ],
            [
                InlineKeyboardButton("❓ Ask Question", callback_data="menu_ask"),
                InlineKeyboardButton("📚 Search", callback_data="menu_search")
            ],
            [
                InlineKeyboardButton("⏰ Reminders", callback_data="menu_reminders"),
                InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_quiz_menu_keyboard(self):
        """Create enhanced quiz difficulty selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🟢 Easy Quiz", callback_data="quiz_easy"),
                InlineKeyboardButton("🟡 Medium Quiz", callback_data="quiz_medium")
            ],
            [
                InlineKeyboardButton("🔴 Hard Quiz", callback_data="quiz_hard"),
                InlineKeyboardButton("🎲 Random Quiz", callback_data="quiz_random")
            ],
            [
                InlineKeyboardButton("⭐ Daily Challenge", callback_data="menu_daily_quiz")
            ],
            [
                InlineKeyboardButton("📊 My Score", callback_data="menu_score"),
                InlineKeyboardButton("🏆 Leaderboard", callback_data="menu_leaderboard")
            ],
            [
                InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_reading_menu_keyboard(self):
        """Create enhanced reading menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📖 Today", callback_data="reading_today"),
                InlineKeyboardButton("📅 Pick Day", callback_data="reading_pick")
            ],
            [
                InlineKeyboardButton("📊 Progress", callback_data="menu_progress"),
                InlineKeyboardButton("🔥 Streak", callback_data="menu_streak")
            ],
            [
                InlineKeyboardButton("📈 Stats", callback_data="menu_stats"),
                InlineKeyboardButton("📚 Search", callback_data="menu_search")
            ],
            [
                InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_quick_actions_keyboard(self):
        """Create quick action buttons for common commands"""
        keyboard = [
            [
                InlineKeyboardButton("📖 Today", callback_data="menu_today"),
                InlineKeyboardButton("🎯 Quiz", callback_data="menu_quiz"),
                InlineKeyboardButton("📊 Progress", callback_data="menu_progress")
            ],
            [
                InlineKeyboardButton("⭐ Challenge", callback_data="menu_daily_quiz"),
                InlineKeyboardButton("📖 Verse", callback_data="menu_verse"),
                InlineKeyboardButton("🏆 Badges", callback_data="menu_achievements")
            ],
            [
                InlineKeyboardButton("📈 Leaderboard", callback_data="menu_leaderboard"),
                InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command - show enhanced main menu"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Get user stats for personalized menu
        progress = get_user_progress(user_id)
        current_streak = get_current_streak(user_id)
        score = get_user_score(user_id)
        
        menu_text = f"""📱 *Main Menu*

👋 Welcome! Choose an option below:

📊 *Quick Stats:*
• Reading: {progress['total_completed']} days completed
• Streak: {current_streak} days 🔥
• Quiz Score: {score.get('total_correct', 0)} correct answers

{MESSAGE_SEPARATOR}
*Tap a button to get started!* 👇"""
        
        await update.message.reply_text(
            menu_text,
            parse_mode='Markdown',
            reply_markup=self.get_main_menu_keyboard()
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        # Ensure user is subscribed
        self._ensure_subscribed(update.effective_user.id)
        
        help_text = """📖 *Bible in a Year Bot - Help*

*🎯 Main Features:*
Everything is button-based! Just tap the buttons below to interact.

*📚 Reading Commands:*
/today - Get today's Bible reading
/day [number] - Get reading for a specific day (1-365)
/search [book] - Search for a Bible book in the reading plan

*🎯 Quiz Commands:*
/quiz - Start a random Bible quiz
/quiz_easy - Start an easy quiz
/quiz_medium - Start a medium quiz
/quiz_hard - Start a hard quiz
/daily_quiz or /challenge - Take today's special daily challenge quiz
/score - View your quiz statistics and rank
/leaderboard - See top 10 players
/quiz_stop - Stop your current quiz session

*⭐ New Features:*
/daily_quiz - Take today's special quiz challenge (one per day)
/verse - Get today's inspiring Bible verse
/verse [reference] - Get a specific verse (e.g., /verse John 3:16)
/achievements or /badges - View your unlocked achievements
/remind [time] - Set reading reminders (e.g., /remind 8am)
/remind_off - Disable reading reminders

*❓ Q&A Commands:*
/ask [question] - Ask a Bible question and get an answer
/question [question] - Same as /ask

*📊 Reading Progress:*
/progress - View your reading progress
/streak - See your current reading streak
/stats - Detailed reading statistics
/completed [day] - Mark a specific day as completed

*📊 Quiz Features:*
• 280+ questions covering all 66 books of the Bible
• Difficulty levels: Easy, Medium, Hard
• Daily Challenge Quiz - one special quiz per day
• Leaderboard rankings based on best scores
• Achievement badges for milestones

*🏆 Achievements:*
Unlock badges by:
• Completing readings
• Maintaining streaks
• Answering quiz questions
• Completing daily challenges

*📬 Daily Messages:*
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
            is_valid, day_number, error_msg = self._validate_day_number(context.args[0])
            if not is_valid:
                await update.message.reply_text(error_msg)
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
        """Handle /search command - search for Bible books in the reading plan"""
        # Ensure user is subscribed
        self._ensure_subscribed(update.effective_user.id)
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
        
        search_term = ' '.join(context.args).strip()
        is_valid, error_msg = self._validate_search_term(search_term)
        if not is_valid:
            await update.message.reply_text(error_msg, parse_mode='Markdown')
            return
        
        search_term = search_term.lower()
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
    
    async def quiz_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quiz command - start a Bible quiz"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Check if user already has an active quiz
        active_quiz = get_quiz_session(user_id)
        if active_quiz:
            await update.message.reply_text(
                "🎯 *You already have an active quiz!*\n\n"
                f"Current score: {active_quiz['score']}/{active_quiz['total']}\n\n"
                "Answer the current question or use /quiz_stop to start a new quiz."
            )
            return
        
        # Parse optional arguments for difficulty and category
        difficulty = None
        category = None
        
        if context.args:
            args_lower = [arg.lower() for arg in context.args]
            
            # Check for difficulty
            for diff in DIFFICULTIES:
                if diff in args_lower:
                    difficulty = diff
                    break
            
            # Check for category
            for cat_key, cat_name in CATEGORIES.items():
                if cat_key in args_lower or cat_name.lower() in args_lower:
                    category = cat_key
                    break
        
        # Start a new quiz with optional filters
        # Get recently asked question indices for this user to avoid repeats
        from quiz_questions import get_question_index
        recent_indices = self._recent_questions.get(str(user_id), [])
        
        question = get_random_question(difficulty=difficulty, category=category, exclude_indices=recent_indices)
        
        # Track this question to avoid repeats
        question_index = get_question_index(question)
        if question_index is not None:
            if str(user_id) not in self._recent_questions:
                self._recent_questions[str(user_id)] = []
            self._recent_questions[str(user_id)].append(question_index)
            # Keep only last MAX_RECENT_QUESTIONS to avoid memory issues
            if len(self._recent_questions[str(user_id)]) > MAX_RECENT_QUESTIONS:
                self._recent_questions[str(user_id)] = self._recent_questions[str(user_id)][-MAX_RECENT_QUESTIONS:]
        
        # Try to save to file, but also save in-memory as fallback
        try:
            start_quiz_session(user_id, 0, question, difficulty=difficulty, category=category)
        except Exception as e:
            logger.error(f"Error starting quiz session in file for user {user_id}: {e}")
        
        # Always save in-memory as fallback
        user_id_str = str(user_id)
        self._in_memory_quizzes[user_id_str] = {
            'question_index': 0,
            'question_data': question,
            'score': 0,
            'total': 0,
            'started_at': None,
            'difficulty': difficulty,
            'category': category
        }
        
        # Format question with options
        options_text = ""
        for i, option in enumerate(question['options']):
            options_text += f"{i+1}. {option}\n"
        
        # Build difficulty and category info
        diff_info = f"Difficulty: {question.get('difficulty', 'unknown').title()}\n" if question.get('difficulty') else ""
        cat_info = f"Category: {CATEGORIES.get(question.get('category', ''), 'General')}\n" if question.get('category') else ""
        
        # Use HTML parse mode to avoid Markdown escaping issues
        quiz_message = f"""🎯 <b>Bible Quiz Started!</b>

{diff_info}{cat_info}<b>Question:</b>
{question['question']}

<b>Tap your answer below:</b>"""
        
        await update.message.reply_text(
            quiz_message, 
            parse_mode='HTML',
            reply_markup=self.get_quiz_answer_keyboard(question)
        )
        logger.info(f"User {user_id} started a quiz (difficulty: {difficulty}, category: {category})")
    
    async def quiz_easy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quiz_easy command - start an easy quiz"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Check if user already has an active quiz
        active_quiz = get_quiz_session(user_id)
        if active_quiz:
            await update.message.reply_text(
                "🎯 *You already have an active quiz!*\n\n"
                f"Current score: {active_quiz['score']}/{active_quiz['total']}\n\n"
                "Answer the current question or use /quiz_stop to start a new quiz."
            )
            return
        
        # Start a new quiz with easy difficulty
        from quiz_questions import get_question_index
        recent_indices = self._recent_questions.get(str(user_id), [])
        question = get_random_question(difficulty="easy", exclude_indices=recent_indices)
        
        # Track this question to avoid repeats
        question_index = get_question_index(question)
        if question_index is not None:
            if str(user_id) not in self._recent_questions:
                self._recent_questions[str(user_id)] = []
            self._recent_questions[str(user_id)].append(question_index)
            if len(self._recent_questions[str(user_id)]) > MAX_RECENT_QUESTIONS:
                self._recent_questions[str(user_id)] = self._recent_questions[str(user_id)][-MAX_RECENT_QUESTIONS:]
        
        # Try to save to file, but also save in-memory as fallback
        try:
            start_quiz_session(user_id, 0, question, difficulty="easy", category=None)
        except Exception as e:
            logger.error(f"Error starting quiz session in file for user {user_id}: {e}")
        
        # Always save in-memory as fallback
        user_id_str = str(user_id)
        self._in_memory_quizzes[user_id_str] = {
            'question_index': 0,
            'question_data': question,
            'score': 0,
            'total': 0,
            'started_at': None,
            'difficulty': "easy",
            'category': None
        }
        
        # Format question with options
        options_text = ""
        for i, option in enumerate(question['options']):
            options_text += f"{i+1}. {option}\n"
        
        quiz_message = f"""🎯 <b>Easy Bible Quiz Started!</b>

<b>Question:</b>
{question['question']}

<b>Tap your answer below:</b>"""
        
        await update.message.reply_text(
            quiz_message, 
            parse_mode='HTML',
            reply_markup=self.get_quiz_answer_keyboard(question)
        )
        logger.info(f"User {user_id} started an easy quiz")
    
    async def quiz_medium_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quiz_medium command - start a medium quiz"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Check if user already has an active quiz
        active_quiz = get_quiz_session(user_id)
        if active_quiz:
            await update.message.reply_text(
                "🎯 *You already have an active quiz!*\n\n"
                f"Current score: {active_quiz['score']}/{active_quiz['total']}\n\n"
                "Answer the current question or use /quiz_stop to start a new quiz."
            )
            return
        
        # Start a new quiz with medium difficulty
        from quiz_questions import get_question_index
        recent_indices = self._recent_questions.get(str(user_id), [])
        question = get_random_question(difficulty="medium", exclude_indices=recent_indices)
        
        # Track this question to avoid repeats
        question_index = get_question_index(question)
        if question_index is not None:
            if str(user_id) not in self._recent_questions:
                self._recent_questions[str(user_id)] = []
            self._recent_questions[str(user_id)].append(question_index)
            if len(self._recent_questions[str(user_id)]) > MAX_RECENT_QUESTIONS:
                self._recent_questions[str(user_id)] = self._recent_questions[str(user_id)][-MAX_RECENT_QUESTIONS:]
        
        # Try to save to file, but also save in-memory as fallback
        try:
            start_quiz_session(user_id, 0, question, difficulty="medium", category=None)
        except Exception as e:
            logger.error(f"Error starting quiz session in file for user {user_id}: {e}")
        
        # Always save in-memory as fallback
        user_id_str = str(user_id)
        self._in_memory_quizzes[user_id_str] = {
            'question_index': 0,
            'question_data': question,
            'score': 0,
            'total': 0,
            'started_at': None,
            'difficulty': "medium",
            'category': None
        }
        
        # Format question with options
        options_text = ""
        for i, option in enumerate(question['options']):
            options_text += f"{i+1}. {option}\n"
        
        quiz_message = f"""🎯 <b>Medium Bible Quiz Started!</b>

<b>Question:</b>
{question['question']}

<b>Tap your answer below:</b>"""
        
        await update.message.reply_text(
            quiz_message, 
            parse_mode='HTML',
            reply_markup=self.get_quiz_answer_keyboard(question)
        )
        logger.info(f"User {user_id} started a medium quiz")
    
    async def quiz_hard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quiz_hard command - start a hard quiz"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Check if user already has an active quiz
        active_quiz = get_quiz_session(user_id)
        if active_quiz:
            await update.message.reply_text(
                "🎯 *You already have an active quiz!*\n\n"
                f"Current score: {active_quiz['score']}/{active_quiz['total']}\n\n"
                "Answer the current question or use /quiz_stop to start a new quiz."
            )
            return
        
        # Start a new quiz with hard difficulty
        from quiz_questions import get_question_index
        recent_indices = self._recent_questions.get(str(user_id), [])
        question = get_random_question(difficulty="hard", exclude_indices=recent_indices)
        
        # Track this question to avoid repeats
        question_index = get_question_index(question)
        if question_index is not None:
            if str(user_id) not in self._recent_questions:
                self._recent_questions[str(user_id)] = []
            self._recent_questions[str(user_id)].append(question_index)
            if len(self._recent_questions[str(user_id)]) > MAX_RECENT_QUESTIONS:
                self._recent_questions[str(user_id)] = self._recent_questions[str(user_id)][-MAX_RECENT_QUESTIONS:]
        
        # Try to save to file, but also save in-memory as fallback
        try:
            start_quiz_session(user_id, 0, question, difficulty="hard", category=None)
        except Exception as e:
            logger.error(f"Error starting quiz session in file for user {user_id}: {e}")
        
        # Always save in-memory as fallback
        user_id_str = str(user_id)
        self._in_memory_quizzes[user_id_str] = {
            'question_index': 0,
            'question_data': question,
            'score': 0,
            'total': 0,
            'started_at': None,
            'difficulty': "hard",
            'category': None
        }
        
        # Format question with options
        options_text = ""
        for i, option in enumerate(question['options']):
            options_text += f"{i+1}. {option}\n"
        
        quiz_message = f"""🎯 <b>Hard Bible Quiz Started!</b>

<b>Question:</b>
{question['question']}

<b>Tap your answer below:</b>"""
        
        await update.message.reply_text(
            quiz_message, 
            parse_mode='HTML',
            reply_markup=self.get_quiz_answer_keyboard(question)
        )
        logger.info(f"User {user_id} started a hard quiz")
    
    async def score_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /score command - show user's quiz statistics"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        score = get_user_score(user_id)
        stats = get_stats()
        
        if score['total_answered'] == 0:
            stats_info = f"""📚 *Quiz Database:*
• Total Questions: {stats['total']}
• Easy: {stats['by_difficulty']['easy']}
• Medium: {stats['by_difficulty']['medium']}
• Hard: {stats['by_difficulty']['hard']}

*Categories:*
• Old Testament: {stats['by_category']['old_testament']}
• New Testament: {stats['by_category']['new_testament']}
• Bible Facts: {stats['by_category']['bible_facts']}"""
            
            await update.message.reply_text(
                "📊 *Your Quiz Score*\n\n"
                "You haven't taken any quizzes yet!\n\n"
                f"{stats_info}\n\n"
                "Use /quiz to start your first Bible quiz! 🎯\n\n"
                "*Try:*\n"
                "• /quiz easy - Easy questions\n"
                "• /quiz medium - Medium difficulty\n"
                "• /quiz hard - Hard questions\n"
                "• /quiz old_testament - OT questions\n"
                "• /quiz new_testament - NT questions"
            )
            return
        
        accuracy = (score['total_correct'] / score['total_answered']) * 100 if score['total_answered'] > 0 else 0
        
        # Build rank info
        rank_info = ""
        user_rank, total_players = get_user_rank(user_id)
        if user_rank:
            rank_info = f"🏅 *Rank:* #{user_rank}\n"
        
        # Get best session info
        best_session_score = score.get('best_session_score', 0)
        best_session_total = score.get('best_session_total', 0)
        best_session_info = ""
        if best_session_total > 0:
            best_session_accuracy = (best_session_score / best_session_total) * 100
            best_session_info = f"🏆 *Best Quiz Session:* {best_session_score}/{best_session_total} ({best_session_accuracy:.1f}%)\n"
        
        score_message = f"""📊 *Your Quiz Statistics*

{rank_info}✅ *Total Correct:* {score['total_correct']}
📝 *Total Answered:* {score['total_answered']}
📈 *Overall Accuracy:* {accuracy:.1f}%
{best_session_info}📚 *Quizzes Completed:* {score.get('quizzes_completed', 0)}

*Quiz Options:*
• /quiz - Random question
• /quiz_easy - Easy questions only
• /quiz_medium - Medium difficulty only
• /quiz_hard - Hard questions only
• /quiz old_testament - Old Testament
• /quiz new_testament - New Testament
• /quiz bible_facts - Bible Facts

*Leaderboard:*
• /leaderboard - See top players

Keep learning! Use /quiz to take another quiz."""
        
        await update.message.reply_text(score_message, parse_mode='Markdown')
    
    async def leaderboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /leaderboard command - show top players"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Update user info
        user = update.effective_user
        update_user_info(user_id, username=user.username, first_name=user.first_name)
        
        leaderboard = get_leaderboard(limit=LEADERBOARD_TOP_N)
        user_rank, user_data = get_user_rank(user_id)
        
        if not leaderboard:
            await update.message.reply_text(
                "🏆 *Leaderboard*\n\n"
                "No players yet! Be the first to take a quiz with /quiz"
            )
            return
        
        # Build leaderboard message
        leaderboard_text = "🏆 *Top Players Leaderboard*\n\n"
        
        medals = ["🥇", "🥈", "🥉"]
        for idx, player in enumerate(leaderboard, start=1):
            medal = medals[idx - 1] if idx <= 3 else f"{idx}."
            
            # Get display name
            display_name = player.get('username')
            if not display_name:
                display_name = player.get('first_name', f"User {player['user_id']}")
            if display_name:
                display_name = f"@{display_name}" if player.get('username') else display_name
            
            leaderboard_text += f"{medal} {display_name}\n"
            leaderboard_text += f"   Best: {player['best_score']:.1f}% | "
            leaderboard_text += f"Correct: {player['total_correct']}/{player['total_answered']} | "
            leaderboard_text += f"Quizzes: {player['quizzes_completed']}\n\n"
        
        # Add user's rank if they're not in top LEADERBOARD_TOP_N
        if user_rank and user_rank > LEADERBOARD_TOP_N:
            user_accuracy = (user_data['total_correct'] / user_data['total_answered']) * 100 if user_data['total_answered'] > 0 else 0
            user_display = user.username if user.username else user.first_name
            if user.username:
                user_display = f"@{user_display}"
            
            leaderboard_text += f"{MESSAGE_SEPARATOR}\n"
            leaderboard_text += f"Your Rank: #{user_rank}\n"
            leaderboard_text += f"Best: {user_data['best_score']:.1f}% | "
            leaderboard_text += f"Correct: {user_data['total_correct']}/{user_data['total_answered']}\n"
        
        leaderboard_text += "\n*Commands:*\n"
        leaderboard_text += "• /quiz_easy - Easy questions\n"
        leaderboard_text += "• /quiz_medium - Medium questions\n"
        leaderboard_text += "• /quiz_hard - Hard questions\n"
        leaderboard_text += "• /score - Your stats"
        
        await update.message.reply_text(
            leaderboard_text, 
            parse_mode='Markdown',
            reply_markup=self.get_main_menu_keyboard()
        )
    
    async def quiz_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quiz_stop command - stop current quiz"""
        user_id = update.effective_user.id
        
        # Check in-memory first
        session = None
        if str(user_id) in self._in_memory_quizzes:
            session = self._in_memory_quizzes[str(user_id)]
            del self._in_memory_quizzes[str(user_id)]
        
        # Also check file-based storage
        if not session:
            session = end_quiz_session(user_id)
        
        if session:
            # Check if this was a daily quiz
            is_daily_quiz = session.get('is_daily_quiz', False)
            
            # Save the quiz results
            if session['total'] > 0:
                user = update.effective_user
                update_user_score(
                    user_id, 
                    session['score'], 
                    session['total'],
                    username=user.username,
                    first_name=user.first_name
                )
                accuracy = (session['score'] / session['total']) * 100
                
                # Mark daily quiz as completed if applicable
                if is_daily_quiz:
                    mark_daily_quiz_completed(user_id, session['score'], session['total'])
                    # Check for achievements
                    newly_unlocked = check_and_award_achievements(user_id)
                    
                    message = f"✅ *Daily Challenge Completed!*\n\n"
                    message += f"Final Score: {session['score']}/{session['total']} ({accuracy:.1f}%)\n\n"
                    
                    if newly_unlocked:
                        message += "🎉 *New Achievement Unlocked!*\n\n"
                        for achievement_id in newly_unlocked:
                            achievement = ACHIEVEMENTS[achievement_id]
                            message += f"{achievement['emoji']} {achievement['name']}\n"
                        message += "\n"
                    
                    message += "Come back tomorrow for a new challenge!"
                    
                    await update.message.reply_text(
                        message,
                        parse_mode='Markdown',
                        reply_markup=self.get_main_menu_keyboard()
                    )
                else:
                    await update.message.reply_text(
                        f"✅ *Quiz Ended*\n\n"
                        f"Final Score: {session['score']}/{session['total']} ({accuracy:.1f}%)\n\n"
                        f"Use the buttons below to continue!",
                        parse_mode='Markdown',
                        reply_markup=self.get_main_menu_keyboard()
                    )
            else:
                await update.message.reply_text(
                    "✅ Quiz session ended.\n\n"
                    "Use the buttons below to continue!",
                    reply_markup=self.get_main_menu_keyboard()
                )
        else:
            await update.message.reply_text(
                "You don't have an active quiz session.\n\n"
                "Use the buttons below to start a quiz!",
                reply_markup=self.get_main_menu_keyboard()
            )
    
    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ask command - answer Bible questions with references"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Get the question from command arguments
        if not context.args:
            topics = get_all_topics()
            topics_list = "\n".join([f"• {topic}" for topic in topics[:15]])
            
            await update.message.reply_text(
                f"❓ *Ask a Bible Question*\n\n"
                f"Ask me any Bible-related question and I'll provide an answer with Bible references!\n\n"
                f"*Examples:*\n"
                f"• /ask How can I be saved?\n"
                f"• /ask What does the Bible say about love?\n"
                f"• /ask How should I pray?\n"
                f"• /ask What is faith?\n\n"
                f"*Topics I can help with:*\n"
                f"{topics_list}\n"
                f"... and more!\n\n"
                f"Just type: /ask [your question]"
            )
            return
        
        # Combine all arguments into a question
        user_question = " ".join(context.args)
        
        # Validate question
        is_valid, error_msg = self._validate_question(user_question)
        if not is_valid:
            await update.message.reply_text(error_msg, parse_mode='Markdown')
            return
        
        # Find matching answer
        answer_data = find_answer(user_question)
        
        if answer_data:
            # Format the answer with references (use HTML to avoid Markdown issues)
            response = f"❓ <b>Question:</b> {answer_data['question']}\n\n"
            response += f"💡 <b>Answer:</b>\n{answer_data['answer']}\n\n"
            response += "📖 <b>Bible References:</b>\n"
            
            for ref in answer_data['references']:
                # Escape HTML special characters in references
                ref_escaped = ref.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                response += f"• {ref_escaped}\n"
            
            response += "\n💡 <b>Tip:</b> Use /ask [question] to ask more questions!"
            
            try:
                await update.message.reply_text(response, parse_mode='HTML')
            except Exception as e:
                logger.error(f"Error sending ask response: {e}")
                # Fallback to plain text
                response_plain = response.replace('<b>', '').replace('</b>', '').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                await update.message.reply_text(response_plain)
            
            logger.info(f"User {user_id} asked: {user_question}")
        else:
            # No good match found
            await update.message.reply_text(
                f"❓ *Question Not Found*\n\n"
                f"I couldn't find a specific answer for: \"{user_question}\"\n\n"
                f"*Try asking about:*\n"
                f"• Salvation and forgiveness\n"
                f"• God's love and grace\n"
                f"• Prayer and faith\n"
                f"• Hope and peace\n"
                f"• Wisdom and purpose\n"
                f"• Marriage and relationships\n"
                f"• Money and finances\n"
                f"• Suffering and trials\n\n"
                f"*Examples:*\n"
                f"• /ask How can I be saved?\n"
                f"• /ask What does the Bible say about love?\n"
                f"• /ask How should I pray?\n\n"
                f"Or use /quiz to test your Bible knowledge!"
            )
    
    async def handle_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text queries (non-command messages) - only for natural language questions"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        text = update.message.text.strip()
        text_lower = text.lower()
        
        # Check if user has an active quiz session
        # If they do, remind them to use buttons instead of typing
        active_quiz = None
        try:
            active_quiz = get_quiz_session(user_id)
        except Exception as e:
            logger.error(f"Error getting quiz session from file for user {user_id}: {e}")
        
        # Fallback to in-memory storage if file storage failed
        if not active_quiz and str(user_id) in self._in_memory_quizzes:
            active_quiz = self._in_memory_quizzes[str(user_id)]
            logger.info(f"Using in-memory quiz session for user {user_id}")
        
        if active_quiz and 'question_data' in active_quiz:
            # User has an active quiz - remind them to use buttons
            await update.message.reply_text(
                "🎯 *You have an active quiz!*\n\n"
                "Please use the answer buttons below the question to select your answer.\n\n"
                "If you want to ask a Bible question instead, use the '❓ Ask Question' button from the main menu.",
                parse_mode='Markdown',
                reply_markup=self.get_quiz_answer_keyboard(active_quiz['question_data'])
            )
            return
        
        # No active quiz - treat as a Bible question or query
        
        # Check for day number queries
        day_match = re.search(r'\bday\s+(\d+)\b', text)
        if day_match:
            day_number = int(day_match.group(1))
            if 1 <= day_number <= DAYS_IN_YEAR:
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
        
        # Default: treat as a Bible question
        # Try to find an answer using the Q&A system
        answer = find_answer(text)
        if answer:
            await update.message.reply_text(
                answer,
                parse_mode='Markdown',
                reply_markup=self.get_quick_actions_keyboard()
            )
        else:
            # If no answer found, show main menu and suggest using buttons
            await update.message.reply_text(
                "❓ *I didn't understand that question.*\n\n"
                "You can:\n"
                "• Ask me a Bible question (e.g., 'What does the Bible say about love?')\n"
                "• Use the buttons below to navigate\n"
                "• Type 'day 45' to get a specific day's reading\n"
                "• Type 'today' to get today's reading\n\n"
                "*Tip: Use the buttons below for easier navigation!* 👇",
                parse_mode='Markdown',
                reply_markup=self.get_main_menu_keyboard()
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
            return 0, 0
        
        logger.info(f"Sending daily reading to {len(users)} subscribed users")
        
        success_count = 0
        failed_users = []
        for user_id in users:
            if await self.send_daily_to_user(user_id):
                success_count += 1
            else:
                failed_users.append(user_id)
            await asyncio.sleep(0.1)  # Small delay to avoid rate limiting
        
        logger.info(f"Successfully sent to {success_count}/{len(users)} users")
        if failed_users:
            logger.warning(f"Failed to send to users: {failed_users}")
        
        return success_count, len(users)
    
    async def daily_quiz_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /daily_quiz command - take today's special quiz"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Check if already completed
        if has_completed_daily_quiz(user_id):
            stats = get_daily_quiz_stats(user_id)
            await update.message.reply_text(
                f"✅ *Daily Challenge Completed!*\n\n"
                f"You've already completed today's challenge!\n\n"
                f"*Your Daily Challenge Stats:*\n"
                f"• Total Completed: {stats['total_completed']}\n"
                f"• Current Streak: {stats['current_streak']} days\n"
                f"• Best Score: {stats['best_score']:.1f}%\n\n"
                f"Come back tomorrow for a new challenge!",
                parse_mode='Markdown',
                reply_markup=self.get_quick_actions_keyboard()
            )
            return
        
        # Get today's question
        question = get_today_quiz_question()
        
        # Check if user has active quiz
        active_quiz = get_quiz_session(user_id)
        if active_quiz:
            await update.message.reply_text(
                "🎯 *You already have an active quiz!*\n\n"
                f"Current score: {active_quiz['score']}/{active_quiz['total']}\n\n"
                "Complete or stop your current quiz first.",
                parse_mode='Markdown',
                reply_markup=self.get_quick_actions_keyboard()
            )
            return
        
        # Start daily quiz session
        try:
            start_quiz_session(user_id, 0, question, difficulty=question.get('difficulty'), category=question.get('category'))
        except Exception as e:
            logger.error(f"Error starting daily quiz session: {e}")
        
        user_id_str = str(user_id)
        self._in_memory_quizzes[user_id_str] = {
            'question_index': 0,
            'question_data': question,
            'score': 0,
            'total': 0,
            'started_at': None,
            'difficulty': question.get('difficulty'),
            'category': question.get('category'),
            'is_daily_quiz': True  # Mark as daily quiz
        }
        
        quiz_message = f"""⭐ <b>Daily Challenge Quiz!</b>

{MESSAGE_SEPARATOR}

🎯 <b>Today's Special Question:</b>
{question['question']}

{MESSAGE_SEPARATOR}

<b>Tap your answer below:</b>

💡 <i>Complete today's challenge to earn points and maintain your streak!</i>"""
        
        await update.message.reply_text(
            quiz_message,
            parse_mode='HTML',
            reply_markup=self.get_quiz_answer_keyboard(question)
        )
    
    async def verse_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /verse command - get verse of the day or specific verse"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        if not context.args:
            # Show verse of the day
            verse_data = get_verse_of_the_day()
            verse_text = f"""📖 <b>Verse of the Day</b>

{MESSAGE_SEPARATOR}

<b>{verse_data['reference']}</b>

{verse_data['verse']}

{MESSAGE_SEPARATOR}

💡 <i>Topic: {verse_data['topic']}</i>

*Use /verse [reference] to get a specific verse*
*Example: /verse John 3:16*"""
            
            await update.message.reply_text(
                verse_text,
                parse_mode='HTML',
                reply_markup=self.get_verse_keyboard()
            )
            return
        
        # Try to get specific verse
        verse_input = " ".join(context.args)
        
        # Validate verse reference
        is_valid, error_msg = self._validate_verse_reference(verse_input)
        if not is_valid:
            await update.message.reply_text(error_msg, parse_mode='Markdown')
            return
        
        # Try as reference first
        verse_data = get_verse_by_reference(verse_input)
        
        if not verse_data:
            # Try search
            matches = search_verses(verse_input)
            if matches:
                verse_data = matches[0]  # Use first match
            else:
                await update.message.reply_text(
                    f"❓ *Verse Not Found*\n\n"
                    f"Couldn't find a verse matching '{verse_input}'.\n\n"
                    f"*Try:*\n"
                    f"• /verse - Get today's verse\n"
                    f"• /verse John 3:16 - Get specific verse\n"
                    f"• /verse love - Search by keyword",
                    parse_mode='Markdown',
                    reply_markup=self.get_quick_actions_keyboard()
                )
                return
        
        verse_text = f"""📖 <b>{verse_data['reference']}</b>

{MESSAGE_SEPARATOR}

{verse_data['verse']}

{MESSAGE_SEPARATOR}

💡 <i>Topic: {verse_data['topic']}</i>"""
        
        await update.message.reply_text(
            verse_text,
            parse_mode='HTML',
            reply_markup=self.get_verse_keyboard()
        )
    
    async def achievements_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /achievements command - show user's achievements"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        # Check for new achievements
        from reading_progress import get_user_progress
        from quiz_storage import get_user_score
        from daily_quiz import get_daily_quiz_stats
        
        reading_progress = get_user_progress(user_id)
        quiz_stats = get_user_score(user_id)
        daily_quiz_stats = get_daily_quiz_stats(user_id)
        
        newly_unlocked = check_and_award_achievements(
            user_id, reading_progress, quiz_stats, daily_quiz_stats
        )
        
        display = get_achievement_display(user_id)
        
        # Show notification if new achievements unlocked
        if newly_unlocked:
            notification = "🎉 *New Achievement Unlocked!*\n\n"
            for achievement_id in newly_unlocked:
                achievement = ACHIEVEMENTS[achievement_id]
                notification += f"{achievement['emoji']} *{achievement['name']}*\n"
                notification += f"   {achievement['description']}\n\n"
            notification += f"{MESSAGE_SEPARATOR}\n\n"
            display = notification + display
        
        await update.message.reply_text(
            display,
            parse_mode='Markdown',
            reply_markup=self.get_back_to_menu_keyboard()
        )
    
    async def remind_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /remind command - set reading reminder"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        if not context.args:
            # Show current reminders
            reminders = get_user_reminders(user_id)
            if reminders['enabled'] and reminders['times']:
                times_list = "\n".join([f"• {time}" for time in reminders['times']])
                reminder_text = f"""⏰ *Your Reading Reminders*

{MESSAGE_SEPARATOR}

*Reminder Times:*
{times_list}

{MESSAGE_SEPARATOR}

*To add a reminder:*
/remind 8am
/remind 14:30
/remind 9:00pm

*To remove a reminder:*
/remind_off"""
            else:
                reminder_text = """⏰ *Reading Reminders*

{MESSAGE_SEPARATOR}

You don't have any reminders set.

*Set a reminder:*
/remind 8am
/remind 14:30
/remind 9:00pm

*Examples:*
• /remind 8am - Remind at 8:00 AM
• /remind 14:30 - Remind at 2:30 PM
• /remind 9:00pm - Remind at 9:00 PM"""
            
            await update.message.reply_text(
                reminder_text,
                parse_mode='Markdown',
                reply_markup=self.get_back_to_menu_keyboard()
            )
            return
        
        # Parse time
        time_str = " ".join(context.args)
        
        # Validate time string format
        is_valid, error_msg = self._validate_time_string(time_str)
        if not is_valid:
            await update.message.reply_text(error_msg, parse_mode='Markdown')
            return
        
        hour, minute = parse_time_string(time_str)
        
        if hour is None:
            await update.message.reply_text(
                "❌ *Invalid Time Format*\n\n"
                "*Examples:*\n"
                "• /remind 8am\n"
                "• /remind 14:30\n"
                "• /remind 9:00pm",
                parse_mode='Markdown',
                reply_markup=self.get_quick_actions_keyboard()
            )
            return
        
        if set_reminder(user_id, hour, minute):
            await update.message.reply_text(
                f"✅ *Reminder Set!*\n\n"
                f"You'll be reminded to read at {hour:02d}:{minute:02d} every day.\n\n"
                f"*Note:* Reminders are currently being set up. They will be active soon!",
                parse_mode='Markdown',
                reply_markup=self.get_quick_actions_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Error setting reminder. Please try again.",
                reply_markup=self.get_quick_actions_keyboard()
            )
    
    async def remind_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /remind_off command - disable reminders"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        if disable_reminders(user_id):
            await update.message.reply_text(
                "✅ *Reminders Disabled*\n\n"
                "You won't receive reading reminders anymore.\n\n"
                "Use /remind [time] to set them again.",
                parse_mode='Markdown',
                reply_markup=self.get_quick_actions_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Error disabling reminders. Please try again.",
                reply_markup=self.get_quick_actions_keyboard()
            )
    
    async def test_daily_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /test_daily command - manually test daily message sending"""
        # Ensure user is subscribed
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        await update.message.reply_text(
            "🔄 Testing daily message sending...\n\n"
            "This will send today's reading to all subscribed users."
        )
        
        try:
            success_count, total_users = await self.send_daily_to_all_subscribed()
            await update.message.reply_text(
                f"✅ Test completed!\n\n"
                f"Successfully sent to {success_count}/{total_users} users."
            )
            logger.info(f"User {user_id} manually tested daily message sending")
        except Exception as e:
            logger.error(f"Error in test_daily_command: {e}", exc_info=True)
            await update.message.reply_text(
                f"❌ Error testing daily messages:\n{str(e)}"
            )
    
    async def progress_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /progress command - show reading progress"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        progress = get_user_progress(user_id)
        current_streak = get_current_streak(user_id)
        longest_streak = get_longest_streak(user_id)
        current_day, _ = self.get_day_of_year()
        
        # Calculate days remaining
        total_days = 365
        current_year = datetime.now().year
        if current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0):
            total_days = 366
        
        days_remaining = total_days - current_day
        days_completed = progress['total_completed']
        
        # Create progress bar (visual representation)
        progress_bar_length = 20
        filled = int((progress['completion_percentage'] / 100) * progress_bar_length)
        progress_bar = "█" * filled + "░" * (progress_bar_length - filled)
        
        progress_text = f"""📊 *Your Reading Progress*

📖 *Completion:* {days_completed}/{total_days} days ({progress['completion_percentage']:.1f}%)
{progress_bar}

🔥 *Current Streak:* {current_streak} days
🏆 *Longest Streak:* {longest_streak} days

📅 *Today:* Day {current_day}
⏳ *Days Remaining:* {days_remaining}

💡 *Tip:* Use /today to read today's passage and automatically mark it as completed!

*Commands:*
• /streak - View your reading streak
• /stats - Detailed statistics
• /completed [day] - Mark a specific day as completed"""
        
        await update.message.reply_text(progress_text, parse_mode='Markdown')
    
    async def streak_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /streak command - show reading streak"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        current_streak = get_current_streak(user_id)
        longest_streak_this_year = get_longest_streak(user_id, year=datetime.now().year)
        longest_streak_all_time = get_longest_streak(user_id, year=None)  # All-time
        progress = get_user_progress(user_id)
        current_day, _ = self.get_day_of_year()
        
        # Check if today is completed
        today_completed = is_day_completed(user_id, current_day)
        
        streak_text = f"""🔥 *Your Reading Streak*

📅 *Current Streak:* {current_streak} days
🏆 *Longest Streak (This Year):* {longest_streak_this_year} days
🌟 *Longest Streak (All-Time):* {longest_streak_all_time} days

{"✅ Today's reading is completed!" if today_completed else "⚠️ Don't forget to read today! Use /today"}
        
💪 *Keep it up!* Consistency is key to completing the Bible in a Year.

*Commands:*
• /progress - Full progress overview
• /stats - Detailed statistics
• /today - Read today's passage"""
        
        await update.message.reply_text(
            streak_text, 
            parse_mode='Markdown',
            reply_markup=self.get_main_menu_keyboard()
        )
    
    async def completed_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /completed command - mark days as completed"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        if not context.args:
            # Show help
            await update.message.reply_text(
                "📝 *Mark Days as Completed*\n\n"
                "Usage: /completed [day number]\n\n"
                "Examples:\n"
                "• /completed 45 - Mark day 45 as completed\n"
                "• /completed 100 - Mark day 100 as completed\n\n"
                "💡 *Note:* Viewing /today automatically marks today as completed!\n\n"
                "Use /progress to see your completion status."
            )
            return
        
        try:
            day_number = int(context.args[0])
            if day_number < 1 or day_number > 365:
                await update.message.reply_text(
                    "Please enter a day number between 1 and 365."
                )
                return
            
            # Mark as completed
            if mark_day_completed(user_id, day_number):
                is_already = is_day_completed(user_id, day_number)
                if is_already:
                    await update.message.reply_text(
                        f"✅ Day {day_number} is already marked as completed!\n\n"
                        f"Use /progress to see your full reading progress."
                    )
                else:
                    await update.message.reply_text(
                        f"✅ Day {day_number} marked as completed!\n\n"
                        f"Use /progress to see your updated reading progress."
                    )
            else:
                await update.message.reply_text(
                    "❌ Error marking day as completed. Please try again."
                )
        except ValueError:
            await update.message.reply_text(
                "Please enter a valid day number (1-365).\n"
                "Example: /completed 45"
            )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - show detailed reading statistics"""
        user_id = update.effective_user.id
        self._ensure_subscribed(user_id)
        
        progress = get_user_progress(user_id)
        current_streak = get_current_streak(user_id)
        longest_streak = get_longest_streak(user_id)
        current_day, date_str = self.get_day_of_year()
        
        # Calculate statistics
        total_days = 365
        current_year = datetime.now().year
        if current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0):
            total_days = 366
        
        days_remaining = total_days - current_day
        days_completed = progress['total_completed']
        completion_rate = (days_completed / current_day * 100) if current_day > 0 else 0
        
        # Find last completed day
        last_completed = progress.get('last_completed', 'None')
        if last_completed:
            last_completed_text = f"Day {last_completed}"
        else:
            last_completed_text = "No days completed yet"
        
        stats_text = f"""📊 *Detailed Reading Statistics*

📖 *Overall Progress:*
• Days Completed: {days_completed}/{total_days}
• Completion: {progress['completion_percentage']:.1f}%
• Days Remaining: {days_remaining}

🔥 *Streaks:*
• Current Streak: {current_streak} days
• Longest Streak: {longest_streak} days

📅 *Current Status:*
• Today: Day {current_day} ({date_str})
• Last Completed: {last_completed_text}
• Completion Rate: {completion_rate:.1f}% (of days so far)

💡 *Tips:*
• Read every day to maintain your streak!
• Use /today to automatically mark today as completed
• Use /progress for a visual progress bar

*Commands:*
• /progress - Visual progress overview
• /streak - Streak information
• /completed [day] - Mark a day as completed"""
        
        await update.message.reply_text(
            stats_text, 
            parse_mode='Markdown',
            reply_markup=self.get_progress_navigation_keyboard()
        )
    
    async def safe_edit_message(self, query, text, parse_mode=None, reply_markup=None):
        """Safely edit a message, handling 'message not modified' errors"""
        try:
            await query.edit_message_text(
                text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
        except BadRequest as e:
            # "Message is not modified" is not a real error - just ignore it
            if "message is not modified" in str(e).lower():
                logger.debug(f"Message not modified (same content): {e}")
                return
            # For other BadRequest errors (like parsing errors), log and try to send new message
            logger.error(f"BadRequest error editing message: {e}")
            try:
                await query.message.reply_text(
                    text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup
                )
            except Exception as e2:
                logger.error(f"Error sending new message: {e2}")
        except Exception as e:
            logger.error(f"Unexpected error editing message: {e}")
            raise
    
    # ==================== Callback Handler Methods ====================
    # These methods handle specific groups of callbacks to keep handle_callback() manageable
    
    async def _handle_menu_callback(self, query, callback_data: str, user_id: int):
        """Handle menu-related callbacks"""
        if callback_data == "menu_main":
            await self.safe_edit_message(
                query,
                "📱 *Main Menu*\n\nChoose an option:",
                parse_mode='Markdown',
                reply_markup=self.get_main_menu_keyboard()
            )
        elif callback_data == "menu_today":
            day_number, date_str = self.get_day_of_year()
            reading = self.get_bible_reading(day_number)
            encouragement = self.get_encouragement(day_number)
            message = self.format_message(day_number, date_str, reading, encouragement)
            mark_day_completed(user_id, day_number)
            await self.safe_edit_message(query, 
                message,
                parse_mode='Markdown',
                reply_markup=self.get_reading_menu_keyboard()
            )
        elif callback_data == "menu_progress":
            from reading_progress import get_user_progress, get_current_streak, get_longest_streak
            progress = get_user_progress(user_id)
            current_streak = get_current_streak(user_id)
            longest_streak_this_year = get_longest_streak(user_id, year=datetime.now().year)
            longest_streak_all_time = get_longest_streak(user_id, year=None)
            current_day, _ = self.get_day_of_year()
            
            current_year = datetime.now().year
            is_leap_year = current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0)
            total_days = DAYS_IN_LEAP_YEAR if is_leap_year else DAYS_IN_YEAR
            
            days_remaining = total_days - current_day
            filled = int((progress['completion_percentage'] / 100) * PROGRESS_BAR_LENGTH)
            progress_bar = "█" * filled + "░" * (PROGRESS_BAR_LENGTH - filled)
            
            progress_text = f"""📊 *Your Reading Progress*

📖 *Completion:* {progress['total_completed']}/{total_days} days ({progress['completion_percentage']:.1f}%)
{progress_bar}

🔥 *Current Streak:* {current_streak} days
🏆 *Longest Streak (This Year):* {longest_streak_this_year} days
🌟 *Longest Streak (All-Time):* {longest_streak_all_time} days

📅 *Today:* Day {current_day}
⏳ *Days Remaining:* {days_remaining}"""
            
            keyboard = [
                [InlineKeyboardButton("🔥 View Streak", callback_data="menu_streak")],
                [InlineKeyboardButton("📈 Detailed Stats", callback_data="menu_stats")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                progress_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif callback_data == "menu_streak":
            from reading_progress import get_current_streak, get_longest_streak, is_day_completed
            current_streak = get_current_streak(user_id)
            longest_streak_this_year = get_longest_streak(user_id, year=datetime.now().year)
            longest_streak_all_time = get_longest_streak(user_id, year=None)
            current_day, _ = self.get_day_of_year()
            today_completed = is_day_completed(user_id, current_day)
            
            today_status = "✅ Today's reading is completed!" if today_completed else "⚠️ Don't forget to read today! Use /today"
            
            streak_text = f"""🔥 *Your Reading Streak*

📅 *Current Streak:* {current_streak} days
🏆 *Longest Streak \\(This Year\\):* {longest_streak_this_year} days
🌟 *Longest Streak \\(All-Time\\):* {longest_streak_all_time} days

{today_status}
        
💪 *Keep it up!* Consistency is key."""
            
            keyboard = [
                [InlineKeyboardButton("📊 View Progress", callback_data="menu_progress")],
                [InlineKeyboardButton("📖 Read Today", callback_data="menu_today")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                streak_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif callback_data == "menu_quiz":
            quiz_text = f"""🎯 *Bible Quiz*

Choose your difficulty level:
• 🟢 Easy - Beginner questions
• 🟡 Medium - Intermediate questions  
• 🔴 Hard - Advanced questions
• 🎲 Random - Mixed difficulty

*{TOTAL_QUIZ_QUESTIONS}+ questions covering all 66 books of the Bible!*"""
            
            await self.safe_edit_message(query, 
                quiz_text,
                parse_mode='Markdown',
                reply_markup=self.get_quiz_menu_keyboard()
            )
        elif callback_data == "menu_help":
            help_text = f"""📖 *Bible in a Year Bot - Help*

{MESSAGE_SEPARATOR}

*🎯 Main Features:*
Everything is button-based! Just tap the buttons to interact.

*📚 Reading:*
• /today - Get today's Bible reading
• /day [number] - Get reading for a specific day
• /search [book] - Search for a Bible book

*🎯 Quiz:*
• /quiz - Start a random Bible quiz
• /daily_quiz - Take today's special challenge
• /score - View your statistics
• /leaderboard - See top players

*⭐ New Features:*
• /verse - Get verse of the day
• /achievements - View your badges
• /remind [time] - Set reading reminders

{MESSAGE_SEPARATOR}

*Use the buttons below to navigate!*"""
            
            keyboard = [
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                help_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            # Route to other menu handlers
            await self._handle_other_menu_callbacks(query, callback_data, user_id)
    
    async def _handle_other_menu_callbacks(self, query, callback_data: str, user_id: int):
        """Handle additional menu callbacks (daily_quiz, verse, achievements, reminders, leaderboard, score, stats, ask, search)"""
        if callback_data == "menu_daily_quiz":
            # Check if already completed
            if has_completed_daily_quiz(user_id):
                stats = get_daily_quiz_stats(user_id)
                await self.safe_edit_message(query, 
                    f"✅ *Daily Challenge Completed!*\n\n"
                    f"You've already completed today's challenge!\n\n"
                    f"*Your Daily Challenge Stats:*\n"
                    f"• Total Completed: {stats['total_completed']}\n"
                    f"• Current Streak: {stats['current_streak']} days\n"
                    f"• Best Score: {stats['best_score']:.1f}%\n\n"
                    f"Come back tomorrow for a new challenge!",
                    parse_mode='Markdown',
                    reply_markup=self.get_quick_actions_keyboard()
                )
                return
            
            # Get today's question
            question = get_today_quiz_question()
            
            # Check if user has active quiz
            active_quiz = get_quiz_session(user_id)
            if active_quiz:
                await self.safe_edit_message(query, 
                    "🎯 *You already have an active quiz!*\n\n"
                    f"Current score: {active_quiz['score']}/{active_quiz['total']}\n\n"
                    "Complete or stop your current quiz first.",
                    parse_mode='Markdown',
                    reply_markup=self.get_quick_actions_keyboard()
                )
                return
            
            # Start daily quiz session
            try:
                start_quiz_session(user_id, 0, question, difficulty=question.get('difficulty'), category=question.get('category'))
            except Exception as e:
                logger.error(f"Error starting daily quiz session: {e}")
            
            user_id_str = str(user_id)
            self._in_memory_quizzes[user_id_str] = {
                'question_index': 0,
                'question_data': question,
                'score': 0,
                'total': 0,
                'started_at': None,
                'difficulty': question.get('difficulty'),
                'category': question.get('category'),
                'is_daily_quiz': True
            }
            
            quiz_message = f"""⭐ <b>Daily Challenge Quiz!</b>

{MESSAGE_SEPARATOR}

🎯 <b>Today's Special Question:</b>
{question['question']}

{MESSAGE_SEPARATOR}

<b>Tap your answer below:</b>

💡 <i>Complete today's challenge to earn points and maintain your streak!</i>"""
            
            await self.safe_edit_message(query, 
                quiz_message,
                parse_mode='HTML',
                reply_markup=self.get_quiz_answer_keyboard(question)
            )
        
        elif callback_data == "menu_verse":
            verse_data = get_verse_of_the_day()
            verse_text = f"""📖 <b>Verse of the Day</b>

{MESSAGE_SEPARATOR}

<b>{verse_data['reference']}</b>

{verse_data['verse']}

{MESSAGE_SEPARATOR}

💡 <i>Topic: {verse_data['topic']}</i>

*Use /verse [reference] to get a specific verse*
*Example: /verse John 3:16*"""
            
            await self.safe_edit_message(query, 
                verse_text,
                parse_mode='HTML',
                reply_markup=self.get_verse_keyboard()
            )
        
        elif callback_data == "menu_achievements":
            # Check for new achievements
            from reading_progress import get_user_progress
            from quiz_storage import get_user_score
            from daily_quiz import get_daily_quiz_stats
            
            reading_progress = get_user_progress(user_id)
            quiz_stats = get_user_score(user_id)
            daily_quiz_stats = get_daily_quiz_stats(user_id)
            
            newly_unlocked = check_and_award_achievements(
                user_id, reading_progress, quiz_stats, daily_quiz_stats
            )
            
            display = get_achievement_display(user_id)
            
            # Show notification if new achievements unlocked
            if newly_unlocked:
                notification = "🎉 *New Achievement Unlocked!*\n\n"
                for achievement_id in newly_unlocked:
                    achievement = ACHIEVEMENTS[achievement_id]
                    notification += f"{achievement['emoji']} *{achievement['name']}*\n"
                    notification += f"   {achievement['description']}\n\n"
                notification += f"{MESSAGE_SEPARATOR}\n\n"
                display = notification + display
            
            keyboard = [
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                display,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif callback_data == "menu_reminders":
            reminders = get_user_reminders(user_id)
            if reminders['enabled'] and reminders['times']:
                times_list = "\n".join([f"• {time}" for time in reminders['times']])
                reminder_text = f"""⏰ *Your Reading Reminders*

{MESSAGE_SEPARATOR}

*Reminder Times:*
{times_list}

{MESSAGE_SEPARATOR}

*To add a reminder:*
/remind 8am
/remind 14:30
/remind 9:00pm

*To remove a reminder:*
/remind_off"""
            else:
                reminder_text = f"""⏰ *Reading Reminders*

{MESSAGE_SEPARATOR}

You don't have any reminders set.

*Set a reminder:*
/remind 8am
/remind 14:30
/remind 9:00pm

*Examples:*
• /remind 8am - Remind at 8:00 AM
• /remind 14:30 - Remind at 2:30 PM
• /remind 9:00pm - Remind at 9:00 PM"""
            
            keyboard = [
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                reminder_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif callback_data == "menu_leaderboard":
            leaderboard = get_leaderboard(limit=LEADERBOARD_TOP_N)
            user_rank, total_players = get_user_rank(user_id)
            
            if not leaderboard:
                leaderboard_text = "📈 *Leaderboard*\n\nNo players yet. Be the first!"
            else:
                leaderboard_text = "📈 *Top 10 Players*\n\n"
                leaderboard_text += f"{MESSAGE_SEPARATOR}\n\n"
                
                medals = ["🥇", "🥈", "🥉"]
                for i, player in enumerate(leaderboard):
                    medal = medals[i] if i < 3 else f"{i+1}."
                    name = player.get('first_name') or player.get('username') or f"User {player['user_id']}"
                    best_score = player.get('best_score', 0)
                    total_correct = player.get('total_correct', 0)
                    leaderboard_text += f"{medal} {name}\n"
                    leaderboard_text += f"   Best: {best_score:.1f}% | Correct: {total_correct}\n\n"
                
                leaderboard_text += f"{MESSAGE_SEPARATOR}\n\n"
                if user_rank:
                    leaderboard_text += f"*Your Rank:* #{user_rank} of {total_players} players"
                else:
                    leaderboard_text += f"*Total Players:* {total_players}"
            
            keyboard = [
                [InlineKeyboardButton("📊 My Score", callback_data="menu_score")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                leaderboard_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif callback_data == "menu_score":
            score = get_user_score(user_id)
            rank, total_players = get_user_rank(user_id)
            
            if score['total_answered'] == 0:
                score_text = f"""📊 *Your Quiz Score*

{MESSAGE_SEPARATOR}

You haven't answered any questions yet!

*Start a quiz to begin earning points:*
• Tap '🎯 Start Quiz' to begin
• Complete daily challenges
• Climb the leaderboard!"""
            else:
                accuracy = (score['total_correct'] / score['total_answered'] * 100) if score['total_answered'] > 0 else 0
                rank_text = f"#{rank} of {total_players}" if rank else "Not ranked"
                
                score_text = f"""📊 *Your Quiz Statistics*

{MESSAGE_SEPARATOR}

🎯 *Performance:*
• Total Answered: {score['total_answered']}
• Correct Answers: {score['total_correct']}
• Accuracy: {accuracy:.1f}%
• Best Score: {score.get('best_score', 0):.1f}%
• Quizzes Completed: {score.get('quizzes_completed', 0)}

{MESSAGE_SEPARATOR}

🏆 *Ranking:*
• Your Rank: {rank_text}

{MESSAGE_SEPARATOR}

💪 *Keep practicing to improve your score!*"""
            
            keyboard = [
                [InlineKeyboardButton("🎯 Start Quiz", callback_data="menu_quiz")],
                [InlineKeyboardButton("📈 Leaderboard", callback_data="menu_leaderboard")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                score_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif callback_data == "menu_stats":
            progress = get_user_progress(user_id)
            current_streak = get_current_streak(user_id)
            longest_streak = get_longest_streak(user_id)
            current_day, date_str = self.get_day_of_year()
            
            current_year = datetime.now().year
            is_leap_year = current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0)
            total_days = DAYS_IN_LEAP_YEAR if is_leap_year else DAYS_IN_YEAR
            
            days_completed = progress['total_completed']
            days_remaining = total_days - current_day
            completion_rate = (days_completed / current_day * 100) if current_day > 0 else 0
            
            stats_text = f"""📊 *Detailed Reading Statistics*

{MESSAGE_SEPARATOR}

📖 *Overall Progress:*
• Days Completed: {days_completed}/{total_days}
• Completion: {progress['completion_percentage']:.1f}%
• Days Remaining: {days_remaining}

{MESSAGE_SEPARATOR}

🔥 *Streaks:*
• Current Streak: {current_streak} days
• Longest Streak: {longest_streak} days

{MESSAGE_SEPARATOR}

📅 *Current Status:*
• Today: Day {current_day} ({date_str})
• Completion Rate: {completion_rate:.1f}% (of days so far)

{MESSAGE_SEPARATOR}

💡 *Tips:*
• Read every day to maintain your streak!
• Use /today to automatically mark today as completed"""
            
            keyboard = [
                [InlineKeyboardButton("📊 Progress", callback_data="menu_progress")],
                [InlineKeyboardButton("🔥 Streak", callback_data="menu_streak")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                stats_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif callback_data == "menu_ask":
            topics = get_all_topics()
            topics_list = "\n".join([f"• {topic}" for topic in topics[:10]])
            ask_text = f"""❓ *Ask a Bible Question*

{MESSAGE_SEPARATOR}

Type your question or use these common questions:

*Examples:*
• How can I be saved?
• What does the Bible say about love?
• How should I pray?

{MESSAGE_SEPARATOR}

*Topics I can help with:*
{topics_list}
... and more!

{MESSAGE_SEPARATOR}

*Type your question or use /ask [question]*"""
            
            keyboard = [
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                ask_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif callback_data == "menu_search":
            search_text = f"""📚 *Search Reading Plan*

{MESSAGE_SEPARATOR}

Type the name of a Bible book to find which days include it.

*Examples:*
• Genesis
• Matthew
• Psalms

{MESSAGE_SEPARATOR}

*Type a book name or use /search [book]*"""
            
            keyboard = [
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            await self.safe_edit_message(query, 
                search_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        else:
            # Unknown menu callback - return to main menu
            await self.safe_edit_message(query, 
                "📱 *Main Menu*\n\nChoose an option:",
                parse_mode='Markdown',
                reply_markup=self.get_main_menu_keyboard()
            )
    
    async def _handle_quiz_callback(self, query, callback_data: str, user_id: int):
        """Handle quiz-related callbacks (quiz start, quiz answers, quiz stop)"""
        if callback_data in ["quiz_easy", "quiz_medium", "quiz_hard", "quiz_random"]:
            # Start quiz based on difficulty
            active_quiz = get_quiz_session(user_id)
            if active_quiz:
                await self.safe_edit_message(query, 
                    f"🎯 *You already have an active quiz!*\n\n"
                    f"Current score: {active_quiz['score']}/{active_quiz['total']}\n\n"
                    f"{ERROR_MESSAGE_QUIZ_ACTIVE}",
                    parse_mode='Markdown'
                )
                return
            
            difficulty = None
            if callback_data == "quiz_easy":
                difficulty = "easy"
            elif callback_data == "quiz_medium":
                difficulty = "medium"
            elif callback_data == "quiz_hard":
                difficulty = "hard"
            # quiz_random keeps difficulty as None
            
            from quiz_questions import get_question_index
            recent_indices = self._recent_questions.get(str(user_id), [])
            question = get_random_question(difficulty=difficulty, exclude_indices=recent_indices)
            
            # Track this question to avoid repeats
            question_index = get_question_index(question)
            if question_index is not None:
                if str(user_id) not in self._recent_questions:
                    self._recent_questions[str(user_id)] = []
                self._recent_questions[str(user_id)].append(question_index)
                if len(self._recent_questions[str(user_id)]) > MAX_RECENT_QUESTIONS:
                    self._recent_questions[str(user_id)] = self._recent_questions[str(user_id)][-MAX_RECENT_QUESTIONS:]
            
            try:
                start_quiz_session(user_id, 0, question, difficulty=difficulty, category=None)
            except Exception as e:
                logger.error(f"Error starting quiz session: {e}")
            
            user_id_str = str(user_id)
            self._in_memory_quizzes[user_id_str] = {
                'question_index': 0,
                'question_data': question,
                'score': 0,
                'total': 0,
                'started_at': None,
                'difficulty': difficulty,
                'category': None
            }
            
            diff_name = difficulty.title() if difficulty else "Random"
            quiz_message = f"""🎯 <b>{diff_name} Bible Quiz Started!</b>

{MESSAGE_SEPARATOR}

<b>Question:</b>
{question['question']}

{MESSAGE_SEPARATOR}

<b>Tap your answer below:</b>"""
            
            await self.safe_edit_message(query, 
                quiz_message, 
                parse_mode='HTML',
                reply_markup=self.get_quiz_answer_keyboard(question)
            )
        
        elif callback_data == "quiz_stop":
            # Handle quiz stop from inline button
            session = None
            if str(user_id) in self._in_memory_quizzes:
                session = self._in_memory_quizzes[str(user_id)]
                del self._in_memory_quizzes[str(user_id)]
            
            if not session:
                session = end_quiz_session(user_id)
            
            if session and session['total'] > 0:
                user = query.from_user
                update_user_score(
                    user_id, 
                    session['score'], 
                    session['total'],
                    username=user.username,
                    first_name=user.first_name
                )
                accuracy = (session['score'] / session['total'] * 100) if session['total'] > 0 else 0
                
                is_daily_quiz = session.get('is_daily_quiz', False)
                if is_daily_quiz:
                    mark_daily_quiz_completed(user_id, session['score'], session['total'])
                    newly_unlocked = check_and_award_achievements(user_id)
                    message = f"✅ *Daily Challenge Completed!*\n\n"
                    message += f"Final Score: {session['score']}/{session['total']} ({accuracy:.1f}%)\n\n"
                    if newly_unlocked:
                        message += "🎉 *New Achievement Unlocked!*\n\n"
                        for achievement_id in newly_unlocked:
                            achievement = ACHIEVEMENTS[achievement_id]
                            message += f"{achievement['emoji']} {achievement['name']}\n"
                        message += "\n"
                    message += "Come back tomorrow for a new challenge!"
                else:
                    message = f"✅ *Quiz Ended*\n\n"
                    message += f"Final Score: {session['score']}/{session['total']} ({accuracy:.1f}%)\n\n"
                    message += "Tap '🎯 Start Quiz' to start a new quiz!"
                
                keyboard = [
                    [InlineKeyboardButton("🎯 Start Quiz", callback_data="menu_quiz")],
                    [InlineKeyboardButton("📊 My Score", callback_data="menu_score")],
                    [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
                ]
                
                await self.safe_edit_message(query, 
                    message,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await self.safe_edit_message(query, 
                    "✅ Quiz session ended.\n\n"
                    "Tap '🎯 Start Quiz' to start a new quiz!",
                    parse_mode='Markdown',
                    reply_markup=self.get_quick_actions_keyboard()
                )
        
        elif callback_data.startswith("quiz_answer_"):
            # Handle quiz answer - this is a large handler, keeping it here for now
            # Could be further refactored into _handle_quiz_answer method
            await self._handle_quiz_answer(query, callback_data, user_id)
        
        else:
            # Unknown quiz callback
            await self.safe_edit_message(query, 
                "❌ Unknown quiz action. Please try again.",
                reply_markup=self.get_main_menu_keyboard()
            )
    
    async def _handle_quiz_answer(self, query, callback_data: str, user_id: int):
        """Handle quiz answer callbacks - separated for better organization"""
        active_quiz = get_quiz_session(user_id)
        if not active_quiz and str(user_id) in self._in_memory_quizzes:
            active_quiz = self._in_memory_quizzes[str(user_id)]
        
        if not active_quiz:
            await self.safe_edit_message(query, 
                "Your quiz session has ended. Please start a new one.",
                reply_markup=self.get_quick_actions_keyboard()
            )
            return
        
        question_data = active_quiz['question_data']
        chosen_option_index = int(callback_data.split('_')[-1])
        
        is_correct = (chosen_option_index == question_data['correct'])
        new_score = active_quiz['score'] + (1 if is_correct else 0)
        new_total = active_quiz['total'] + 1
        
        try:
            update_quiz_session(user_id, new_score, new_total)
        except Exception as e:
            logger.error(f"Error updating quiz session in file for user {user_id}: {e}")
        
        if str(user_id) in self._in_memory_quizzes:
            self._in_memory_quizzes[str(user_id)]['score'] = new_score
            self._in_memory_quizzes[str(user_id)]['total'] = new_total
        
        correct_option = question_data['options'][question_data['correct']]
        chosen_option = question_data['options'][chosen_option_index]
        
        # Build enhanced feedback
        if is_correct:
            feedback = f"✅ <b>Correct!</b>\n\n"
            feedback += f"<b>Your answer:</b> {chosen_option}\n\n"
        else:
            feedback = f"❌ <b>Incorrect</b>\n\n"
            feedback += f"<b>Your answer:</b> {chosen_option}\n"
            feedback += f"<b>Correct answer:</b> {correct_option}\n\n"
        
        # Try to get the actual Bible verse
        verse_data = get_verse_by_reference(question_data['reference'])
        if verse_data:
            feedback += f"📖 <b>{verse_data['reference']}</b>\n\n"
            feedback += f"<i>\"{verse_data['verse']}\"</i>\n\n"
        else:
            feedback += f"📖 <b>Bible Reference:</b> {question_data['reference']}\n\n"
        
        feedback += f"{MESSAGE_SEPARATOR}\n\n"
        feedback += f"<b>Your Score:</b> {new_score}/{new_total}\n\n"
        
        user = query.from_user
        update_user_score(user_id, new_score, new_total, username=user.username, first_name=user.first_name)
        logger.info(f"User {user_id} answered quiz question via button: {'correct' if is_correct else 'incorrect'}")
        
        # Send feedback as a NEW message (not editing) so previous question remains visible
        try:
            await query.message.reply_text(
                feedback,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Error sending feedback message: {e}")
        
        # Check if this is a daily quiz
        is_daily_quiz = active_quiz.get('is_daily_quiz', False)
        
        if is_daily_quiz:
            # Daily quiz is complete after one question
            mark_daily_quiz_completed(user_id, new_score, new_total)
            try:
                end_quiz_session(user_id)
            except Exception as e:
                logger.error(f"Error ending daily quiz session: {e}")
            
            if str(user_id) in self._in_memory_quizzes:
                del self._in_memory_quizzes[str(user_id)]
            
            newly_unlocked = check_and_award_achievements(user_id)
            
            completion_msg = f"{MESSAGE_SEPARATOR}\n\n"
            completion_msg += "✅ <b>Daily Challenge Completed!</b>\n\n"
            
            if newly_unlocked:
                completion_msg += "🎉 <b>New Achievement Unlocked!</b>\n\n"
                for achievement_id in newly_unlocked:
                    achievement = ACHIEVEMENTS[achievement_id]
                    completion_msg += f"{achievement['emoji']} {achievement['name']}\n"
                completion_msg += "\n"
            
            completion_msg += "Come back tomorrow for a new challenge!"
            
            keyboard = [
                [InlineKeyboardButton("⭐ New Challenge", callback_data="menu_daily_quiz")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")]
            ]
            
            # Send completion as new message
            await query.message.reply_text(
                completion_msg,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
        
        # For regular quizzes: Save current session to history, end it, then start new session
        await asyncio.sleep(1)
        
        # Save current session to history before ending it
        session_to_save = {
            'question_data': question_data,
            'score': new_score,
            'total': new_total,
            'difficulty': active_quiz.get('difficulty'),
            'category': active_quiz.get('category'),
            'chosen_answer': chosen_option_index,
            'is_correct': is_correct
        }
        save_quiz_to_history(user_id, session_to_save)
        
        # Update user score with this question AND track complete quiz session
        user = query.from_user
        update_user_score(
            user_id, 
            new_score,  # 1 if correct, 0 if incorrect
            new_total,  # Always 1 for single question
            username=user.username,
            first_name=user.first_name,
            quiz_session_score=new_score,  # Score for this session
            quiz_session_total=new_total   # Total for this session (always 1)
        )
        
        # End current session
        try:
            end_quiz_session(user_id)
        except Exception as e:
            logger.error(f"Error ending quiz session: {e}")
        
        # Remove from in-memory quizzes
        if str(user_id) in self._in_memory_quizzes:
            del self._in_memory_quizzes[str(user_id)]
        
        # Get new question with same difficulty/category
        quiz_difficulty = active_quiz.get('difficulty')
        quiz_category = active_quiz.get('category')
        
        # Get recently asked question indices for this user to avoid repeats
        from quiz_questions import get_question_index
        recent_indices = self._recent_questions.get(str(user_id), [])
        
        # Get a new random question (keep same difficulty/category, exclude recent ones)
        new_question = get_random_question(
            difficulty=quiz_difficulty, 
            category=quiz_category,
            exclude_indices=recent_indices
        )
        
        # Track this question to avoid repeats
        question_index = get_question_index(new_question)
        if question_index is not None:
            if str(user_id) not in self._recent_questions:
                self._recent_questions[str(user_id)] = []
            self._recent_questions[str(user_id)].append(question_index)
            if len(self._recent_questions[str(user_id)]) > MAX_RECENT_QUESTIONS:
                self._recent_questions[str(user_id)] = self._recent_questions[str(user_id)][-MAX_RECENT_QUESTIONS:]
        
        # Start a NEW session with the new question
        user_id_str = str(user_id)
        try:
            start_quiz_session(user_id, 0, new_question, difficulty=quiz_difficulty, category=quiz_category)
        except Exception as e:
            logger.error(f"Error starting new quiz session: {e}")
        
        # Also save in-memory as fallback
        self._in_memory_quizzes[user_id_str] = {
            'question_data': new_question,
            'question_index': 0,
            'score': 0,  # Reset score for new session
            'total': 0,  # Reset total for new session
            'difficulty': quiz_difficulty,
            'category': quiz_category
        }
        
        diff_name = new_question.get('difficulty', 'random').title()
        next_question_msg = f"""🎯 <b>New {diff_name} Quiz Question</b>

{MESSAGE_SEPARATOR}

<b>Question:</b>
{new_question['question']}

{MESSAGE_SEPARATOR}

<b>Tap your answer below:</b>"""
        
        # Send next question as a NEW message (not editing) so all questions remain visible
        await query.message.reply_text(
            next_question_msg,
            parse_mode='HTML',
            reply_markup=self.get_quiz_answer_keyboard(new_question)
        )
    
    async def _handle_reading_callback(self, query, callback_data: str, user_id: int):
        """Handle reading-related callbacks"""
        if callback_data == "reading_today":
            day_number, date_str = self.get_day_of_year()
            reading = self.get_bible_reading(day_number)
            encouragement = self.get_encouragement(day_number)
            message = self.format_message(day_number, date_str, reading, encouragement)
            mark_day_completed(user_id, day_number)
            await self.safe_edit_message(query, 
                message,
                parse_mode='Markdown',
                reply_markup=self.get_reading_menu_keyboard()
            )
        elif callback_data == "reading_pick":
            await self.safe_edit_message(query, 
                "📅 *Pick a Day*\n\n"
                "Type a day number (1-365) or use:\n"
                "/day [number]\n\n"
                "*Example:* /day 45",
                parse_mode='Markdown',
                reply_markup=self.get_reading_menu_keyboard()
            )
        else:
            # Unknown reading callback
            await self.safe_edit_message(query, 
                "❌ Unknown reading action. Please try again.",
                reply_markup=self.get_reading_menu_keyboard()
            )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks - routes to specific handler methods"""
        query = update.callback_query
        await query.answer()  # Acknowledge the callback
        
        user_id = query.from_user.id
        self._ensure_subscribed(user_id)
        callback_data = query.data
        
        try:
            # Route to appropriate handler based on callback prefix
            if callback_data.startswith("menu_"):
                await self._handle_menu_callback(query, callback_data, user_id)
            elif callback_data.startswith("quiz_") or callback_data.startswith("daily_quiz_"):
                await self._handle_quiz_callback(query, callback_data, user_id)
            elif callback_data.startswith("reading_"):
                await self._handle_reading_callback(query, callback_data, user_id)
            else:
                # Unknown callback - return to main menu
                await self.safe_edit_message(query, 
                    "📱 *Main Menu*\n\nChoose an option:",
                    parse_mode='Markdown',
                    reply_markup=self.get_main_menu_keyboard()
                )
            
            # All handlers have been migrated to helper methods above
            # No legacy code needed - routing is complete
            
        except Exception as e:
            logger.error(f"Error handling callback {callback_data}: {e}", exc_info=True)
            try:
                await self.safe_edit_message(
                    query,
                    ERROR_MESSAGE_GENERIC,
                    reply_markup=self.get_main_menu_keyboard()
                )
            except Exception as e2:
                logger.error(f"Error sending error message: {e2}")
                # Try to send as new message
                try:
                    await query.message.reply_text(
                        ERROR_MESSAGE_GENERIC,
                        reply_markup=self.get_main_menu_keyboard()
                    )
                except:
                    pass
    
    
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
