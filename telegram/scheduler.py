#!/usr/bin/env python3
"""
Scheduler script to run the bot daily at a specific time
"""

import schedule
import time
import asyncio
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
    
    # Schedule the bot to run daily at 4:00 AM GMT
    # Note: schedule library uses system local time, so we rely on TZ=GMT environment variable
    # We'll also check the time manually to ensure it's GMT
    def schedule_at_gmt_4am():
        """Wrapper to ensure we're checking GMT time"""
        current_time = datetime.now()
        # Double-check it's actually 4 AM
        if current_time.hour == 4 and current_time.minute == 0:
            logger.info(f"Triggering daily sender at GMT 4:00 AM (current time: {current_time})")
            run_bot()
        else:
            logger.warning(f"Scheduled task triggered but time is {current_time}, not 4:00 AM GMT")
    
    schedule.every().day.at("04:00").do(schedule_at_gmt_4am)
    
    # Log next run time
    try:
        next_run = schedule.next_run()
        if next_run:
            logger.info(f"Next scheduled execution: {next_run}")
    except:
        logger.info("Next scheduled execution: Tomorrow at 04:00 GMT")
    
    # You can also test immediately (uncomment to test)
    # logger.info("TESTING: Running daily sender now...")
    # run_bot()
    
    logger.info("Scheduler started. Bot will run daily at 4:00 AM GMT")
    logger.info("Press Ctrl+C to stop")
    
    last_logged_hour = -1
    last_triggered_date = None
    try:
        while True:
            # Check schedule library
            schedule.run_pending()
            
            # Also manually check if it's 4:00 AM GMT (double-check)
            try:
                gmt = pytz.timezone('GMT')
                current_gmt = datetime.now(gmt)
                current_date = current_gmt.date()
                
                # If it's 4:00 AM GMT and we haven't triggered today
                if current_gmt.hour == 4 and current_gmt.minute == 0:
                    if last_triggered_date != current_date:
                        logger.info(f"Manual check: It's 4:00 AM GMT! Triggering daily sender...")
                        run_bot()
                        last_triggered_date = current_date
                
                # Log every hour to confirm scheduler is running
                if current_gmt.hour != last_logged_hour and current_gmt.minute == 0:
                    logger.info(f"Scheduler is running... Current GMT time: {current_gmt.strftime('%Y-%m-%d %H:%M:%S %Z')}, Next run: {schedule.next_run()}")
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

