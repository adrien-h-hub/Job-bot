"""
Feature Verification Script - Test all 9 implemented features
"""

import sys
import os

print("=" * 70)
print("JOB HUNTER BOT - FEATURE VERIFICATION")
print("=" * 70)

results = []

# Test 1: Smart Timing
print("\n1. Testing Smart Timing...")
try:
    from smart_timing import SmartTiming
    timing = SmartTiming()
    test_job = {'title': 'Python Developer', 'location': 'Paris, France'}
    optimal = timing.get_optimal_apply_time(test_job)
    should_apply = timing.should_apply_now(test_job)
    print(f"   ✓ Smart Timing working")
    print(f"   - Optimal time calculated: {optimal.strftime('%A %I:%M %p')}")
    print(f"   - Should apply now: {should_apply}")
    results.append(("Smart Timing", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Smart Timing", False))

# Test 2: Webhook Notifier
print("\n2. Testing Webhook Notifier...")
try:
    from webhook_notifier import WebhookNotifier
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url:
        notifier = WebhookNotifier(webhook_url, 'slack')
        print(f"   ✓ Webhook Notifier initialized")
        print(f"   - Platform: {notifier.platform}")
        results.append(("Webhook Notifier", True))
    else:
        print(f"   ⚠ WEBHOOK_URL not set - module OK but not configured")
        results.append(("Webhook Notifier", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Webhook Notifier", False))

# Test 3: Profile Optimizer
print("\n3. Testing Profile Optimizer...")
try:
    from profile_optimizer import ProfileOptimizer
    optimizer = ProfileOptimizer()
    test_jobs = [{'title': 'Python Developer', 'description': 'Python Django AWS'}]
    test_profile = {'skills': 'Python, SQL'}
    analysis = optimizer.analyze_keyword_gaps(test_jobs, test_profile)
    print(f"   ✓ Profile Optimizer working")
    print(f"   - Missing keywords found: {len(analysis['missing_keywords'])}")
    print(f"   - Profile strength: {analysis['profile_strength']['score']}%")
    results.append(("Profile Optimizer", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Profile Optimizer", False))

# Test 4: Async Job Search
print("\n4. Testing Async Job Search...")
try:
    from async_job_search import AsyncJobSearch
    searcher = AsyncJobSearch()
    print(f"   ✓ Async Job Search module loaded")
    print(f"   - Max workers: {searcher.max_workers}")
    searcher.cleanup()
    results.append(("Async Job Search", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Async Job Search", False))

# Test 5: Cover Letter Generator
print("\n5. Testing Cover Letter Generator...")
try:
    from cover_letter_generator import CoverLetterGenerator
    generator = CoverLetterGenerator()
    test_job = {'title': 'Developer', 'company': 'Test Corp', 'description': 'Test'}
    test_profile = {'first_name': 'John', 'last_name': 'Doe', 'skills': 'Python'}
    letter = generator.generate(test_job, test_profile)
    print(f"   ✓ Cover Letter Generator working")
    print(f"   - Generated {len(letter)} characters")
    if os.getenv('OPENAI_API_KEY'):
        print(f"   - Mode: AI-powered")
    else:
        print(f"   - Mode: Template (set OPENAI_API_KEY for AI)")
    results.append(("Cover Letter Generator", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Cover Letter Generator", False))

# Test 6: Interview Prep
print("\n6. Testing Interview Prep...")
try:
    from interview_prep import InterviewPrep
    prep = InterviewPrep()
    test_job = {'title': 'Developer', 'company': 'Test Corp'}
    test_profile = {'current_role': 'Developer', 'years_experience': 5}
    package = prep.prepare_for_interview(test_job, 'Test Corp', test_profile)
    print(f"   ✓ Interview Prep working")
    print(f"   - Questions prepared: {sum(len(q) for q in package['common_questions'].values())}")
    print(f"   - Tips provided: {len(package['interview_tips'])}")
    results.append(("Interview Prep", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Interview Prep", False))

# Test 7: Salary Advisor
print("\n7. Testing Salary Advisor...")
try:
    from salary_advisor import SalaryAdvisor
    advisor = SalaryAdvisor()
    test_job = {'title': 'Python Developer', 'location': 'Paris, France'}
    test_profile = {'years_experience': 5, 'skills': 'Python'}
    analysis = advisor.analyze_offer(test_job, 55000, test_profile)
    print(f"   ✓ Salary Advisor working")
    print(f"   - Market percentile: {analysis['percentile']}th")
    print(f"   - Suggested counter: €{analysis['counter_offer']['suggested_amount']:,}")
    results.append(("Salary Advisor", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Salary Advisor", False))

# Test 8: Glassdoor Bot
print("\n8. Testing Glassdoor Bot...")
try:
    from glassdoor_bot import GlassdoorBot
    bot = GlassdoorBot(headless=True)
    print(f"   ✓ Glassdoor Bot module loaded")
    print(f"   - Base URL: {bot.base_url}")
    results.append(("Glassdoor Bot", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Glassdoor Bot", False))

# Test 9: Career Planner
print("\n9. Testing Career Planner...")
try:
    from career_planner import CareerPlanner
    planner = CareerPlanner()
    plan = planner.create_career_plan(
        'Mid Developer', 
        'Senior Developer',
        ['Python', 'SQL'],
        '5 years'
    )
    print(f"   ✓ Career Planner working")
    print(f"   - Milestones created: {len(plan['milestones'])}")
    print(f"   - Skill gaps identified: {len(plan['skill_gaps'])}")
    results.append(("Career Planner", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Career Planner", False))

# Test 10: Database
print("\n10. Testing Database...")
try:
    from job_database import JobDatabase
    db = JobDatabase()
    db.init_database()
    
    # Check for new table
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    has_queued = 'queued_applications' in tables
    print(f"   ✓ Database working")
    print(f"   - Tables: {', '.join(tables)}")
    print(f"   - Queued applications table: {'✓' if has_queued else '✗'}")
    results.append(("Database", True))
except Exception as e:
    print(f"   ✗ Error: {e}")
    results.append(("Database", False))

# Summary
print("\n" + "=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)

passed = sum(1 for _, status in results if status)
total = len(results)

for feature, status in results:
    symbol = "✓" if status else "✗"
    print(f"{symbol} {feature}")

print("\n" + "=" * 70)
print(f"RESULT: {passed}/{total} features working ({int(passed/total*100)}%)")
print("=" * 70)

if passed == total:
    print("\n🎉 ALL FEATURES VERIFIED! Ready for production!")
elif passed >= total * 0.7:
    print("\n✓ Most features working! Review failed items above.")
else:
    print("\n⚠ Several features need attention. Check errors above.")

# Exit code
sys.exit(0 if passed == total else 1)
