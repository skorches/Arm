#!/usr/bin/env python3
"""
Scheduler script to run the bot daily at a specific time
"""

import schedule
import time
import asyncio
import subprocess
import logging
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_bot():
    """Run the daily sender script"""
    try:
        logger.info(f"Running daily sender at {datetime.now()}")
        result = subprocess.run(
            ['python3', 'daily_sender.py'],
            cwd='/home/wars09/Cursor/Arm/telegram',
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("Daily messages sent successfully")
        else:
            logger.error(f"Daily sender failed: {result.stderr}")
    except Exception as e:
        logger.error(f"Error running daily sender: {e}")

def main():
    """Main scheduler function"""
    # Schedule the bot to run daily at 4:00 AM GMT
    schedule.every().day.at("04:00").do(run_bot)
    
    # You can also test immediately
    # run_bot()
    
    logger.info("Scheduler started. Bot will run daily at 4:00 AM GMT")
    logger.info("Press Ctrl+C to stop")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")

if __name__ == "__main__":
    main()

