"""
Job Hunter Scheduler - Run searches automatically at scheduled times
"""

import schedule
import time
import logging
from datetime import datetime

from job_hunter import JobHunter
from config import APPLICATION

# Setup logging
logging.basicConfig(
    filename='job_hunter.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def run_job_search():
    """Run the job search"""
    print(f"\n{'='*60}")
    print(f"🕐 Scheduled Job Search - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    logging.info("Starting scheduled job search")
    
    try:
        hunter = JobHunter()
        jobs = hunter.run_search(headless=True)
        
        logging.info(f"Found {len(jobs)} matching jobs")
        
        # Auto-apply if enabled
        if APPLICATION.get('auto_apply'):
            hunter.auto_apply(jobs)
            logging.info("Auto-apply completed")
        
        hunter.show_stats()
        
    except Exception as e:
        logging.error(f"Job search error: {e}")
        print(f"❌ Error: {e}")


def check_responses_job():
    """Check for email responses"""
    print(f"\n{'='*60}")
    print(f"📧 Checking Email Responses - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    logging.info("Starting email response check")
    
    try:
        hunter = JobHunter()
        hunter.check_responses()
        logging.info("Email check completed")
        
    except Exception as e:
        logging.error(f"Email check error: {e}")
        print(f"❌ Error: {e}")


def auto_apply_job():
    """Run auto-apply for pending jobs"""
    print(f"\n{'='*60}")
    print(f"🤖 Auto-Apply Run - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    logging.info("Starting auto-apply job")
    
    try:
        hunter = JobHunter()
        hunter.auto_apply(max_applications=10)
        logging.info("Auto-apply completed")
        
    except Exception as e:
        logging.error(f"Auto-apply error: {e}")
        print(f"❌ Error: {e}")


def run_scheduler():
    """Run the scheduler"""
    print("\n" + "="*60)
    print("🤖 JOB HUNTER SCHEDULER STARTED")
    print("="*60)
    print("Scheduled tasks:")
    print("  📋 Job Search: Every day at 9:00 AM and 6:00 PM")
    print("  📧 Email Check: Every 2 hours")
    print("  🤖 Auto-Apply: Every 4 hours (if enabled)")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Schedule job searches
    schedule.every().day.at("09:00").do(run_job_search)
    schedule.every().day.at("18:00").do(run_job_search)
    
    # Schedule email response checking (every 2 hours)
    schedule.every(2).hours.do(check_responses_job)
    
    # Schedule auto-apply (every 4 hours, if enabled)
    if APPLICATION.get('auto_apply'):
        schedule.every(4).hours.do(auto_apply_job)
        print("✅ Auto-apply is ENABLED")
    else:
        print("⚠️  Auto-apply is DISABLED")
    
    # Run job search immediately on start
    run_job_search()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped. Goodbye!")
