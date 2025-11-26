"""
Reading Reminder System
Customizable reminder times for users
"""

import json
import os
import logging
from datetime import datetime, time

logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REMINDERS_FILE = os.path.join(SCRIPT_DIR, "reminders.json")

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
    _fix_storage_file(REMINDERS_FILE)
except Exception as e:
    logger.error(f"Error checking storage file: {e}")

def load_reminders():
    """Load user reminders"""
    if not _fix_storage_file(REMINDERS_FILE):
        return {}
    
    if not os.path.exists(REMINDERS_FILE):
        return {}
    
    try:
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading reminders: {e}")
        return {}

def save_reminders(reminders):
    """Save user reminders"""
    if not _fix_storage_file(REMINDERS_FILE):
        return False
    
    try:
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(reminders, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving reminders: {e}")
        return False

def set_reminder(user_id, hour, minute):
    """Set reminder time for user"""
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str not in reminders:
        reminders[user_id_str] = {
            'enabled': True,
            'times': []
        }
    
    reminder_time = f"{hour:02d}:{minute:02d}"
    
    if reminder_time not in reminders[user_id_str]['times']:
        reminders[user_id_str]['times'].append(reminder_time)
        reminders[user_id_str]['times'].sort()
    
    reminders[user_id_str]['enabled'] = True
    save_reminders(reminders)
    return True

def remove_reminder(user_id, hour, minute):
    """Remove a specific reminder time"""
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str not in reminders:
        return False
    
    reminder_time = f"{hour:02d}:{minute:02d}"
    
    if reminder_time in reminders[user_id_str]['times']:
        reminders[user_id_str]['times'].remove(reminder_time)
        save_reminders(reminders)
        return True
    
    return False

def disable_reminders(user_id):
    """Disable all reminders for user"""
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str not in reminders:
        reminders[user_id_str] = {
            'enabled': False,
            'times': []
        }
    else:
        reminders[user_id_str]['enabled'] = False
    
    save_reminders(reminders)
    return True

def enable_reminders(user_id):
    """Enable reminders for user"""
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str not in reminders:
        reminders[user_id_str] = {
            'enabled': True,
            'times': []
        }
    else:
        reminders[user_id_str]['enabled'] = True
    
    save_reminders(reminders)
    return True

def get_user_reminders(user_id):
    """Get user's reminder settings"""
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str not in reminders:
        return {
            'enabled': False,
            'times': []
        }
    
    return reminders[user_id_str]

def get_users_to_remind(current_hour, current_minute):
    """Get list of users who should be reminded at this time"""
    reminders = load_reminders()
    reminder_time = f"{current_hour:02d}:{current_minute:02d}"
    
    users_to_remind = []
    
    for user_id_str, reminder_data in reminders.items():
        if reminder_data.get('enabled', False) and reminder_time in reminder_data.get('times', []):
            users_to_remind.append(int(user_id_str))
    
    return users_to_remind

def parse_time_string(time_str):
    """Parse time string like '8am', '14:30', '9:00pm'"""
    time_str = time_str.strip().lower()
    
    # Remove common words
    time_str = time_str.replace('at', '').replace('am', '').replace('pm', '').strip()
    
    # Check for 24-hour format
    if ':' in time_str:
        parts = time_str.split(':')
        try:
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
            return hour, minute
        except ValueError:
            return None, None
    
    # Check for 12-hour format
    try:
        hour = int(time_str)
        return hour, 0
    except ValueError:
        return None, None


