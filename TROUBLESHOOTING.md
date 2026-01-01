# 🔧 Troubleshooting Guide - Job Hunter Bot

## Common Issues and Solutions

---

## Issue 1: LinkedIn Login Failed ❌

**Error:** `Login may have failed - check for security verification`

### Causes:
- LinkedIn detected automated login
- Security verification (CAPTCHA) required
- Incorrect credentials
- Account locked/restricted

### Solutions:

#### Option A: Manual Login First (Recommended)
```python
# Run LinkedIn bot without headless mode
from linkedin_bot import LinkedInBot
from config import LINKEDIN

bot = LinkedInBot(LINKEDIN['email'], LINKEDIN['password'], headless=False)
bot.login()

# Complete CAPTCHA manually in the browser window
# Then the bot can continue
```

#### Option B: Use LinkedIn Session Cookies
1. Login to LinkedIn manually in Chrome
2. Export cookies using extension (EditThisCookie)
3. Save cookies to file
4. Load cookies in bot before searching

#### Option C: Disable LinkedIn Temporarily
Edit `config.py`:
```python
JOB_SEARCH = {
    'sources': ['indeed'],  # Remove 'linkedin'
    # ... rest of config
}
```

#### Option D: Use LinkedIn API (Advanced)
- Apply for LinkedIn API access
- Use official API instead of scraping
- More reliable but requires approval

---

## Issue 2: Indeed 403 Forbidden ❌

**Error:** `403 Client Error: Forbidden`

### Causes:
- Indeed detected bot/scraper
- Too many requests too quickly
- Missing proper headers
- IP blocked temporarily

### Solutions:

#### Option A: Add Delays and Rotate User Agents
Edit `indeed_bot.py` to add more realistic behavior:
```python
# Add longer delays
self.random_delay(5, 10)  # Instead of 2, 4

# Rotate user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    # Add more
]
```

#### Option B: Use Selenium Instead of Requests
Indeed blocks simple HTTP requests. Use browser automation:
```python
# In indeed_bot.py, use self.driver instead of self.session
# This makes it look like a real browser
```

#### Option C: Use Proxy/VPN
```python
# Add proxy to requests
proxies = {
    'http': 'http://your-proxy:port',
    'https': 'https://your-proxy:port'
}
response = self.session.get(url, proxies=proxies)
```

#### Option D: Use Indeed API (if available)
- Check if Indeed offers API access
- More reliable than scraping

#### Option E: Manual Job Import
For now, manually copy job URLs and add them:
```python
from job_database import JobDatabase

db = JobDatabase()
manual_jobs = [
    {
        'job_id': 'manual_001',
        'title': 'Python Developer',
        'company': 'Tech Corp',
        'location': 'Paris, France',
        'url': 'https://...',
        'source': 'manual',
        'match_score': 80
    }
]

for job in manual_jobs:
    db.add_job(job)
```

---

## Issue 3: No Jobs Found

### Quick Fixes:

1. **Test with Glassdoor instead:**
```powershell
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "
from glassdoor_bot import GlassdoorBot
bot = GlassdoorBot(headless=False)
jobs = bot.search_jobs('Python Developer', 'Paris, France')
print(f'Found {len(jobs)} jobs')
"
```

2. **Use job aggregator APIs:**
- Adzuna API (free tier available)
- The Muse API
- GitHub Jobs API

3. **Import from RSS feeds:**
Many job boards offer RSS feeds that are easier to scrape

---

## Recommended Workaround for Now

### Use Glassdoor + Manual LinkedIn

1. **Search Glassdoor (works better):**
```python
from glassdoor_bot import GlassdoorBot
from job_database import JobDatabase

bot = GlassdoorBot(headless=False)
db = JobDatabase()

jobs = bot.search_jobs('Python Developer', 'Paris, France')

for job in jobs:
    db.add_job(job)

print(f"Added {len(jobs)} jobs from Glassdoor")
```

2. **Manually browse LinkedIn:**
- Search jobs on LinkedIn website
- Copy URLs of interesting jobs
- Add them to database manually

3. **Use the enhanced features:**
Even without automated search, you can use:
- ✅ Profile Optimizer (with manual jobs)
- ✅ Cover Letter Generator
- ✅ Interview Prep
- ✅ Salary Advisor
- ✅ Career Planner

---

## Alternative: Job Board APIs

### Free Job APIs You Can Use:

1. **Adzuna API**
```python
import requests

app_id = "your_app_id"
app_key = "your_app_key"

url = f"https://api.adzuna.com/v1/api/jobs/fr/search/1"
params = {
    'app_id': app_id,
    'app_key': app_key,
    'what': 'Python Developer',
    'where': 'Paris'
}

response = requests.get(url, params=params)
jobs = response.json()['results']
```

2. **The Muse API**
```python
url = "https://www.themuse.com/api/public/jobs"
params = {
    'category': 'Software Engineering',
    'location': 'Paris, France',
    'page': 1
}

response = requests.get(url, params=params)
jobs = response.json()['results']
```

---

## Testing Without Job Search

You can still test all features with sample data:

```python
# Create sample jobs for testing
from job_database import JobDatabase

db = JobDatabase()

sample_jobs = [
    {
        'job_id': 'test_001',
        'title': 'Senior Python Developer',
        'company': 'Tech Innovations',
        'location': 'Paris, France',
        'salary': '€60,000 - €80,000',
        'description': 'Python Django AWS Docker PostgreSQL',
        'url': 'https://example.com/job1',
        'source': 'manual',
        'match_score': 85
    },
    {
        'job_id': 'test_002',
        'title': 'Full Stack Developer',
        'company': 'StartupCo',
        'location': 'Paris, France',
        'salary': '€50,000 - €70,000',
        'description': 'React Node.js MongoDB',
        'url': 'https://example.com/job2',
        'source': 'manual',
        'match_score': 75
    }
]

for job in sample_jobs:
    db.add_job(job)

print("✓ Sample jobs added - now test the features!")
```

Then run:
```powershell
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" complete_workflow.py
```

---

## Next Steps

1. ✅ **Use sample data** to test all features
2. ✅ **Try Glassdoor** for real job search
3. ✅ **Apply for job board APIs** (Adzuna, The Muse)
4. ⏳ **Fix LinkedIn** login (manual CAPTCHA)
5. ⏳ **Improve Indeed** scraping (use Selenium)

---

## Summary

**What Works Now:**
- ✅ All 9 enhancement features (100% verified)
- ✅ Profile optimization
- ✅ Cover letter generation
- ✅ Interview prep
- ✅ Salary analysis
- ✅ Career planning
- ✅ Smart timing
- ✅ Database operations

**What Needs Fixing:**
- ❌ LinkedIn automated login (security blocks)
- ❌ Indeed scraping (anti-bot protection)

**Recommended Solution:**
Use Glassdoor + manual job entry + job board APIs while the enhanced features work perfectly with any job data source!
