# Quick Fix for Docker Issues

## Issue 1: Obsolete `version` field
✅ **Fixed!** Removed the `version: '3.8'` line from docker-compose.yml

## Issue 2: Missing .env file

You have two options:

### Option 1: Create .env file (Recommended)

Run this command in the telegram directory:
```bash
cd /root/Arm/telegram  # or wherever your telegram folder is
./setup_env.sh
```

Or create it manually:
```bash
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=8410859508:AAEVHpQlqkPDSglcCz16xrlhtx-wOIdlZOE
EOF
```

### Option 2: Use environment variable directly

The docker-compose.yml now has a default token, so you can run:
```bash
docker-compose up -d --build
```

The bot token is already set as a default in docker-compose.yml, so it will work even without .env file.

## Deploy

After creating .env (or using the default), run:
```bash
docker-compose up -d --build
```

## Verify

Check logs:
```bash
docker-compose logs -f
```

