#!/usr/bin/env python3
"""
Scheduler script to run the bot daily at a specific time
"""

import time
import subprocess
import logging
import os
from datetime import datetime
import pytz

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_bot():
    """Run the daily sender script"""
    try:
        import os
        current_time = datetime.now()
        logger.info(f"Running daily sender at {current_time} (GMT)")
        
        # Get the script directory (works in both host and Docker)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        result = subprocess.run(
            ['python3', 'daily_sender.py'],
            cwd=script_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Daily messages sent successfully")
            if result.stdout:
                logger.info(f"Daily sender output: {result.stdout}")
        else:
            logger.error(f"Daily sender failed with code {result.returncode}")
            if result.stderr:
                logger.error(f"Error: {result.stderr}")
            if result.stdout:
                logger.error(f"Output: {result.stdout}")
    except Exception as e:
        logger.error(f"Error running daily sender: {e}", exc_info=True)

def main():
    """Main scheduler function"""
    # Set timezone to GMT
    os.environ['TZ'] = 'GMT'
    try:
        time.tzset()  # Apply timezone change (Unix only)
    except AttributeError:
        # time.tzset() not available on Windows, but we're in Docker/Linux
        pass
    
    # Load and log existing subscribers on startup
    from user_storage import get_all_subscribed_users
    existing_users = get_all_subscribed_users()
    logger.info(f"Scheduler starting - {len(existing_users)} subscribers will receive daily messages at 4:00 AM GMT")
    
    # Get current time in GMT for logging
    try:
        gmt = pytz.timezone('GMT')
        current_gmt = datetime.now(gmt)
        logger.info(f"Current GMT time: {current_gmt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    except:
        current_time = datetime.now()
        logger.info(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # We'll use manual GMT time checking for accurate triggering at 4:00 AM GMT
    # The schedule library is unreliable with timezone changes, so we check manually
    logger.info("Using manual GMT time checking for daily trigger at 4:00 AM GMT")
    
    # You can also test immediately (uncomment to test)
    # logger.info("TESTING: Running daily sender now...")
    # run_bot()
    
    logger.info("Scheduler started. Bot will run daily at 4:00 AM GMT")
    logger.info("Press Ctrl+C to stop")
    
    last_logged_hour = -1
    last_triggered_date = None
    last_triggered_minute = -1  # Track the minute to prevent multiple triggers in the same minute
    try:
        while True:
            # Manually check if it's 4:00 AM GMT
            try:
                gmt = pytz.timezone('GMT')
                current_gmt = datetime.now(gmt)
                current_date = current_gmt.date()
                current_minute = current_gmt.minute
                
                # If it's 4:00 AM GMT and we haven't triggered today
                # Check both hour and minute, and ensure we haven't triggered in this exact minute
                if current_gmt.hour == 4 and current_minute == 0:
                    if last_triggered_date != current_date or last_triggered_minute != current_minute:
                        logger.info(f"Manual check: It's 4:00 AM GMT! Triggering daily sender...")
                        run_bot()
                        last_triggered_date = current_date
                        last_triggered_minute = current_minute
                
                # Log every hour to confirm scheduler is running
                if current_gmt.hour != last_logged_hour and current_gmt.minute == 0:
                    next_trigger = f"Tomorrow at 04:00 GMT" if current_gmt.hour >= 4 else f"Today at 04:00 GMT"
                    logger.info(f"Scheduler is running... Current GMT time: {current_gmt.strftime('%Y-%m-%d %H:%M:%S %Z')}, Next trigger: {next_trigger}")
                    last_logged_hour = current_gmt.hour
            except Exception as e:
                logger.error(f"Error in time check: {e}")
                # Fallback to basic time check
                current_time = datetime.now()
                if current_time.hour != last_logged_hour and current_time.minute == 0:
                    logger.info(f"Scheduler is running... Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    last_logged_hour = current_time.hour
            
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")

if __name__ == "__main__":
    main()

