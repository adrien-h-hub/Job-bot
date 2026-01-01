"""
Interview Preparation Assistant - Comprehensive interview prep system
"""

import os
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup


class InterviewPrep:
    """Prepare for job interviews with company research and practice questions"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize interview prep assistant
        
        Args:
            api_key: OpenAI API key for AI-generated answers
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                pass
        
        # Common interview questions by category
        self.question_bank = {
            'behavioral': [
                "Tell me about yourself",
                "What are your greatest strengths?",
                "What are your weaknesses?",
                "Why do you want to work here?",
                "Where do you see yourself in 5 years?",
                "Tell me about a time you faced a challenge",
                "Describe a time you showed leadership",
                "How do you handle conflict?",
                "What motivates you?",
                "Why are you leaving your current job?"
            ],
            'technical': [
                "Explain your most complex project",
                "How do you approach problem-solving?",
                "What's your development process?",
                "How do you ensure code quality?",
                "Describe your experience with [technology]",
                "How do you stay updated with technology?",
                "Walk me through your technical decision-making",
                "How do you handle technical debt?",
                "Explain a technical challenge you overcame",
                "What's your testing strategy?"
            ],
            'situational': [
                "How would you handle a tight deadline?",
                "What would you do if you disagreed with your manager?",
                "How do you prioritize tasks?",
                "How would you handle an underperforming team member?",
                "What would you do if you made a mistake?",
                "How do you handle multiple priorities?",
                "How would you approach learning a new technology?",
                "What would you do if a project was failing?",
                "How do you handle feedback?",
                "How would you deal with a difficult stakeholder?"
            ],
            'company_specific': [
                "Why do you want to work at [Company]?",
                "What do you know about our company?",
                "How would you contribute to our team?",
                "What interests you about this role?",
                "How do your values align with ours?",
                "What do you think about our products/services?",
                "How would you improve our [product/service]?",
                "What challenges do you think we face?",
                "Why should we hire you?",
                "What questions do you have for us?"
            ]
        }
    
    def prepare_for_interview(self, job: Dict, company: str, profile: Dict) -> Dict:
        """
        Generate comprehensive interview prep package
        
        Args:
            job: Job details
            company: Company name
            profile: User profile
            
        Returns:
            Dict with company research, questions, answers, and tips
        """
        prep_package = {
            'company_research': self._research_company(company),
            'common_questions': self._get_relevant_questions(job),
            'suggested_answers': self._generate_answers(job, profile),
            'questions_to_ask': self._suggest_questions_to_ask(company, job),
            'salary_data': self._get_salary_range(job),
            'interview_tips': self._get_interview_tips(job),
            'follow_up_template': self._create_follow_up_template(job, company)
        }
        
        return prep_package
    
    def _research_company(self, company: str) -> Dict:
        """
        Compile company information from various sources
        
        Args:
            company: Company name
            
        Returns:
            Dict with company information
        """
        research = {
            'about': f"Research {company} on their website and LinkedIn",
            'mission': "Check company mission statement",
            'values': "Review company values and culture",
            'recent_news': "Search for recent news articles",
            'products': "Understand their main products/services",
            'competitors': "Know their main competitors",
            'size': "Company size and locations",
            'leadership': "Key executives and leadership team"
        }
        
        # Try to scrape basic info (simplified)
        try:
            # This is a placeholder - real implementation would scrape company website
            research['scraped_info'] = f"Visit {company}'s website for detailed information"
        except Exception as e:
            research['error'] = str(e)
        
        return research
    
    def _get_relevant_questions(self, job: Dict) -> Dict:
        """Get questions relevant to the job role"""
        role_type = self._classify_role(job.get('title', ''))
        
        questions = {
            'behavioral': self.question_bank['behavioral'][:5],
            'technical': self.question_bank['technical'][:5],
            'situational': self.question_bank['situational'][:5],
            'company_specific': self.question_bank['company_specific'][:5]
        }
        
        # Add role-specific questions
        if role_type == 'technical':
            questions['role_specific'] = [
                f"Explain your experience with {job.get('title', 'this role')}",
                "What's your approach to code reviews?",
                "How do you handle production issues?",
                "Describe your ideal development environment"
            ]
        elif role_type == 'management':
            questions['role_specific'] = [
                "What's your management style?",
                "How do you motivate your team?",
                "How do you handle performance issues?",
                "Describe a successful project you led"
            ]
        
        return questions
    
    def _classify_role(self, title: str) -> str:
        """Classify role type from title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['developer', 'engineer', 'programmer']):
            return 'technical'
        elif any(word in title_lower for word in ['manager', 'director', 'lead']):
            return 'management'
        elif any(word in title_lower for word in ['analyst', 'scientist']):
            return 'analytical'
        else:
            return 'general'
    
    def _generate_answers(self, job: Dict, profile: Dict) -> List[Dict]:
        """Generate suggested answers using STAR method"""
        answers = []
        
        # Example STAR answer template
        star_template = {
            'question': "Tell me about a time you faced a challenge",
            'situation': f"In my role as {profile.get('current_role', 'professional')}...",
            'task': "I was responsible for...",
            'action': "I took the following steps...",
            'result': "As a result, we achieved..."
        }
        
        if self.client:
            # Use AI to generate personalized answers
            answers = self._generate_ai_answers(job, profile)
        else:
            # Use template answers
            answers = [
                {
                    'question': "Tell me about yourself",
                    'answer': f"I'm a {profile.get('current_role', 'professional')} with {profile.get('years_experience', 'several')} years of experience in {profile.get('field', 'the industry')}. I specialize in {profile.get('skills', 'various areas')} and have a track record of {profile.get('achievements', 'success')}."
                },
                {
                    'question': "Why do you want this role?",
                    'answer': f"I'm excited about this {job.get('title', 'position')} because it aligns perfectly with my skills in {profile.get('skills', 'key areas')} and offers the opportunity to {profile.get('career_goal', 'grow and contribute')}."
                }
            ]
        
        return answers
    
    def _generate_ai_answers(self, job: Dict, profile: Dict) -> List[Dict]:
        """Generate AI-powered interview answers"""
        try:
            prompt = f"""Generate 5 strong interview answers using the STAR method for:

Job: {job.get('title')} at {job.get('company')}
Candidate: {profile.get('current_role')} with {profile.get('years_experience')} years experience
Skills: {profile.get('skills')}

Questions:
1. Tell me about yourself
2. Why do you want this role?
3. Describe a challenging project
4. What's your greatest strength?
5. Where do you see yourself in 5 years?

Format each answer with Situation, Task, Action, Result."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            # Parse response (simplified)
            return [{'answer': response.choices[0].message.content}]
        except:
            return []
    
    def _suggest_questions_to_ask(self, company: str, job: Dict) -> List[str]:
        """Suggest intelligent questions to ask the interviewer"""
        questions = [
            f"What does success look like in this {job.get('title', 'role')} after 6 months?",
            "What are the biggest challenges facing the team right now?",
            "How does this role contribute to the company's goals?",
            "What's the team structure and who would I be working with?",
            "What opportunities are there for professional development?",
            f"What do you enjoy most about working at {company}?",
            "What's the onboarding process like?",
            "How do you measure performance in this role?",
            "What's the company culture like?",
            "What are the next steps in the interview process?"
        ]
        
        return questions
    
    def _get_salary_range(self, job: Dict) -> Dict:
        """Get salary range for the position"""
        return {
            'market_range': 'Research on Glassdoor, Levels.fyi, Payscale',
            'negotiation_tip': 'Let them make the first offer',
            'factors': ['Experience level', 'Location', 'Company size', 'Industry']
        }
    
    def _get_interview_tips(self, job: Dict) -> List[str]:
        """Get interview tips specific to the role"""
        tips = [
            "Research the company thoroughly before the interview",
            "Prepare 2-3 examples for each common question using STAR method",
            "Dress professionally and arrive 10 minutes early",
            "Bring copies of your resume and a notepad",
            "Practice your answers out loud beforehand",
            "Prepare thoughtful questions to ask the interviewer",
            "Follow up with a thank-you email within 24 hours",
            "Be ready to discuss your salary expectations",
            "Show enthusiasm and genuine interest in the role",
            "Turn off your phone before the interview"
        ]
        
        role_type = self._classify_role(job.get('title', ''))
        
        if role_type == 'technical':
            tips.extend([
                "Be prepared for technical questions or coding challenges",
                "Review fundamental concepts in your tech stack",
                "Bring a portfolio or examples of your work"
            ])
        
        return tips
    
    def _create_follow_up_template(self, job: Dict, company: str) -> str:
        """Create thank-you email template"""
        template = f"""Subject: Thank you - {job.get('title', 'Position')} Interview

Dear [Interviewer Name],

Thank you for taking the time to meet with me today to discuss the {job.get('title', 'position')} role at {company}. I enjoyed learning more about the team and the exciting projects you're working on.

Our conversation reinforced my enthusiasm for this opportunity. I'm particularly excited about [specific aspect discussed in interview], and I believe my experience with [relevant skill/experience] would allow me to contribute meaningfully to your team.

Please don't hesitate to reach out if you need any additional information. I look forward to hearing about the next steps in the process.

Thank you again for your time and consideration.

Best regards,
[Your Name]"""
        
        return template
    
    def generate_report(self, prep_package: Dict) -> str:
        """Generate formatted interview prep report"""
        report = []
        report.append("=" * 70)
        report.append("INTERVIEW PREPARATION GUIDE")
        report.append("=" * 70)
        
        # Company Research
        report.append("\n📊 COMPANY RESEARCH")
        report.append("-" * 70)
        for key, value in prep_package['company_research'].items():
            report.append(f"  {key.title()}: {value}")
        
        # Common Questions
        report.append("\n❓ COMMON INTERVIEW QUESTIONS")
        report.append("-" * 70)
        for category, questions in prep_package['common_questions'].items():
            report.append(f"\n  {category.upper().replace('_', ' ')}:")
            for i, q in enumerate(questions, 1):
                report.append(f"    {i}. {q}")
        
        # Questions to Ask
        report.append("\n🤔 QUESTIONS TO ASK THE INTERVIEWER")
        report.append("-" * 70)
        for i, q in enumerate(prep_package['questions_to_ask'], 1):
            report.append(f"  {i}. {q}")
        
        # Interview Tips
        report.append("\n💡 INTERVIEW TIPS")
        report.append("-" * 70)
        for tip in prep_package['interview_tips']:
            report.append(f"  • {tip}")
        
        # Follow-up Template
        report.append("\n📧 THANK-YOU EMAIL TEMPLATE")
        report.append("-" * 70)
        report.append(prep_package['follow_up_template'])
        
        report.append("\n" + "=" * 70)
        report.append("Good luck with your interview! 🍀")
        report.append("=" * 70)
        
        return '\n'.join(report)


# Example usage
if __name__ == "__main__":
    prep = InterviewPrep()
    
    test_job = {
        'title': 'Senior Python Developer',
        'company': 'Tech Innovations Inc',
        'description': 'Looking for experienced Python developer...'
    }
    
    test_profile = {
        'current_role': 'Python Developer',
        'years_experience': 5,
        'skills': 'Python, Django, AWS',
        'field': 'software development',
        'achievements': 'Led 3 major projects'
    }
    
    print("Interview Preparation Assistant - Test Mode")
    print("=" * 70)
    
    package = prep.prepare_for_interview(test_job, 'Tech Innovations Inc', test_profile)
    print(prep.generate_report(package))
