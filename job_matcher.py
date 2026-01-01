"""
Job Matcher - Analyzes jobs against your profile and preferences
"""

import re
from typing import Dict, List


class JobMatcher:
    def __init__(self, required_keywords: List[str], exclude_keywords: List[str],
                 experience_level: List[str] = None, min_salary: int = None):
        self.required_keywords = [kw.lower() for kw in required_keywords]
        self.exclude_keywords = [kw.lower() for kw in exclude_keywords]
        self.experience_level = experience_level or []
        self.min_salary = min_salary
        
    def calculate_match_score(self, job: Dict) -> float:
        """
        Calculate how well a job matches the search criteria
        Returns a score from 0 to 100
        """
        score = 50  # Base score
        
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        full_text = f"{title} {description}"
        
        # Check for excluded keywords (-30 points each, can go negative)
        for keyword in self.exclude_keywords:
            if keyword in full_text:
                score -= 30
                
        # Check for required keywords (+15 points each)
        keywords_found = 0
        for keyword in self.required_keywords:
            if keyword in full_text:
                score += 15
                keywords_found += 1
        
        # Bonus for having multiple required keywords
        if keywords_found >= 3:
            score += 10
        
        # Experience level check
        experience_patterns = {
            'entry': [r'entry.?level', r'junior', r'graduate', r'0-2 years', r'débutant'],
            'junior': [r'junior', r'1-3 years', r'2-3 years'],
            'mid': [r'mid.?level', r'3-5 years', r'intermediate'],
            'senior': [r'senior', r'5\+ years', r'lead', r'principal'],
        }
        
        for level in self.experience_level:
            if level in experience_patterns:
                for pattern in experience_patterns[level]:
                    if re.search(pattern, full_text):
                        score += 10
                        break
        
        # Salary check (if provided)
        salary_text = job.get('salary', '')
        if salary_text and self.min_salary:
            salary_match = self._parse_salary(salary_text)
            if salary_match:
                if salary_match >= self.min_salary:
                    score += 15
                elif salary_match < self.min_salary * 0.8:
                    score -= 20
        
        # Easy Apply bonus
        if job.get('easy_apply'):
            score += 5
        
        # Recent posting bonus
        posted = job.get('posted_date', '').lower()
        if any(word in posted for word in ['today', "aujourd'hui", 'just', 'hour']):
            score += 10
        elif any(word in posted for word in ['yesterday', 'hier', '1 day']):
            score += 5
            
        # Cap score between 0 and 100
        return max(0, min(100, score))
    
    def _parse_salary(self, salary_text: str) -> int:
        """Parse salary from text, return annual amount"""
        salary_text = salary_text.lower().replace(' ', '').replace(',', '')
        
        # Try to find numbers
        numbers = re.findall(r'\d+', salary_text)
        if not numbers:
            return 0
        
        # Get the main number
        salary = int(numbers[0])
        
        # Check if it's monthly (convert to annual)
        if 'month' in salary_text or 'mois' in salary_text or '/m' in salary_text:
            salary *= 12
        
        # Handle K notation (e.g., 45K)
        if salary < 1000:
            salary *= 1000
            
        return salary
    
    def filter_jobs(self, jobs: List[Dict], min_score: int = 40) -> List[Dict]:
        """Filter and score jobs, return only those above minimum score"""
        scored_jobs = []
        
        for job in jobs:
            score = self.calculate_match_score(job)
            job['match_score'] = score
            
            if score >= min_score:
                scored_jobs.append(job)
        
        # Sort by score (highest first)
        scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        return scored_jobs
    
    def get_match_explanation(self, job: Dict) -> str:
        """Get explanation of why a job matched or didn't match"""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        full_text = f"{title} {description}"
        
        reasons = []
        
        # Found required keywords
        found_keywords = [kw for kw in self.required_keywords if kw in full_text]
        if found_keywords:
            reasons.append(f"✅ Keywords found: {', '.join(found_keywords)}")
        
        # Found excluded keywords
        found_excluded = [kw for kw in self.exclude_keywords if kw in full_text]
        if found_excluded:
            reasons.append(f"⚠️ Excluded keywords found: {', '.join(found_excluded)}")
        
        # Easy apply
        if job.get('easy_apply'):
            reasons.append("✅ Easy Apply available")
        
        # Score
        score = job.get('match_score', 0)
        reasons.append(f"📊 Match score: {score}%")
        
        return '\n'.join(reasons)


def test_matcher():
    """Test job matcher"""
    matcher = JobMatcher(
        required_keywords=['python', 'django', 'javascript', 'react'],
        exclude_keywords=['senior', 'lead', '10+ years'],
        experience_level=['entry', 'junior', 'mid'],
        min_salary=35000
    )
    
    test_jobs = [
        {
            'title': 'Junior Python Developer',
            'description': 'Looking for a junior developer with Python and Django experience. React is a plus.',
            'salary': '35K - 45K',
            'easy_apply': True
        },
        {
            'title': 'Senior Software Engineer',
            'description': 'Need senior developer with 10+ years experience',
            'salary': '80K',
            'easy_apply': False
        },
        {
            'title': 'Full Stack Developer',
            'description': 'Python, JavaScript, React needed. Entry level position.',
            'salary': '40000/year',
            'easy_apply': True
        }
    ]
    
    filtered = matcher.filter_jobs(test_jobs)
    
    print("Filtered Jobs:")
    for job in filtered:
        print(f"\n{job['title']} - Score: {job['match_score']}")
        print(matcher.get_match_explanation(job))


if __name__ == "__main__":
    test_matcher()
