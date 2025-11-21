#!/bin/bash
# Script to create .env file if it doesn't exist

ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Creating .env file..."
    cat > "$ENV_FILE" << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE

# Note: TELEGRAM_CHAT_ID is no longer needed!
# The bot now handles multiple users and subscriptions automatically.
# Users can subscribe using /subscribe command in the bot.
EOF
    echo "✅ .env file created!"
    echo "📝 Edit it if you need to change the bot token."
else
    echo "✅ .env file already exists"
fi

