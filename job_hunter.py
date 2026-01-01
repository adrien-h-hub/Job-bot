"""
Job Hunter Bot - Main Application
Searches LinkedIn and Indeed for jobs, filters them, and optionally auto-applies
"""

import time
import argparse
import logging
from datetime import datetime
from typing import List, Dict

from config import (
    PROFILE, JOB_SEARCH, EXCLUDE_KEYWORDS, REQUIRED_KEYWORDS,
    LINKEDIN, INDEED, APPLICATION, EMAIL, DATABASE
)
from job_database import JobDatabase
from job_matcher import JobMatcher
from linkedin_bot import LinkedInBot
from indeed_bot import IndeedBot
from email_notifier import EmailNotifier
from smart_timing import SmartTiming
from webhook_notifier import WebhookNotifier

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_hunter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JobHunter:
    def __init__(self):
        self.db = JobDatabase(DATABASE['path'])
        self.matcher = JobMatcher(
            required_keywords=REQUIRED_KEYWORDS,
            exclude_keywords=EXCLUDE_KEYWORDS,
            experience_level=JOB_SEARCH.get('experience_level', []),
            min_salary=JOB_SEARCH.get('salary_min')
        )
        self.linkedin_bot = None
        self.indeed_bot = None
        self.email_notifier = None
        self.smart_timing = SmartTiming()
        self.webhook_notifier = None
        
        # Initialize webhook if configured
        import os
        webhook_url = os.getenv('WEBHOOK_URL')
        webhook_platform = os.getenv('WEBHOOK_PLATFORM', 'slack')
        if webhook_url:
            self.webhook_notifier = WebhookNotifier(webhook_url, webhook_platform)
        
        # Initialize email if configured
        if APPLICATION['send_email_summary'] and EMAIL.get('from_email'):
            self.email_notifier = EmailNotifier(
                smtp_server=EMAIL['smtp_server'],
                smtp_port=EMAIL['smtp_port'],
                smtp_username=EMAIL['smtp_username'],
                smtp_password=EMAIL['smtp_password'],
                from_email=EMAIL['from_email'],
                from_name=EMAIL['from_name']
            )
    
    def run_search(self, sources: List[str] = None, headless: bool = False) -> List[Dict]:
        """
        Run job search on specified sources
        
        Args:
            sources: List of sources to search ['linkedin', 'indeed']
            headless: Run browsers in headless mode
        """
        if sources is None:
            sources = ['linkedin', 'indeed']
        
        all_jobs = []
        
        print("\n" + "="*60)
        print("🎯 JOB HUNTER BOT - Starting Search")
        print("="*60)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"🔍 Keywords: {', '.join(JOB_SEARCH['keywords'])}")
        print(f"📍 Location: {JOB_SEARCH['location']}")
        print(f"🌐 Sources: {', '.join(sources)}")
        print("="*60 + "\n")
        
        # Search LinkedIn
        if 'linkedin' in sources:
            linkedin_jobs = self._search_linkedin(headless)
            all_jobs.extend(linkedin_jobs)
        
        # Search Indeed
        if 'indeed' in sources:
            indeed_jobs = self._search_indeed(headless)
            all_jobs.extend(indeed_jobs)
        
        # Filter and score jobs
        print("\n📊 Analyzing jobs...")
        filtered_jobs = self.matcher.filter_jobs(all_jobs, min_score=40)
        
        print(f"\n✅ Found {len(filtered_jobs)} jobs matching your criteria (out of {len(all_jobs)} total)")
        
        # Notify about high-match jobs
        if self.webhook_notifier:
            for job in filtered_jobs:
                if job.get('match_score', 0) >= 70:
                    self.webhook_notifier.notify_new_job(job)
        
        # Save to database
        if APPLICATION['save_jobs']:
            new_count = 0
            for job in filtered_jobs:
                if self.db.add_job(job):
                    new_count += 1
            print(f"💾 Saved {new_count} new jobs to database")
        
        # Display top jobs
        self._display_top_jobs(filtered_jobs[:10])
        
        # Send email summary
        if self.email_notifier and filtered_jobs:
            stats = self.db.get_stats()
            self.email_notifier.send_job_summary(
                recipient_email=EMAIL['recipient_email'],
                jobs=filtered_jobs,
                stats=stats
            )
        
        return filtered_jobs
    
    def _search_linkedin(self, headless: bool = False, max_retries: int = 3) -> List[Dict]:
        """Search LinkedIn for jobs with retry logic"""
        print("\n🔵 Searching LinkedIn...")
        
        for attempt in range(max_retries):
            try:
                if not self.linkedin_bot:
                    self.linkedin_bot = LinkedInBot(
                        LINKEDIN['email'], 
                        LINKEDIN['password'],
                        headless=headless
                    )
                
                if not self.linkedin_bot.logged_in:
                    if not self.linkedin_bot.login():
                        logger.warning(f"LinkedIn login failed (attempt {attempt + 1}/{max_retries})")
                        if attempt < max_retries - 1:
                            time.sleep(5 * (attempt + 1))  # Exponential backoff
                            continue
                        print("❌ LinkedIn login failed after all retries")
                        return []
                
                jobs = []
                for keyword in JOB_SEARCH['keywords']:
                    keyword_jobs = self.linkedin_bot.search_jobs(
                        keywords=keyword,
                        location=JOB_SEARCH['location'],
                        easy_apply_only=LINKEDIN.get('easy_apply_only', True)
                    )
                    jobs.extend(keyword_jobs)
                    time.sleep(5)  # Be nice to LinkedIn
                
                print(f"✅ Found {len(jobs)} jobs on LinkedIn")
                logger.info(f"LinkedIn search successful: {len(jobs)} jobs found")
                return jobs
                
            except Exception as e:
                logger.error(f"LinkedIn search error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print(f"⚠️  Retrying in {5 * (attempt + 1)} seconds...")
                    time.sleep(5 * (attempt + 1))
                else:
                    print(f"❌ LinkedIn search failed after {max_retries} attempts: {e}")
                    return []
        
        return []
    
    def _search_indeed(self, headless: bool = False, max_retries: int = 3) -> List[Dict]:
        """Search Indeed for jobs with retry logic"""
        print("\n🟢 Searching Indeed...")
        
        for attempt in range(max_retries):
            try:
                if not self.indeed_bot:
                    self.indeed_bot = IndeedBot(headless=headless)
                
                jobs = []
                for keyword in JOB_SEARCH['keywords']:
                    keyword_jobs = self.indeed_bot.search_jobs(
                        keywords=keyword,
                        location=JOB_SEARCH['location'],
                        posted_within_days=JOB_SEARCH.get('posted_within_days', 7),
                        remote=JOB_SEARCH.get('remote', False)
                    )
                    jobs.extend(keyword_jobs)
                    time.sleep(3)  # Be nice to Indeed
                
                print(f"✅ Found {len(jobs)} jobs on Indeed")
                logger.info(f"Indeed search successful: {len(jobs)} jobs found")
                return jobs
                
            except Exception as e:
                logger.error(f"Indeed search error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print(f"⚠️  Retrying in {3 * (attempt + 1)} seconds...")
                    time.sleep(3 * (attempt + 1))
                else:
                    print(f"❌ Indeed search failed after {max_retries} attempts: {e}")
                    return []
        
        return []
    
    def _display_top_jobs(self, jobs: List[Dict]):
        """Display top matching jobs"""
        if not jobs:
            return
        
        print("\n" + "="*60)
        print("🏆 TOP MATCHING JOBS")
        print("="*60)
        
        for i, job in enumerate(jobs, 1):
            score = job.get('match_score', 0)
            easy = "⚡" if job.get('easy_apply') else ""
            source = job.get('source', 'unknown').upper()
            
            print(f"\n{i}. [{score}% match] {job.get('title')}")
            print(f"   🏢 {job.get('company')} ({source}) {easy}")
            print(f"   📍 {job.get('location')}")
            if job.get('salary'):
                print(f"   💰 {job.get('salary')}")
            print(f"   🔗 {job.get('url', 'No URL')[:60]}...")
    
    def auto_apply(self, jobs: List[Dict] = None, max_applications: int = 10):
        """
        Auto-apply to jobs
        ⚠️ USE WITH CAUTION - Make sure your profile is complete
        """
        if not APPLICATION['auto_apply']:
            print("❌ Auto-apply is disabled in config")
            return
        
        if jobs is None:
            jobs = self.db.get_new_jobs()
        
        # Filter for easy apply only
        easy_apply_jobs = [j for j in jobs if j.get('easy_apply')]
        
        print(f"\n🤖 Auto-Apply Mode")
        print(f"Found {len(easy_apply_jobs)} Easy Apply jobs")
        
        applied_count = 0
        
        for job in easy_apply_jobs[:max_applications]:
            print(f"\n📝 Applying to: {job.get('title')} at {job.get('company')}")
            
            # Check if timing is optimal
            if not self.smart_timing.should_apply_now(job):
                optimal_time = self.smart_timing.get_optimal_apply_time(job)
                print(f"   ⏰ Queuing for optimal time: {self.smart_timing.format_optimal_time(job)}")
                self.db.add_queued_application(
                    job.get('job_id'),
                    optimal_time.isoformat()
                )
                continue
            
            try:
                if 'linkedin' in job.get('source', ''):
                    if not self.linkedin_bot:
                        self.linkedin_bot = LinkedInBot(
                            LINKEDIN['email'], LINKEDIN['password']
                        )
                        self.linkedin_bot.login()
                    
                    success, complex_questions = self.linkedin_bot.apply_easy_apply(
                        job.get('url'),
                        PROFILE.get('resume_path')
                    )
                    
                    if complex_questions:
                        print(f"   ⚠️ Complex questions detected - manual intervention required")
                        for q in complex_questions:
                            print(f"      - {q.get('text', 'Unknown question')}")
                        continue
                else:
                    if not self.indeed_bot:
                        self.indeed_bot = IndeedBot()
                
                # Delay between applications
                time.sleep(APPLICATION.get('delay_between_applications', 30))
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        print(f"\n🎉 Applied to {applied_count} jobs!")
    
    def show_stats(self):
        """Display application statistics"""
        stats = self.db.get_stats()
        
        print("\n" + "="*40)
        print("📊 YOUR JOB SEARCH STATISTICS")
        print("="*40)
        print(f"📋 Total Jobs Found: {stats['total_jobs']}")
        print(f"🆕 New Jobs: {stats['new_jobs']}")
        print(f"📨 Applied: {stats['applied']}")
        print(f"❌ Rejected: {stats['rejected']}")
        print(f"🎤 Interviews: {stats['interviews']}")
        print("="*40)
    
    def find_company_contacts(self, company_name: str):
        """Find and store contacts for a company"""
        try:
            from email_finder import EmailFinder
            
            finder = EmailFinder(company_name)
            
            # Find RHE contact
            rhe = finder.find_rhe_contact()
            if rhe:
                self.db.add_contact({
                    'company_name': company_name,
                    'name': rhe.get('name', 'RHE'),
                    'email': rhe.get('email'),
                    'position': 'RHE',
                    'source': 'email_finder',
                    'confidence': 0.8
                })
                print(f"      ✅ Found RHE: {rhe.get('email')}")
            
            # Find Site Manager contact
            site_manager = finder.find_site_manager_contact()
            if site_manager:
                self.db.add_contact({
                    'company_name': company_name,
                    'name': site_manager.get('name', 'Site Manager'),
                    'email': site_manager.get('email'),
                    'position': 'Site Manager',
                    'source': 'email_finder',
                    'confidence': 0.8
                })
                print(f"      ✅ Found Site Manager: {site_manager.get('email')}")
            
            if not rhe and not site_manager:
                print(f"      ℹ️ No contacts found for {company_name}")
                
        except Exception as e:
            print(f"      ⚠️ Error finding contacts: {e}")
    
    def check_responses(self):
        """Check for email responses and process them"""
        try:
            from response_manager import ResponseManager
            
            print("\n📧 Checking for email responses...")
            
            config = {
                'profile': PROFILE,
                'email': EMAIL
            }
            
            manager = ResponseManager(config, DATABASE['path'])
            manager.check_and_process_responses()
            
            print("✅ Email check complete")
            
        except Exception as e:
            print(f"❌ Error checking responses: {e}")
    
    def process_queued_applications(self):
        """Process applications that are ready to be submitted"""
        print("\n⏰ Processing queued applications...")
        
        pending = self.db.get_pending_applications()
        
        if not pending:
            print("No applications ready to submit")
            return
        
        print(f"Found {len(pending)} applications ready to submit")
        
        for app in pending:
            job = {
                'job_id': app['job_id'],
                'title': app['title'],
                'company': app['company'],
                'url': app['url'],
                'source': app['source']
            }
            
            print(f"\n📝 Submitting queued application: {job['title']} at {job['company']}")
            
            try:
                if 'linkedin' in job.get('source', ''):
                    if not self.linkedin_bot:
                        self.linkedin_bot = LinkedInBot(
                            LINKEDIN['email'], LINKEDIN['password']
                        )
                        self.linkedin_bot.login()
                    
                    success, complex_questions = self.linkedin_bot.apply_easy_apply(
                        job.get('url'),
                        PROFILE.get('resume_path')
                    )
                else:
                    if not self.indeed_bot:
                        self.indeed_bot = IndeedBot()
                    
                    success, complex_questions = self.indeed_bot.apply_to_job(job.get('url'), PROFILE)
                
                if success:
                    self.db.mark_as_applied(job.get('job_id'))
                    self.db.mark_queue_completed(app['id'])
                    print("   ✅ Application submitted!")
                    
                    if self.email_notifier:
                        self.email_notifier.send_application_confirmation(
                            EMAIL['recipient_email'], job
                        )
                else:
                    print("   ⚠️ Application may have failed")
                
            except Exception as e:
                logger.error(f"Error processing queued application: {e}")
                print(f"   ❌ Error: {e}")
    
    def export_jobs(self, filepath: str = "jobs_export.csv"):
        """Export jobs to CSV"""
        self.db.export_to_csv(filepath)


def main():
    parser = argparse.ArgumentParser(description='Job Hunter Bot')
    parser.add_argument('--search', action='store_true', help='Run job search')
    parser.add_argument('--apply', action='store_true', help='Auto-apply to jobs')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--export', type=str, help='Export jobs to CSV file')
    parser.add_argument('--linkedin-only', action='store_true', help='Search LinkedIn only')
    parser.add_argument('--indeed-only', action='store_true', help='Search Indeed only')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    
    args = parser.parse_args()
    
    hunter = JobHunter()
    
    if args.stats:
        hunter.show_stats()
    
    if args.export:
        hunter.export_jobs(args.export)
    
    if args.search:
        sources = []
        if args.linkedin_only:
            sources = ['linkedin']
        elif args.indeed_only:
            sources = ['indeed']
        else:
            sources = ['linkedin', 'indeed']
        
        jobs = hunter.run_search(sources=sources, headless=args.headless)
        
        if args.apply:
            hunter.auto_apply(jobs)
    
    if not any([args.search, args.apply, args.stats, args.export]):
        # Default: run search
        hunter.run_search()


if __name__ == "__main__":
    main()
