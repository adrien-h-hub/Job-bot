"""
Job Hunter Bot - Web Dashboard with Authentication
Beautiful modern UI with login system
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from functools import wraps
import os
import hashlib
import json
from datetime import datetime, timedelta
from job_database import JobDatabase
from profile_optimizer import ProfileOptimizer
from cover_letter_generator import CoverLetterGenerator
from interview_prep import InterviewPrep
from salary_advisor import SalaryAdvisor
from career_planner import CareerPlanner
from smart_timing import SmartTiming
from config import PROFILE

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# User credentials (in production, use a proper database)
USERS = {
    'admin': {
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),
        'name': 'Administrator',
        'role': 'admin'
    },
    'user': {
        'password': hashlib.sha256('user123'.encode()).hexdigest(),
        'name': 'Job Seeker',
        'role': 'user'
    },
    'demo': {
        'password': hashlib.sha256('demo123'.encode()).hexdigest(),
        'name': 'Demo User',
        'role': 'user'
    }
}

# Initialize modules
db = JobDatabase()
optimizer = ProfileOptimizer()
cover_gen = CoverLetterGenerator()
interview_prep = InterviewPrep()
salary_adv = SalaryAdvisor()
career_planner = CareerPlanner()
timing = SmartTiming()
ai_assistant = AIAssistant()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'username' in session:
        if 'preferences' not in session:
            return redirect(url_for('onboarding'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if username in USERS and USERS[username]['password'] == hashed_password:
            session['username'] = username
            session['name'] = USERS[username]['name']
            session['role'] = USERS[username]['role']
            flash(f'Welcome back, {USERS[username]["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    if request.method == 'POST':
        # Save user preferences
        session['preferences'] = {
            'domain': request.form.get('domain'),
            'city': request.form.get('city'),
            'job_type': request.form.get('job_type'),
            'duration': request.form.get('duration'),
            'company_size': request.form.getlist('company_size'),
            'remote': request.form.get('remote')
        }
        flash(f'Préférences enregistrées! Recherche pour {session["preferences"]["domain"]} à {session["preferences"]["city"]}', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('onboarding.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    stats = db.get_stats()
    jobs = db.get_new_jobs()
    
    # Get profile analysis
    profile_analysis = None
    if jobs:
        profile_analysis = optimizer.analyze_keyword_gaps(jobs, PROFILE)
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         jobs=jobs[:5],
                         profile_analysis=profile_analysis,
                         user=session)

@app.route('/jobs')
@login_required
def jobs():
    all_jobs = db.get_new_jobs()
    return render_template('jobs.html', jobs=all_jobs, user=session)

@app.route('/job/<job_id>')
@login_required
def job_detail(job_id):
    job = db.get_job(job_id)
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('jobs'))
    
    # Generate materials for this job
    cover_letter = cover_gen.generate(job, PROFILE)
    interview_package = interview_prep.prepare_for_interview(job, job.get('company'), PROFILE)
    optimal_time = timing.format_optimal_time(job)
    
    return render_template('job_detail.html', 
                         job=job, 
                         cover_letter=cover_letter,
                         interview_package=interview_package,
                         optimal_time=optimal_time,
                         user=session)

@app.route('/profile')
@login_required
def profile():
    jobs = db.get_new_jobs()
    analysis = None
    
    if jobs:
        analysis = optimizer.analyze_keyword_gaps(jobs, PROFILE)
    
    return render_template('profile.html', 
                         profile=PROFILE, 
                         analysis=analysis,
                         user=session)

@app.route('/career-plan')
@login_required
def career_plan():
    current_role = PROFILE.get('current_role', 'Mid-Level Developer')
    target_role = 'Senior Software Architect'
    current_skills = PROFILE.get('skills', 'Python, Django, SQL').split(', ')
    
    plan = career_planner.create_career_plan(current_role, target_role, current_skills, '5 years')
    
    return render_template('career_plan.html', plan=plan, user=session)


@app.route('/api/stats')
@login_required
def api_stats():
    stats = db.get_stats()
    return jsonify(stats)

@app.route('/api/generate-cover-letter/<job_id>')
@login_required
def api_generate_cover_letter(job_id):
    job = db.get_job(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    letter = cover_gen.generate(job, PROFILE)
    return jsonify({'letter': letter})

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 JOB HUNTER BOT - WEB DASHBOARD")
    print("=" * 70)
    print("\n📋 Login Credentials:")
    print("\n  Admin Account:")
    print("    Username: admin")
    print("    Password: admin123")
    print("\n  User Account:")
    print("    Username: user")
    print("    Password: user123")
    print("\n  Demo Account:")
    print("    Username: demo")
    print("    Password: demo123")
    print("\n" + "=" * 70)
    print("🌐 Access the dashboard at: http://localhost:5000")
    print("=" * 70)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
