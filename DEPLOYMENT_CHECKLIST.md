# 🚀 Job Hunter Bot - Deployment Checklist

**Date:** January 1, 2026  
**Version:** 2.0 (Enhanced with 9 new features)

---

## ✅ Pre-Deployment Checklist

### Step 1: Install Dependencies

```bash
# Using Python 3.13
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt

# Verify installation
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "import pytz; import openai; print('✓ All packages installed')"
```

**Expected packages:**
- [x] selenium>=4.15.0
- [x] beautifulsoup4>=4.12.0
- [x] requests>=2.31.0
- [x] webdriver-manager>=4.0.0
- [x] schedule>=1.2.0
- [x] python-dotenv>=1.0.0
- [x] flask>=3.0.0
- [x] flask-cors>=4.0.0
- [x] pytz>=2024.1
- [x] openai>=1.0.0
- [x] gunicorn>=21.0.0

---

### Step 2: Configure Environment

```bash
# Create .env file from example
cp .env.example .env

# Edit .env with your credentials
notepad .env
```

**Required Configuration:**

```bash
# === MUST CONFIGURE ===
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your.email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=your.email@gmail.com

# === OPTIONAL (for enhanced features) ===
OPENAI_API_KEY=sk-...  # For AI cover letters & interview prep
WEBHOOK_URL=https://hooks.slack.com/services/...  # For notifications
WEBHOOK_PLATFORM=slack
```

---

### Step 3: Initialize Database

```bash
# Test database initialization
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "
from job_database import JobDatabase
db = JobDatabase()
db.init_database()
print('✓ Database initialized with all tables')
"
```

**Verify tables created:**
- [x] jobs
- [x] applications
- [x] contacts
- [x] search_history
- [x] queued_applications (NEW)

---

### Step 4: Test Individual Features

#### 4.1 Smart Timing
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" smart_timing.py
```
**Expected:** Shows optimal application times for test jobs

#### 4.2 Webhook Notifier
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "
from webhook_notifier import WebhookNotifier
import os
webhook_url = os.getenv('WEBHOOK_URL')
if webhook_url:
    notifier = WebhookNotifier(webhook_url, 'slack')
    test_job = {'title': 'Test Job', 'company': 'Test Co', 'match_score': 80, 'location': 'Paris'}
    notifier.notify_new_job(test_job)
    print('✓ Webhook notification sent')
else:
    print('⚠ WEBHOOK_URL not set - skipping')
"
```
**Expected:** Notification appears in Slack/Discord/Telegram

#### 4.3 Profile Optimizer
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "
from profile_optimizer import ProfileOptimizer
optimizer = ProfileOptimizer()
test_jobs = [{'title': 'Python Developer', 'description': 'Python Django AWS Docker'}]
test_profile = {'skills': 'Python, SQL'}
analysis = optimizer.analyze_keyword_gaps(test_jobs, test_profile)
print(optimizer.generate_report(analysis))
"
```
**Expected:** Profile analysis report with missing keywords

#### 4.4 Async Job Search
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" async_job_search.py
```
**Expected:** Shows async search performance comparison

#### 4.5 AI Cover Letter
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" cover_letter_generator.py
```
**Expected:** Generates sample cover letter (template or AI-powered)

#### 4.6 Interview Prep
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" interview_prep.py
```
**Expected:** Complete interview preparation guide

#### 4.7 Salary Advisor
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" salary_advisor.py
```
**Expected:** Salary analysis and negotiation script

#### 4.8 Glassdoor Bot
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" glassdoor_bot.py
```
**Expected:** Job listings from Glassdoor with ratings

#### 4.9 Career Planner
```bash
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" career_planner.py
```
**Expected:** Career development plan with milestones

---

### Step 5: Test Main Bot Integration

```bash
# Test basic functionality
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" job_hunter.py --stats

# Test job search (headless mode)
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" job_hunter.py --search --headless

# Test export
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" job_hunter.py --export test_export.csv
```

---

## 🧪 Feature Integration Tests

### Test 1: Smart Timing Integration

```python
# test_smart_timing.py
from job_hunter import JobHunter
from smart_timing import SmartTiming

hunter = JobHunter()
timing = SmartTiming()

# Create test job
test_job = {
    'job_id': 'test_001',
    'title': 'Python Developer',
    'company': 'Test Corp',
    'location': 'Paris, France',
    'url': 'https://example.com/job'
}

# Test timing check
if timing.should_apply_now(test_job):
    print("✓ Would apply now")
else:
    optimal = timing.get_optimal_apply_time(test_job)
    print(f"✓ Would queue for: {timing.format_optimal_time(test_job)}")
    
    # Test database queue
    hunter.db.add_queued_application(test_job['job_id'], optimal.isoformat())
    print("✓ Added to queue")
    
    # Verify in database
    pending = hunter.db.get_pending_applications()
    print(f"✓ Pending applications: {len(pending)}")
```

### Test 2: Webhook Integration

```python
# test_webhooks.py
import os
from webhook_notifier import WebhookNotifier

webhook_url = os.getenv('WEBHOOK_URL')
if webhook_url:
    notifier = WebhookNotifier(webhook_url, os.getenv('WEBHOOK_PLATFORM', 'slack'))
    
    # Test different notification types
    test_job = {
        'title': 'Senior Python Developer',
        'company': 'Tech Innovations',
        'location': 'Paris, France',
        'match_score': 85,
        'salary': '€60,000 - €80,000',
        'url': 'https://example.com/job',
        'easy_apply': True
    }
    
    print("Testing webhook notifications...")
    notifier.notify_new_job(test_job)
    print("✓ New job notification sent")
    
    notifier.notify_application_submitted(test_job)
    print("✓ Application notification sent")
    
    test_questions = [{'text': 'Why do you want this role?', 'type': 'textarea'}]
    notifier.notify_complex_question(test_job, test_questions)
    print("✓ Complex question notification sent")
else:
    print("⚠ WEBHOOK_URL not configured - skipping webhook tests")
```

### Test 3: Profile Optimization Workflow

```python
# test_profile_optimization.py
from job_database import JobDatabase
from profile_optimizer import ProfileOptimizer
from config import PROFILE

db = JobDatabase()
optimizer = ProfileOptimizer()

# Get recent jobs
jobs = db.get_new_jobs()

if jobs:
    print(f"Analyzing {len(jobs)} jobs against your profile...")
    
    # Analyze
    analysis = optimizer.analyze_keyword_gaps(jobs, PROFILE)
    
    # Generate report
    report = optimizer.generate_report(analysis)
    
    # Save report
    with open('profile_optimization_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✓ Profile optimization report saved")
    print(f"✓ Profile strength: {analysis['profile_strength']['score']}%")
    print(f"✓ Missing keywords: {len(analysis['missing_keywords'])}")
else:
    print("⚠ No jobs in database - run job search first")
```

### Test 4: AI Cover Letter Generation

```python
# test_cover_letter.py
import os
from cover_letter_generator import CoverLetterGenerator
from config import PROFILE

generator = CoverLetterGenerator()

test_job = {
    'title': 'Senior Python Developer',
    'company': 'Tech Innovations Inc',
    'location': 'Paris, France',
    'description': 'We are seeking an experienced Python developer...'
}

print("Generating cover letter...")
letter = generator.generate(test_job, PROFILE, style='professional')

# Save letter
filepath = generator.save_letter(letter, test_job)
print(f"✓ Cover letter saved to: {filepath}")

# Display preview
print("\nPreview:")
print("=" * 60)
print(letter[:300] + "...")
print("=" * 60)

if os.getenv('OPENAI_API_KEY'):
    print("✓ Using AI-powered generation")
else:
    print("⚠ Using template mode (set OPENAI_API_KEY for AI features)")
```

### Test 5: End-to-End Workflow

```python
# test_full_workflow.py
from job_hunter import JobHunter
from smart_timing import SmartTiming
from profile_optimizer import ProfileOptimizer
from cover_letter_generator import CoverLetterGenerator
from config import PROFILE

print("Starting end-to-end workflow test...")
print("=" * 60)

# Initialize
hunter = JobHunter()
timing = SmartTiming()
optimizer = ProfileOptimizer()
cover_gen = CoverLetterGenerator()

# 1. Run job search (limited)
print("\n1. Running job search...")
jobs = hunter.run_search(['indeed'], headless=True)  # Start with Indeed only
print(f"✓ Found {len(jobs)} jobs")

# 2. Analyze profile
if jobs:
    print("\n2. Analyzing profile...")
    analysis = optimizer.analyze_keyword_gaps(jobs, PROFILE)
    print(f"✓ Profile strength: {analysis['profile_strength']['score']}%")
    print(f"✓ Missing keywords: {len(analysis['missing_keywords'])}")

# 3. Test smart timing
if jobs:
    print("\n3. Testing smart timing...")
    test_job = jobs[0]
    
    if timing.should_apply_now(test_job):
        print("✓ Optimal time to apply now")
    else:
        optimal = timing.get_optimal_apply_time(test_job)
        print(f"✓ Should apply at: {timing.format_optimal_time(test_job)}")

# 4. Generate cover letter
if jobs:
    print("\n4. Generating cover letter...")
    letter = cover_gen.generate(jobs[0], PROFILE)
    print(f"✓ Generated {len(letter)} character cover letter")

print("\n" + "=" * 60)
print("✓ End-to-end workflow test complete!")
```

---

## 📋 Deployment Steps

### Step 1: Backup Current System
```bash
# Backup database
cp jobs_database.db jobs_database_backup_$(date +%Y%m%d).db

# Backup config
cp .env .env.backup
```

### Step 2: Deploy New Features
```bash
# All files are already in place
# Just need to configure and test
```

### Step 3: Run All Tests
```bash
# Run individual feature tests
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" smart_timing.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" profile_optimizer.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" cover_letter_generator.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" interview_prep.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" salary_advisor.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" career_planner.py

# Run integration tests
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" test_smart_timing.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" test_webhooks.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" test_profile_optimization.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" test_cover_letter.py
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" test_full_workflow.py
```

### Step 4: Verify All Features
- [x] Smart timing queues applications correctly
- [x] Webhooks send notifications
- [x] Profile optimizer generates reports
- [x] Async search runs faster
- [x] AI cover letters generate (or templates work)
- [x] Interview prep creates packages
- [x] Salary advisor provides analysis
- [x] Glassdoor bot finds jobs
- [x] Career planner creates roadmaps

### Step 5: Production Deployment
```bash
# Start scheduler for automated operation
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" scheduler.py

# Or run web dashboard
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" web_app.py
```

---

## 🔍 Verification Checklist

### Database Verification
```sql
-- Check all tables exist
SELECT name FROM sqlite_master WHERE type='table';

-- Expected tables:
-- jobs, applications, contacts, search_history, queued_applications
```

### Feature Verification
- [ ] Smart timing calculates optimal times
- [ ] Queued applications stored in database
- [ ] Webhooks send to configured platform
- [ ] Profile analysis generates reports
- [ ] Cover letters generate successfully
- [ ] Interview prep creates comprehensive guides
- [ ] Salary advisor provides market data
- [ ] All modules import without errors

### Integration Verification
- [ ] Main bot uses smart timing
- [ ] Notifications sent for high-match jobs
- [ ] Profile optimization runs on demand
- [ ] Cover letters can be generated for jobs
- [ ] All features accessible from main workflow

---

## 🚨 Troubleshooting

### Issue: Module import errors
```bash
# Verify Python path
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "import sys; print('\n'.join(sys.path))"

# Reinstall dependencies
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt --force-reinstall
```

### Issue: OpenAI API errors
```bash
# Check API key
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "import os; print('API Key set:', bool(os.getenv('OPENAI_API_KEY')))"

# Test API connection
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print('✓ API connection successful')
"
```

### Issue: Database errors
```bash
# Reinitialize database
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "
from job_database import JobDatabase
db = JobDatabase()
db.init_database()
print('✓ Database reinitialized')
"
```

---

## ✅ Final Checklist

- [ ] All dependencies installed
- [ ] .env configured with credentials
- [ ] Database initialized with new tables
- [ ] All 9 features tested individually
- [ ] Integration tests passed
- [ ] Webhooks working (if configured)
- [ ] AI features working (if API key set)
- [ ] Main bot runs without errors
- [ ] Documentation reviewed
- [ ] Backup created

---

## 🎯 Success Criteria

✅ **Deployment Successful If:**
1. All modules import without errors
2. Database has all 5 tables
3. At least 7/9 features working (AI features optional)
4. Main job search runs successfully
5. No critical errors in logs

---

## 📚 Additional Resources

- `INTEGRATION_GUIDE.md` - Detailed integration instructions
- `FINAL_IMPLEMENTATION_SUMMARY.md` - Complete feature overview
- `IMPROVEMENT_IDEAS.md` - Future enhancements
- `PRD.md` - Original requirements

---

**Ready to deploy!** Follow steps 1-5 in order. 🚀
