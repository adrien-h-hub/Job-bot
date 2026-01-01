# 🚀 Job Hunter Bot - Deployment Guide

## Quick Start Checklist

- [ ] Create `.env` file with all credentials
- [ ] Test locally with real accounts
- [ ] Push code to GitHub
- [ ] Deploy to Render
- [ ] Configure environment variables on Render
- [ ] Test deployed application

---

## 1. Environment Setup

### Create `.env` File

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

### Required Environment Variables

```bash
# Profile Information
PROFILE_FIRST_NAME=John
PROFILE_LAST_NAME=Doe
PROFILE_EMAIL=john.doe@example.com
PROFILE_PHONE=+33 6 12 34 56 78
PROFILE_LOCATION=Paris, France
PROFILE_RESUME_PATH=resume.pdf
PROFILE_COVER_LETTER_PATH=cover_letter.txt

# LinkedIn Credentials
LINKEDIN_EMAIL=your.linkedin@email.com
LINKEDIN_PASSWORD=your_linkedin_password
LINKEDIN_MAX_APPLICATIONS=50

# Indeed Credentials (optional)
INDEED_EMAIL=your.indeed@email.com
INDEED_PASSWORD=your_indeed_password
INDEED_MAX_APPLICATIONS=30

# Email Configuration (SMTP for sending)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your.email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_FROM=your.email@gmail.com
EMAIL_FROM_NAME=Job Hunter Bot

# Email Configuration (IMAP for receiving)
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993

# Application Settings
AUTO_APPLY=false
MIN_MATCH_SCORE=40
DELAY_BETWEEN_APPLICATIONS=30

# Database
DATABASE_PATH=jobs_database.db
```

### Gmail App Password Setup

1. Go to Google Account Settings
2. Security → 2-Step Verification (enable if not enabled)
3. App Passwords → Generate new password
4. Use this password for `EMAIL_PASSWORD`

---

## 2. Local Testing

### Test Job Search
```bash
python job_hunter.py --search --headless
```

### Test Email Notifications
```bash
python job_hunter.py --search
```
Check your email for the job summary.

### Test Complex Question Detection
Enable auto-apply in `.env`:
```bash
AUTO_APPLY=true
```

Run:
```bash
python job_hunter.py --search --apply
```

Watch for complex question detection messages.

### Test Email Response Checking
```python
from job_hunter import JobHunter

hunter = JobHunter()
hunter.check_responses()
```

### Test Contact Finding
```python
from email_finder import EmailFinder

finder = EmailFinder("Vinci Construction")
rhe = finder.find_rhe_contact()
print(rhe)
```

---

## 3. Deploy to Render

### Prerequisites
- GitHub account
- Render account (free tier available)
- Code pushed to GitHub repository

### Step 1: Prepare Repository

Ensure these files exist:
- `requirements.txt` ✅
- `Procfile` ✅
- `runtime.txt` (optional)
- `.env.example` ✅

### Step 2: Create Render Web Service

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: job-hunter-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python scheduler.py` (for scheduled runs)
   - **OR**: `gunicorn web_app:app` (for web dashboard)

### Step 3: Add Environment Variables

In Render dashboard, go to "Environment" and add all variables from your `.env` file:

```
PROFILE_FIRST_NAME=...
PROFILE_LAST_NAME=...
LINKEDIN_EMAIL=...
LINKEDIN_PASSWORD=...
EMAIL_USERNAME=...
EMAIL_PASSWORD=...
... (all 25 variables)
```

### Step 4: Deploy

Click "Create Web Service" and wait for deployment.

---

## 4. Running Modes

### Mode 1: Scheduler (Automated)

**Procfile:**
```
worker: python scheduler.py
```

**Schedule:**
- Job search: 9:00 AM and 6:00 PM daily
- Email check: Every 2 hours
- Auto-apply: Every 4 hours (if enabled)

**Logs:**
```bash
# View logs on Render dashboard
# Or locally:
tail -f job_hunter.log
```

### Mode 2: Web Dashboard

**Procfile:**
```
web: gunicorn web_app:app
```

**Access:**
- URL: `https://your-app-name.onrender.com`
- Features: Manual job search, view jobs, statistics

### Mode 3: Manual CLI

Run commands manually:
```bash
# Search
python job_hunter.py --search

# Auto-apply
python job_hunter.py --search --apply

# Check responses
python -c "from job_hunter import JobHunter; JobHunter().check_responses()"

# View stats
python job_hunter.py --stats
```

---

## 5. Monitoring & Maintenance

### Check Logs

**Render:**
- Dashboard → Logs tab
- Real-time streaming

**Local:**
```bash
tail -f job_hunter.log
tail -f response_manager.log
```

### Database Management

**Backup:**
```bash
cp jobs_database.db jobs_database_backup_$(date +%Y%m%d).db
```

**View data:**
```bash
sqlite3 jobs_database.db
.tables
SELECT * FROM jobs LIMIT 10;
SELECT * FROM contacts;
```

**Export:**
```bash
python job_hunter.py --export jobs_export.csv
```

### Email Monitoring

Check for:
- ✅ Job summaries received
- ✅ Application confirmations
- ✅ Response processing logs

---

## 6. Troubleshooting

### LinkedIn Login Issues

**Problem:** Login fails or security check
**Solution:**
1. Use 2FA-enabled account
2. Try logging in manually first
3. Check for CAPTCHA requirements
4. Use `headless=False` for debugging

### Email Not Sending

**Problem:** SMTP errors
**Solution:**
1. Verify Gmail App Password
2. Check "Less secure app access" (if not using App Password)
3. Verify SMTP settings
4. Test with simple script:
```python
from email_notifier import EmailNotifier
notifier = EmailNotifier(...)
notifier.send_job_summary(...)
```

### Complex Questions Not Detected

**Problem:** Bot applies despite complex questions
**Solution:**
1. Check logs for detection attempts
2. Adjust keywords in `_classify_question()`
3. Test manually:
```python
from linkedin_bot import LinkedInBot
bot = LinkedInBot(...)
bot.login()
success, questions = bot.apply_easy_apply(job_url)
print(questions)
```

### Database Locked

**Problem:** SQLite database locked error
**Solution:**
1. Only one process should write at a time
2. Use connection pooling
3. Or switch to PostgreSQL for production

### Render Deployment Fails

**Problem:** Build or start errors
**Solution:**
1. Check `requirements.txt` versions
2. Verify Python version compatibility
3. Check environment variables
4. View build logs for specific errors

---

## 7. Security Best Practices

### ✅ DO:
- Use environment variables for all credentials
- Use Gmail App Passwords (not account password)
- Enable 2FA on LinkedIn and email accounts
- Regularly rotate passwords
- Keep `.env` in `.gitignore`
- Use HTTPS for web dashboard

### ❌ DON'T:
- Commit credentials to Git
- Share your `.env` file
- Use the same password everywhere
- Disable security features for convenience
- Run with `AUTO_APPLY=true` without testing

---

## 8. Scaling & Optimization

### For High Volume

1. **Use PostgreSQL instead of SQLite**
   ```python
   # In config.py
   DATABASE = {
       'type': 'postgresql',
       'url': os.getenv('DATABASE_URL')
   }
   ```

2. **Add rate limiting**
   ```python
   # Respect platform limits
   LINKEDIN_REQUESTS_PER_HOUR = 50
   INDEED_REQUESTS_PER_HOUR = 100
   ```

3. **Use Redis for caching**
   ```python
   # Cache job IDs to avoid duplicates
   import redis
   cache = redis.Redis(...)
   ```

4. **Add Celery for async tasks**
   ```python
   # Offload heavy tasks
   from celery import Celery
   app = Celery('job_hunter')
   ```

---

## 9. Advanced Features

### Custom Email Templates

Edit `email_templates.py` to customize:
- Interview request responses
- Follow-up emails
- Rejection responses
- Thank you notes

### Custom Question Detection

Edit `linkedin_bot.py` and `indeed_bot.py`:
```python
complex_keywords = [
    'why', 'describe', 'explain',
    # Add your own keywords
    'motivation', 'experience with'
]
```

### Webhook Notifications

Add Slack/Discord webhooks:
```python
import requests

def send_slack_notification(message):
    webhook_url = os.getenv('SLACK_WEBHOOK')
    requests.post(webhook_url, json={'text': message})
```

---

## 10. Migration from Old Version

### If you have existing code:

1. **Backup database:**
   ```bash
   cp jobs_database.db jobs_database_old.db
   ```

2. **Create `.env` file:**
   - Copy all values from old `config.py`
   - Use `.env.example` as template

3. **Update imports:**
   - Bot return values now tuples: `(success, questions)`
   - Email notifier parameters changed

4. **Test thoroughly:**
   ```bash
   python job_hunter.py --search --headless
   ```

5. **Migrate database schema:**
   - New tables auto-create on first run
   - Old data preserved in `jobs` table

---

## Support & Resources

- **GitHub Issues**: Report bugs and request features
- **Documentation**: See `PRD.md` and `CODE_REVIEW.md`
- **Logs**: Check `job_hunter.log` and `response_manager.log`
- **Community**: Share your experience!

---

**Good luck with your job search! 🍀**
