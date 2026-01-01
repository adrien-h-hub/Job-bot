"""
Email Notifier - Send job summaries via email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
from email_templates import EmailTemplates


class EmailNotifier:
    def __init__(self, smtp_server: str, smtp_port: int, 
                 smtp_username: str, smtp_password: str,
                 from_email: str, from_name: str = "Job Hunter Bot"):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.from_name = from_name
        
    def send_job_summary(self, recipient_email: str, jobs: List[Dict], 
                        stats: Dict = None) -> bool:
        """Send a summary email with found jobs"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🔍 Job Hunter Report - {len(jobs)} Jobs Found - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = recipient_email
            
            # Create HTML content
            html_content = self._create_html_email(jobs, stats)
            text_content = self._create_text_email(jobs, stats)
            
            msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Email error: {e}")
            return False
    
    def _create_html_email(self, jobs: List[Dict], stats: Dict = None) -> str:
        """Create HTML email content"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                .stats {{ display: flex; gap: 20px; margin-bottom: 20px; }}
                .stat-box {{ background: #f0f4f8; padding: 15px; border-radius: 8px; text-align: center; flex: 1; }}
                .stat-number {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                .job-card {{ border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px; }}
                .job-card:hover {{ box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .job-title {{ font-size: 18px; font-weight: bold; color: #2d3748; margin-bottom: 5px; }}
                .job-company {{ color: #667eea; font-weight: 500; }}
                .job-location {{ color: #718096; font-size: 14px; }}
                .job-salary {{ background: #48bb78; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px; display: inline-block; }}
                .job-score {{ float: right; background: #667eea; color: white; padding: 5px 10px; border-radius: 20px; }}
                .apply-btn {{ background: #667eea; color: white; padding: 8px 16px; border-radius: 5px; text-decoration: none; display: inline-block; margin-top: 10px; }}
                .linkedin {{ border-left: 4px solid #0077b5; }}
                .indeed {{ border-left: 4px solid #2164f3; }}
                .source-badge {{ font-size: 10px; background: #e2e8f0; padding: 2px 6px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Job Hunter Daily Report</h1>
                <p>{datetime.now().strftime('%A, %B %d, %Y')}</p>
            </div>
        """
        
        # Stats section
        if stats:
            html += f"""
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{stats.get('total_jobs', 0)}</div>
                    <div>Total Jobs</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats.get('new_jobs', 0)}</div>
                    <div>New Today</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats.get('applied', 0)}</div>
                    <div>Applied</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats.get('interviews', 0)}</div>
                    <div>Interviews</div>
                </div>
            </div>
            """
        
        # Jobs section
        html += f"<h2>📋 {len(jobs)} Jobs Matching Your Criteria</h2>"
        
        for job in jobs[:20]:  # Limit to 20 jobs in email
            source_class = 'linkedin' if 'linkedin' in job.get('source', '') else 'indeed'
            score = job.get('match_score', 0)
            
            html += f"""
            <div class="job-card {source_class}">
                <span class="job-score">{score}% match</span>
                <div class="job-title">{job.get('title', 'Unknown')}</div>
                <div class="job-company">{job.get('company', 'Unknown')} 
                    <span class="source-badge">{job.get('source', 'unknown').upper()}</span>
                </div>
                <div class="job-location">📍 {job.get('location', 'Not specified')}</div>
            """
            
            if job.get('salary'):
                html += f'<span class="job-salary">💰 {job["salary"]}</span>'
            
            if job.get('easy_apply'):
                html += ' <span style="color: #48bb78;">⚡ Easy Apply</span>'
            
            if job.get('url'):
                html += f'<br><a href="{job["url"]}" class="apply-btn">View & Apply →</a>'
            
            html += "</div>"
        
        html += """
            <hr style="margin: 30px 0;">
            <p style="color: #718096; font-size: 12px; text-align: center;">
                This email was sent by Job Hunter Bot 🤖<br>
                Good luck with your job search! 🍀
            </p>
        </body>
        </html>
        """
        
        return html
    
    def _create_text_email(self, jobs: List[Dict], stats: Dict = None) -> str:
        """Create plain text email content"""
        text = f"JOB HUNTER DAILY REPORT\n"
        text += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        text += "=" * 50 + "\n\n"
        
        if stats:
            text += f"STATISTICS:\n"
            text += f"- Total Jobs: {stats.get('total_jobs', 0)}\n"
            text += f"- New Today: {stats.get('new_jobs', 0)}\n"
            text += f"- Applied: {stats.get('applied', 0)}\n"
            text += f"- Interviews: {stats.get('interviews', 0)}\n\n"
        
        text += f"FOUND {len(jobs)} MATCHING JOBS:\n"
        text += "-" * 50 + "\n\n"
        
        for i, job in enumerate(jobs[:20], 1):
            text += f"{i}. {job.get('title', 'Unknown')}\n"
            text += f"   Company: {job.get('company', 'Unknown')}\n"
            text += f"   Location: {job.get('location', 'Not specified')}\n"
            text += f"   Source: {job.get('source', 'unknown').upper()}\n"
            text += f"   Match: {job.get('match_score', 0)}%\n"
            if job.get('salary'):
                text += f"   Salary: {job['salary']}\n"
            if job.get('url'):
                text += f"   URL: {job['url']}\n"
            text += "\n"
        
        text += "\nGood luck with your job search! 🍀\n"
        
        return text
    
    def send_application_confirmation(self, recipient_email: str, job: Dict) -> bool:
        """Send confirmation email when application is submitted"""
        try:
            msg = MIMEMultipart()
            msg['Subject'] = f"✅ Application Submitted: {job.get('title')} at {job.get('company')}"
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = recipient_email
            
            body = f"""
Application Confirmation
========================

You have successfully applied to:

Position: {job.get('title')}
Company: {job.get('company')}
Location: {job.get('location')}
Source: {job.get('source', '').upper()}

Job URL: {job.get('url')}

Applied on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Good luck! 🍀
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_templated_email(self, to_email: str, template_name: str, context: Dict) -> bool:
        """Send an email using a predefined template
        
        Args:
            to_email: Recipient email address
            template_name: Name of the template to use
            context: Dictionary with template variables
        
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Get template
            template_func = getattr(EmailTemplates, template_name, None)
            if not template_func:
                print(f"Template '{template_name}' not found")
                return False
            
            template = template_func(context)
            
            # Create message
            msg = MIMEMultipart()
            msg['Subject'] = template['subject']
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            msg.attach(MIMEText(template['body'], 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Templated email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Template email error: {e}")
            return False
