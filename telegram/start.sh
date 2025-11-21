#!/bin/bash
# Startup script to run both bot and scheduler

# Start the interactive bot in the background (handles user queries)
python3 bot_runner.py &

# Start the scheduler in the foreground (sends daily messages)
python3 scheduler.py

