"""
AI Assistant using Groq API (Free & Fast)
Get your API key at: https://console.groq.com
"""

import os
import requests
from typing import Dict, List, Optional

class AIAssistant:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY', '')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-70b-versatile"  # Fast and powerful
        
    def _make_request(self, messages: List[Dict], temperature: float = 0.7) -> Optional[str]:
        """Make API request to Groq"""
        if not self.api_key:
            return None
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1024
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"AI API Error: {e}")
            return None
    
    def generate_cover_letter(self, job: Dict, profile: Dict) -> str:
        """Generate personalized cover letter using AI"""
        messages = [
            {
                "role": "system",
                "content": "Tu es un expert en rédaction de lettres de motivation pour stages et alternances en France. Écris des lettres professionnelles, personnalisées et convaincantes."
            },
            {
                "role": "user",
                "content": f"""Rédige une lettre de motivation pour:

Poste: {job.get('title', 'Stage')}
Entreprise: {job.get('company', 'Entreprise')}
Description: {job.get('description', '')[:500]}

Profil du candidat:
- Nom: {profile.get('first_name', '')} {profile.get('last_name', '')}
- Compétences: {profile.get('skills', 'Python, Web Development')}
- Localisation: {profile.get('location', 'Paris')}

Écris une lettre de motivation professionnelle, concise (250 mots max), et personnalisée."""
            }
        ]
        
        result = self._make_request(messages, temperature=0.8)
        return result if result else self._fallback_cover_letter(job, profile)
    
    def analyze_job_match(self, job: Dict, profile: Dict) -> Dict:
        """Analyze how well a job matches the profile using AI"""
        messages = [
            {
                "role": "system",
                "content": "Tu es un expert en recrutement. Analyse la compatibilité entre un profil et une offre d'emploi."
            },
            {
                "role": "user",
                "content": f"""Analyse cette compatibilité:

Offre:
- Titre: {job.get('title', '')}
- Description: {job.get('description', '')[:500]}

Profil:
- Compétences: {profile.get('skills', '')}
- Expérience: {profile.get('experience', 'Étudiant')}

Donne:
1. Score de compatibilité (0-100)
2. Points forts (3 max)
3. Points à améliorer (3 max)

Format: JSON avec keys: score, strengths, improvements"""
            }
        ]
        
        result = self._make_request(messages, temperature=0.3)
        
        if result:
            try:
                import json
                # Try to extract JSON from response
                if '{' in result and '}' in result:
                    json_str = result[result.find('{'):result.rfind('}')+1]
                    return json.loads(json_str)
            except:
                pass
        
        return {
            "score": 75,
            "strengths": ["Profil intéressant", "Compétences pertinentes"],
            "improvements": ["Ajouter plus d'expérience"]
        }
    
    def generate_interview_questions(self, job: Dict) -> List[str]:
        """Generate interview questions for a job using AI"""
        messages = [
            {
                "role": "system",
                "content": "Tu es un recruteur expérimenté. Génère des questions d'entretien pertinentes."
            },
            {
                "role": "user",
                "content": f"""Génère 10 questions d'entretien pour:

Poste: {job.get('title', '')}
Entreprise: {job.get('company', '')}
Description: {job.get('description', '')[:500]}

Format: Liste numérotée de questions en français."""
            }
        ]
        
        result = self._make_request(messages, temperature=0.7)
        
        if result:
            # Extract questions from numbered list
            questions = []
            for line in result.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Remove numbering
                    question = line.lstrip('0123456789.-) ').strip()
                    if question and '?' in question:
                        questions.append(question)
            return questions[:10]
        
        return self._fallback_interview_questions()
    
    def optimize_profile_keywords(self, jobs: List[Dict], profile: Dict) -> Dict:
        """Suggest profile improvements based on job requirements"""
        job_descriptions = "\n".join([f"- {j.get('title', '')}: {j.get('description', '')[:200]}" 
                                      for j in jobs[:5]])
        
        messages = [
            {
                "role": "system",
                "content": "Tu es un expert en optimisation de CV et profils professionnels."
            },
            {
                "role": "user",
                "content": f"""Analyse ces offres et suggère des améliorations de profil:

Offres recherchées:
{job_descriptions}

Profil actuel:
- Compétences: {profile.get('skills', '')}
- Expérience: {profile.get('experience', '')}

Suggère:
1. 5 mots-clés à ajouter
2. 3 compétences à développer
3. 2 certifications recommandées

Format: JSON avec keys: keywords, skills, certifications"""
            }
        ]
        
        result = self._make_request(messages, temperature=0.5)
        
        if result:
            try:
                import json
                if '{' in result and '}' in result:
                    json_str = result[result.find('{'):result.rfind('}')+1]
                    return json.loads(json_str)
            except:
                pass
        
        return {
            "keywords": ["Python", "JavaScript", "React", "SQL", "Git"],
            "skills": ["Cloud Computing", "DevOps", "Agile"],
            "certifications": ["AWS Certified", "Google Cloud"]
        }
    
    def _fallback_cover_letter(self, job: Dict, profile: Dict) -> str:
        """Fallback cover letter when AI is unavailable"""
        return f"""Madame, Monsieur,

Je me permets de vous adresser ma candidature pour le poste de {job.get('title', 'stage')} au sein de {job.get('company', 'votre entreprise')}.

Actuellement étudiant(e) et passionné(e) par {profile.get('skills', 'le développement')}, je suis convaincu(e) que mes compétences correspondent parfaitement à vos attentes.

Mon parcours m'a permis de développer des compétences en {profile.get('skills', 'programmation et développement web')}, qui seront des atouts pour contribuer efficacement à vos projets.

Je serais ravi(e) de vous rencontrer pour discuter de ma candidature.

Cordialement,
{profile.get('first_name', '')} {profile.get('last_name', '')}"""
    
    def _fallback_interview_questions(self) -> List[str]:
        """Fallback interview questions"""
        return [
            "Parlez-moi de vous et de votre parcours.",
            "Pourquoi souhaitez-vous rejoindre notre entreprise?",
            "Quelles sont vos principales compétences techniques?",
            "Décrivez un projet dont vous êtes fier.",
            "Comment gérez-vous le travail en équipe?",
            "Quels sont vos objectifs de carrière?",
            "Comment vous tenez-vous informé des nouvelles technologies?",
            "Parlez-moi d'une difficulté que vous avez surmontée.",
            "Pourquoi ce domaine vous intéresse-t-il?",
            "Avez-vous des questions sur le poste ou l'entreprise?"
        ]
