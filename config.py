"""
Job Hunter Bot - Configuration
Configure your job search preferences here
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your Profile Information
PROFILE = {
    "first_name": os.getenv('PROFILE_FIRST_NAME', 'YOUR_FIRST_NAME'),
    "last_name": os.getenv('PROFILE_LAST_NAME', 'YOUR_LAST_NAME'),
    "email": os.getenv('PROFILE_EMAIL', 'your.email@example.com'),
    "phone": os.getenv('PROFILE_PHONE', '+33 6 XX XX XX XX'),
    "location": os.getenv('PROFILE_LOCATION', 'Paris, France'),
    "resume_path": os.getenv('PROFILE_RESUME_PATH', 'resume.pdf'),
    "cover_letter_path": os.getenv('PROFILE_COVER_LETTER_PATH', 'cover_letter.txt'),
}

# Job Search Criteria - Focus on Internships & Alternance
JOB_SEARCH = {
    "keywords": [
        "Stage Développeur Python",
        "Alternance Développeur",
        "Stage Data Analyst",
        "Alternance Full Stack",
        "Stage Informatique",
        "Apprentissage Développeur",
    ],
    "location": os.getenv('JOB_SEARCH_LOCATION', 'Paris, France'),
    "remote": os.getenv('JOB_SEARCH_REMOTE', 'True').lower() == 'true',
    "experience_level": os.getenv('JOB_SEARCH_EXPERIENCE_LEVEL', 'internship,entry,student').split(','),
    "job_type": os.getenv('JOB_SEARCH_JOB_TYPE', 'internship,apprenticeship,stage,alternance').split(','),
    "salary_min": int(os.getenv('JOB_SEARCH_SALARY_MIN', 600)),  # Typical internship stipend
    "posted_within_days": int(os.getenv('JOB_SEARCH_POSTED_WITHIN_DAYS', 7)),
}

# Keywords to EXCLUDE (jobs containing these will be skipped)
EXCLUDE_KEYWORDS = [
    "senior",
    "lead",
    "manager",
    "director",
    "10+ years",
    "8+ years",
]

# Keywords that MUST be present (at least one)
REQUIRED_KEYWORDS = [
    "python",
    "javascript",
    "react",
    "django",
    "flask",
]

# LinkedIn Configuration
LINKEDIN = {
    "email": os.getenv('LINKEDIN_EMAIL', 'your.linkedin.email@example.com'),
    "password": os.getenv('LINKEDIN_PASSWORD', ''),
    "easy_apply_only": os.getenv('LINKEDIN_EASY_APPLY_ONLY', 'True').lower() == 'true',
    "max_applications_per_day": int(os.getenv('LINKEDIN_MAX_APPLICATIONS', 50)),
}

# Indeed Configuration  
INDEED = {
    "email": os.getenv('INDEED_EMAIL', ''),
    "password": os.getenv('INDEED_PASSWORD', ''),
    "max_applications_per_day": int(os.getenv('INDEED_MAX_APPLICATIONS', 30)),
}

# Application Settings
APPLICATION = {
    "auto_apply": os.getenv('AUTO_APPLY', 'false').lower() == 'true',
    "save_jobs": os.getenv('SAVE_JOBS', 'true').lower() == 'true',
    "send_email_summary": os.getenv('SEND_EMAIL_SUMMARY', 'true').lower() == 'true',
    "delay_between_applications": int(os.getenv('DELAY_BETWEEN_APPLICATIONS', 30)),
}

# Email Configuration for notifications
EMAIL = {
    "smtp_server": os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com'),
    "smtp_port": int(os.getenv('EMAIL_SMTP_PORT', 587)),
    "smtp_username": os.getenv('EMAIL_USERNAME', ''),
    "smtp_password": os.getenv('EMAIL_PASSWORD', ''),
    "from_email": os.getenv('EMAIL_FROM', ''),
    "from_name": os.getenv('EMAIL_FROM_NAME', 'Job Hunter Bot'),
    "imap_server": os.getenv('EMAIL_IMAP_SERVER', 'imap.gmail.com'),
    "imap_port": int(os.getenv('EMAIL_IMAP_PORT', 993)),
}

# Database
DATABASE = {
    "path": "jobs_database.db",
}
