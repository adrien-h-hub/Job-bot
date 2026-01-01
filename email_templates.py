"""
Email Templates - Predefined email templates for different response types
"""

from typing import Dict, Optional
from datetime import datetime

class EmailTemplates:
    """Collection of email templates for different response types"""
    
    @staticmethod
    def get_template(template_name: str, context: Dict) -> Dict[str, str]:
        """
        Get an email template by name with the given context
        
        Args:
            template_name: Name of the template to retrieve
            context: Dictionary with values to fill in the template
            
        Returns:
            Dict with 'subject' and 'body' keys
        """
        template_method = getattr(EmailTemplates, f"_{template_name}", None)
        if not template_method or not callable(template_method):
            raise ValueError(f"Template '{template_name}' not found")
            
        return template_method(context)
    
    @staticmethod
    def _interview_request(context: Dict) -> Dict[str, str]:
        """Template for responding to interview requests"""
        subject = f"Disponibilités pour entretien - {context.get('job_title', 'Candidature')}"
        
        body = f"""Bonjour {contact_name},

Je vous remercie pour votre retour concernant ma candidature pour le poste de {job_title}.

Je suis disponible pour un entretien aux créneaux suivants :
- {available_slot_1}
- {available_slot_2}

N'hésitez pas à me proposer d'autres créneaux si ceux-ci ne vous conviennent pas.

Je reste à votre disposition pour tout complément d'information.

Cordialement,
{first_name} {last_name}
{phone}
{email}
""".format(
            contact_name=context.get('contact_name', ''),
            job_title=context.get('job_title', ''),
            available_slot_1=context.get('available_slots', ['', ''])[0],
            available_slot_2=context.get('available_slots', ['', ''])[1],
            first_name=context.get('first_name', ''),
            last_name=context.get('last_name', ''),
            phone=context.get('phone', ''),
            email=context.get('email', '')
        )
        
        return {'subject': subject, 'body': body}
    
    @staticmethod
    def _follow_up(context: Dict) -> Dict[str, str]:
        """Template for follow-up emails"""
        subject = f"Suite à ma candidature - {context.get('job_title', 'Poste')}"
        
        body = f"""Bonjour {contact_name},

Je me permets de faire un suivi concernant ma candidature pour le poste de {job_title} que j'ai soumise le {application_date}.

Je reste très intéressé(e) par cette opportunité et je me tenais à votre disposition pour toute information complémentaire concernant mon profil ou pour programmer un entretien.

Je vous remercie par avance pour le temps que vous accorderez à ma demande et vous prie d'agréer, {contact_title}, mes salutations distinguées.

{first_name} {last_name}
{phone}
{email}
""".format(
            contact_name=context.get('contact_name', ''),
            contact_title='Madame, Monsieur' if not context.get('contact_name') else '',
            job_title=context.get('job_title', ''),
            application_date=context.get('application_date', datetime.now().strftime('%d/%m/%Y')),
            first_name=context.get('first_name', ''),
            last_name=context.get('last_name', ''),
            phone=context.get('phone', ''),
            email=context.get('email', '')
        )
        
        return {'subject': subject, 'body': body}
    
    @staticmethod
    def _information_request(context: Dict) -> Dict[str, str]:
        """Template for responding to information requests"""
        subject = f"Informations complémentaires - {context.get('job_title', 'Candidature')}"
        
        body = f"""Bonjour {contact_name},

Je vous remercie pour votre retour concernant ma candidature pour le poste de {job_title}.

Comme demandé, je me permets de vous transmettre les informations complémentaires suivantes :

{additional_info}

Je reste à votre disposition pour tout complément d'information ou pour échanger plus en détail sur cette opportunité.

Cordialement,
{first_name} {last_name}
{phone}
{email}
""".format(
            contact_name=context.get('contact_name', ''),
            job_title=context.get('job_title', ''),
            additional_info=context.get('additional_info', ''),
            first_name=context.get('first_name', ''),
            last_name=context.get('last_name', ''),
            phone=context.get('phone', ''),
            email=context.get('email', '')
        )
        
        return {'subject': subject, 'body': body}
    
    @staticmethod
    def _thank_you(context: Dict) -> Dict[str, str]:
        """Template for thank you emails after interviews"""
        subject = f"Remerciements - Entretien du {context.get('interview_date', '')} - {context.get('job_title', '')}"
        
        body = f"""Bonjour {contact_name},

Je tenais à vous remercier pour l'entretien que j'ai eu {interview_date} concernant le poste de {job_title}.

J'ai particulièrement apprécié notre échange et les informations que vous m'avez transmises sur {company_name} et les missions du poste. Cette opportunité correspond parfaitement à mes aspirations professionnelles et à mes compétences en {key_skill_1} et {key_skill_2}.

Je réitère tout mon vif intérêt pour ce poste et reste à votre entière disposition pour tout complément d'information.

Je vous remercie à nouveau pour votre accueil et votre confiance, et je reste dans l'attente de votre retour.

Bien cordialement,
{first_name} {last_name}
{phone}
{email}
""".format(
            contact_name=context.get('contact_name', ''),
            interview_date=context.get('interview_date', ''),
            job_title=context.get('job_title', ''),
            company_name=context.get('company_name', 'votre entreprise'),
            key_skill_1=context.get('key_skills', ['', ''])[0],
            key_skill_2=context.get('key_skills', ['', ''])[1],
            first_name=context.get('first_name', ''),
            last_name=context.get('last_name', ''),
            phone=context.get('phone', ''),
            email=context.get('email', '')
        )
        
        return {'subject': subject, 'body': body}
    
    @staticmethod
    def _status_update(context: Dict) -> Dict[str, str]:
        """Template for status update requests"""
        subject = f"Demande de mise à jour - Candidature {context.get('job_title', '')}"
        
        body = f"""Bonjour {contact_name},

Je me permets de vous contacter concernant l'état d'avancement du processus de recrutement pour le poste de {job_title} pour lequel j'ai postulé le {application_date}.

Je reste très intéressé(e) par cette opportunité et j'aimerais savoir s'il y a eu des évolutions récentes concernant ma candidature.

Je vous remercie par avance pour votre retour et reste à votre disposition pour tout complément d'information.

Cordialement,
{first_name} {last_name}
{phone}
{email}
""".format(
            contact_name=context.get('contact_name', ''),
            job_title=context.get('job_title', ''),
            application_date=context.get('application_date', datetime.now().strftime('%d/%m/%Y')),
            first_name=context.get('first_name', ''),
            last_name=context.get('last_name', ''),
            phone=context.get('phone', ''),
            email=context.get('email', '')
        )
        
        return {'subject': subject, 'body': body}
    
    @staticmethod
    def _withdrawal(context: Dict) -> Dict[str, str]:
        """Template for withdrawing an application"""
        subject = f"Retrait de candidature - {context.get('job_title', '')}"
        
        body = f"""Bonjour {contact_name},

Je vous écris pour vous informer que je souhaite retirer ma candidature pour le poste de {job_title}.

{reason}

Je tiens à vous remercier pour le temps que vous avez accordé à l'examen de mon dossier et pour l'opportunité qui m'a été donnée de postuler à ce poste.

Je vous prie d'agréer, {contact_title}, mes salutations distinguées.

{first_name} {last_name}
{email}
""".format(
            contact_name=context.get('contact_name', ''),
            contact_title='Madame, Monsieur' if not context.get('contact_name') else '',
            job_title=context.get('job_title', ''),
            reason=context.get('reason', 'Cette décision a été prise après mûre réflexion.'),
            first_name=context.get('first_name', ''),
            last_name=context.get('last_name', ''),
            email=context.get('email', '')
        )
        
        return {'subject': subject, 'body': body}
    
    @staticmethod
    def _rejection_response(context: Dict) -> Dict[str, str]:
        """Template for responding to rejection emails"""
        subject = f"Suite à votre retour - Candidature {context.get('job_title', '')}"
        
        body = f"""Bonjour {contact_name},

Je vous remercie d'avoir pris le temps d'examiner ma candidature pour le poste de {job_title}.

Bien que déçu(e) de ne pas être retenu(e) pour ce poste, je tiens à vous remercier pour l'opportunité qui m'a été donnée de postuler et pour la qualité des échanges que nous avons eus.

{feedback_request}

Je reste intéressé(e) par les opportunités futures au sein de {company_name} et vous remercie à nouveau pour votre considération.

Cordialement,
{first_name} {last_name}
{email}
""".format(
            contact_name=context.get('contact_name', ''),
            job_title=context.get('job_title', ''),
            feedback_request=context.get('feedback_request', 'Je serais très intéressé(e) par un retour sur ma candidature qui me permettrait d\'améliorer mes futures démarches.') if context.get('request_feedback', True) else '',
            company_name=context.get('company_name', 'votre entreprise'),
            first_name=context.get('first_name', ''),
            last_name=context.get('last_name', ''),
            email=context.get('email', '')
        )
        
        return {'subject': subject, 'body': body}
