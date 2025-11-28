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
QUIZ_HISTORY_FILE = os.path.join(SCRIPT_DIR, "quiz_history.json")

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
    _fix_storage_file(QUIZ_HISTORY_FILE)
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
        'best_score': 0,
        'username': None,
        'first_name': None
    })
    return user_scores

def update_user_info(user_id, username=None, first_name=None):
    """Update user's name information for leaderboard"""
    scores = load_quiz_scores()
    user_id_str = str(user_id)
    
    if user_id_str not in scores:
        scores[user_id_str] = {
            'total_answered': 0,
            'total_correct': 0,
            'quizzes_completed': 0,
            'best_score': 0,
            'username': None,
            'first_name': None
        }
    
    if username:
        scores[user_id_str]['username'] = username
    if first_name:
        scores[user_id_str]['first_name'] = first_name
    
    return save_quiz_scores(scores)

def update_user_score(user_id, correct, total, username=None, first_name=None, quiz_session_score=None, quiz_session_total=None):
    """Update user's quiz score
    
    Args:
        user_id: User ID
        correct: Number of correct answers in this update
        total: Number of total answers in this update
        username: Optional username
        first_name: Optional first name
        quiz_session_score: Optional total score for a complete quiz session
        quiz_session_total: Optional total questions for a complete quiz session
    """
    scores = load_quiz_scores()
    user_id_str = str(user_id)
    
    if user_id_str not in scores:
        scores[user_id_str] = {
            'total_answered': 0,
            'total_correct': 0,
            'quizzes_completed': 0,
            'best_score': 0,
            'best_session_score': 0,
            'best_session_total': 0,
            'username': None,
            'first_name': None
        }
    
    # Update user info if provided
    if username:
        scores[user_id_str]['username'] = username
    if first_name:
        scores[user_id_str]['first_name'] = first_name
    
    # Update cumulative stats
    scores[user_id_str]['total_answered'] += total
    scores[user_id_str]['total_correct'] += correct
    
    # If this is a complete quiz session, track it
    if quiz_session_score is not None and quiz_session_total is not None and quiz_session_total > 0:
        session_accuracy = (quiz_session_score / quiz_session_total) * 100
        scores[user_id_str]['quizzes_completed'] += 1
        
        # Track best session score
        current_best = scores[user_id_str].get('best_session_score', 0)
        current_best_total = scores[user_id_str].get('best_session_total', 0)
        current_best_accuracy = (current_best / current_best_total * 100) if current_best_total > 0 else 0
        
        if session_accuracy > current_best_accuracy or (session_accuracy == current_best_accuracy and quiz_session_total > current_best_total):
            scores[user_id_str]['best_session_score'] = quiz_session_score
            scores[user_id_str]['best_session_total'] = quiz_session_total
    
    # Calculate overall accuracy percentage
    accuracy = (scores[user_id_str]['total_correct'] / scores[user_id_str]['total_answered']) * 100 if scores[user_id_str]['total_answered'] > 0 else 0
    
    # Update best score if this update improved it
    if accuracy > scores[user_id_str]['best_score']:
        scores[user_id_str]['best_score'] = accuracy
    
    return save_quiz_scores(scores)

def get_leaderboard(limit=10):
    """Get top players sorted by best score, then by total correct"""
    scores = load_quiz_scores()
    
    # Filter out users with no scores
    valid_users = []
    for user_id, user_data in scores.items():
        if user_data.get('total_answered', 0) > 0:
            valid_users.append({
                'user_id': user_id,
                'best_score': user_data.get('best_score', 0),
                'total_correct': user_data.get('total_correct', 0),
                'total_answered': user_data.get('total_answered', 0),
                'quizzes_completed': user_data.get('quizzes_completed', 0),
                'username': user_data.get('username'),
                'first_name': user_data.get('first_name')
            })
    
    # Sort by best_score (descending), then by total_correct (descending)
    valid_users.sort(key=lambda x: (x['best_score'], x['total_correct']), reverse=True)
    
    return valid_users[:limit]

def get_user_rank(user_id):
    """Get user's rank in the leaderboard"""
    leaderboard = get_leaderboard(limit=1000)  # Get all users
    user_id_str = str(user_id)
    
    for rank, user in enumerate(leaderboard, start=1):
        if user['user_id'] == user_id_str:
            return rank, user
    
    return None, None

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

def start_quiz_session(user_id, question_index, question_data, difficulty=None, category=None):
    """Start a new quiz session for a user"""
    quizzes = load_active_quizzes()
    quizzes[str(user_id)] = {
        'question_index': question_index,
        'question_data': question_data,
        'score': 0,
        'total': 0,
        'started_at': None,
        'difficulty': difficulty,  # Store difficulty to maintain it throughout session
        'category': category  # Store category to maintain it throughout session
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

def save_quiz_to_history(user_id, session_data):
    """Save a completed quiz session to history"""
    import datetime
    
    # Check if storage file is a directory
    if os.path.exists(QUIZ_HISTORY_FILE) and os.path.isdir(QUIZ_HISTORY_FILE):
        logger.error(f"Storage file is a directory! Cannot save history: {QUIZ_HISTORY_FILE}")
        return False
    
    try:
        # Load existing history
        if os.path.exists(QUIZ_HISTORY_FILE):
            with open(QUIZ_HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = {}
        
        user_id_str = str(user_id)
        
        # Initialize user history if needed
        if user_id_str not in history:
            history[user_id_str] = []
        
        # Add timestamp and save session
        session_with_timestamp = {
            **session_data,
            'completed_at': datetime.datetime.now().isoformat(),
            'session_id': f"{user_id_str}_{datetime.datetime.now().timestamp()}"
        }
        
        history[user_id_str].append(session_with_timestamp)
        
        # Keep only last 100 sessions per user to prevent file from growing too large
        if len(history[user_id_str]) > 100:
            history[user_id_str] = history[user_id_str][-100:]
        
        # Save history
        with open(QUIZ_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        
        return True
    except Exception as e:
        logger.error(f"Error saving quiz to history: {e}")
        return False

def get_quiz_history(user_id, limit=10):
    """Get quiz history for a user"""
    if not os.path.exists(QUIZ_HISTORY_FILE):
        return []
    
    try:
        with open(QUIZ_HISTORY_FILE, 'r') as f:
            history = json.load(f)
        
        user_id_str = str(user_id)
        user_history = history.get(user_id_str, [])
        
        # Return most recent sessions first
        return list(reversed(user_history[-limit:]))
    except Exception as e:
        logger.error(f"Error loading quiz history: {e}")
        return []

