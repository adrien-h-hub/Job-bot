"""
Add Sample Jobs - For testing all features without scraping
"""

from job_database import JobDatabase
from datetime import datetime

print("=" * 70)
print("ADDING SAMPLE JOBS FOR TESTING")
print("=" * 70)

db = JobDatabase()

sample_jobs = [
    {
        'job_id': 'sample_001',
        'title': 'Senior Python Developer',
        'company': 'Tech Innovations Inc',
        'location': 'Paris, France',
        'salary': '€60,000 - €80,000',
        'description': '''
        We are seeking an experienced Python Developer to join our team.
        
        Requirements:
        - 5+ years Python experience
        - Django, Flask frameworks
        - AWS, Docker, Kubernetes
        - PostgreSQL, MongoDB
        - REST APIs, microservices
        - Git, CI/CD
        - Agile methodology
        
        Nice to have:
        - Machine Learning experience
        - React or Vue.js
        - Team leadership
        ''',
        'url': 'https://example.com/jobs/senior-python-developer',
        'source': 'manual',
        'posted_date': '2 days ago',
        'match_score': 85
    },
    {
        'job_id': 'sample_002',
        'title': 'Full Stack Developer',
        'company': 'StartupCo',
        'location': 'Paris, France',
        'salary': '€50,000 - €70,000',
        'description': '''
        Join our growing startup as a Full Stack Developer!
        
        Tech Stack:
        - Frontend: React, TypeScript, TailwindCSS
        - Backend: Node.js, Express, Python
        - Database: MongoDB, PostgreSQL
        - Cloud: AWS, Docker
        - Tools: Git, Jira, Slack
        
        What we offer:
        - Remote work flexibility
        - Stock options
        - Learning budget
        - Modern tech stack
        ''',
        'url': 'https://example.com/jobs/fullstack-developer',
        'source': 'manual',
        'posted_date': '1 day ago',
        'match_score': 75
    },
    {
        'job_id': 'sample_003',
        'title': 'Data Scientist',
        'company': 'Analytics Corp',
        'location': 'Paris, France',
        'salary': '€65,000 - €85,000',
        'description': '''
        Data Scientist position in AI/ML team.
        
        Requirements:
        - Python (pandas, numpy, scikit-learn)
        - Machine Learning, Deep Learning
        - TensorFlow or PyTorch
        - SQL, data visualization
        - Statistics, mathematics
        - Communication skills
        
        Projects:
        - Predictive modeling
        - NLP applications
        - Computer vision
        - Data pipeline development
        ''',
        'url': 'https://example.com/jobs/data-scientist',
        'source': 'manual',
        'posted_date': '3 days ago',
        'match_score': 80
    },
    {
        'job_id': 'sample_004',
        'title': 'Backend Developer',
        'company': 'Enterprise Solutions',
        'location': 'Paris, France',
        'salary': '€55,000 - €75,000',
        'description': '''
        Backend Developer for enterprise applications.
        
        Stack:
        - Python, Django, FastAPI
        - PostgreSQL, Redis
        - Docker, Kubernetes
        - AWS or Azure
        - Microservices architecture
        - REST and GraphQL APIs
        
        Responsibilities:
        - Design and implement APIs
        - Database optimization
        - Code reviews
        - Mentoring junior developers
        ''',
        'url': 'https://example.com/jobs/backend-developer',
        'source': 'manual',
        'posted_date': '5 days ago',
        'match_score': 78
    },
    {
        'job_id': 'sample_005',
        'title': 'DevOps Engineer',
        'company': 'Cloud Systems Ltd',
        'location': 'Paris, France',
        'salary': '€58,000 - €78,000',
        'description': '''
        DevOps Engineer to manage our cloud infrastructure.
        
        Skills:
        - AWS, Azure, or GCP
        - Docker, Kubernetes
        - Terraform, Ansible
        - CI/CD (Jenkins, GitLab CI)
        - Python, Bash scripting
        - Monitoring (Prometheus, Grafana)
        
        Duties:
        - Infrastructure as Code
        - Automation
        - Performance optimization
        - Security best practices
        ''',
        'url': 'https://example.com/jobs/devops-engineer',
        'source': 'manual',
        'posted_date': '1 week ago',
        'match_score': 70
    }
]

print(f"\nAdding {len(sample_jobs)} sample jobs to database...\n")

added = 0
for job in sample_jobs:
    if db.add_job(job):
        added += 1
        print(f"✓ Added: {job['title']} at {job['company']} ({job['match_score']}% match)")
    else:
        print(f"⚠ Skipped (already exists): {job['title']}")

print(f"\n{'=' * 70}")
print(f"✅ Successfully added {added} sample jobs!")
print(f"{'=' * 70}")

# Show stats
stats = db.get_stats()
print(f"\n📊 Database Statistics:")
print(f"  Total Jobs: {stats['total_jobs']}")
print(f"  New Jobs: {stats['new_jobs']}")
print(f"  Applied: {stats['applied']}")

print(f"\n💡 Next Steps:")
print(f"  1. Run: python complete_workflow.py")
print(f"  2. Test profile optimization")
print(f"  3. Generate cover letters")
print(f"  4. Create interview prep materials")
print(f"\n{'=' * 70}")
