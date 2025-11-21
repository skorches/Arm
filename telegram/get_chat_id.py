#!/usr/bin/env python3
"""
Quick script to get your Telegram Chat ID
Run this after messaging your bot
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE')

print("=" * 50)
print("Getting your Chat ID...")
print("=" * 50)
print("\n1. First, send a message to your bot on Telegram")
print("2. Then press Enter here to continue...")
input()

url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
response = requests.get(url)
data = response.json()

if data.get('ok') and data.get('result'):
    print("\n✅ Found updates! Here are your chat IDs:\n")
    seen_chats = set()
    
    for update in data['result']:
        if 'message' in update:
            chat = update['message']['chat']
            chat_id = chat['id']
            chat_type = chat.get('type', 'unknown')
            
            if chat_id not in seen_chats:
                seen_chats.add(chat_id)
                if chat_type == 'private':
                    name = chat.get('first_name', '') + ' ' + chat.get('last_name', '')
                    print(f"👤 Personal Chat ID: {chat_id}")
                    print(f"   Name: {name.strip()}")
                elif chat_type == 'group':
                    print(f"👥 Group Chat ID: {chat_id}")
                    print(f"   Title: {chat.get('title', 'N/A')}")
                elif chat_type == 'channel':
                    print(f"📢 Channel ID: {chat_id}")
                    print(f"   Title: {chat.get('title', 'N/A')}")
                print()
    
    if seen_chats:
        print("=" * 50)
        print("Copy one of these Chat IDs to your .env file")
        print("=" * 50)
    else:
        print("❌ No messages found. Make sure you've sent a message to your bot first!")
else:
    print("❌ No updates found. Make sure you've sent a message to your bot first!")
    print(f"\nYou can also manually check: https://api.telegram.org/bot{bot_token}/getUpdates")

