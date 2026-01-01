"""
Job Hunter Web Application
Flask-based web interface for the job hunter bot
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import threading
import json
from datetime import datetime
import os

from job_database import JobDatabase
from job_matcher import JobMatcher
from indeed_bot import IndeedBot

app = Flask(__name__)
CORS(app)

# Initialize database
db = JobDatabase('jobs_database.db')

# Global search status
search_status = {
    'running': False,
    'progress': 0,
    'message': 'Ready',
    'last_search': None
}


@app.route('/')
def index():
    """Main dashboard"""
    stats = db.get_stats()
    new_jobs = db.get_new_jobs()[:10]  # Top 10 new jobs
    return render_template('dashboard.html', stats=stats, jobs=new_jobs, status=search_status)


@app.route('/api/search', methods=['POST'])
def start_search():
    """Start a new job search"""
    global search_status
    
    if search_status['running']:
        return jsonify({'error': 'Search already running'}), 400
    
    data = request.json or {}
    keywords = data.get('keywords', 'Python Developer')
    location = data.get('location', 'Paris, France')
    sources = data.get('sources', ['indeed'])
    
    # Start search in background
    def run_search():
        global search_status
        search_status['running'] = True
        search_status['progress'] = 0
        search_status['message'] = 'Starting search...'
        
        try:
            all_jobs = []
            
            if 'indeed' in sources:
                search_status['message'] = 'Searching Indeed...'
                search_status['progress'] = 20
                
                indeed = IndeedBot(headless=True)
                jobs = indeed.search_jobs(keywords, location, posted_within_days=7)
                all_jobs.extend(jobs)
                indeed.close()
            
            search_status['message'] = 'Analyzing jobs...'
            search_status['progress'] = 60
            
            # Score jobs
            matcher = JobMatcher(
                required_keywords=['python', 'javascript', 'react', 'django'],
                exclude_keywords=['senior', 'lead', '10+ years'],
                min_salary=35000
            )
            filtered_jobs = matcher.filter_jobs(all_jobs, min_score=30)
            
            search_status['message'] = 'Saving to database...'
            search_status['progress'] = 80
            
            # Save to database
            new_count = 0
            for job in filtered_jobs:
                if db.add_job(job):
                    new_count += 1
            
            search_status['progress'] = 100
            search_status['message'] = f'Found {len(filtered_jobs)} jobs, {new_count} new'
            search_status['last_search'] = datetime.now().isoformat()
            
        except Exception as e:
            search_status['message'] = f'Error: {str(e)}'
        finally:
            search_status['running'] = False
    
    thread = threading.Thread(target=run_search)
    thread.start()
    
    return jsonify({'status': 'started'})


@app.route('/api/status')
def get_status():
    """Get current search status"""
    return jsonify(search_status)


@app.route('/api/jobs')
def get_jobs():
    """Get all jobs"""
    status_filter = request.args.get('status', 'new')
    source_filter = request.args.get('source')
    
    if source_filter:
        jobs = db.get_jobs_by_source(source_filter)
    else:
        jobs = db.get_new_jobs() if status_filter == 'new' else []
    
    return jsonify(jobs)


@app.route('/api/jobs/<job_id>/status', methods=['POST'])
def update_job_status(job_id):
    """Update job status"""
    data = request.json
    new_status = data.get('status')
    
    if new_status in ['new', 'applied', 'rejected', 'interview', 'offer', 'skipped']:
        db.update_job_status(job_id, new_status)
        if new_status == 'applied':
            db.mark_as_applied(job_id)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid status'}), 400


@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    return jsonify(db.get_stats())


@app.route('/api/export')
def export_jobs():
    """Export jobs to CSV"""
    filepath = 'jobs_export.csv'
    db.export_to_csv(filepath)
    return jsonify({'file': filepath})


# Create templates directory and HTML template
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(TEMPLATE_DIR, exist_ok=True)

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Job Hunter Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { transition: transform 0.2s, box-shadow 0.2s; }
        .card:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    </style>
</head>
<body class="bg-gray-100 min-h-screen">
    <!-- Header -->
    <header class="gradient-bg text-white p-6 shadow-lg">
        <div class="max-w-6xl mx-auto flex justify-between items-center">
            <div>
                <h1 class="text-3xl font-bold">🎯 Job Hunter</h1>
                <p class="opacity-80">Find your dream job automatically</p>
            </div>
            <div class="text-right">
                <div id="status-badge" class="bg-white/20 px-4 py-2 rounded-full">
                    {{ status.message }}
                </div>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto p-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-white rounded-xl p-6 card">
                <div class="text-gray-500 text-sm">Total Jobs</div>
                <div class="text-3xl font-bold text-purple-600">{{ stats.total_jobs }}</div>
            </div>
            <div class="bg-white rounded-xl p-6 card">
                <div class="text-gray-500 text-sm">New Jobs</div>
                <div class="text-3xl font-bold text-blue-600">{{ stats.new_jobs }}</div>
            </div>
            <div class="bg-white rounded-xl p-6 card">
                <div class="text-gray-500 text-sm">Applied</div>
                <div class="text-3xl font-bold text-green-600">{{ stats.applied }}</div>
            </div>
            <div class="bg-white rounded-xl p-6 card">
                <div class="text-gray-500 text-sm">Interviews</div>
                <div class="text-3xl font-bold text-yellow-600">{{ stats.interviews }}</div>
            </div>
        </div>

        <!-- Search Controls -->
        <div class="bg-white rounded-xl p-6 mb-8 card">
            <h2 class="text-xl font-bold mb-4">🔍 New Search</h2>
            <div class="grid md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm text-gray-600 mb-1">Keywords</label>
                    <input type="text" id="keywords" value="Python Developer" 
                        class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-purple-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm text-gray-600 mb-1">Location</label>
                    <input type="text" id="location" value="Paris, France"
                        class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-purple-500 outline-none">
                </div>
                <div class="flex items-end">
                    <button onclick="startSearch()" id="search-btn"
                        class="w-full bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition font-semibold">
                        🚀 Start Search
                    </button>
                </div>
            </div>
            <!-- Progress Bar -->
            <div id="progress-container" class="mt-4 hidden">
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div id="progress-bar" class="bg-purple-600 h-2 rounded-full transition-all" style="width: 0%"></div>
                </div>
                <p id="progress-text" class="text-sm text-gray-600 mt-1"></p>
            </div>
        </div>

        <!-- Job List -->
        <div class="bg-white rounded-xl p-6 card">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold">📋 Recent Jobs</h2>
                <button onclick="exportJobs()" class="text-purple-600 hover:underline text-sm">
                    📥 Export CSV
                </button>
            </div>
            <div id="job-list" class="space-y-4">
                {% for job in jobs %}
                <div class="border rounded-lg p-4 hover:bg-gray-50 transition">
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <div class="flex items-center gap-2">
                                <h3 class="font-semibold text-lg">{{ job.title }}</h3>
                                {% if job.match_score %}
                                <span class="bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full text-xs">
                                    {{ job.match_score|int }}% match
                                </span>
                                {% endif %}
                            </div>
                            <p class="text-purple-600">{{ job.company }}</p>
                            <p class="text-gray-500 text-sm">📍 {{ job.location }}</p>
                            {% if job.salary %}
                            <p class="text-green-600 text-sm">💰 {{ job.salary }}</p>
                            {% endif %}
                        </div>
                        <div class="flex gap-2">
                            <button onclick="updateStatus('{{ job.job_id }}', 'applied')" 
                                class="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600">
                                ✓ Applied
                            </button>
                            <button onclick="updateStatus('{{ job.job_id }}', 'skipped')"
                                class="bg-gray-300 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-400">
                                ✗ Skip
                            </button>
                            {% if job.url %}
                            <a href="{{ job.url }}" target="_blank" 
                                class="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600">
                                View →
                            </a>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% else %}
                <p class="text-gray-500 text-center py-8">No jobs found yet. Start a search!</p>
                {% endfor %}
            </div>
        </div>
    </main>

    <script>
        let searchInterval = null;

        function startSearch() {
            const keywords = document.getElementById('keywords').value;
            const location = document.getElementById('location').value;
            
            fetch('/api/search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({keywords, location, sources: ['indeed']})
            }).then(r => r.json()).then(data => {
                if (data.status === 'started') {
                    document.getElementById('progress-container').classList.remove('hidden');
                    document.getElementById('search-btn').disabled = true;
                    document.getElementById('search-btn').textContent = '⏳ Searching...';
                    checkStatus();
                }
            });
        }

        function checkStatus() {
            fetch('/api/status').then(r => r.json()).then(status => {
                document.getElementById('progress-bar').style.width = status.progress + '%';
                document.getElementById('progress-text').textContent = status.message;
                document.getElementById('status-badge').textContent = status.message;
                
                if (status.running) {
                    setTimeout(checkStatus, 1000);
                } else {
                    document.getElementById('search-btn').disabled = false;
                    document.getElementById('search-btn').textContent = '🚀 Start Search';
                    if (status.progress === 100) {
                        setTimeout(() => location.reload(), 1500);
                    }
                }
            });
        }

        function updateStatus(jobId, status) {
            fetch(`/api/jobs/${jobId}/status`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({status})
            }).then(() => location.reload());
        }

        function exportJobs() {
            fetch('/api/export').then(r => r.json()).then(data => {
                alert('Jobs exported to ' + data.file);
            });
        }
    </script>
</body>
</html>
'''

# Write template file
with open(os.path.join(TEMPLATE_DIR, 'dashboard.html'), 'w', encoding='utf-8') as f:
    f.write(DASHBOARD_HTML)


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎯 JOB HUNTER WEB DASHBOARD")
    print("="*50)
    print("Starting server at http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)
