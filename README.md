# 🎯 Job Hunter Bot

Automated job search and application bot for LinkedIn and Indeed.

## Features

- 🔍 **Multi-platform Search**: Search jobs on LinkedIn and Indeed simultaneously
- 🎯 **Smart Matching**: AI-powered job matching based on your preferences
- ⚡ **Easy Apply**: Auto-apply to LinkedIn Easy Apply jobs
- 📧 **Email Reports**: Daily email summaries with matching jobs
- 💾 **Database Storage**: Track all found jobs and applications
- 📊 **Statistics**: Monitor your job search progress

## Installation

1. Install Python 3.10+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install ChromeDriver (required for LinkedIn):
   - Download from: https://chromedriver.chromium.org/
   - Or use webdriver-manager (auto-installs)

## Configuration

Edit `config.py` with your settings:

### 1. Your Profile
```python
PROFILE = {
    "first_name": "Your Name",
    "last_name": "Your Last Name",
    "email": "your.email@example.com",
    "phone": "+33 6 XX XX XX XX",
    "resume_path": "path/to/resume.pdf",
}
```

### 2. Job Search Criteria
```python
JOB_SEARCH = {
    "keywords": ["Python Developer", "Data Analyst"],
    "location": "Paris, France",
    "remote": True,
    "posted_within_days": 7,
}
```

### 3. LinkedIn Credentials
```python
LINKEDIN = {
    "email": "your.linkedin@email.com",
    "password": "your_password",  # Use env var in production!
}
```

### 4. Email Settings (for Gmail)
```python
EMAIL = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your@gmail.com",
    "sender_password": "YOUR_APP_PASSWORD",  # Gmail App Password
}
```

## Usage

### Search Jobs
```bash
python job_hunter.py --search
```

### Search Specific Platform
```bash
python job_hunter.py --search --linkedin-only
python job_hunter.py --search --indeed-only
```

### Search and Auto-Apply
```bash
python job_hunter.py --search --apply
```

### View Statistics
```bash
python job_hunter.py --stats
```

### Export to CSV
```bash
python job_hunter.py --export jobs.csv
```

### Headless Mode (no browser window)
```bash
python job_hunter.py --search --headless
```

## Scheduled Runs

Create a scheduled task to run daily:

### Windows Task Scheduler
```
schtasks /create /tn "JobHunter" /tr "python job_hunter.py --search" /sc daily /st 09:00
```

### Linux/Mac Cron
```
0 9 * * * cd /path/to/job_hunter_bot && python job_hunter.py --search
```

## Security Notes

⚠️ **Important**:
- Never commit your `config.py` with real passwords
- Use environment variables for sensitive data
- LinkedIn may detect automation - use responsibly
- Respect rate limits and terms of service

## Environment Variables (Recommended)

Create a `.env` file:
```
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=your_password
SMTP_PASSWORD=your_app_password
```

## Database

Jobs are stored in SQLite database (`jobs_database.db`):
- `jobs` table: All found jobs with match scores
- `applications` table: Application tracking
- `search_history` table: Search logs

## Troubleshooting

### LinkedIn Login Issues
- Enable 2FA and use App Password
- May need to solve CAPTCHA manually first time
- Try running without headless mode

### Indeed Scraping Issues
- Indeed may block repeated requests
- Add delays between searches
- Try VPN if blocked

## License

For personal use only. Use responsibly and respect website ToS.
