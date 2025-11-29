#!/usr/bin/env python3
"""
Configuration constants for the Bible in a Year Telegram Bot
"""

# Quiz Configuration
MAX_RECENT_QUESTIONS = 50  # Maximum number of recent questions to track per user
MAX_QUIZ_QUESTIONS = 10  # Maximum questions per quiz session
TOTAL_QUIZ_QUESTIONS = 567  # Total questions in database

# Reading Plan Configuration
DAYS_IN_YEAR = 365
DAYS_IN_LEAP_YEAR = 366
PROGRESS_BAR_LENGTH = 20  # Length of progress bar in characters

# Daily Message Configuration
DAILY_MESSAGE_HOUR = 4  # Hour (24-hour format) for daily messages
DAILY_MESSAGE_TIMEZONE = "GMT"  # Timezone for daily messages

# Leaderboard Configuration
LEADERBOARD_TOP_N = 10  # Number of top users to show in leaderboard

# UI Configuration
ENCOURAGEMENT_MESSAGES = [
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

# Quiz Session Configuration
QUIZ_SESSION_TIMEOUT_HOURS = 1  # Hours before inactive quiz session expires
IN_MEMORY_QUIZZES_CLEANUP_INTERVAL = 3600  # Seconds between cleanup runs

# Message Formatting
MESSAGE_SEPARATOR = "━━━━━━━━━━━━━━━━━━━━"

# Error Messages
ERROR_MESSAGE_GENERIC = "❌ An error occurred. Please try again or use /menu to return to the main menu."
ERROR_MESSAGE_QUIZ_ACTIVE = "🎯 *You already have an active quiz!*\n\nAnswer the current question or use /quiz_stop to start a new quiz."
ERROR_MESSAGE_INVALID_DAY = "❌ Invalid day number. Please enter a number between 1 and 365."

# Success Messages
SUCCESS_QUIZ_COMPLETED = "✅ Quiz completed! Great job!"
SUCCESS_DAY_MARKED = "✅ Day marked as completed!"

