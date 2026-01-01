"""
Profile Optimizer - Analyze job keywords and suggest profile improvements
"""

from typing import Dict, List, Set
from collections import Counter
import re


class ProfileOptimizer:
    """Analyze keyword gaps between jobs and user profile"""
    
    def __init__(self):
        # Common stop words to ignore
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
    
    def analyze_keyword_gaps(self, jobs: List[Dict], profile: Dict) -> Dict:
        """
        Find keywords in jobs missing from profile
        
        Args:
            jobs: List of job dictionaries
            profile: User profile dictionary
            
        Returns:
            Dict with missing keywords, suggestions, and priority skills
        """
        # Extract keywords from jobs
        job_keywords = self._extract_keywords_from_jobs(jobs)
        
        # Extract keywords from profile
        profile_keywords = self._extract_keywords_from_profile(profile)
        
        # Find missing keywords
        missing = set(job_keywords.keys()) - set(profile_keywords.keys())
        
        # Sort by frequency in job descriptions
        missing_sorted = sorted(
            missing,
            key=lambda k: job_keywords[k],
            reverse=True
        )[:30]  # Top 30 missing keywords
        
        # Categorize keywords
        categorized = self._categorize_keywords(missing_sorted, job_keywords)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(categorized, profile)
        
        # Identify priority skills
        priority_skills = self._identify_priority_skills(job_keywords, profile_keywords)
        
        return {
            'missing_keywords': missing_sorted,
            'keyword_frequency': {k: job_keywords[k] for k in missing_sorted},
            'categorized_keywords': categorized,
            'suggestions': suggestions,
            'priority_skills': priority_skills,
            'profile_strength': self._calculate_profile_strength(job_keywords, profile_keywords)
        }
    
    def _extract_keywords_from_jobs(self, jobs: List[Dict]) -> Counter:
        """Extract and count keywords from job descriptions"""
        keywords = Counter()
        
        for job in jobs:
            # Combine title and description
            text = f"{job.get('title', '')} {job.get('description', '')}"
            
            # Extract keywords
            words = self._extract_keywords(text)
            keywords.update(words)
        
        return keywords
    
    def _extract_keywords_from_profile(self, profile: Dict) -> Counter:
        """Extract keywords from user profile"""
        keywords = Counter()
        
        # Combine all profile text
        text_parts = [
            profile.get('summary', ''),
            profile.get('experience', ''),
            profile.get('skills', ''),
            profile.get('education', ''),
            ' '.join(profile.get('certifications', []))
        ]
        
        text = ' '.join(text_parts)
        words = self._extract_keywords(text)
        keywords.update(words)
        
        return keywords
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces and hyphens
        text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Filter out stop words and short words
        keywords = [
            word for word in words
            if word not in self.stop_words and len(word) > 2
        ]
        
        # Also extract common multi-word phrases
        bigrams = self._extract_bigrams(text)
        keywords.extend(bigrams)
        
        return keywords
    
    def _extract_bigrams(self, text: str) -> List[str]:
        """Extract common two-word phrases"""
        words = text.split()
        bigrams = []
        
        # Common technical bigrams
        tech_patterns = [
            'machine learning', 'data science', 'artificial intelligence',
            'deep learning', 'natural language', 'computer vision',
            'cloud computing', 'software development', 'web development',
            'mobile development', 'full stack', 'front end', 'back end',
            'database management', 'project management', 'agile development',
            'continuous integration', 'continuous deployment', 'version control'
        ]
        
        text_lower = text.lower()
        for pattern in tech_patterns:
            if pattern in text_lower:
                bigrams.append(pattern.replace(' ', '_'))
        
        return bigrams
    
    def _categorize_keywords(self, keywords: List[str], frequency: Counter) -> Dict:
        """Categorize keywords into technical skills, soft skills, tools, etc."""
        categories = {
            'programming_languages': [],
            'frameworks': [],
            'tools': [],
            'soft_skills': [],
            'methodologies': [],
            'other': []
        }
        
        # Define category patterns
        programming_langs = {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby',
            'go', 'rust', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab'
        }
        
        frameworks = {
            'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy'
        }
        
        tools = {
            'git', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp',
            'jira', 'confluence', 'slack', 'linux', 'windows', 'macos'
        }
        
        soft_skills = {
            'leadership', 'communication', 'teamwork', 'problem-solving',
            'analytical', 'creative', 'organized', 'detail-oriented'
        }
        
        methodologies = {
            'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd'
        }
        
        for keyword in keywords:
            if keyword in programming_langs:
                categories['programming_languages'].append(keyword)
            elif keyword in frameworks:
                categories['frameworks'].append(keyword)
            elif keyword in tools:
                categories['tools'].append(keyword)
            elif keyword in soft_skills:
                categories['soft_skills'].append(keyword)
            elif keyword in methodologies:
                categories['methodologies'].append(keyword)
            else:
                categories['other'].append(keyword)
        
        return categories
    
    def _generate_suggestions(self, categorized: Dict, profile: Dict) -> List[str]:
        """Generate actionable suggestions for profile improvement"""
        suggestions = []
        
        # Programming languages
        if categorized['programming_languages']:
            langs = ', '.join(categorized['programming_languages'][:3])
            suggestions.append(
                f"Add programming languages to your skills: {langs}"
            )
        
        # Frameworks
        if categorized['frameworks']:
            frameworks = ', '.join(categorized['frameworks'][:3])
            suggestions.append(
                f"Highlight experience with frameworks: {frameworks}"
            )
        
        # Tools
        if categorized['tools']:
            tools = ', '.join(categorized['tools'][:3])
            suggestions.append(
                f"Mention tools you've used: {tools}"
            )
        
        # Soft skills
        if categorized['soft_skills']:
            skills = ', '.join(categorized['soft_skills'][:3])
            suggestions.append(
                f"Emphasize soft skills in your summary: {skills}"
            )
        
        # Methodologies
        if categorized['methodologies']:
            methods = ', '.join(categorized['methodologies'][:2])
            suggestions.append(
                f"Include methodologies you're familiar with: {methods}"
            )
        
        # General suggestions
        if not profile.get('summary'):
            suggestions.append(
                "Add a professional summary highlighting your key strengths"
            )
        
        if not profile.get('certifications'):
            suggestions.append(
                "Consider adding relevant certifications to boost credibility"
            )
        
        return suggestions
    
    def _identify_priority_skills(self, job_keywords: Counter, profile_keywords: Counter) -> List[Dict]:
        """Identify high-demand skills to prioritize learning"""
        # Find keywords that appear frequently in jobs but not in profile
        priority = []
        
        for keyword, count in job_keywords.most_common(50):
            if keyword not in profile_keywords:
                priority.append({
                    'skill': keyword,
                    'demand': count,
                    'priority': 'high' if count > 10 else 'medium' if count > 5 else 'low'
                })
        
        return priority[:15]  # Top 15 priority skills
    
    def _calculate_profile_strength(self, job_keywords: Counter, profile_keywords: Counter) -> Dict:
        """Calculate profile strength score"""
        total_job_keywords = len(job_keywords)
        matching_keywords = len(set(job_keywords.keys()) & set(profile_keywords.keys()))
        
        if total_job_keywords == 0:
            strength_score = 0
        else:
            strength_score = (matching_keywords / total_job_keywords) * 100
        
        # Categorize strength
        if strength_score >= 70:
            category = 'Excellent'
            recommendation = 'Your profile is well-optimized for these jobs'
        elif strength_score >= 50:
            category = 'Good'
            recommendation = 'Add a few more keywords to improve visibility'
        elif strength_score >= 30:
            category = 'Fair'
            recommendation = 'Consider adding more relevant skills and experience'
        else:
            category = 'Needs Improvement'
            recommendation = 'Significant profile optimization recommended'
        
        return {
            'score': round(strength_score, 1),
            'category': category,
            'matching_keywords': matching_keywords,
            'total_keywords': total_job_keywords,
            'recommendation': recommendation
        }
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a formatted report of the analysis"""
        report = []
        report.append("=" * 60)
        report.append("PROFILE OPTIMIZATION REPORT")
        report.append("=" * 60)
        
        # Profile strength
        strength = analysis['profile_strength']
        report.append(f"\nProfile Strength: {strength['score']}% ({strength['category']})")
        report.append(f"Matching Keywords: {strength['matching_keywords']}/{strength['total_keywords']}")
        report.append(f"Recommendation: {strength['recommendation']}")
        
        # Missing keywords
        report.append(f"\n\nTop Missing Keywords ({len(analysis['missing_keywords'])} total):")
        for i, keyword in enumerate(analysis['missing_keywords'][:10], 1):
            freq = analysis['keyword_frequency'][keyword]
            report.append(f"  {i}. {keyword} (appears in {freq} jobs)")
        
        # Categorized keywords
        report.append("\n\nMissing Keywords by Category:")
        for category, keywords in analysis['categorized_keywords'].items():
            if keywords:
                report.append(f"  {category.replace('_', ' ').title()}: {', '.join(keywords[:5])}")
        
        # Priority skills
        report.append("\n\nPriority Skills to Learn:")
        for i, skill in enumerate(analysis['priority_skills'][:5], 1):
            report.append(f"  {i}. {skill['skill']} - {skill['priority'].upper()} priority (demand: {skill['demand']})")
        
        # Suggestions
        report.append("\n\nActionable Suggestions:")
        for i, suggestion in enumerate(analysis['suggestions'], 1):
            report.append(f"  {i}. {suggestion}")
        
        report.append("\n" + "=" * 60)
        
        return '\n'.join(report)


# Example usage
if __name__ == "__main__":
    optimizer = ProfileOptimizer()
    
    # Test data
    test_jobs = [
        {
            'title': 'Senior Python Developer',
            'description': 'Looking for Python developer with Django, Flask, AWS experience. Strong problem-solving skills required.'
        },
        {
            'title': 'Data Scientist',
            'description': 'Machine learning, Python, TensorFlow, pandas, data analysis, communication skills'
        }
    ]
    
    test_profile = {
        'summary': 'Software developer with Java experience',
        'skills': 'Java, SQL, Git',
        'experience': 'Worked on web applications'
    }
    
    analysis = optimizer.analyze_keyword_gaps(test_jobs, test_profile)
    print(optimizer.generate_report(analysis))
