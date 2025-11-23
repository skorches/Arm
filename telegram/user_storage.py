"""
Simple file-based storage for user subscriptions
"""

import json
import os
import logging
import shutil

logger = logging.getLogger(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FILE = os.path.join(SCRIPT_DIR, "subscribed_users.json")

def _fix_storage_file():
    """Fix storage file if it's a directory (Docker volume mount issue)"""
    if os.path.exists(STORAGE_FILE) and os.path.isdir(STORAGE_FILE):
        logger.error(f"Storage file path is a directory! Cannot remove mounted directory: {STORAGE_FILE}")
        logger.error("Please stop the container, remove the directory on the host, and create a file instead:")
        logger.error(f"  rm -rf {STORAGE_FILE}")
        logger.error(f"  echo '{{\"users\": []}}' > {STORAGE_FILE}")
        logger.error("Then restart the container.")
        # Don't crash - just log the error and continue
        # The user will need to fix this manually on the host
        return False
    return True

# Try to fix storage file on module load (non-fatal if it fails)
try:
    _fix_storage_file()
except Exception as e:
    logger.error(f"Error checking storage file: {e}")
    # Continue anyway - the file operations will handle errors

# Log the storage file path on module load for debugging
logger.info(f"User storage file path: {STORAGE_FILE}")

def load_subscribed_users():
    """Load list of subscribed user IDs from file"""
    # Check if storage file is a directory (shouldn't happen after fix, but double-check)
    if os.path.exists(STORAGE_FILE) and os.path.isdir(STORAGE_FILE):
        logger.error(f"Storage file is still a directory! Attempting to fix: {STORAGE_FILE}")
        _fix_storage_file()
        return []  # Return empty list after fixing
    
    if not os.path.exists(STORAGE_FILE):
        logger.info(f"Storage file does not exist yet: {STORAGE_FILE}")
        return []
    
    try:
        with open(STORAGE_FILE, 'r') as f:
            data = json.load(f)
            users = data.get('users', [])
            logger.info(f"Loaded {len(users)} subscribed users from {STORAGE_FILE}")
            return users
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in storage file {STORAGE_FILE}: {e}")
        return []
    except Exception as e:
        logger.error(f"Error loading subscribed users from {STORAGE_FILE}: {e}")
        return []

def save_subscribed_users(user_ids):
    """Save list of subscribed user IDs to file"""
    try:
        # Check if storage file is a directory (shouldn't happen after fix, but double-check)
        if os.path.exists(STORAGE_FILE) and os.path.isdir(STORAGE_FILE):
            logger.error(f"Storage file is a directory! Attempting to fix: {STORAGE_FILE}")
            _fix_storage_file()
        
        # Ensure directory exists (only if STORAGE_FILE has a directory component)
        storage_dir = os.path.dirname(STORAGE_FILE)
        if storage_dir:  # Only create directory if path has a directory component
            os.makedirs(storage_dir, exist_ok=True)
        
        data = {'users': list(set(user_ids))}  # Remove duplicates
        with open(STORAGE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Successfully saved {len(data['users'])} subscribed users to {STORAGE_FILE}")
        
        # Verify the file was written correctly
        if os.path.exists(STORAGE_FILE) and os.path.isfile(STORAGE_FILE):
            file_size = os.path.getsize(STORAGE_FILE)
            logger.info(f"Storage file verified: {STORAGE_FILE} ({file_size} bytes)")
        else:
            logger.warning(f"Storage file was not created or is not a file: {STORAGE_FILE}")
            return False
        
        return True
    except PermissionError as e:
        logger.error(f"Permission denied saving subscribed users to {STORAGE_FILE}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error saving subscribed users to {STORAGE_FILE}: {e}")
        return False

def add_user(user_id):
    """Add a user to the subscription list"""
    try:
        users = load_subscribed_users()
        if user_id not in users:
            users.append(user_id)
            if save_subscribed_users(users):
                logger.info(f"Successfully added user {user_id} to subscriptions")
                return True
            else:
                logger.error(f"Failed to save user {user_id} to subscriptions")
                return False
        else:
            logger.info(f"User {user_id} is already subscribed")
            return True  # Already subscribed, consider it success
    except Exception as e:
        logger.error(f"Error adding user {user_id}: {e}")
        return False

def remove_user(user_id):
    """Remove a user from the subscription list"""
    try:
        users = load_subscribed_users()
        if user_id in users:
            users.remove(user_id)
            if save_subscribed_users(users):
                logger.info(f"Successfully removed user {user_id} from subscriptions")
                return True
            else:
                logger.error(f"Failed to save after removing user {user_id} from subscriptions")
                return False
        else:
            logger.info(f"User {user_id} is not subscribed")
            return False  # Not subscribed, return False
    except Exception as e:
        logger.error(f"Error removing user {user_id}: {e}")
        return False

def is_subscribed(user_id):
    """Check if a user is subscribed"""
    users = load_subscribed_users()
    return user_id in users

def get_all_subscribed_users():
    """Get all subscribed user IDs"""
    return load_subscribed_users()

