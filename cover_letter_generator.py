"""
AI Cover Letter Generator - Generate personalized cover letters using GPT
"""

import os
from typing import Dict, Optional
from datetime import datetime


class CoverLetterGenerator:
    """Generate AI-powered cover letters for job applications"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize cover letter generator
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: Model to use (gpt-4, gpt-3.5-turbo, claude-3, etc.)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.client = None
        
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                print("⚠️ OpenAI package not installed. Run: pip install openai")
    
    def generate(self, job: Dict, profile: Dict, style: str = 'professional') -> str:
        """
        Generate personalized cover letter
        
        Args:
            job: Job dictionary with title, company, description
            profile: User profile with experience, skills, etc.
            style: Writing style (professional, enthusiastic, technical, creative)
            
        Returns:
            Generated cover letter text
        """
        if not self.client:
            return self._generate_template_letter(job, profile)
        
        prompt = self._build_prompt(job, profile, style)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert career coach and professional writer specializing in compelling cover letters."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            letter = response.choices[0].message.content
            return letter
            
        except Exception as e:
            print(f"❌ AI generation error: {e}")
            return self._generate_template_letter(job, profile)
    
    def _build_prompt(self, job: Dict, profile: Dict, style: str) -> str:
        """Build prompt for AI model"""
        style_instructions = {
            'professional': 'Write in a formal, professional tone. Be concise and focus on qualifications.',
            'enthusiastic': 'Write with enthusiasm and passion. Show genuine excitement about the opportunity.',
            'technical': 'Focus on technical skills and achievements. Use industry terminology.',
            'creative': 'Be creative and engaging. Stand out while remaining professional.'
        }
        
        instruction = style_instructions.get(style, style_instructions['professional'])
        
        prompt = f"""Write a compelling cover letter for the following job application:

JOB DETAILS:
- Position: {job.get('title', 'N/A')}
- Company: {job.get('company', 'N/A')}
- Location: {job.get('location', 'N/A')}
- Description: {job.get('description', 'N/A')[:500]}

CANDIDATE PROFILE:
- Name: {profile.get('first_name', '')} {profile.get('last_name', '')}
- Current Role: {profile.get('current_role', 'Professional')}
- Experience: {profile.get('years_experience', 'Several')} years
- Key Skills: {profile.get('skills', 'Various technical skills')}
- Education: {profile.get('education', 'Relevant degree')}
- Notable Achievements: {profile.get('achievements', 'Strong track record of success')}

STYLE: {instruction}

REQUIREMENTS:
1. Keep it under 300 words
2. Include specific examples from the candidate's experience
3. Show understanding of the company and role
4. Explain why the candidate is a great fit
5. End with a strong call to action
6. Use proper business letter format
7. Be genuine and avoid clichés

Generate the cover letter now:"""
        
        return prompt
    
    def _generate_template_letter(self, job: Dict, profile: Dict) -> str:
        """Generate template-based cover letter (fallback)"""
        today = datetime.now().strftime('%B %d, %Y')
        
        letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job.get('title', 'position')} role at {job.get('company', 'your company')}. With {profile.get('years_experience', 'several')} years of experience in {profile.get('field', 'the industry')} and a proven track record of {profile.get('achievements', 'delivering results')}, I am confident I would be a valuable addition to your team.

In my current role as {profile.get('current_role', 'a professional')}, I have developed expertise in {profile.get('skills', 'key areas')} that directly align with the requirements of this position. I am particularly drawn to this opportunity because {job.get('company', 'your company')} is known for {profile.get('company_interest', 'innovation and excellence')}.

My key qualifications include:
• {profile.get('qualification_1', 'Strong technical skills and problem-solving abilities')}
• {profile.get('qualification_2', 'Proven track record of successful project delivery')}
• {profile.get('qualification_3', 'Excellent communication and teamwork skills')}

I am excited about the possibility of contributing to {job.get('company', 'your team')} and would welcome the opportunity to discuss how my background and skills would benefit your organization.

Thank you for considering my application. I look forward to speaking with you soon.

Sincerely,
{profile.get('first_name', '')} {profile.get('last_name', '')}
{profile.get('email', '')}
{profile.get('phone', '')}"""
        
        return letter
    
    def generate_multiple_versions(self, job: Dict, profile: Dict, 
                                   count: int = 3) -> list[str]:
        """
        Generate multiple versions for A/B testing
        
        Args:
            job: Job details
            profile: User profile
            count: Number of versions to generate
            
        Returns:
            List of cover letter variations
        """
        styles = ['professional', 'enthusiastic', 'technical', 'creative']
        letters = []
        
        for i in range(count):
            style = styles[i % len(styles)]
            letter = self.generate(job, profile, style)
            letters.append({
                'version': i + 1,
                'style': style,
                'content': letter
            })
        
        return letters
    
    def save_letter(self, letter: str, job: Dict, filepath: Optional[str] = None) -> str:
        """
        Save cover letter to file
        
        Args:
            letter: Cover letter text
            job: Job details
            filepath: Optional custom filepath
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            company = job.get('company', 'Company').replace(' ', '_')
            title = job.get('title', 'Position').replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d')
            filepath = f"cover_letter_{company}_{title}_{timestamp}.txt"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(letter)
            print(f"✅ Cover letter saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving cover letter: {e}")
            return ""
    
    def customize_for_company(self, base_letter: str, company_research: Dict) -> str:
        """
        Customize letter with company-specific information
        
        Args:
            base_letter: Base cover letter
            company_research: Company information (values, recent news, culture)
            
        Returns:
            Customized cover letter
        """
        if not self.client:
            return base_letter
        
        prompt = f"""Enhance this cover letter by incorporating specific company information:

ORIGINAL LETTER:
{base_letter}

COMPANY INFORMATION:
- Values: {company_research.get('values', 'N/A')}
- Recent News: {company_research.get('news', 'N/A')}
- Culture: {company_research.get('culture', 'N/A')}
- Mission: {company_research.get('mission', 'N/A')}

Add 1-2 sentences that show you've researched the company and understand their values/mission. Keep the same length and tone.

Enhanced letter:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Customization error: {e}")
            return base_letter


# Example usage
if __name__ == "__main__":
    generator = CoverLetterGenerator()
    
    test_job = {
        'title': 'Senior Python Developer',
        'company': 'Tech Innovations Inc',
        'location': 'Paris, France',
        'description': 'We are seeking an experienced Python developer to join our team...'
    }
    
    test_profile = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+33 6 12 34 56 78',
        'current_role': 'Python Developer',
        'years_experience': 5,
        'skills': 'Python, Django, AWS, Docker',
        'education': 'Master in Computer Science',
        'achievements': 'Led development of 3 major projects'
    }
    
    print("Cover Letter Generator - Test Mode")
    print("=" * 60)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️ OPENAI_API_KEY not set - using template mode")
        print("\nTo use AI generation:")
        print("1. Get API key from https://platform.openai.com")
        print("2. Set environment variable: OPENAI_API_KEY=your-key")
        print("3. Install: pip install openai")
    
    print("\nGenerating cover letter...")
    letter = generator.generate(test_job, test_profile, style='professional')
    
    print("\n" + "=" * 60)
    print("GENERATED COVER LETTER")
    print("=" * 60)
    print(letter)
    print("=" * 60)
