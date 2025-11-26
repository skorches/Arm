"""
Storage for reading progress tracking
Tracks which days users have completed in their Bible reading
"""

import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "reading_progress.json")

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
    _fix_storage_file(PROGRESS_FILE)
except Exception as e:
    logger.error(f"Error checking storage file: {e}")

def load_reading_progress():
    """Load reading progress from file"""
    if not _fix_storage_file(PROGRESS_FILE):
        return {}
    
    if not os.path.exists(PROGRESS_FILE):
        return {}
    
    try:
        with open(PROGRESS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('progress', {})
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in progress file {PROGRESS_FILE}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading reading progress: {e}")
        return {}

def save_reading_progress(progress):
    """Save reading progress to file"""
    if not _fix_storage_file(PROGRESS_FILE):
        return False
    
    try:
        data = {'progress': progress}
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving reading progress: {e}")
        return False

def mark_day_completed(user_id, day_number, year=None):
    """Mark a day as completed for a user"""
    if year is None:
        year = datetime.now().year
    
    progress = load_reading_progress()
    user_id_str = str(user_id)
    year_str = str(year)
    
    if user_id_str not in progress:
        progress[user_id_str] = {}
    
    if year_str not in progress[user_id_str]:
        progress[user_id_str][year_str] = {
            'completed_days': [],
            'last_completed': None,
            'total_completed': 0
        }
    
    if day_number not in progress[user_id_str][year_str]['completed_days']:
        progress[user_id_str][year_str]['completed_days'].append(day_number)
        progress[user_id_str][year_str]['completed_days'].sort()
        progress[user_id_str][year_str]['last_completed'] = day_number
        progress[user_id_str][year_str]['total_completed'] = len(progress[user_id_str][year_str]['completed_days'])
    
    return save_reading_progress(progress)

def get_user_progress(user_id, year=None):
    """Get reading progress for a user"""
    if year is None:
        year = datetime.now().year
    
    progress = load_reading_progress()
    user_id_str = str(user_id)
    year_str = str(year)
    
    if user_id_str not in progress or year_str not in progress[user_id_str]:
        return {
            'completed_days': [],
            'last_completed': None,
            'total_completed': 0,
            'completion_percentage': 0.0
        }
    
    user_data = progress[user_id_str][year_str]
    total_days = 365  # Standard year
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        total_days = 366  # Leap year
    
    completion_percentage = (user_data['total_completed'] / total_days) * 100
    
    return {
        'completed_days': user_data.get('completed_days', []),
        'last_completed': user_data.get('last_completed'),
        'total_completed': user_data.get('total_completed', 0),
        'completion_percentage': completion_percentage
    }

def get_current_streak(user_id, year=None):
    """Calculate current reading streak (consecutive days)"""
    if year is None:
        year = datetime.now().year
    
    progress = get_user_progress(user_id, year)
    completed_days = set(progress['completed_days'])
    
    if not completed_days:
        return 0
    
    # Get current day of year
    today = datetime.now()
    current_day = today.timetuple().tm_yday
    
    # Check if today is completed
    if current_day in completed_days:
        # Count backwards from today
        streak = 0
        check_day = current_day
        while check_day in completed_days and check_day > 0:
            streak += 1
            check_day -= 1
        return streak
    else:
        # Count backwards from yesterday
        streak = 0
        check_day = current_day - 1
        while check_day in completed_days and check_day > 0:
            streak += 1
            check_day -= 1
        return streak

def get_longest_streak(user_id, year=None):
    """Calculate longest reading streak for the year"""
    if year is None:
        year = datetime.now().year
    
    progress = get_user_progress(user_id, year)
    completed_days = sorted(progress['completed_days'])
    
    if not completed_days:
        return 0
    
    longest_streak = 1
    current_streak = 1
    
    for i in range(1, len(completed_days)):
        if completed_days[i] == completed_days[i-1] + 1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1
    
    return longest_streak

def is_day_completed(user_id, day_number, year=None):
    """Check if a specific day is completed"""
    if year is None:
        year = datetime.now().year
    
    progress = get_user_progress(user_id, year)
    return day_number in progress['completed_days']


