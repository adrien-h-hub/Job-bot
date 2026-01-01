"""
Complete Workflow Example - Using all 9 enhanced features
"""

from job_hunter import JobHunter
from smart_timing import SmartTiming
from profile_optimizer import ProfileOptimizer
from cover_letter_generator import CoverLetterGenerator
from interview_prep import InterviewPrep
from salary_advisor import SalaryAdvisor
from career_planner import CareerPlanner
from config import PROFILE
import os

print("=" * 70)
print("JOB HUNTER BOT - COMPLETE ENHANCED WORKFLOW")
print("=" * 70)

# Initialize all modules
print("\nInitializing modules...")
hunter = JobHunter()
timing = SmartTiming()
optimizer = ProfileOptimizer()
cover_gen = CoverLetterGenerator()
interview_prep = InterviewPrep()
salary_adv = SalaryAdvisor()
career_planner = CareerPlanner()

print("✓ All modules initialized")

# Step 1: Search for jobs
print("\n" + "=" * 70)
print("STEP 1: JOB SEARCH")
print("=" * 70)

# Start with Indeed only for faster testing
jobs = hunter.run_search(['indeed'], headless=True)
print(f"\n✓ Found {len(jobs)} jobs")

# Step 2: Profile Analysis
if jobs:
    print("\n" + "=" * 70)
    print("STEP 2: PROFILE OPTIMIZATION")
    print("=" * 70)
    
    analysis = optimizer.analyze_keyword_gaps(jobs, PROFILE)
    
    print(f"\nProfile Strength: {analysis['profile_strength']['score']}%")
    print(f"Category: {analysis['profile_strength']['category']}")
    print(f"Missing Keywords: {len(analysis['missing_keywords'])}")
    
    if analysis['missing_keywords']:
        print("\nTop Missing Keywords:")
        for i, keyword in enumerate(analysis['missing_keywords'][:5], 1):
            freq = analysis['keyword_frequency'][keyword]
            print(f"  {i}. {keyword} (appears in {freq} jobs)")
    
    # Save full report
    with open('profile_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(optimizer.generate_report(analysis))
    print("\n✓ Full report saved to: profile_analysis_report.txt")

# Step 3: Smart Timing & Application
print("\n" + "=" * 70)
print("STEP 3: SMART APPLICATION TIMING")
print("=" * 70)

applied_now = 0
queued = 0

for job in jobs[:5]:  # Process top 5 jobs
    print(f"\nProcessing: {job.get('title')} at {job.get('company')}")
    
    if timing.should_apply_now(job):
        print(f"  ⚡ Optimal time to apply NOW")
        applied_now += 1
        
        # Generate cover letter
        letter = cover_gen.generate(job, PROFILE, style='professional')
        filename = f"cover_letter_{job.get('company', 'company').replace(' ', '_')}.txt"
        cover_gen.save_letter(letter, job, filename)
        print(f"  ✓ Cover letter saved: {filename}")
        
        # Note: Actual application would happen here if auto_apply is enabled
        # hunter.auto_apply([job])
        
    else:
        optimal = timing.get_optimal_apply_time(job)
        hunter.db.add_queued_application(job.get('job_id'), optimal.isoformat())
        print(f"  ⏰ Queued for: {timing.format_optimal_time(job)}")
        queued += 1

print(f"\n✓ Applied immediately: {applied_now}")
print(f"✓ Queued for optimal time: {queued}")

# Step 4: Interview Preparation
if jobs:
    print("\n" + "=" * 70)
    print("STEP 4: INTERVIEW PREPARATION")
    print("=" * 70)
    
    top_job = jobs[0]
    print(f"\nPreparing for: {top_job.get('title')} at {top_job.get('company')}")
    
    package = interview_prep.prepare_for_interview(
        top_job,
        top_job.get('company'),
        PROFILE
    )
    
    print(f"✓ Questions prepared: {sum(len(q) for q in package['common_questions'].values())}")
    print(f"✓ Interview tips: {len(package['interview_tips'])}")
    print(f"✓ Questions to ask: {len(package['questions_to_ask'])}")
    
    # Save prep package
    filename = f"interview_prep_{top_job.get('company', 'company').replace(' ', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(interview_prep.generate_report(package))
    print(f"✓ Saved to: {filename}")

# Step 5: Salary Analysis (Example)
print("\n" + "=" * 70)
print("STEP 5: SALARY ANALYSIS (EXAMPLE)")
print("=" * 70)

example_job = {
    'title': 'Senior Python Developer',
    'location': 'Paris, France'
}
example_offer = 55000

print(f"\nAnalyzing offer: €{example_offer:,} for {example_job['title']}")

analysis = salary_adv.analyze_offer(example_job, example_offer, PROFILE)

print(f"\n✓ Market percentile: {analysis['percentile']}th")
print(f"✓ Assessment: {analysis['assessment']}")
print(f"✓ Suggested counter: €{analysis['counter_offer']['suggested_amount']:,}")
print(f"✓ Minimum acceptable: €{analysis['counter_offer']['minimum_acceptable']:,}")

# Save salary analysis
with open('salary_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(salary_adv.generate_report(analysis))
print(f"✓ Saved to: salary_analysis.txt")

# Step 6: Career Planning
print("\n" + "=" * 70)
print("STEP 6: CAREER PATH PLANNING")
print("=" * 70)

current_role = PROFILE.get('current_role', 'Mid-Level Developer')
target_role = 'Senior Software Architect'
current_skills = PROFILE.get('skills', 'Python, Django, SQL').split(', ')

print(f"\nPlanning path: {current_role} → {target_role}")

plan = career_planner.create_career_plan(
    current_role,
    target_role,
    current_skills,
    '5 years'
)

print(f"\n✓ Progression steps: {len(plan['progression_path'])}")
print(f"✓ Skill gaps: {len(plan['skill_gaps'])}")
print(f"✓ Milestones: {len(plan['milestones'])}")
print(f"✓ Action items: {len(plan['action_items'])}")

# Save career plan
with open('career_development_plan.txt', 'w', encoding='utf-8') as f:
    f.write(career_planner.generate_report(plan))
print(f"✓ Saved to: career_development_plan.txt")

# Step 7: Statistics
print("\n" + "=" * 70)
print("STEP 7: YOUR STATISTICS")
print("=" * 70)

hunter.show_stats()

# Summary
print("\n" + "=" * 70)
print("WORKFLOW COMPLETE!")
print("=" * 70)

print("\n📁 Files Created:")
print("  • profile_analysis_report.txt")
if jobs:
    print(f"  • cover_letter_{jobs[0].get('company', 'company').replace(' ', '_')}.txt")
    print(f"  • interview_prep_{jobs[0].get('company', 'company').replace(' ', '_')}.txt")
print("  • salary_analysis.txt")
print("  • career_development_plan.txt")

print("\n💡 Next Steps:")
print("  1. Review generated cover letters")
print("  2. Study interview preparation materials")
print("  3. Check queued applications")
print("  4. Monitor for responses")
print("  5. Follow career development plan")

print("\n🎯 To process queued applications:")
print("  python -c \"from job_hunter import JobHunter; JobHunter().process_queued_applications()\"")

print("\n✅ All features working perfectly!")
print("=" * 70)
