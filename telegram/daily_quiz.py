"""
Daily Quiz Challenge System
One special quiz per day that all users can take
"""

import json
import os
import logging
from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DAILY_QUIZ_FILE = os.path.join(SCRIPT_DIR, "daily_quiz.json")

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
    _fix_storage_file(DAILY_QUIZ_FILE)
except Exception as e:
    logger.error(f"Error checking storage file: {e}")

def load_daily_quiz_data():
    """Load daily quiz data"""
    if not _fix_storage_file(DAILY_QUIZ_FILE):
        return {}
    
    if not os.path.exists(DAILY_QUIZ_FILE):
        return {}
    
    try:
        with open(DAILY_QUIZ_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading daily quiz data: {e}")
        return {}

def save_daily_quiz_data(data):
    """Save daily quiz data"""
    if not _fix_storage_file(DAILY_QUIZ_FILE):
        return False
    
    try:
        with open(DAILY_QUIZ_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving daily quiz data: {e}")
        return False

def get_today_quiz_question():
    """Get today's daily quiz question (same for all users)"""
    from quiz_questions import get_random_question
    
    today = date.today().isoformat()
    data = load_daily_quiz_data()
    
    # Check if we already have a question for today
    if 'daily_quizzes' in data and today in data['daily_quizzes']:
        return data['daily_quizzes'][today]
    
    # Generate a new question for today
    question = get_random_question()
    question['date'] = today
    
    if 'daily_quizzes' not in data:
        data['daily_quizzes'] = {}
    
    data['daily_quizzes'][today] = question
    save_daily_quiz_data(data)
    
    return question

def get_quiz_question_for_date(target_date):
    """Get daily quiz question for a specific date"""
    data = load_daily_quiz_data()
    date_key = target_date.isoformat() if isinstance(target_date, date) else target_date
    
    if 'daily_quizzes' in data and date_key in data['daily_quizzes']:
        return data['daily_quizzes'][date_key]
    
    return None

def mark_daily_quiz_completed(user_id, score, total):
    """Mark daily quiz as completed for a user"""
    today = date.today().isoformat()
    data = load_daily_quiz_data()
    
    if 'completions' not in data:
        data['completions'] = {}
    
    user_id_str = str(user_id)
    if user_id_str not in data['completions']:
        data['completions'][user_id_str] = {}
    
    if today not in data['completions'][user_id_str]:
        data['completions'][user_id_str][today] = {
            'score': score,
            'total': total,
            'accuracy': (score / total * 100) if total > 0 else 0,
            'completed_at': datetime.now().isoformat()
        }
        save_daily_quiz_data(data)
        return True
    
    return False  # Already completed today

def has_completed_daily_quiz(user_id):
    """Check if user has completed today's daily quiz"""
    today = date.today().isoformat()
    data = load_daily_quiz_data()
    
    if 'completions' not in data:
        return False
    
    user_id_str = str(user_id)
    if user_id_str not in data['completions']:
        return False
    
    return today in data['completions'][user_id_str]

def get_daily_quiz_stats(user_id):
    """Get user's daily quiz statistics"""
    data = load_daily_quiz_data()
    user_id_str = str(user_id)
    
    if 'completions' not in data or user_id_str not in data['completions']:
        return {
            'total_completed': 0,
            'total_correct': 0,
            'total_answered': 0,
            'best_score': 0,
            'current_streak': 0
        }
    
    user_completions = data['completions'][user_id_str]
    total_completed = len(user_completions)
    total_correct = sum(c['score'] for c in user_completions.values())
    total_answered = sum(c['total'] for c in user_completions.values())
    best_score = max((c['accuracy'] for c in user_completions.values()), default=0)
    
    # Calculate current streak
    sorted_dates = sorted(user_completions.keys(), reverse=True)
    current_streak = 0
    today = date.today()
    
    for i, date_str in enumerate(sorted_dates):
        completion_date = datetime.fromisoformat(date_str).date()
        expected_date = today - timedelta(days=i)
        if completion_date == expected_date:
            current_streak += 1
        else:
            break
    
    return {
        'total_completed': total_completed,
        'total_correct': total_correct,
        'total_answered': total_answered,
        'best_score': best_score,
        'current_streak': current_streak
    }

def get_daily_quiz_leaderboard(limit=10):
    """Get daily quiz leaderboard (based on total completions and accuracy)"""
    data = load_daily_quiz_data()
    
    if 'completions' not in data:
        return []
    
    user_stats = []
    for user_id, completions in data['completions'].items():
        total_completed = len(completions)
        total_correct = sum(c['score'] for c in completions.values())
        total_answered = sum(c['total'] for c in completions.values())
        avg_accuracy = (total_correct / total_answered * 100) if total_answered > 0 else 0
        
        user_stats.append({
            'user_id': user_id,
            'total_completed': total_completed,
            'avg_accuracy': avg_accuracy,
            'total_correct': total_correct
        })
    
    # Sort by total completed, then by average accuracy
    user_stats.sort(key=lambda x: (x['total_completed'], x['avg_accuracy']), reverse=True)
    
    return user_stats[:limit]

