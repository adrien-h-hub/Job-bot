"""
Response Handler - Manages different types of responses and follow-ups
"""

import re
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from email_finder import EmailFinder

class ResponseHandler:
    def __init__(self, job_data: Dict, user_profile: Dict):
        self.job_data = job_data
        self.user_profile = user_profile
        self.company_name = job_data.get('company', '')
        self.job_title = job_data.get('title', '')
        self.response_plan = []
    
    def analyze_response(self, email_text: str) -> Dict:
        """
        Analyze the response email and determine the appropriate action
        Returns: {
            'action': 'follow_up'|'send_info'|'schedule_interview'|'rejection'|'unknown',
            'confidence': float (0-1),
            'next_steps': List[str],
            'suggested_response': str
        }
        """
        email_text = email_text.lower()
        
        # Check for common positive responses
        positive_indicators = [
            'intéressé', 'intéressée', 'intéressant', 'souhaitez-vous', 'disponible',
            'entretien', 'rencontrer', 'convoquer', 'disponibilité', 'parler',
            'téléphone', 'appel', 'zoom', 'teams', 'meet', 'visio',
            'expérience', 'cv', 'curriculum vitae', 'parcours',
            'poste', 'mission', 'profil', 'candidature'
        ]
        
        # Check for negative responses
        negative_indicators = [
            'ne correspond pas', 'pas retenu', 'pas sélectionné', 'malheureusement',
            'candidature retenue', 'poste pourvu', 'plus avancer', 'ne correspond pas',
            'pas le profil', 'pas d\'opportunité', 'pas d\'ouverture', 'pas de poste',
            'rester en contact', 'prochaine opportunité', 'candidature future',
            'refus', 'refuser', 'décliné', 'décliner', 'refusé'
        ]
        
        # Check for information requests
        info_requests = [
            'plus d\'information', 'plus de détails', 'précision', 'préciser',
            'questions', 'renseignement', 'savoir plus', 'en savoir plus',
            'disponible', 'expérience', 'compétence', 'formation', 'diplôme',
            'rémunération', 'salaire', 'prétention salariale', 'prétention',
            'début', 'disponibilité', 'mobile', 'télétravail', 'présentiel',
            'permis', 'véhicule', 'déplacement', 'mobilité'
        ]
        
        # Calculate scores
        positive_score = sum(1 for word in positive_indicators if word in email_text)
        negative_score = sum(1 for word in negative_indicators if word in email_text)
        info_score = sum(1 for word in info_requests if word in email_text)
        
        # Determine the most likely action
        if positive_score > 0 and positive_score > negative_score:
            if any(word in email_text for word in ['entretien', 'rencontre', 'rencontrer', 'disponible']):
                return self._handle_interview_request()
            return self._handle_positive_response()
        
        elif negative_score > 0:
            return self._handle_rejection()
        
        elif info_score > 2:
            return self._handle_information_request()
        
        else:
            return self._handle_unknown_response()
    
    def _handle_interview_request(self) -> Dict:
        """Handle interview scheduling requests"""
        # Try to find the best contact for scheduling
        contacts = self._find_company_contacts()
        
        response = {
            'action': 'schedule_interview',
            'confidence': 0.9,
            'next_steps': [
                'Confirm availability for interview',
                'Prepare questions about the role and company',
                'Research the interviewers (if provided)'
            ],
            'suggested_response': self._generate_interview_response(contacts)
        }
        
        if contacts:
            response['contacts'] = contacts
        
        return response
    
    def _handle_positive_response(self) -> Dict:
        """Handle positive but non-interview responses"""
        return {
            'action': 'follow_up',
            'confidence': 0.8,
            'next_steps': [
                'Send a thank you email',
                'Follow up on next steps',
                'Prepare additional information about your experience'
            ],
            'suggested_response': self._generate_follow_up_response()
        }
    
    def _handle_rejection(self) -> Dict:
        """Handle rejection emails"""
        return {
            'action': 'rejection',
            'confidence': 0.85,
            'next_steps': [
                'Send a polite thank you email',
                'Ask for feedback on your application',
                'Request to be considered for future opportunities'
            ],
            'suggested_response': self._generate_rejection_response()
        }
    
    def _handle_information_request(self) -> Dict:
        """Handle requests for more information"""
        return {
            'action': 'send_info',
            'confidence': 0.9,
            'next_steps': [
                'Prepare detailed information about the requested topics',
                'Update your resume or portfolio if needed',
                'Follow up after sending the information'
            ],
            'suggested_response': self._generate_info_response()
        }
    
    def _handle_unknown_response(self) -> Dict:
        """Handle unrecognized responses"""
        return {
            'action': 'unknown',
            'confidence': 0.5,
            'next_steps': [
                'Review the email carefully',
                'Consider forwarding to a human for review',
                'Prepare a polite request for clarification'
            ],
            'suggested_response': self._generate_generic_response()
        }
    
    def _find_company_contacts(self) -> List[Dict]:
        """Find relevant contacts at the company"""
        finder = EmailFinder(company_name=self.company_name)
        contacts = []
        
        # Try to find RHE (Responsable Hygiène et Sécurité)
        rhe = finder.find_rhe_contact()
        if rhe:
            contacts.append(rhe)
        
        # Try to find Site Manager/Chef de Chantier
        site_manager = finder.find_site_manager_contact()
        if site_manager:
            contacts.append(site_manager)
        
        return contacts
    
    def _generate_interview_response(self, contacts: List[Dict] = None) -> str:
        """Generate a response to an interview request"""
        salutations = [
            f"Bonjour,\n\n",
            f"Madame, Monsieur,\n\n",
            f"Bonjour à vous,\n\n"
        ]
        
        # Add contact name if available
        if contacts and len(contacts) > 0:
            contact = contacts[0]
            salutation = f"Bonjour {contact.get('name', '').split(' ')[0] if contact.get('name') else ''},\n\n"
        else:
            salutation = random.choice(salutations)
        
        # Generate available times
        today = datetime.now()
        time_slots = [
            (today + timedelta(days=2)).strftime("lundi %d/%m entre 9h et 12h"),
            (today + timedelta(days=3)).strftime("mardi %d/%m entre 14h et 17h"),
            (today + timedelta(days=4)).strftime("mercredi %d/%m entre 10h et 16h"),
            (today + timedelta(days=5)).strftime("jeudi %d/%m entre 9h et 18h")
        ]
        
        selected_slots = random.sample(time_slots, 2)
        
        response = f"""{salutation}Je vous remercie pour votre retour concernant ma candidature pour le poste de {self.job_title}.

Je suis disponible pour un entretien aux créneaux suivants :
- {selected_slots[0]}
- {selected_slots[1]}

N'hésitez pas à me proposer d'autres créneaux si ceux-ci ne vous conviennent pas.

Je reste à votre disposition pour tout complément d'information.

Cordialement,
{self.user_profile.get('first_name', '')} {self.user_profile.get('last_name', '')}
{self.user_profile.get('phone', '')}
{self.user_profile.get('email', '')}
"""
        return response
    
    def _generate_follow_up_response(self) -> str:
        """Generate a follow-up response"""
        return f"""Bonjour,

Je vous remercie pour votre retour concernant ma candidature pour le poste de {self.job_title}.

Je me tiens à votre disposition pour toute information complémentaire concernant mon profil ou mon expérience.

Dans l'attente de votre retour, je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.

{self.user_profile.get('first_name', '')} {self.user_profile.get('last_name', '')}
{self.user_profile.get('phone', '')}
{self.user_profile.get('email', '')}
"""
    
    def _generate_rejection_response(self) -> str:
        """Generate a response to a rejection"""
        return f"""Bonjour,

Je vous remercie d'avoir pris le temps d'examiner ma candidature pour le poste de {self.job_title}.

Bien que déçu de ne pas être retenu pour ce poste, je reste intéressé par les opportunités futures au sein de votre entreprise. Je vous serais reconnaissant de bien vouloir me faire part des raisons de cette décision, afin que je puisse améliorer ma candidature pour de futures opportunités.

Je vous remercie par avance pour votre retour et vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.

{self.user_profile.get('first_name', '')} {self.user_profile.get('last_name', '')}
{self.user_profile.get('email', '')}
"""
    
    def _generate_info_response(self) -> str:
        """Generate a response to an information request"""
        return f"""Bonjour,

Je vous remercie pour votre intérêt pour ma candidature au poste de {self.job_title}.

Je me permets de vous transmettre les informations complémentaires suivantes concernant mon profil :

- [Détails sur l'expérience pertinente]
- [Informations sur les compétences demandées]
- [Disponibilités]
- [Prétentions salariales si demandées]

Je reste à votre disposition pour toute information complémentaire ou pour échanger plus en détail sur cette opportunité.

Cordialement,
{self.user_profile.get('first_name', '')} {self.user_profile.get('last_name', '')}
{self.user_profile.get('phone', '')}
{self.user_profile.get('email', '')}
"""
    
    def _generate_generic_response(self) -> str:
        """Generate a generic response for unknown email types"""
        return f"""Bonjour,

Je vous remercie pour votre message concernant ma candidature pour le poste de {self.job_title}.

Je vous prie de bien vouloir m'excuser, mais je souhaiterais obtenir des précisions sur votre demande afin de pouvoir y répondre de la manière la plus appropriée.

Je reste à votre disposition pour tout complément d'information.

Cordialement,
{self.user_profile.get('first_name', '')} {self.user_profile.get('last_name', '')}
{self.user_profile.get('phone', '')}
{self.user_profile.get('email', '')}
"""
