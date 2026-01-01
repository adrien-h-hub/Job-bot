# Product Requirements Document (PRD)
## Job Hunter Bot

**Version:** 1.0  
**Date:** January 1, 2026  
**Status:** Draft for Review

---

## 1. Executive Summary

### 1.1 Product Name
**Job Hunter Bot** - Automated Job Search & Application Assistant

### 1.2 Product Vision
An intelligent automation system that finds, evaluates, and applies to job opportunities on LinkedIn and Indeed based on user-defined criteria, while intelligently handling complex application scenarios and maintaining professional communication with recruiters.

### 1.3 Target Users
- **Primary:** Job seekers who want to automate repetitive job search and application tasks
- **Secondary:** Professionals looking to expand their job search reach while maintaining quality applications
- **Initial Deployment:** Single-user (personal use), with potential for multi-user SaaS expansion

### 1.4 Core Value Proposition
- **Save Time:** Automate 90% of job search and application tasks
- **Increase Reach:** Apply to more relevant positions than manual search allows
- **Smart Assistance:** Intelligent detection of complex questions requiring human input
- **Direct Contact:** Find and reach key decision-makers (RHE, Site Managers) directly
- **Full Visibility:** Web dashboard to track all applications and responses

---

## 2. Product Goals & Success Metrics

### 2.1 Primary Goals
1. **Automation:** Successfully apply to 20+ relevant jobs per day without manual intervention
2. **Quality:** Maintain 70%+ match score on all auto-applied positions
3. **Intelligence:** Detect 95%+ of complex application questions requiring human review
4. **Reach:** Find contact information for key personnel in 60%+ of target companies
5. **Visibility:** Provide real-time dashboard access to all job search activities

### 2.2 Success Metrics
- **Applications per day:** Target 20-50 automated applications
- **Response rate:** Track percentage of applications receiving responses
- **Interview rate:** Monitor conversion from application to interview
- **Time saved:** Measure automation efficiency (target: 2+ hours/day saved)
- **User satisfaction:** Manual intervention required <10% of the time

---

## 3. Features & Requirements

### 3.1 Core Features (MVP - Must Have)

#### F1: Job Search & Collection
**Priority:** P0 (Critical)

**Description:** Automated scraping and collection of job postings from multiple platforms

**Requirements:**
- **F1.1** Search Indeed for jobs matching user criteria
  - Keywords, location, job type, salary range, remote options
  - Posted within last N days filter
  - Extract: title, company, location, salary, description, URL, posted date
- **F1.2** Search LinkedIn for jobs matching user criteria
  - Same filters as Indeed
  - Support for LinkedIn Easy Apply detection
  - Extract same fields as Indeed
- **F1.3** Deduplication logic to avoid processing same job twice
- **F1.4** Rate limiting and respectful scraping (delays, user-agent rotation)

**Technical Notes:**
- Indeed: requests + BeautifulSoup (no login required)
- LinkedIn: Selenium (requires login)
- Store job_id as unique identifier

---

#### F2: Job Matching & Scoring
**Priority:** P0 (Critical)

**Description:** Intelligent scoring system to rank jobs by relevance to user profile

**Requirements:**
- **F2.1** Keyword matching (required keywords, excluded keywords)
- **F2.2** Salary range filtering
- **F2.3** Experience level matching
- **F2.4** Location preferences (remote, on-site, hybrid)
- **F2.5** Generate match score (0-100) with explanation
- **F2.6** Filter jobs below minimum threshold (configurable, default 30%)

**Scoring Algorithm:**
```
Base Score: 0
+ Required keywords present: +10 per keyword (max 40)
+ Salary meets minimum: +20
+ Experience level matches: +15
+ Location preference matches: +15
+ Job type matches: +10
- Excluded keywords present: -50 per keyword
= Final Score (0-100)
```

---

#### F3: Automated Application
**Priority:** P0 (Critical)

**Description:** Automatically apply to jobs that meet criteria, with intelligent question handling

**Requirements:**
- **F3.1** LinkedIn Easy Apply automation
  - Fill standard fields (name, email, phone, resume upload)
  - Handle multi-step forms
  - Detect question types (yes/no, dropdown, text input)
- **F3.2** Indeed application automation
  - Similar field filling as LinkedIn
  - Handle external redirects
- **F3.3** Intelligent question detection
  - **Simple questions:** Auto-answer (yes/no, dropdowns with clear answers)
  - **Complex questions:** Detect open-ended or nuanced questions
  - Examples of complex: "Describe your experience with...", "Why are you interested...", "Provide details about..."
- **F3.4** Complex question handling workflow
  - Pause application
  - Save application state
  - Send email to user with:
    - Job details
    - Question text
    - Context needed
    - Suggested response (if available)
  - Wait for user response
  - Resume application with user's answer

**Question Detection Logic:**
```python
Complex if:
- Text input field with >100 char limit
- Question contains: "why", "describe", "explain", "tell us about"
- Question contains: "experience", "motivation", "interest"
- No clear yes/no or dropdown options
```

---

#### F4: Email Management & Notifications
**Priority:** P0 (Critical)

**Description:** Comprehensive email system for notifications, alerts, and response handling

**Requirements:**
- **F4.1** Daily summary emails
  - Jobs found today
  - Applications submitted
  - Responses received
  - Actions required
- **F4.2** Complex question alerts
  - Immediate email when complex question detected
  - Include job details, question, and context
  - Provide suggested response if available
- **F4.3** Response received notifications
  - Parse incoming emails from recruiters
  - Categorize: interview request, rejection, info request, unknown
  - Suggest appropriate response
- **F4.4** Application confirmation emails
  - Confirm each successful application
  - Include job details and application timestamp

**Email Templates:**
- Daily summary (HTML + plain text)
- Complex question alert
- Response received notification
- Application confirmation

---

#### F5: Contact Discovery (Email Finder)
**Priority:** P1 (High)

**Description:** Find email addresses of key decision-makers within target companies

**Requirements:**
- **F5.1** Target roles
  - **Primary:** RHE (Responsable Hygiène et Sécurité)
  - **Primary:** Chef de Chantier (Site Manager)
  - **Secondary:** HR/Recruitment contacts
- **F5.2** Discovery methods
  - Company website scraping (contact pages, team pages, about pages)
  - Common email pattern testing (rhe@, hse@, chantier@, etc.)
  - LinkedIn profile search (placeholder for future API integration)
- **F5.3** Email validation
  - Format validation (regex)
  - Filter out generic emails (noreply@, info@, etc.)
  - Confidence scoring (0.0-1.0)
- **F5.4** Contact storage
  - Store found contacts in database
  - Link to company/job
  - Track source and confidence level

**Use Cases:**
- Direct outreach after application
- Follow-up on complex questions
- Networking for future opportunities

---

#### F6: Web Dashboard
**Priority:** P1 (High)

**Description:** Flask-based web interface for monitoring and controlling the bot

**Requirements:**
- **F6.1** Dashboard overview
  - Statistics cards (total jobs, new jobs, applied, interviews)
  - Recent activity feed
  - Search status indicator
- **F6.2** Job search controls
  - Manual search trigger with custom parameters
  - Real-time progress bar
  - Status updates during search
- **F6.3** Job list management
  - View all jobs with filters (status, source, date)
  - Job cards with key info (title, company, location, salary, match score)
  - Quick actions: Apply, Skip, View details
  - Update job status manually
- **F6.4** Application tracking
  - View all applications by status
  - Timeline view of application process
  - Response tracking
- **F6.5** Export functionality
  - Export jobs to CSV
  - Export applications report
- **F6.6** Settings page (future)
  - Update search criteria
  - Manage email settings
  - Configure automation rules

**Tech Stack:**
- Flask backend
- TailwindCSS for styling
- Vanilla JavaScript (no heavy frameworks)
- RESTful API endpoints

---

#### F7: Database & Persistence
**Priority:** P0 (Critical)

**Description:** SQLite database for storing all job data, applications, and search history

**Requirements:**
- **F7.1** Jobs table
  - job_id (unique), title, company, location, salary, description
  - url, source, posted_date, found_date
  - status, match_score, applied_date
- **F7.2** Applications table
  - application_id, job_id, applied_date, status
  - questions_encountered, responses_given
  - last_updated
- **F7.3** Contacts table
  - contact_id, company_name, name, email, position
  - source, confidence, found_date
- **F7.4** Search history table
  - search_id, timestamp, keywords, location
  - jobs_found, jobs_applied, duration
- **F7.5** Database operations
  - CRUD for all tables
  - Query methods (by status, source, date range)
  - Statistics aggregation
  - Export to CSV

---

### 3.2 Advanced Features (Post-MVP - Nice to Have)

#### F8: Response Intelligence
**Priority:** P2 (Medium)

**Description:** Automated analysis and response to recruiter emails

**Requirements:**
- **F8.1** Email parsing and categorization
  - Interview request → Auto-suggest available times
  - Rejection → Send thank you + request feedback
  - Info request → Alert user with context
  - Unknown → Forward to user for review
- **F8.2** Response templates
  - Pre-written templates for common scenarios
  - Personalization with job/company details
  - Multiple language support (French, English)
- **F8.3** Auto-response (with user approval)
  - Draft responses automatically
  - Send to user for approval before sending
  - One-click approve and send

---

#### F9: Scheduler & Automation
**Priority:** P2 (Medium)

**Description:** Automated scheduling for hands-free operation

**Requirements:**
- **F9.1** Scheduled searches
  - Run job search at specified times (e.g., 9am, 6pm daily)
  - Configurable frequency and timing
- **F9.2** Auto-apply scheduling
  - Apply to new jobs automatically during specified hours
  - Rate limiting (max applications per hour)
- **F9.3** Email check scheduling
  - Check for responses periodically
  - Process and categorize incoming emails
- **F9.4** Maintenance tasks
  - Clean up old jobs (>30 days)
  - Archive completed applications
  - Database optimization

---

#### F10: Analytics & Insights
**Priority:** P3 (Low)

**Description:** Advanced analytics and insights on job search performance

**Requirements:**
- **F10.1** Success metrics dashboard
  - Application-to-response rate
  - Response-to-interview rate
  - Average time to response
  - Best performing job sources
- **F10.2** Trend analysis
  - Jobs by industry/company over time
  - Salary trends
  - Application success patterns
- **F10.3** Recommendations
  - Suggest keywords to add/remove
  - Recommend best times to apply
  - Identify high-response companies

---

## 4. System Architecture

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│  ┌──────────────────┐              ┌──────────────────┐    │
│  │  Web Dashboard   │              │  Email Client    │    │
│  │   (Flask App)    │              │  (SMTP/IMAP)     │    │
│  └────────┬─────────┘              └─────────┬────────┘    │
└───────────┼────────────────────────────────────┼────────────┘
            │                                    │
┌───────────┼────────────────────────────────────┼────────────┐
│           │         ORCHESTRATION LAYER        │            │
│  ┌────────▼─────────┐              ┌──────────▼─────────┐  │
│  │   Job Hunter     │              │  Response Manager  │  │
│  │  (Main Logic)    │              │  (Email Handler)   │  │
│  └────────┬─────────┘              └──────────┬─────────┘  │
└───────────┼────────────────────────────────────┼────────────┘
            │                                    │
┌───────────┼────────────────────────────────────┼────────────┐
│           │         BUSINESS LOGIC LAYER       │            │
│  ┌────────▼─────────┐  ┌──────────────┐  ┌───▼──────────┐ │
│  │  Job Matcher     │  │ Email Finder │  │   Response   │ │
│  │   (Scoring)      │  │  (Contacts)  │  │   Handler    │ │
│  └──────────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────────────────────────────────────────────┘
            │                                    │
┌───────────┼────────────────────────────────────┼────────────┐
│           │         DATA ACCESS LAYER          │            │
│  ┌────────▼─────────┐  ┌──────────────────────▼─────────┐  │
│  │  Job Database    │  │    Email Notifier              │  │
│  │   (SQLite)       │  │    (SMTP Client)               │  │
│  └──────────────────┘  └────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
            │                                    │
┌───────────┼────────────────────────────────────┼────────────┐
│           │      EXTERNAL INTEGRATIONS         │            │
│  ┌────────▼─────────┐  ┌──────────────────────▼─────────┐  │
│  │  LinkedIn Bot    │  │    Indeed Bot                  │  │
│  │   (Selenium)     │  │    (Requests + Selenium)       │  │
│  └──────────────────┘  └────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### 4.2 Module Responsibilities

#### Core Modules

**`config.py`**
- **Purpose:** Centralized configuration management
- **Responsibilities:**
  - User profile (name, email, phone, resume path)
  - Job search criteria (keywords, location, salary, etc.)
  - Platform credentials (LinkedIn, Indeed)
  - Email settings (SMTP config)
  - Application settings (auto-apply rules, thresholds)
  - Database path
- **Dependencies:** python-dotenv (for .env file support)

**`job_hunter.py`**
- **Purpose:** Main orchestration and business logic
- **Responsibilities:**
  - Coordinate job search across platforms
  - Filter and score jobs using JobMatcher
  - Trigger auto-apply for qualifying jobs
  - Send email summaries
  - Handle CLI arguments and execution modes
  - Logging and error handling
- **Dependencies:** All other modules

**`job_database.py`**
- **Purpose:** Database abstraction layer
- **Responsibilities:**
  - SQLite connection management
  - CRUD operations for jobs, applications, contacts, search history
  - Query methods (filters, aggregations)
  - Statistics calculation
  - CSV export functionality
- **Dependencies:** sqlite3

#### Platform Integration Modules

**`linkedin_bot.py`**
- **Purpose:** LinkedIn automation
- **Responsibilities:**
  - Login to LinkedIn
  - Search jobs with filters
  - Extract job details
  - Easy Apply automation
  - Multi-step form handling
  - Question detection and handling
  - Browser management (Selenium)
- **Dependencies:** selenium, webdriver-manager

**`indeed_bot.py`**
- **Purpose:** Indeed automation
- **Responsibilities:**
  - Search jobs (scraping with requests/BeautifulSoup)
  - Extract job details
  - Application automation (Selenium for apply pages)
  - Form filling
  - Question detection and handling
- **Dependencies:** requests, beautifulsoup4, selenium

#### Intelligence Modules

**`job_matcher.py`**
- **Purpose:** Job scoring and filtering
- **Responsibilities:**
  - Calculate match scores based on criteria
  - Filter jobs by minimum score
  - Provide match explanations
  - Keyword matching logic
  - Salary and experience validation
- **Dependencies:** None (pure Python logic)

**`email_finder.py`**
- **Purpose:** Contact discovery
- **Responsibilities:**
  - Scrape company websites for emails
  - Test common email patterns
  - Validate email addresses
  - Extract names from emails
  - Categorize contacts by role
  - Confidence scoring
- **Dependencies:** requests, beautifulsoup4

**`response_handler.py`**
- **Purpose:** Email response analysis
- **Responsibilities:**
  - Analyze incoming email content
  - Categorize response type (interview, rejection, info request, etc.)
  - Generate suggested responses
  - Provide next steps recommendations
  - Confidence scoring
- **Dependencies:** None (pure Python logic)

**`response_manager.py`**
- **Purpose:** Response workflow orchestration
- **Responsibilities:**
  - Process incoming emails
  - Match emails to job applications
  - Coordinate with ResponseHandler for analysis
  - Trigger appropriate actions (send response, notify user, etc.)
  - Update job statuses
  - Logging and tracking
- **Dependencies:** response_handler, email_finder, email_notifier, job_database

#### Communication Modules

**`email_notifier.py`**
- **Purpose:** Email sending
- **Responsibilities:**
  - SMTP connection management
  - Send emails (HTML and plain text)
  - Email template rendering
  - Attachment handling
  - Error handling and retries
- **Dependencies:** smtplib, email

**`email_templates.py`**
- **Purpose:** Email template library
- **Responsibilities:**
  - Pre-defined email templates for all scenarios
  - Template rendering with context
  - Multi-language support (French/English)
  - Personalization logic
- **Dependencies:** None (pure Python strings)

#### Web Interface Modules

**`web_app.py`**
- **Purpose:** Flask web application
- **Responsibilities:**
  - HTTP server and routing
  - Dashboard page rendering
  - RESTful API endpoints
  - Background job execution
  - Real-time status updates
  - Static file serving
- **Dependencies:** flask, flask-cors

**`templates/dashboard.html`**
- **Purpose:** Web UI
- **Responsibilities:**
  - Dashboard layout and styling
  - Job list display
  - Search controls
  - Statistics visualization
  - AJAX interactions
- **Dependencies:** TailwindCSS, Lucide icons

#### Automation Modules

**`scheduler.py`**
- **Purpose:** Scheduled task execution
- **Responsibilities:**
  - Schedule job searches
  - Schedule auto-apply runs
  - Schedule email checks
  - Maintenance tasks
  - Error handling and logging
- **Dependencies:** schedule

### 4.3 Data Flow Diagrams

#### Job Search Flow
```
User/Scheduler → job_hunter.py
                      ↓
          ┌───────────┴───────────┐
          ↓                       ↓
    linkedin_bot.py         indeed_bot.py
          ↓                       ↓
          └───────────┬───────────┘
                      ↓
              job_matcher.py (score & filter)
                      ↓
              job_database.py (save)
                      ↓
              email_notifier.py (summary)
```

#### Auto-Apply Flow
```
job_hunter.py → Get jobs with status='new' and score>threshold
                      ↓
          ┌───────────┴───────────┐
          ↓                       ↓
    linkedin_bot.apply()    indeed_bot.apply()
          ↓                       ↓
    Detect question type    Detect question type
          ↓                       ↓
    ┌─────┴─────┐           ┌─────┴─────┐
    ↓           ↓           ↓           ↓
  Simple    Complex       Simple    Complex
    ↓           ↓           ↓           ↓
  Auto-     Pause &      Auto-     Pause &
  answer    Email User   answer    Email User
    ↓           ↓           ↓           ↓
    └───────────┴───────────┴───────────┘
                      ↓
              Update status in DB
                      ↓
              Send confirmation email
```

#### Response Handling Flow
```
Email received → response_manager.py
                      ↓
              Find related job in DB
                      ↓
              response_handler.py (analyze)
                      ↓
          ┌───────────┴───────────┐
          ↓           ↓           ↓
      Interview   Rejection   Info Request
          ↓           ↓           ↓
    Find contacts  Send thanks  Alert user
          ↓           ↓           ↓
    Suggest times  Request feedback  Provide context
          ↓           ↓           ↓
          └───────────┴───────────┘
                      ↓
              Email user with suggestion
                      ↓
              Update job status
```

---

## 5. Technical Specifications

### 5.1 Technology Stack

**Backend:**
- Python 3.13+
- Flask 3.0+ (web framework)
- SQLite 3 (database)
- Selenium 4.15+ (browser automation)
- BeautifulSoup4 4.12+ (HTML parsing)
- Requests 2.31+ (HTTP client)

**Frontend:**
- HTML5
- TailwindCSS 3.x (styling)
- Vanilla JavaScript (no frameworks)
- Lucide Icons

**Infrastructure:**
- Render.com (hosting)
- Gunicorn (WSGI server)
- Git/GitHub (version control)

**External Services:**
- SMTP server (email sending)
- LinkedIn (job platform)
- Indeed (job platform)

### 5.2 Configuration Management

**Environment Variables (`.env`):**
```
# LinkedIn Credentials
LINKEDIN_EMAIL=user@example.com
LINKEDIN_PASSWORD=secure_password

# Indeed Credentials (optional)
INDEED_EMAIL=user@example.com
INDEED_PASSWORD=secure_password

# Email Configuration
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=user@gmail.com
EMAIL_PASSWORD=app_specific_password
EMAIL_FROM=user@gmail.com
EMAIL_FROM_NAME=Job Hunter Bot

# Job Search Criteria
JOB_KEYWORDS=Python Developer,Software Engineer
JOB_LOCATION=Paris, France
JOB_MIN_SALARY=35000
JOB_REMOTE=true

# Application Settings
AUTO_APPLY=true
MIN_MATCH_SCORE=30
MAX_APPLICATIONS_PER_DAY=50

# Database
DATABASE_PATH=jobs_database.db
```

### 5.3 Database Schema

**Jobs Table:**
```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    salary TEXT,
    description TEXT,
    url TEXT,
    source TEXT,
    posted_date TEXT,
    found_date TEXT,
    status TEXT DEFAULT 'new',
    match_score INTEGER,
    applied_date TEXT,
    notes TEXT
);
```

**Applications Table:**
```sql
CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT,
    applied_date TEXT,
    status TEXT,
    questions_encountered TEXT,
    responses_given TEXT,
    last_updated TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);
```

**Contacts Table:**
```sql
CREATE TABLE contacts (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    name TEXT,
    email TEXT,
    position TEXT,
    source TEXT,
    confidence REAL,
    found_date TEXT
);
```

**Search History Table:**
```sql
CREATE TABLE search_history (
    search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    keywords TEXT,
    location TEXT,
    jobs_found INTEGER,
    jobs_applied INTEGER,
    duration INTEGER
);
```

### 5.4 API Endpoints

**Web Dashboard API:**

```
GET  /                          - Dashboard page
GET  /api/status                - Get current search status
POST /api/search                - Start new job search
GET  /api/jobs                  - Get all jobs (with filters)
POST /api/jobs/<id>/status      - Update job status
GET  /api/stats                 - Get statistics
GET  /api/export                - Export jobs to CSV
```

### 5.5 Error Handling & Logging

**Logging Strategy:**
- Console output for real-time monitoring
- File logging for persistence (`job_hunter.log`)
- Separate logs for each module
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Error Handling:**
- Graceful degradation (continue on non-critical errors)
- Retry logic for network requests (3 attempts with exponential backoff)
- Email alerts for critical errors
- Database transaction rollback on errors

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Job search: Complete within 5 minutes for 100 jobs
- Auto-apply: Process 1 application per minute
- Dashboard: Page load <2 seconds
- Database queries: <100ms for common operations

### 6.2 Reliability
- Uptime: 99% (excluding scheduled maintenance)
- Data persistence: No data loss on crashes
- Graceful error recovery
- Automatic retry on transient failures

### 6.3 Security
- Credentials stored in environment variables (never in code)
- HTTPS for all external communications
- No sensitive data in logs
- Database file permissions restricted
- Rate limiting to avoid platform bans

### 6.4 Scalability
- Support for 1000+ jobs in database
- Handle 50+ applications per day
- Multiple concurrent searches (future)
- Multi-user support (future)

### 6.5 Maintainability
- Modular architecture (loose coupling)
- Clear separation of concerns
- Comprehensive documentation
- Type hints for all functions
- Unit tests for core logic (future)

### 6.6 Usability
- Web dashboard accessible from any device
- Clear status indicators and progress bars
- Intuitive job management interface
- Helpful error messages
- Email notifications for all important events

---

## 7. Deployment & Operations

### 7.1 Deployment Process
1. Push code to GitHub repository
2. Render auto-deploys from `main` branch
3. Environment variables configured in Render dashboard
4. Database file persists on Render disk (ephemeral)
5. Application accessible via Render URL

### 7.2 Environment Setup
- Python 3.13+ runtime
- Install dependencies: `pip install -r requirements.txt`
- Configure environment variables
- Initialize database: `python job_database.py`
- Run web app: `gunicorn web_app:app`

### 7.3 Monitoring
- Render dashboard for service health
- Application logs via Render logs viewer
- Email notifications for errors
- Web dashboard for job search metrics

### 7.4 Backup & Recovery
- Database: Manual backup via CSV export
- Code: Version controlled in Git
- Configuration: Documented in `.env.example`

---

## 8. Future Enhancements

### 8.1 Phase 2 Features
- Multi-user support with authentication
- PostgreSQL for persistent storage
- Advanced analytics dashboard
- Mobile app (React Native)
- Browser extension for one-click apply

### 8.2 Phase 3 Features
- AI-powered cover letter generation
- Interview preparation assistant
- Salary negotiation advisor
- Career path recommendations
- Integration with more job platforms (Glassdoor, Monster, etc.)

### 8.3 Technical Debt
- Add comprehensive unit tests
- Implement CI/CD pipeline
- Add API rate limiting
- Implement caching layer
- Add database migrations system

---

## 9. Risks & Mitigation

### 9.1 Technical Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Platform changes break scraping | High | Medium | Regular monitoring, fallback to manual mode |
| Account bans from platforms | High | Low | Rate limiting, human-like behavior simulation |
| Database corruption | Medium | Low | Regular backups, transaction management |
| Email delivery issues | Medium | Low | Retry logic, multiple SMTP providers |

### 9.2 Business Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Low application success rate | Medium | Medium | Improve matching algorithm, user feedback |
| User overwhelmed by emails | Low | Medium | Configurable notification settings |
| Complex questions not detected | Medium | Medium | Improve detection algorithm, user feedback |

---

## 10. Success Criteria & Acceptance

### 10.1 MVP Acceptance Criteria
- [ ] Successfully search and collect jobs from LinkedIn and Indeed
- [ ] Score and filter jobs with 70%+ accuracy
- [ ] Auto-apply to simple applications without errors
- [ ] Detect complex questions with 90%+ accuracy
- [ ] Send email notifications for all key events
- [ ] Web dashboard displays all jobs and statistics
- [ ] Find contact information for 50%+ of companies
- [ ] Zero data loss or corruption
- [ ] Deploy successfully to Render

### 10.2 User Acceptance Testing
- [ ] Run for 7 days without manual intervention
- [ ] Apply to 20+ jobs per day
- [ ] Receive interview requests from applications
- [ ] Successfully handle complex questions
- [ ] Dashboard accessible and functional
- [ ] Email notifications received and accurate

---

## 11. Appendix

### 11.1 Glossary
- **Easy Apply:** LinkedIn's one-click application feature
- **RHE:** Responsable Hygiène et Sécurité (Health & Safety Manager)
- **Chef de Chantier:** Site Manager/Construction Manager
- **Match Score:** Calculated relevance score (0-100) for a job
- **Complex Question:** Open-ended application question requiring human input

### 11.2 References
- LinkedIn Developer Documentation
- Indeed API Documentation (unofficial)
- Selenium WebDriver Documentation
- Flask Documentation
- Render Deployment Guide

### 11.3 Document History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-01 | System | Initial PRD creation |

---

**END OF DOCUMENT**
