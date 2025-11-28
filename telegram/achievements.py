"""
Achievement System
Track and award badges for milestones
"""

import json
import os
import logging
from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACHIEVEMENTS_FILE = os.path.join(SCRIPT_DIR, "achievements.json")

def _fix_storage_file(file_path):
    """Fix storage file if it's a directory (Docker volume mount issue)"""
    if os.path.exists(file_path) and os.path.isdir(file_path):
        logger.error(f"Storage file path is a directory! Cannot remove mounted directory: {file_path}")
        logger.error("Please stop the container, remove the directory on the host, and create a file instead:")
        logger.error(f"  rm -rf {file_path}")
        logger.error(f"  echo '{{}}' > {file_path}")
        logger.error("Then restart the container.")
        return False
    return True

# Try to fix storage file on module load
try:
    _fix_storage_file(ACHIEVEMENTS_FILE)
except Exception as e:
    logger.error(f"Error checking storage file: {e}")

ACHIEVEMENTS = {
    "first_steps": {
        "name": "First Steps",
        "description": "Complete your first Bible reading",
        "emoji": "👣",
        "condition": "reading_completed >= 1"
    },
    "week_warrior": {
        "name": "Week Warrior",
        "description": "Maintain a 7-day reading streak",
        "emoji": "🔥",
        "condition": "streak >= 7"
    },
    "month_master": {
        "name": "Month Master",
        "description": "Maintain a 30-day reading streak",
        "emoji": "👑",
        "condition": "streak >= 30"
    },
    "quiz_master": {
        "name": "Quiz Master",
        "description": "Answer 100 quiz questions correctly",
        "emoji": "🎯",
        "condition": "quiz_correct >= 100"
    },
    "perfect_score": {
        "name": "Perfect Score",
        "description": "Get 100% on a quiz",
        "emoji": "💯",
        "condition": "quiz_perfect_score == True"
    },
    "bible_scholar": {
        "name": "Bible Scholar",
        "description": "Complete all 365 days of reading",
        "emoji": "📚",
        "condition": "reading_completed >= 365"
    },
    "daily_champion": {
        "name": "Daily Champion",
        "description": "Complete 10 daily quiz challenges",
        "emoji": "🏆",
        "condition": "daily_quiz_completed >= 10"
    },
    "century_club": {
        "name": "Century Club",
        "description": "Complete 100 days of reading",
        "emoji": "💎",
        "condition": "reading_completed >= 100"
    },
}

def load_achievements():
    """Load user achievements"""
    if not _fix_storage_file(ACHIEVEMENTS_FILE):
        return {}
    
    if not os.path.exists(ACHIEVEMENTS_FILE):
        return {}
    
    try:
        with open(ACHIEVEMENTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading achievements: {e}")
        return {}

def save_achievements(achievements):
    """Save user achievements"""
    if not _fix_storage_file(ACHIEVEMENTS_FILE):
        return False
    
    try:
        with open(ACHIEVEMENTS_FILE, 'w') as f:
            json.dump(achievements, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving achievements: {e}")
        return False

def get_user_achievements(user_id):
    """Get user's unlocked achievements"""
    achievements = load_achievements()
    user_id_str = str(user_id)
    
    if user_id_str not in achievements:
        return []
    
    return achievements[user_id_str].get('unlocked', [])

def unlock_achievement(user_id, achievement_id):
    """Unlock an achievement for a user"""
    achievements = load_achievements()
    user_id_str = str(user_id)
    
    if user_id_str not in achievements:
        achievements[user_id_str] = {
            'unlocked': [],
            'unlocked_at': {}
        }
    
    if achievement_id not in achievements[user_id_str]['unlocked']:
        achievements[user_id_str]['unlocked'].append(achievement_id)
        achievements[user_id_str]['unlocked_at'][achievement_id] = datetime.now().isoformat()
        save_achievements(achievements)
        return True
    
    return False  # Already unlocked

def check_and_award_achievements(user_id, reading_progress=None, quiz_stats=None, daily_quiz_stats=None):
    """Check if user qualifies for any achievements and award them"""
    from reading_progress import get_current_streak
    from quiz_storage import get_user_score
    from daily_quiz import get_daily_quiz_stats
    
    newly_unlocked = []
    
    # Get current stats
    if reading_progress is None:
        from reading_progress import get_user_progress
        reading_progress = get_user_progress(user_id)
    
    if quiz_stats is None:
        quiz_stats = get_user_score(user_id)
    
    if daily_quiz_stats is None:
        daily_quiz_stats = get_daily_quiz_stats(user_id)
    
    current_streak = get_current_streak(user_id)
    
    # Check each achievement
    for achievement_id, achievement in ACHIEVEMENTS.items():
        # Skip if already unlocked
        if achievement_id in get_user_achievements(user_id):
            continue
        
        # Check conditions
        if achievement_id == "first_steps" and reading_progress['total_completed'] >= 1:
            if unlock_achievement(user_id, achievement_id):
                newly_unlocked.append(achievement_id)
        
        elif achievement_id == "week_warrior" and current_streak >= 7:
            if unlock_achievement(user_id, achievement_id):
                newly_unlocked.append(achievement_id)
        
        elif achievement_id == "month_master" and current_streak >= 30:
            if unlock_achievement(user_id, achievement_id):
                newly_unlocked.append(achievement_id)
        
        elif achievement_id == "quiz_master" and quiz_stats['total_correct'] >= 100:
            if unlock_achievement(user_id, achievement_id):
                newly_unlocked.append(achievement_id)
        
        elif achievement_id == "perfect_score":
            # Check if user has a perfect score (100% on any quiz)
            if quiz_stats['best_score'] >= 100:
                if unlock_achievement(user_id, achievement_id):
                    newly_unlocked.append(achievement_id)
        
        elif achievement_id == "bible_scholar" and reading_progress['total_completed'] >= 365:
            if unlock_achievement(user_id, achievement_id):
                newly_unlocked.append(achievement_id)
        
        elif achievement_id == "daily_champion" and daily_quiz_stats['total_completed'] >= 10:
            if unlock_achievement(user_id, achievement_id):
                newly_unlocked.append(achievement_id)
        
        elif achievement_id == "century_club" and reading_progress['total_completed'] >= 100:
            if unlock_achievement(user_id, achievement_id):
                newly_unlocked.append(achievement_id)
    
    return newly_unlocked

def get_achievement_display(user_id):
    """Get formatted achievement display for user"""
    achievements_data = load_achievements()
    user_id_str = str(user_id)
    unlocked = get_user_achievements(user_id)
    unlocked_at = achievements_data.get(user_id_str, {}).get('unlocked_at', {})
    
    display = "🏆 *Your Achievements*\n\n"
    display += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # Show unlocked achievements first
    if unlocked:
        display += "*✅ Unlocked Achievements:*\n\n"
        for achievement_id in unlocked:
            achievement = ACHIEVEMENTS[achievement_id]
            unlock_date = unlocked_at.get(achievement_id, "Unknown")
            if unlock_date != "Unknown":
                try:
                    from datetime import datetime
                    date_obj = datetime.fromisoformat(unlock_date)
                    unlock_date = date_obj.strftime("%B %d, %Y")
                except:
                    pass
            display += f"{achievement['emoji']} *{achievement['name']}*\n"
            display += f"   {achievement['description']}\n"
            display += f"   📅 Unlocked: {unlock_date}\n\n"
        display += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # Show locked achievements
    locked = [aid for aid in ACHIEVEMENTS.keys() if aid not in unlocked]
    if locked:
        display += "*🔒 Locked Achievements:*\n\n"
        for achievement_id in locked:
            achievement = ACHIEVEMENTS[achievement_id]
            display += f"🔒 {achievement['name']}\n"
            display += f"   {achievement['description']}\n\n"
    
    if not unlocked and not locked:
        display += "No achievements available.\n"
    
    return display


