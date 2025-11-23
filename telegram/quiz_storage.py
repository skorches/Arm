"""
Storage for quiz scores and active quiz sessions
"""

import json
import os
import logging
import shutil

logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCORES_FILE = os.path.join(SCRIPT_DIR, "quiz_scores.json")
ACTIVE_QUIZZES_FILE = os.path.join(SCRIPT_DIR, "active_quizzes.json")

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

# Try to fix storage files on module load (non-fatal if it fails)
try:
    _fix_storage_file(SCORES_FILE)
    _fix_storage_file(ACTIVE_QUIZZES_FILE)
except Exception as e:
    logger.error(f"Error checking storage files: {e}")

def load_quiz_scores():
    """Load quiz scores from file"""
    if not os.path.exists(SCORES_FILE):
        return {}
    
    try:
        with open(SCORES_FILE, 'r') as f:
            data = json.load(f)
            return data.get('scores', {})
    except Exception as e:
        logger.error(f"Error loading quiz scores: {e}")
        return {}

def save_quiz_scores(scores):
    """Save quiz scores to file"""
    try:
        data = {'scores': scores}
        with open(SCORES_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving quiz scores: {e}")
        return False

def get_user_score(user_id):
    """Get user's quiz score"""
    scores = load_quiz_scores()
    user_scores = scores.get(str(user_id), {
        'total_answered': 0,
        'total_correct': 0,
        'quizzes_completed': 0,
        'best_score': 0
    })
    return user_scores

def update_user_score(user_id, correct, total):
    """Update user's quiz score"""
    scores = load_quiz_scores()
    user_id_str = str(user_id)
    
    if user_id_str not in scores:
        scores[user_id_str] = {
            'total_answered': 0,
            'total_correct': 0,
            'quizzes_completed': 0,
            'best_score': 0
        }
    
    scores[user_id_str]['total_answered'] += total
    scores[user_id_str]['total_correct'] += correct
    scores[user_id_str]['quizzes_completed'] += 1
    
    # Calculate accuracy percentage
    accuracy = (scores[user_id_str]['total_correct'] / scores[user_id_str]['total_answered']) * 100 if scores[user_id_str]['total_answered'] > 0 else 0
    
    # Update best score if this quiz was better
    if accuracy > scores[user_id_str]['best_score']:
        scores[user_id_str]['best_score'] = accuracy
    
    return save_quiz_scores(scores)

def load_active_quizzes():
    """Load active quiz sessions"""
    # Check if storage file is a directory
    if os.path.exists(ACTIVE_QUIZZES_FILE) and os.path.isdir(ACTIVE_QUIZZES_FILE):
        logger.error(f"Storage file is still a directory! Attempting to fix: {ACTIVE_QUIZZES_FILE}")
        _fix_storage_file(ACTIVE_QUIZZES_FILE)
        return {}
    
    if not os.path.exists(ACTIVE_QUIZZES_FILE):
        return {}
    
    try:
        with open(ACTIVE_QUIZZES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading active quizzes: {e}")
        return {}

def save_active_quizzes(quizzes):
    """Save active quiz sessions"""
    try:
        # Check if storage file is a directory
        if os.path.exists(ACTIVE_QUIZZES_FILE) and os.path.isdir(ACTIVE_QUIZZES_FILE):
            logger.error(f"Storage file is a directory! Attempting to fix: {ACTIVE_QUIZZES_FILE}")
            _fix_storage_file(ACTIVE_QUIZZES_FILE)
            return False
        
        with open(ACTIVE_QUIZZES_FILE, 'w') as f:
            json.dump(quizzes, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving active quizzes: {e}")
        return False

def start_quiz_session(user_id, question_index, question_data):
    """Start a new quiz session for a user"""
    quizzes = load_active_quizzes()
    quizzes[str(user_id)] = {
        'question_index': question_index,
        'question_data': question_data,
        'score': 0,
        'total': 0,
        'started_at': None
    }
    return save_active_quizzes(quizzes)

def get_quiz_session(user_id):
    """Get active quiz session for a user"""
    quizzes = load_active_quizzes()
    return quizzes.get(str(user_id))

def update_quiz_session(user_id, score, total):
    """Update quiz session with new score"""
    quizzes = load_active_quizzes()
    user_id_str = str(user_id)
    
    if user_id_str in quizzes:
        quizzes[user_id_str]['score'] = score
        quizzes[user_id_str]['total'] = total
        return save_active_quizzes(quizzes)
    return False

def end_quiz_session(user_id):
    """End and remove quiz session for a user"""
    quizzes = load_active_quizzes()
    user_id_str = str(user_id)
    
    if user_id_str in quizzes:
        session = quizzes[user_id_str]
        del quizzes[user_id_str]
        save_active_quizzes(quizzes)
        return session
    return None

