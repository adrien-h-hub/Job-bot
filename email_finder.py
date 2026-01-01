"""
Email Finder - Find professional emails using various techniques
Targets RHE (Responsable Hygiène et Sécurité) and Site Managers
"""

import re
import time
import random
import requests
from typing import Optional, Dict, List
from urllib.parse import quote_plus, urljoin, urlparse
from bs4 import BeautifulSoup

class EmailFinder:
    def __init__(self, company_name: str, company_website: str = None):
        self.company_name = company_name
        self.company_website = company_name.lower().replace(' ', '') + '.fr' if not company_website else company_website
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    def find_emails(self) -> Dict[str, List[str]]:
        """Find emails for key roles in the company"""
        print(f"🔍 Searching for key contacts at {self.company_name}...")
        
        # Try different methods to find emails
        emails = {
            'rhe': [],
            'site_manager': [],
            'hr': [],
            'other': []
        }
        
        # Method 1: Check common email patterns
        emails.update(self._check_common_patterns())
        
        # Method 2: Check company website
        if self.company_website:
            emails.update(self._scrape_company_website())
        
        # Method 3: Check LinkedIn (would require LinkedIn API or web scraping)
        # emails.update(self._check_linkedin())
        
        # Filter and validate emails
        return self._filter_emails(emails)
    
    def _check_common_patterns(self) -> Dict[str, List[str]]:
        """Check common email patterns for the company"""
        common_patterns = [
            # Common French email patterns
            'rhe@', 'hse@', 'rh@', 'recrutement@',
            'securite@', 'prevention@', 'qse@',
            'chantier@', 'direction@', 'contact@',
            'info@', 'commercial@', 'administration@'
        ]
        
        domain = self.company_website
        if not domain.startswith('http'):
            domain = f'https://{domain}'
        
        # Try with and without www
        base_domains = [
            domain.replace('https://', '').replace('http://', '').rstrip('/'),
            domain.replace('https://', 'www.').rstrip('/')
        ]
        
        found_emails = {'rhe': [], 'site_manager': [], 'hr': [], 'other': []}
        
        for domain in set(base_domains):
            for pattern in common_patterns:
                email = f"{pattern}{domain}"
                if self._validate_email(email):
                    if 'rhe' in email or 'hse' in email or 'securite' in email or 'prevention' in email:
                        found_emails['rhe'].append(email)
                    elif 'rh' in email or 'recrutement' in email:
                        found_emails['hr'].append(email)
                    elif 'chantier' in email or 'direction' in email:
                        found_emails['site_manager'].append(email)
                    else:
                        found_emails['other'].append(email)
        
        return found_emails
    
    def _scrape_company_website(self) -> Dict[str, List[str]]:
        """Scrape company website for email addresses"""
        found_emails = {'rhe': [], 'site_manager': [], 'hr': [], 'other': []}
        
        try:
            # Try to get contact page
            urls_to_check = [
                f"https://{self.company_website}/contact",
                f"https://{self.company_website}/nous-contacter",
                f"https://{self.company_website}/contactez-nous",
                f"https://{self.company_website}/contact.html",
                f"https://{self.company_website}/contact.php",
            ]
            
            for url in urls_to_check:
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        # Look for email patterns
                        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
                        for email in emails:
                            email = email.lower()
                            if self._validate_email(email):
                                if 'rhe' in email or 'hse' in email or 'securite' in email or 'prevention' in email:
                                    found_emails['rhe'].append(email)
                                elif 'rh' in email or 'recrutement' in email or 'carriere' in email:
                                    found_emails['hr'].append(email)
                                elif 'chantier' in email or 'chef' in email or 'conducteur' in email or 'directeur' in email:
                                    found_emails['site_manager'].append(email)
                                else:
                                    found_emails['other'].append(email)
                except:
                    continue
                
                # Be nice to the server
                time.sleep(1)
                
        except Exception as e:
            print(f"⚠️ Error scraping website: {e}")
        
        return found_emails
    
    def _filter_emails(self, emails: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Filter and deduplicate emails"""
        filtered = {'rhe': [], 'site_manager': [], 'hr': [], 'other': []}
        seen_emails = set()
        
        for category in emails:
            for email in emails[category]:
                if email not in seen_emails and self._validate_email(email):
                    filtered[category].append(email)
                    seen_emails.add(email)
        
        return filtered
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Basic email validation"""
        if not email or not isinstance(email, str):
            return False
            
        # Check for common invalid patterns
        invalid_patterns = [
            'noreply', 'no-reply', 'contact', 'info', 'support',
            'hello', 'bonjour', 'service', 'newsletter', 'notification'
        ]
        
        if any(pattern in email.lower() for pattern in invalid_patterns):
            return False
            
        # Basic regex check
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def find_linkedin_contacts(self, position: str = None) -> List[Dict]:
        """Find LinkedIn profiles for specific positions (would require LinkedIn API)"""
        # This is a placeholder for LinkedIn API integration
        # In a real implementation, you would use the LinkedIn API here
        print("⚠️ LinkedIn integration requires API access")
        return []
    
    def find_rhe_contact(self) -> Optional[Dict]:
        """Find RHE (Responsable Hygiène et Sécurité) contact"""
        emails = self.find_emails()
        
        # Try to find RHE email first
        if emails['rhe']:
            return {
                'name': 'Responsable Hygiène et Sécurité',
                'email': emails['rhe'][0],
                'position': 'RHE',
                'source': 'company_website'
            }
        
        # If no RHE email found, try to find on LinkedIn
        linkedin_contacts = self.find_linkedin_contacts("Responsable Hygiène et Sécurité")
        if linkedin_contacts:
            return linkedin_contacts[0]
        
        return None
    
    def find_site_manager_contact(self) -> Optional[Dict]:
        """Find Site Manager/Chef de Chantier contact"""
        emails = self.find_emails()
        
        # Try to find site manager email
        if emails['site_manager']:
            return {
                'name': 'Chef de Chantier',
                'email': emails['site_manager'][0],
                'position': 'Site Manager',
                'source': 'company_website'
            }
        
        # If no site manager email found, try to find on LinkedIn
        linkedin_contacts = self.find_linkedin_contacts("Chef de Chantier")
        if linkedin_contacts:
            return linkedin_contacts[0]
        
        return None


def test_email_finder():
    """Test the EmailFinder"""
    companies = [
        "Vinci Construction",
        "Bouygues Construction",
        "Eiffage Construction"
    ]
    
    for company in companies:
        print(f"\n🔎 Searching for contacts at {company}...")
        finder = EmailFinder(company)
        
        # Find RHE
        rhe = finder.find_rhe_contact()
        if rhe:
            print(f"   🛡️ RHE: {rhe.get('name', 'N/A')} - {rhe.get('email', 'N/A')}")
        else:
            print("   ❌ No RHE contact found")
        
        # Find Site Manager
        site_manager = finder.find_site_manager_contact()
        if site_manager:
            print(f"   👷 Site Manager: {site_manager.get('name', 'N/A')} - {site_manager.get('email', 'N/A')}")
        else:
            print("   ❌ No Site Manager contact found")


if __name__ == "__main__":
    test_email_finder()
