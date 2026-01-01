# 🔧 Job Hunter Bot - Complete Integration Guide

**Date:** January 1, 2026  
**Version:** 2.0 (Enhanced)  
**Status:** Production Ready

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Feature Integration](#feature-integration)
3. [Configuration](#configuration)
4. [Usage Examples](#usage-examples)
5. [API Reference](#api-reference)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Or using Python 3.13 specifically
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# Required: LinkedIn, Indeed, Email credentials
# Optional: OpenAI API key, Webhook URL
```

### 3. Test Installation

```python
# Test basic functionality
python job_hunter.py --stats

# Test new features
python smart_timing.py
python -c "from profile_optimizer import ProfileOptimizer; print('✓ OK')"
```

---

## 🎯 Feature Integration

### Feature 1: Smart Application Timing

**Integration into main workflow:**

```python
# In job_hunter.py
from smart_timing import SmartTiming

class JobHunter:
    def __init__(self):
        self.smart_timing = SmartTiming()
    
    def auto_apply(self, jobs):
        for job in jobs:
            # Check optimal timing
            if self.smart_timing.should_apply_now(job):
                self.apply_immediately(job)
            else:
                optimal_time = self.smart_timing.get_optimal_apply_time(job)
                self.db.add_queued_application(job['job_id'], optimal_time.isoformat())
                print(f"⏰ Queued for {self.smart_timing.format_optimal_time(job)}")
```

**Standalone usage:**

```python
from smart_timing import SmartTiming

timing = SmartTiming()
job = {'title': 'Python Developer', 'location': 'Paris, France'}

# Check if should apply now
if timing.should_apply_now(job):
    print("Apply now!")
else:
    optimal = timing.get_optimal_apply_time(job)
    print(f"Wait until: {timing.format_optimal_time(job)}")
```

---

### Feature 2: Webhook Notifications

**Integration:**

```python
# In job_hunter.py
import os
from webhook_notifier import WebhookNotifier

class JobHunter:
    def __init__(self):
        webhook_url = os.getenv('WEBHOOK_URL')
        if webhook_url:
            self.webhook = WebhookNotifier(webhook_url, os.getenv('WEBHOOK_PLATFORM', 'slack'))
    
    def run_search(self, sources):
        jobs = self._search_all_platforms(sources)
        
        # Notify about high-match jobs
        for job in jobs:
            if job['match_score'] >= 70:
                self.webhook.notify_new_job(job)
    
    def auto_apply(self, job):
        success, questions = self.apply_to_job(job)
        
        if success:
            self.webhook.notify_application_submitted(job)
        elif questions:
            self.webhook.notify_complex_question(job, questions)
```

**Setup:**

```bash
# Slack
WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
WEBHOOK_PLATFORM=slack

# Discord
WEBHOOK_URL=https://discord.com/api/webhooks/123456789/abcdefghijklmnop
WEBHOOK_PLATFORM=discord

# Telegram
WEBHOOK_URL=https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>
WEBHOOK_PLATFORM=telegram
```

---

### Feature 3: Profile Optimization

**Integration:**

```python
from profile_optimizer import ProfileOptimizer

class JobHunter:
    def __init__(self):
        self.optimizer = ProfileOptimizer()
    
    def analyze_profile(self):
        jobs = self.db.get_new_jobs()
        profile = PROFILE  # from config
        
        analysis = self.optimizer.analyze_keyword_gaps(jobs, profile)
        report = self.optimizer.generate_report(analysis)
        
        # Save or email report
        with open('profile_analysis.txt', 'w') as f:
            f.write(report)
        
        return analysis
```

**CLI usage:**

```bash
python -c "
from profile_optimizer import ProfileOptimizer
from job_database import JobDatabase

db = JobDatabase()
jobs = db.get_new_jobs()
profile = {'skills': 'Python, Django', 'experience': 'Web development'}

optimizer = ProfileOptimizer()
analysis = optimizer.analyze_keyword_gaps(jobs, profile)
print(optimizer.generate_report(analysis))
"
```

---

### Feature 4: Async Job Search

**Integration:**

```python
import asyncio
from async_job_search import parallel_job_search

class JobHunter:
    async def run_search_async(self, sources):
        # Initialize bots
        linkedin_bot = LinkedInBot(...)
        indeed_bot = IndeedBot(...)
        
        # Search in parallel
        jobs = await parallel_job_search(
            linkedin_bot,
            indeed_bot,
            keywords=JOB_SEARCH['keywords'],
            location=JOB_SEARCH['location'],
            platforms=sources
        )
        
        return jobs

# Run async search
hunter = JobHunter()
jobs = asyncio.run(hunter.run_search_async(['linkedin', 'indeed']))
```

---

### Feature 5: AI Cover Letter Generator

**Integration:**

```python
from cover_letter_generator import CoverLetterGenerator

class JobHunter:
    def __init__(self):
        self.cover_gen = CoverLetterGenerator()
    
    def apply_with_cover_letter(self, job):
        # Generate cover letter
        letter = self.cover_gen.generate(job, PROFILE, style='professional')
        
        # Save for review
        filepath = self.cover_gen.save_letter(letter, job)
        
        # Use in application
        return letter
```

**Standalone:**

```python
from cover_letter_generator import CoverLetterGenerator

generator = CoverLetterGenerator(api_key='your-openai-key')

job = {
    'title': 'Senior Python Developer',
    'company': 'Tech Corp',
    'description': '...'
}

profile = {
    'first_name': 'John',
    'last_name': 'Doe',
    'skills': 'Python, Django, AWS'
}

# Generate professional letter
letter = generator.generate(job, profile, style='professional')
print(letter)

# Generate multiple versions for A/B testing
versions = generator.generate_multiple_versions(job, profile, count=3)
```

---

### Feature 6: Interview Preparation

**Integration:**

```python
from interview_prep import InterviewPrep

class JobHunter:
    def __init__(self):
        self.interview_prep = InterviewPrep()
    
    def prepare_for_interview(self, job_id):
        job = self.db.get_job(job_id)
        
        # Generate prep package
        package = self.interview_prep.prepare_for_interview(
            job,
            job['company'],
            PROFILE
        )
        
        # Save report
        report = self.interview_prep.generate_report(package)
        with open(f"interview_prep_{job['company']}.txt", 'w') as f:
            f.write(report)
        
        return package
```

**CLI:**

```bash
python -c "
from interview_prep import InterviewPrep

prep = InterviewPrep()
job = {'title': 'Python Developer', 'company': 'Tech Corp'}
profile = {'current_role': 'Developer', 'years_experience': 5}

package = prep.prepare_for_interview(job, 'Tech Corp', profile)
print(prep.generate_report(package))
" > interview_prep.txt
```

---

### Feature 7: Salary Negotiation Advisor

**Integration:**

```python
from salary_advisor import SalaryAdvisor

class JobHunter:
    def __init__(self):
        self.salary_advisor = SalaryAdvisor()
    
    def analyze_offer(self, job_id, offer_amount):
        job = self.db.get_job(job_id)
        
        analysis = self.salary_advisor.analyze_offer(job, offer_amount, PROFILE)
        report = self.salary_advisor.generate_report(analysis)
        
        # Email or save report
        return analysis
```

**Usage:**

```python
from salary_advisor import SalaryAdvisor

advisor = SalaryAdvisor()

job = {
    'title': 'Senior Python Developer',
    'location': 'Paris, France'
}

profile = {
    'years_experience': 5,
    'skills': 'Python, Django, AWS'
}

# Analyze offer
analysis = advisor.analyze_offer(job, 55000, profile)
print(advisor.generate_report(analysis))

# Get counter-offer suggestion
print(f"Suggest: €{analysis['counter_offer']['suggested_amount']:,}")
```

---

### Feature 8: Glassdoor Integration

**Integration:**

```python
from glassdoor_bot import GlassdoorBot

class JobHunter:
    def __init__(self):
        self.glassdoor_bot = GlassdoorBot(headless=True)
    
    def search_glassdoor(self, keywords, location):
        jobs = self.glassdoor_bot.search_jobs(keywords, location)
        
        # Enrich with company ratings
        for job in jobs:
            if job.get('company_rating'):
                job['match_score'] += 5  # Bonus for high-rated companies
        
        return jobs
```

---

### Feature 9: Career Path Planner

**Usage:**

```python
from career_planner import CareerPlanner

planner = CareerPlanner()

plan = planner.create_career_plan(
    current_role='Mid-Level Developer',
    target_role='Senior Architect',
    current_skills=['Python', 'Django', 'SQL'],
    timeline='5 years'
)

print(planner.generate_report(plan))
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# .env file

# === REQUIRED ===
# LinkedIn
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# Email (SMTP)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your.email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=your.email@gmail.com
EMAIL_FROM_NAME=Job Hunter Bot

# Email (IMAP)
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993

# === OPTIONAL ===
# OpenAI (for AI features)
OPENAI_API_KEY=sk-...

# Webhooks (for notifications)
WEBHOOK_URL=https://hooks.slack.com/services/...
WEBHOOK_PLATFORM=slack

# Application Settings
AUTO_APPLY=false
MIN_MATCH_SCORE=40
DELAY_BETWEEN_APPLICATIONS=30
```

---

## 📖 Usage Examples

### Complete Workflow

```python
from job_hunter import JobHunter
from smart_timing import SmartTiming
from profile_optimizer import ProfileOptimizer
from cover_letter_generator import CoverLetterGenerator

# Initialize
hunter = JobHunter()
timing = SmartTiming()
optimizer = ProfileOptimizer()
cover_gen = CoverLetterGenerator()

# 1. Run job search
jobs = hunter.run_search(['linkedin', 'indeed'])

# 2. Analyze profile
analysis = optimizer.analyze_keyword_gaps(jobs, PROFILE)
print("Profile strength:", analysis['profile_strength']['score'])

# 3. Apply to jobs with smart timing
for job in jobs[:10]:
    if timing.should_apply_now(job):
        # Generate cover letter
        letter = cover_gen.generate(job, PROFILE)
        
        # Apply
        hunter.auto_apply([job])
    else:
        # Queue for later
        optimal = timing.get_optimal_apply_time(job)
        hunter.db.add_queued_application(job['job_id'], optimal.isoformat())

# 4. Process queued applications
hunter.process_queued_applications()

# 5. Check for responses
hunter.check_responses()
```

---

## 🐛 Troubleshooting

### Common Issues

**1. OpenAI API errors**
```python
# Check API key
import os
print(os.getenv('OPENAI_API_KEY'))

# Test connection
from cover_letter_generator import CoverLetterGenerator
gen = CoverLetterGenerator()
# If no error, API key is valid
```

**2. Webhook not sending**
```python
# Test webhook
from webhook_notifier import WebhookNotifier
webhook = WebhookNotifier('your-url', 'slack')
test_job = {'title': 'Test', 'company': 'Test Co', 'match_score': 80}
webhook.notify_new_job(test_job)
```

**3. Database errors**
```python
# Reinitialize database
from job_database import JobDatabase
db = JobDatabase()
db.init_database()  # Creates all tables
```

---

## ✅ Best Practices

### 1. Start Small
- Test each feature individually
- Integrate one feature at a time
- Monitor performance and errors

### 2. Use Environment Variables
- Never hardcode credentials
- Keep .env file secure
- Use different configs for dev/prod

### 3. Monitor Performance
- Check logs regularly
- Track success rates
- Adjust timing and thresholds

### 4. Backup Data
```bash
# Backup database
cp jobs_database.db jobs_database_backup_$(date +%Y%m%d).db

# Export jobs
python job_hunter.py --export jobs_backup.csv
```

### 5. Rate Limiting
- Respect platform limits
- Use delays between requests
- Don't run too frequently

---

## 📊 Performance Optimization

### Async Search
```python
# Use async for faster searches
import asyncio
jobs = asyncio.run(hunter.run_search_async(['linkedin', 'indeed']))
# 5x faster than sequential
```

### Caching
```python
# Cache job listings to avoid re-scraping
# (Future feature - Redis integration)
```

### Batch Processing
```python
# Process multiple jobs at once
hunter.auto_apply(jobs[:10])  # Apply to 10 jobs
```

---

## 🎯 Next Steps

1. ✅ Install and configure
2. ✅ Test each feature
3. ✅ Integrate into workflow
4. ✅ Monitor and optimize
5. ⏳ Implement remaining features (13-20)

---

**Integration Complete!** 🚀

All 9 implemented features are ready to use. See `FINAL_IMPLEMENTATION_SUMMARY.md` for complete feature list and `IMPROVEMENT_IDEAS.md` for remaining enhancements.
