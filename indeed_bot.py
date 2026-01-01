"""
Indeed Job Search Bot
Uses requests + BeautifulSoup for scraping and Selenium for applications
"""

import time
import random
import hashlib
import requests
from datetime import datetime
from typing import Tuple, List, Dict, Optional
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class IndeedBot:
    def __init__(self, headless: bool = False):
        self.driver = None
        self.headless = headless
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        
    def setup_driver(self):
        """Setup Chrome driver for applications"""
        if self.driver:
            return
            
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    def random_delay(self, min_sec: float = 1, max_sec: float = 3):
        """Add random delay"""
        time.sleep(random.uniform(min_sec, max_sec))
        
    def search_jobs(self, keywords: str, location: str, 
                    posted_within_days: int = 7,
                    job_type: str = None,
                    salary_min: int = None,
                    remote: bool = False) -> List[Dict]:
        """
        Search for jobs on Indeed
        
        Args:
            keywords: Job search keywords
            location: Location to search
            posted_within_days: Filter by days posted (1, 3, 7, 14)
            job_type: fulltime, parttime, contract, internship
            salary_min: Minimum salary
            remote: Include remote jobs
        """
        jobs = []
        
        # Build Indeed URL (France version - change domain for other countries)
        base_url = "https://fr.indeed.com/jobs"  # Use indeed.com for US
        
        params = {
            'q': keywords,
            'l': location,
        }
        
        # Date posted filter
        date_filters = {1: 'last', 3: '3', 7: '7', 14: '14'}
        if posted_within_days in date_filters:
            params['fromage'] = date_filters[posted_within_days]
        
        # Job type filter
        if job_type:
            type_map = {
                'fulltime': 'fulltime',
                'parttime': 'parttime', 
                'contract': 'contract',
                'internship': 'internship',
                'cdi': 'permanent',
                'cdd': 'contract'
            }
            if job_type in type_map:
                params['jt'] = type_map[job_type]
        
        # Remote filter
        if remote:
            params['remotejob'] = '1'
        
        # Build URL
        query_string = '&'.join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
        search_url = f"{base_url}?{query_string}"
        
        print(f"Searching Indeed: {search_url}")
        
        # Fetch multiple pages
        for page in range(3):  # First 3 pages
            page_url = f"{search_url}&start={page * 10}"
            
            try:
                response = self.session.get(page_url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                if not job_cards:
                    # Try alternative selectors
                    job_cards = soup.find_all('div', {'class': lambda x: x and 'jobsearch-ResultsList' in x})
                    if not job_cards:
                        job_cards = soup.select('[data-jk]')
                
                print(f"Page {page + 1}: Found {len(job_cards)} jobs")
                
                for card in job_cards:
                    job_data = self._extract_job_data(card, soup)
                    if job_data:
                        jobs.append(job_data)
                
                self.random_delay(2, 4)
                
            except Exception as e:
                print(f"Error fetching page {page + 1}: {e}")
                continue
        
        return jobs
    
    def _extract_job_data(self, card, soup) -> Optional[Dict]:
        """Extract job data from Indeed job card"""
        try:
            # Extract job ID
            job_id = card.get('data-jk', '')
            if not job_id:
                # Try to find in link
                link = card.find('a', href=True)
                if link and 'jk=' in link['href']:
                    job_id = link['href'].split('jk=')[-1].split('&')[0]
                else:
                    job_id = hashlib.md5(str(card)[:100].encode()).hexdigest()[:12]
            
            # Title
            title_elem = card.find('h2', class_='jobTitle') or card.find('a', {'data-jk': True})
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            title = title.replace('new', '').strip()  # Remove 'new' badge
            
            # Company
            company_elem = card.find('span', {'data-testid': 'company-name'}) or \
                          card.find('span', class_='companyName')
            company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
            
            # Location
            location_elem = card.find('div', {'data-testid': 'text-location'}) or \
                           card.find('div', class_='companyLocation')
            location = location_elem.get_text(strip=True) if location_elem else ""
            
            # Salary (if available)
            salary_elem = card.find('div', class_='salary-snippet') or \
                         card.find('div', {'data-testid': 'attribute_snippet_testid'})
            salary = salary_elem.get_text(strip=True) if salary_elem else ""
            
            # Description snippet
            desc_elem = card.find('div', class_='job-snippet') or \
                       card.find('ul', style=lambda x: x and 'list-style' in str(x))
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Job URL
            link_elem = card.find('a', href=True)
            job_url = ""
            if link_elem:
                href = link_elem['href']
                if href.startswith('/'):
                    job_url = f"https://fr.indeed.com{href}"
                else:
                    job_url = href
            
            # Posted date
            date_elem = card.find('span', class_='date') or \
                       card.find('span', {'data-testid': 'myJobsStateDate'})
            posted_date = date_elem.get_text(strip=True) if date_elem else ""
            
            return {
                'job_id': f"indeed_{job_id}",
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'description': description[:500],
                'url': job_url,
                'source': 'indeed',
                'posted_date': posted_date,
                'easy_apply': False  # Indeed doesn't have easy apply like LinkedIn
            }
            
        except Exception as e:
            print(f"Error parsing job card: {e}")
            return None
    
    def get_job_details(self, job_url: str) -> Dict:
        """Get full job details from job page"""
        try:
            response = self.session.get(job_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Full description
            desc_div = soup.find('div', id='jobDescriptionText') or \
                      soup.find('div', class_='jobsearch-jobDescriptionText')
            full_description = desc_div.get_text(strip=True) if desc_div else ""
            
            # Requirements
            requirements = []
            for li in soup.find_all('li'):
                text = li.get_text(strip=True)
                if any(kw in text.lower() for kw in ['require', 'experience', 'skill', 'must']):
                    requirements.append(text)
            
            return {
                'full_description': full_description,
                'requirements': requirements[:10]  # First 10 requirements
            }
            
        except Exception as e:
            print(f"Error getting job details: {e}")
            return {}
    
    def apply_to_job(self, job_url: str, profile: dict) -> Tuple[bool, List[Dict]]:
        """
        Apply to a job on Indeed (opens application page)
        Indeed typically redirects to company website for applications
        
        Returns:
            Tuple[bool, List[Dict]]: (success, complex_questions)
        """
        try:
            self.setup_driver()
            self.driver.get(job_url)
            self.random_delay(2, 4)
            
            # Find Apply button
            apply_btn = None
            selectors = [
                'button#applyButtonLinkContainer',
                'button.ia-IndeedApplyButton',
                'a[href*="apply"]',
                'button[aria-label*="Apply"]'
            ]
            
            for selector in selectors:
                try:
                    apply_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if apply_btn:
                apply_btn.click()
                self.random_delay(2, 4)
                
                # Check if Indeed Apply or external
                current_url = self.driver.current_url
                if 'indeed.com' in current_url:
                    print("Indeed Apply detected - filling form...")
                    return self._fill_indeed_application(profile)
                else:
                    print(f"External application - redirected to: {current_url}")
                    # Could add company-specific handling here
                    return False, []
            else:
                print("Apply button not found")
                return False, []
                
        except Exception as e:
            print(f"Apply error: {e}")
            return False, []
    
    def _fill_indeed_application(self, profile: dict) -> Tuple[bool, List[Dict]]:
        """Fill Indeed's application form"""
        try:
            # Check for complex questions before proceeding
            complex_questions = self._detect_complex_questions()
            if complex_questions:
                print(f" Detected {len(complex_questions)} complex question(s) - pausing application")
                return False, complex_questions
            
            # If we found application form, try to fill it
            # This is basic - many Indeed applications redirect to company sites
            print(" Application process may require manual completion")
            return False, []
            
        except Exception as e:
            print(f"Form fill error: {e}")
            return False, []
    
    def _detect_complex_questions(self) -> List[Dict]:
        """Detect complex questions in Indeed application forms"""
        complex_questions = []
        
        try:
            # Find all form elements
            form_elements = self.driver.find_elements(By.CSS_SELECTOR, 'input, textarea, select')
            
            for element in form_elements:
                if self._is_complex_question(element):
                    question_text = self._get_question_text(element)
                    if question_text:
                        complex_questions.append({
                            'text': question_text,
                            'element_type': element.tag_name,
                            'detected_at': datetime.now().isoformat()
                        })
        
        except Exception as e:
            print(f"Error detecting questions: {e}")
        
        return complex_questions
    
    def _is_complex_question(self, element) -> bool:
        """Check if a form element represents a complex question"""
        try:
            tag = element.tag_name
            
            # Textareas are complex
            if tag == 'textarea':
                return True
            
            # Check input fields
            if tag == 'input':
                input_type = element.get_attribute('type') or 'text'
                
                # Simple types
                if input_type in ['checkbox', 'radio', 'hidden', 'submit', 'button', 'email', 'tel']:
                    return False
                
                # Text inputs - check for complexity
                if input_type == 'text':
                    text = self._get_question_text(element).lower()
                    
                    complex_keywords = [
                        'why', 'describe', 'explain', 'tell us', 'tell me',
                        'experience', 'motivation', 'interest',
                        'what makes', 'how would', 'provide details',
                        'elaborate', 'summary', 'qualifications'
                    ]
                    
                    return any(keyword in text for keyword in complex_keywords)
            
            return False
            
        except:
            return False
    
    def _get_question_text(self, element) -> str:
        """Extract question text from form element"""
        try:
            # Try multiple sources
            sources = [
                element.get_attribute('placeholder'),
                element.get_attribute('aria-label'),
                element.get_attribute('label'),
                element.get_attribute('title')
            ]
            
            # Try to find label
            try:
                element_id = element.get_attribute('id')
                if element_id:
                    label = self.driver.find_element(By.CSS_SELECTOR, f'label[for="{element_id}"]')
                    sources.append(label.text)
            except:
                pass
            
            # Return first non-empty
            for text in sources:
                if text and text.strip():
                    return text.strip()
            
            return ''
        except:
            return ''
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")


def test_indeed():
    """Test Indeed bot"""
    bot = IndeedBot(headless=False)
    
    jobs = bot.search_jobs(
        keywords="Python Developer",
        location="Paris",
        posted_within_days=7,
        remote=True
    )
    
    print(f"\nFound {len(jobs)} jobs on Indeed:")
    for job in jobs[:10]:
        print(f"  - {job['title']} at {job['company']} ({job['location']})")
        if job['salary']:
            print(f"    Salary: {job['salary']}")
    
    bot.close()


if __name__ == "__main__":
    test_indeed()
