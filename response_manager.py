"""
Response Manager - Handles incoming responses and manages follow-ups
"""

import os
import logging
import imaplib
import email
from email.header import decode_header
from typing import Dict, List, Optional
from datetime import datetime
from email_finder import EmailFinder
from response_handler import ResponseHandler
from email_templates import EmailTemplates
from email_notifier import EmailNotifier
from job_database import JobDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('response_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ResponseManager:
    def __init__(self, config: Dict, db_path: str = 'job_hunter.db'):
        """
        Initialize the Response Manager
        
        Args:
            config: Configuration dictionary with user profile and email settings
            db_path: Path to the SQLite database file
        """
        self.config = config
        self.db = JobDatabase(db_path)
        self.imap_server = config['email'].get('imap_server', 'imap.gmail.com')
        self.imap_port = config['email'].get('imap_port', 993)
        self.email_notifier = EmailNotifier(
            smtp_server=config['email']['smtp_server'],
            smtp_port=config['email']['smtp_port'],
            smtp_username=config['email']['smtp_username'],
            smtp_password=config['email']['smtp_password'],
            from_email=config['email']['from_email'],
            from_name=config['email']['from_name']
        )
        
    def fetch_new_emails(self) -> List[Dict]:
        """
        Fetch new unread emails from inbox using IMAP
        
        Returns:
            List of email dictionaries with keys: from_email, subject, body, received_date
        """
        emails = []
        
        try:
            # Connect to IMAP server
            logger.info(f"Connecting to IMAP server: {self.imap_server}:{self.imap_port}")
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            
            # Login
            mail.login(
                self.config['email']['smtp_username'],
                self.config['email']['smtp_password']
            )
            logger.info("Successfully logged in to email account")
            
            # Select inbox
            mail.select('inbox')
            
            # Search for unread emails
            _, message_numbers = mail.search(None, 'UNSEEN')
            email_ids = message_numbers[0].split()
            
            logger.info(f"Found {len(email_ids)} unread emails")
            
            # Process last 10 unread emails
            for email_id in email_ids[-10:]:
                try:
                    _, msg_data = mail.fetch(email_id, '(RFC822)')
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    # Extract sender
                    from_email = email_message['From']
                    if '<' in from_email:
                        from_email = from_email.split('<')[1].split('>')[0]
                    
                    # Extract subject
                    subject = email_message['Subject']
                    if subject:
                        decoded_subject = decode_header(subject)[0]
                        if isinstance(decoded_subject[0], bytes):
                            subject = decoded_subject[0].decode(decoded_subject[1] or 'utf-8')
                        else:
                            subject = decoded_subject[0]
                    
                    # Extract body
                    body = self._get_email_body(email_message)
                    
                    # Extract date
                    received_date = email_message['Date']
                    
                    emails.append({
                        'from_email': from_email,
                        'subject': subject or '',
                        'body': body,
                        'received_date': received_date
                    })
                    
                    logger.info(f"Processed email from {from_email}: {subject}")
                    
                except Exception as e:
                    logger.error(f"Error processing email {email_id}: {e}")
                    continue
            
            # Close connection
            mail.close()
            mail.logout()
            
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
        
        return emails
    
    def _get_email_body(self, email_message) -> str:
        """
        Extract the body text from an email message
        """
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Get text/plain parts
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        pass
        else:
            # Not multipart - get payload directly
            try:
                body = email_message.get_payload(decode=True).decode()
            except:
                body = str(email_message.get_payload())
        
        return body
    
    def check_and_process_responses(self):
        """
        Main method to check for new emails and process all responses
        """
        logger.info("Starting email response check...")
        
        # Fetch new emails
        emails = self.fetch_new_emails()
        
        if not emails:
            logger.info("No new emails to process")
            return
        
        logger.info(f"Processing {len(emails)} new emails")
        
        # Process each email
        for email_data in emails:
            try:
                result = self.process_incoming_email(email_data)
                logger.info(f"Email processed: {result.get('status')}")
            except Exception as e:
                logger.error(f"Error processing email: {e}")
                continue
        
        logger.info("Email response check complete")
    
    def process_incoming_email(self, email_data: Dict) -> Dict:
        """
        Process an incoming email and determine the appropriate action
        
        Args:
            email_data: Dictionary containing email data with keys:
                - from_email: Sender's email address
                - subject: Email subject
                - body: Email body text
                - received_date: When the email was received
                - job_id: Optional job ID if this is related to an application
        """
        logger.info(f"Processing email from {email_data.get('from_email')} with subject: {email_data.get('subject')}")
        
        # Try to find the related job application
        job_data = self._find_related_job(email_data)
        if not job_data:
            logger.warning("No related job found for this email")
            return {'status': 'error', 'message': 'No related job found'}
        
        # Analyze the email content
        handler = ResponseHandler(job_data, self.config['profile'])
        analysis = handler.analyze_response(email_data['body'])
        
        # Log the analysis
        logger.info(f"Email analysis result: {analysis['action']} (confidence: {analysis['confidence']:.2f})")
        
        # Take appropriate action based on the analysis
        result = self._handle_analysis_result(analysis, job_data, email_data)
        
        # Update job status in the database
        self._update_job_status(job_data, analysis['action'])
        
        return {
            'status': 'success',
            'action': analysis['action'],
            'job_id': job_data.get('job_id'),
            'job_title': job_data.get('title'),
            'company': job_data.get('company'),
            'result': result
        }
    
    def _find_related_job(self, email_data: Dict) -> Optional[Dict]:
        """
        Find the job related to this email
        
        Args:
            email_data: Dictionary containing email data
            
        Returns:
            Job data as a dictionary or None if not found
        """
        # First try to find by job_id if provided
        if 'job_id' in email_data:
            job = self.db.get_job(email_data['job_id'])
            if job:
                return job
        
        # Otherwise try to match by company and position in subject/body
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        
        # Get recent applications (last 30 days)
        recent_jobs = self.db.get_recent_applications(days=30)
        
        # Try to find a match
        for job in recent_jobs:
            company = job.get('company', '').lower()
            title = job.get('title', '').lower()
            
            # Check if company name is in subject or body
            if company and (company in subject or company in body):
                # If we also have a job title, check for that too
                if not title or (title in subject or title in body):
                    return job
            
            # Check for job reference numbers if present
            if 'reference' in job and job['reference']:
                ref = job['reference'].lower()
                if ref in subject or ref in body:
                    return job
        
        return None
    
    def _handle_analysis_result(self, analysis: Dict, job_data: Dict, email_data: Dict) -> Dict:
        """
        Handle the result of email analysis
        
        Args:
            analysis: Dictionary with analysis results
            job_data: Job data from the database
            email_data: Original email data
            
        Returns:
            Dictionary with results of the action taken
        """
        action = analysis.get('action')
        
        if action == 'schedule_interview':
            return self._handle_interview_request(analysis, job_data, email_data)
        elif action == 'follow_up':
            return self._handle_follow_up(analysis, job_data, email_data)
        elif action == 'send_info':
            return self._handle_information_request(analysis, job_data, email_data)
        elif action == 'rejection':
            return self._handle_rejection(analysis, job_data, email_data)
        else:
            return self._handle_unknown_response(analysis, job_data, email_data)
    
    def _handle_interview_request(self, analysis: Dict, job_data: Dict, email_data: Dict) -> Dict:
        """Handle interview scheduling requests"""
        logger.info(f"Handling interview request for job: {job_data.get('job_id')}")
        
        # Get the suggested response from the analysis
        suggested_response = analysis.get('suggested_response', '')
        
        # If we have contacts, try to find the best one to respond to
        contacts = analysis.get('contacts', [])
        recipient_email = email_data.get('from_email')
        
        # If we have RHE or Site Manager contacts, use them for follow-up
        if contacts:
            # Prefer RHE over Site Manager if both are available
            contact = next((c for c in contacts if c.get('position') == 'RHE'), None) or \
                     next((c for c in contacts if c.get('position') == 'Site Manager'), None)
            
            if contact and contact.get('email'):
                recipient_email = contact['email']
                logger.info(f"Found contact for follow-up: {contact.get('name')} ({contact.get('position')}) - {contact.get('email')}")
        
        # Send the response
        subject = f"Disponibilités pour entretien - {job_data.get('title', 'Candidature')}"
        
        # Use the template if available, otherwise use the suggested response
        try:
            template = EmailTemplates.get_template('interview_request', {
                'job_title': job_data.get('title', ''),
                'first_name': self.config['profile'].get('first_name', ''),
                'last_name': self.config['profile'].get('last_name', ''),
                'email': self.config['email'].get('from_email', ''),
                'phone': self.config['profile'].get('phone', '')
            })
            subject = template['subject']
            body = template['body']
        except Exception as e:
            logger.warning(f"Error loading email template: {e}")
            body = suggested_response
        
        # Send the email
        try:
            self.email_notifier.send_email(
                to_email=recipient_email,
                subject=subject,
                message=body,
                is_html=False
            )
            
            logger.info(f"Sent interview response to {recipient_email}")
            return {'status': 'success', 'message': 'Interview response sent', 'to': recipient_email}
            
        except Exception as e:
            logger.error(f"Error sending interview response: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _handle_follow_up(self, analysis: Dict, job_data: Dict, email_data: Dict) -> Dict:
        """Handle follow-up actions"""
        logger.info(f"Handling follow-up for job: {job_data.get('job_id')}")
        
        # Check if we need to send a follow-up email
        if analysis.get('suggested_response'):
            try:
                # Get the recipient email (default to the sender of the original email)
                recipient_email = email_data.get('from_email')
                
                # Try to find a better contact if available
                finder = EmailFinder(company_name=job_data.get('company', ''))
                contacts = finder.find_company_contacts()
                
                if contacts:
                    # Prefer RHE over Site Manager if both are available
                    contact = next((c for c in contacts if c.get('position') == 'RHE'), None) or \
                             next((c for c in contacts if c.get('position') == 'Site Manager'), None)
                    
                    if contact and contact.get('email'):
                        recipient_email = contact['email']
                        logger.info(f"Found contact for follow-up: {contact.get('name')} ({contact.get('position')}) - {contact.get('email')}")
                
                # Prepare the email
                subject = f"Suite à ma candidature - {job_data.get('title', 'Poste')}"
                
                # Use the template if available, otherwise use the suggested response
                try:
                    template = EmailTemplates.get_template('follow_up', {
                        'job_title': job_data.get('title', ''),
                        'first_name': self.config['profile'].get('first_name', ''),
                        'last_name': self.config['profile'].get('last_name', ''),
                        'email': self.config['email'].get('from_email', ''),
                        'phone': self.config['profile'].get('phone', ''),
                        'application_date': job_data.get('applied_date', datetime.now().strftime('%d/%m/%Y')),
                        'contact_name': contact.get('name', '') if contact else ''
                    })
                    subject = template['subject']
                    body = template['body']
                except Exception as e:
                    logger.warning(f"Error loading email template: {e}")
                    body = analysis.get('suggested_response', '')
                
                # Send the email
                self.email_notifier.send_email(
                    to_email=recipient_email,
                    subject=subject,
                    message=body,
                    is_html=False
                )
                
                logger.info(f"Sent follow-up email to {recipient_email}")
                return {'status': 'success', 'message': 'Follow-up email sent', 'to': recipient_email}
                
            except Exception as e:
                logger.error(f"Error sending follow-up email: {e}")
                return {'status': 'error', 'message': str(e)}
        
        return {'status': 'no_action', 'message': 'No follow-up action required'}
    
    def _handle_information_request(self, analysis: Dict, job_data: Dict, email_data: Dict) -> Dict:
        """Handle requests for more information"""
        logger.info(f"Handling information request for job: {job_data.get('job_id')}")
        
        # Notify the user about the information request
        user_email = self.config['email'].get('from_email')
        subject = f"Action Requise: Réponse à une demande d'information - {job_data.get('title', '')}"
        
        message = f"""Bonjour,

Vous avez reçu une demande d'information concernant votre candidature pour le poste de {job_title} chez {company}.

Détails de la demande :
- Poste : {job_title}
- Entreprise : {company}
- Date de candidature : {applied_date}

Message reçu :
{email_body}

---

Voici une suggestion de réponse que vous pouvez utiliser :

{suggested_response}

---

Veuillez répondre directement à cet email avec votre réponse ou les informations demandées.

Cordialement,
Votre assistant de recherche d'emploi
""".format(
            job_title=job_data.get('title', ''),
            company=job_data.get('company', ''),
            applied_date=job_data.get('applied_date', ''),
            email_body=email_data.get('body', '')[:500] + '...' if email_data.get('body') else '',
            suggested_response=analysis.get('suggested_response', '')
        )
        
        try:
            self.email_notifier.send_email(
                to_email=user_email,
                subject=subject,
                message=message,
                is_html=False
            )
            
            logger.info(f"Notified user about information request: {user_email}")
            return {'status': 'success', 'message': 'User notified about information request'}
            
        except Exception as e:
            logger.error(f"Error notifying user about information request: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _handle_rejection(self, analysis: Dict, job_data: Dict, email_data: Dict) -> Dict:
        """Handle rejection emails"""
        logger.info(f"Handling rejection for job: {job_data.get('job_id')}")
        
        # Update the job status in the database
        self.db.update_job_status(job_data.get('job_id'), 'rejected', {
            'rejection_date': datetime.now().strftime('%Y-%m-%d'),
            'rejection_reason': 'Received rejection email',
            'rejection_details': email_data.get('body', '')[:1000]
        })
        
        # Notify the user about the rejection
        user_email = self.config['email'].get('from_email')
        subject = f"Mise à jour de candidature : Refus - {job_data.get('title', '')}"
        
        message = f"""Bonjour,

Nous avons reçu une mise à jour concernant votre candidature pour le poste de {job_title} chez {company}.

Statut : ❌ Non retenu(e)

Message reçu :
{email_body}

---

Voici une suggestion de réponse de remerciement que vous pouvez utiliser :

{suggested_response}

---

Nous continuons à surveiller d'autres opportunités pour vous.

Cordialement,
Votre assistant de recherche d'emploi
""".format(
            job_title=job_data.get('title', ''),
            company=job_data.get('company', ''),
            email_body=email_data.get('body', '')[:500] + '...' if email_data.get('body') else '',
            suggested_response=analysis.get('suggested_response', '')
        )
        
        try:
            self.email_notifier.send_email(
                to_email=user_email,
                subject=subject,
                message=message,
                is_html=False
            )
            
            logger.info(f"Notified user about rejection: {user_email}")
            return {'status': 'success', 'message': 'User notified about rejection'}
            
        except Exception as e:
            logger.error(f"Error notifying user about rejection: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _handle_unknown_response(self, analysis: Dict, job_data: Dict, email_data: Dict) -> Dict:
        """Handle unrecognized responses"""
        logger.info(f"Handling unknown response type for job: {job_data.get('job_id')}")
        
        # Notify the user about the unknown response
        user_email = self.config['email'].get('from_email')
        subject = f"Réponse inattendue concernant votre candidature - {job_data.get('title', '')}"
        
        message = f"""Bonjour,

Nous avons reçu une réponse concernant votre candidature pour le poste de {job_title} chez {company}, mais nous n'avons pas pu déterminer automatiquement la meilleure façon de la traiter.

Détails de la candidature :
- Poste : {job_title}
- Entreprise : {company}
- Date de candidature : {applied_date}

Message reçu :
{email_body}

---

Notre analyse indique :
{analysis}

---

Veuillez examiner ce message et prendre les mesures appropriées.

Cordialement,
Votre assistant de recherche d'emploi
""".format(
            job_title=job_data.get('title', ''),
            company=job_data.get('company', ''),
            applied_date=job_data.get('applied_date', ''),
            email_body=email_data.get('body', '')[:500] + '...' if email_data.get('body') else '',
            analysis='\n'.join([f"- {k}: {v}" for k, v in analysis.items()])
        )
        
        try:
            self.email_notifier.send_email(
                to_email=user_email,
                subject=subject,
                message=message,
                is_html=False
            )
            
            logger.info(f"Notified user about unknown response: {user_email}")
            return {'status': 'success', 'message': 'User notified about unknown response'}
            
        except Exception as e:
            logger.error(f"Error notifying user about unknown response: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _update_job_status(self, job_data: Dict, action: str) -> bool:
        """
        Update the job status based on the action taken
        
        Args:
            job_data: Job data from the database
            action: The action taken (e.g., 'schedule_interview', 'rejection')
            
        Returns:
            True if the update was successful, False otherwise
        """
        status_map = {
            'schedule_interview': 'interview_scheduled',
            'follow_up': 'follow_up_sent',
            'send_info': 'info_requested',
            'rejection': 'rejected',
            'unknown': 'response_received'
        }
        
        new_status = status_map.get(action, 'response_received')
        
        try:
            self.db.update_job_status(
                job_data.get('job_id'),
                new_status,
                {'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            )
            logger.info(f"Updated job {job_data.get('job_id')} status to {new_status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating job status: {e}")
            return False
