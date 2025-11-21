"""
Simple file-based storage for user subscriptions
"""

import json
import os
import logging

logger = logging.getLogger(__name__)

STORAGE_FILE = "subscribed_users.json"

def load_subscribed_users():
    """Load list of subscribed user IDs from file"""
    if not os.path.exists(STORAGE_FILE):
        return []
    
    try:
        with open(STORAGE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('users', [])
    except Exception as e:
        logger.error(f"Error loading subscribed users: {e}")
        return []

def save_subscribed_users(user_ids):
    """Save list of subscribed user IDs to file"""
    try:
        data = {'users': list(set(user_ids))}  # Remove duplicates
        with open(STORAGE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving subscribed users: {e}")
        return False

def add_user(user_id):
    """Add a user to the subscription list"""
    users = load_subscribed_users()
    if user_id not in users:
        users.append(user_id)
        save_subscribed_users(users)
        return True
    return False

def remove_user(user_id):
    """Remove a user from the subscription list"""
    users = load_subscribed_users()
    if user_id in users:
        users.remove(user_id)
        save_subscribed_users(users)
        return True
    return False

def is_subscribed(user_id):
    """Check if a user is subscribed"""
    users = load_subscribed_users()
    return user_id in users

def get_all_subscribed_users():
    """Get all subscribed user IDs"""
    return load_subscribed_users()

