"""
Webhook Notifier - Send real-time notifications to Slack, Discord, or Telegram
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class WebhookNotifier:
    """Send notifications to various platforms via webhooks"""
    
    def __init__(self, webhook_url: str, platform: str = 'slack'):
        """
        Initialize webhook notifier
        
        Args:
            webhook_url: Webhook URL for the platform
            platform: Platform type ('slack', 'discord', 'telegram')
        """
        self.webhook_url = webhook_url
        self.platform = platform.lower()
    
    def notify_new_job(self, job: Dict):
        """
        Send notification for new high-match job found
        
        Args:
            job: Job dictionary with details
        """
        match_score = job.get('match_score', 0)
        
        # Only notify for high-match jobs (>= 70%)
        if match_score < 70:
            return
        
        if self.platform == 'slack':
            self._send_slack_new_job(job)
        elif self.platform == 'discord':
            self._send_discord_new_job(job)
        elif self.platform == 'telegram':
            self._send_telegram_new_job(job)
    
    def notify_application_submitted(self, job: Dict):
        """
        Send notification when application is submitted
        
        Args:
            job: Job dictionary
        """
        if self.platform == 'slack':
            self._send_slack_application(job)
        elif self.platform == 'discord':
            self._send_discord_application(job)
        elif self.platform == 'telegram':
            self._send_telegram_application(job)
    
    def notify_response_received(self, job: Dict, response_type: str):
        """
        Send notification when recruiter responds
        
        Args:
            job: Job dictionary
            response_type: Type of response (interview, rejection, info_request)
        """
        if self.platform == 'slack':
            self._send_slack_response(job, response_type)
        elif self.platform == 'discord':
            self._send_discord_response(job, response_type)
        elif self.platform == 'telegram':
            self._send_telegram_response(job, response_type)
    
    def notify_complex_question(self, job: Dict, questions: List[Dict]):
        """
        Send notification when complex questions detected
        
        Args:
            job: Job dictionary
            questions: List of complex questions
        """
        if self.platform == 'slack':
            self._send_slack_complex_question(job, questions)
        elif self.platform == 'discord':
            self._send_discord_complex_question(job, questions)
        elif self.platform == 'telegram':
            self._send_telegram_complex_question(job, questions)
    
    # Slack implementations
    def _send_slack_new_job(self, job: Dict):
        """Send Slack notification for new job"""
        match_score = job.get('match_score', 0)
        color = 'good' if match_score >= 80 else 'warning'
        
        message = {
            'text': '🎯 High Match Job Found!',
            'attachments': [{
                'color': color,
                'fields': [
                    {'title': 'Position', 'value': job.get('title', 'N/A'), 'short': False},
                    {'title': 'Company', 'value': job.get('company', 'N/A'), 'short': True},
                    {'title': 'Location', 'value': job.get('location', 'N/A'), 'short': True},
                    {'title': 'Match Score', 'value': f"{match_score}%", 'short': True},
                    {'title': 'Salary', 'value': job.get('salary', 'Not specified'), 'short': True},
                    {'title': 'Source', 'value': job.get('source', 'N/A').upper(), 'short': True},
                    {'title': 'Easy Apply', 'value': '✅ Yes' if job.get('easy_apply') else '❌ No', 'short': True},
                ],
                'footer': 'Job Hunter Bot',
                'ts': int(datetime.now().timestamp())
            }]
        }
        
        if job.get('url'):
            message['attachments'][0]['actions'] = [{
                'type': 'button',
                'text': 'View Job',
                'url': job['url']
            }]
        
        self._send_webhook(message)
    
    def _send_slack_application(self, job: Dict):
        """Send Slack notification for application submitted"""
        message = {
            'text': '✅ Application Submitted!',
            'attachments': [{
                'color': 'good',
                'fields': [
                    {'title': 'Position', 'value': job.get('title', 'N/A'), 'short': False},
                    {'title': 'Company', 'value': job.get('company', 'N/A'), 'short': True},
                    {'title': 'Time', 'value': datetime.now().strftime('%I:%M %p'), 'short': True}
                ],
                'footer': 'Job Hunter Bot'
            }]
        }
        self._send_webhook(message)
    
    def _send_slack_response(self, job: Dict, response_type: str):
        """Send Slack notification for recruiter response"""
        emoji_map = {
            'interview': '🎤',
            'rejection': '❌',
            'info_request': 'ℹ️',
            'unknown': '📧'
        }
        
        color_map = {
            'interview': 'good',
            'rejection': 'danger',
            'info_request': 'warning',
            'unknown': '#808080'
        }
        
        emoji = emoji_map.get(response_type, '📧')
        color = color_map.get(response_type, '#808080')
        
        message = {
            'text': f'{emoji} Response Received: {response_type.replace("_", " ").title()}',
            'attachments': [{
                'color': color,
                'fields': [
                    {'title': 'Position', 'value': job.get('title', 'N/A'), 'short': True},
                    {'title': 'Company', 'value': job.get('company', 'N/A'), 'short': True},
                ],
                'footer': 'Job Hunter Bot'
            }]
        }
        self._send_webhook(message)
    
    def _send_slack_complex_question(self, job: Dict, questions: List[Dict]):
        """Send Slack notification for complex questions"""
        question_text = '\n'.join([f"• {q.get('text', 'Unknown')[:100]}" for q in questions[:3]])
        
        message = {
            'text': '⚠️ Complex Questions Detected - Manual Input Required',
            'attachments': [{
                'color': 'warning',
                'fields': [
                    {'title': 'Position', 'value': job.get('title', 'N/A'), 'short': True},
                    {'title': 'Company', 'value': job.get('company', 'N/A'), 'short': True},
                    {'title': 'Questions', 'value': question_text, 'short': False}
                ],
                'footer': f'{len(questions)} question(s) need your attention'
            }]
        }
        
        if job.get('url'):
            message['attachments'][0]['actions'] = [{
                'type': 'button',
                'text': 'Complete Application',
                'url': job['url']
            }]
        
        self._send_webhook(message)
    
    # Discord implementations
    def _send_discord_new_job(self, job: Dict):
        """Send Discord notification for new job"""
        match_score = job.get('match_score', 0)
        color = 0x00FF00 if match_score >= 80 else 0xFFA500  # Green or Orange
        
        embed = {
            'title': '🎯 High Match Job Found!',
            'description': f"**{job.get('title', 'N/A')}** at **{job.get('company', 'N/A')}**",
            'color': color,
            'fields': [
                {'name': 'Location', 'value': job.get('location', 'N/A'), 'inline': True},
                {'name': 'Match Score', 'value': f"{match_score}%", 'inline': True},
                {'name': 'Salary', 'value': job.get('salary', 'Not specified'), 'inline': True},
                {'name': 'Source', 'value': job.get('source', 'N/A').upper(), 'inline': True},
                {'name': 'Easy Apply', 'value': '✅ Yes' if job.get('easy_apply') else '❌ No', 'inline': True}
            ],
            'footer': {'text': 'Job Hunter Bot'},
            'timestamp': datetime.now().isoformat()
        }
        
        if job.get('url'):
            embed['url'] = job['url']
        
        message = {'embeds': [embed]}
        self._send_webhook(message)
    
    def _send_discord_application(self, job: Dict):
        """Send Discord notification for application"""
        embed = {
            'title': '✅ Application Submitted!',
            'description': f"Applied to **{job.get('title', 'N/A')}** at **{job.get('company', 'N/A')}**",
            'color': 0x00FF00,
            'timestamp': datetime.now().isoformat()
        }
        self._send_webhook({'embeds': [embed]})
    
    def _send_discord_response(self, job: Dict, response_type: str):
        """Send Discord notification for response"""
        color_map = {
            'interview': 0x00FF00,
            'rejection': 0xFF0000,
            'info_request': 0xFFA500,
            'unknown': 0x808080
        }
        
        embed = {
            'title': f'📧 Response: {response_type.replace("_", " ").title()}',
            'description': f"**{job.get('title', 'N/A')}** at **{job.get('company', 'N/A')}**",
            'color': color_map.get(response_type, 0x808080),
            'timestamp': datetime.now().isoformat()
        }
        self._send_webhook({'embeds': [embed]})
    
    def _send_discord_complex_question(self, job: Dict, questions: List[Dict]):
        """Send Discord notification for complex questions"""
        question_text = '\n'.join([f"• {q.get('text', 'Unknown')[:100]}" for q in questions[:3]])
        
        embed = {
            'title': '⚠️ Complex Questions Detected',
            'description': f"**{job.get('title', 'N/A')}** at **{job.get('company', 'N/A')}**",
            'color': 0xFFA500,
            'fields': [
                {'name': 'Questions Requiring Input', 'value': question_text, 'inline': False}
            ],
            'footer': {'text': f'{len(questions)} question(s) need your attention'},
            'timestamp': datetime.now().isoformat()
        }
        
        if job.get('url'):
            embed['url'] = job['url']
        
        self._send_webhook({'embeds': [embed]})
    
    # Telegram implementations
    def _send_telegram_new_job(self, job: Dict):
        """Send Telegram notification for new job"""
        match_score = job.get('match_score', 0)
        
        text = f"""
🎯 *High Match Job Found!*

*Position:* {job.get('title', 'N/A')}
*Company:* {job.get('company', 'N/A')}
*Location:* {job.get('location', 'N/A')}
*Match Score:* {match_score}%
*Salary:* {job.get('salary', 'Not specified')}
*Source:* {job.get('source', 'N/A').upper()}
*Easy Apply:* {'✅ Yes' if job.get('easy_apply') else '❌ No'}
"""
        
        if job.get('url'):
            text += f"\n[View Job]({job['url']})"
        
        message = {
            'text': text,
            'parse_mode': 'Markdown'
        }
        self._send_webhook(message)
    
    def _send_telegram_application(self, job: Dict):
        """Send Telegram notification for application"""
        text = f"""
✅ *Application Submitted!*

*Position:* {job.get('title', 'N/A')}
*Company:* {job.get('company', 'N/A')}
*Time:* {datetime.now().strftime('%I:%M %p')}
"""
        self._send_webhook({'text': text, 'parse_mode': 'Markdown'})
    
    def _send_telegram_response(self, job: Dict, response_type: str):
        """Send Telegram notification for response"""
        emoji_map = {
            'interview': '🎤',
            'rejection': '❌',
            'info_request': 'ℹ️',
            'unknown': '📧'
        }
        
        emoji = emoji_map.get(response_type, '📧')
        
        text = f"""
{emoji} *Response Received: {response_type.replace('_', ' ').title()}*

*Position:* {job.get('title', 'N/A')}
*Company:* {job.get('company', 'N/A')}
"""
        self._send_webhook({'text': text, 'parse_mode': 'Markdown'})
    
    def _send_telegram_complex_question(self, job: Dict, questions: List[Dict]):
        """Send Telegram notification for complex questions"""
        question_text = '\n'.join([f"• {q.get('text', 'Unknown')[:100]}" for q in questions[:3]])
        
        text = f"""
⚠️ *Complex Questions Detected*

*Position:* {job.get('title', 'N/A')}
*Company:* {job.get('company', 'N/A')}

*Questions:*
{question_text}

{len(questions)} question(s) need your attention
"""
        
        if job.get('url'):
            text += f"\n\n[Complete Application]({job['url']})"
        
        self._send_webhook({'text': text, 'parse_mode': 'Markdown'})
    
    def _send_webhook(self, payload: Dict):
        """
        Send webhook request
        
        Args:
            payload: Message payload
        """
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Webhook notification failed: {e}")


# Example usage
if __name__ == "__main__":
    # Test with Slack webhook (replace with your actual webhook URL)
    # webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    # notifier = WebhookNotifier(webhook_url, platform='slack')
    
    test_job = {
        'title': 'Senior Python Developer',
        'company': 'Tech Corp',
        'location': 'Paris, France',
        'salary': '€60,000 - €80,000',
        'match_score': 85,
        'source': 'linkedin',
        'easy_apply': True,
        'url': 'https://linkedin.com/jobs/123'
    }
    
    print("Webhook Notifier - Test Mode")
    print("=" * 60)
    print("To use, set WEBHOOK_URL environment variable")
    print("\nExample notifications would be sent for:")
    print(f"- New job: {test_job['title']} ({test_job['match_score']}% match)")
    print("- Application submitted")
    print("- Response received")
    print("- Complex questions detected")
