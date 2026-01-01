"""
LinkedIn Job Search and Apply Bot
Uses Selenium for browser automation
"""

import time
import random
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    ElementClickInterceptedException
)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class LinkedInBot:
    def __init__(self, email: str, password: str, headless: bool = False):
        self.email = email
        self.password = password
        self.driver = None
        self.headless = headless
        self.logged_in = False
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add user agent to appear more human
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def random_delay(self, min_sec: float = 1, max_sec: float = 3):
        """Add random delay to appear more human"""
        time.sleep(random.uniform(min_sec, max_sec))
        
    def login(self) -> bool:
        """Login to LinkedIn"""
        try:
            self.setup_driver()
            self.driver.get('https://www.linkedin.com/login')
            self.random_delay(2, 4)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            email_field.send_keys(self.email)
            self.random_delay()
            
            # Enter password
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(self.password)
            self.random_delay()
            
            # Click login
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            
            # Wait for login to complete
            self.random_delay(3, 5)
            
            # Check if login successful
            if 'feed' in self.driver.current_url or 'mynetwork' in self.driver.current_url:
                self.logged_in = True
                print("✅ Successfully logged in to LinkedIn")
                return True
            else:
                print("❌ Login may have failed - check for security verification")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def search_jobs(self, keywords: str, location: str, easy_apply_only: bool = True, 
                    posted_within: str = "week") -> List[Dict]:
        """Search for jobs on LinkedIn"""
        if not self.logged_in:
            print("Please login first")
            return []
        
        jobs = []
        
        try:
            # Build search URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}"
            
            if easy_apply_only:
                search_url += "&f_AL=true"  # Easy Apply filter
            
            # Time posted filter
            time_filters = {
                "day": "&f_TPR=r86400",
                "week": "&f_TPR=r604800",
                "month": "&f_TPR=r2592000"
            }
            if posted_within in time_filters:
                search_url += time_filters[posted_within]
            
            self.driver.get(search_url)
            self.random_delay(3, 5)
            
            # Scroll to load more jobs
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay(1, 2)
            
            # Find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, '.job-card-container')
            
            print(f"Found {len(job_cards)} job listings")
            
            for card in job_cards[:25]:  # Limit to first 25
                try:
                    job_data = self._extract_job_data(card)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    print(f"Error extracting job: {e}")
                    continue
                    
        except Exception as e:
            print(f"Search error: {e}")
        
        return jobs
    
    def _extract_job_data(self, card) -> Optional[Dict]:
        """Extract job data from a job card"""
        try:
            # Click on job card to load details
            card.click()
            self.random_delay(1, 2)
            
            # Extract basic info
            title = card.find_element(By.CSS_SELECTOR, '.job-card-list__title').text
            company = card.find_element(By.CSS_SELECTOR, '.job-card-container__company-name').text
            location = card.find_element(By.CSS_SELECTOR, '.job-card-container__metadata-item').text
            
            # Try to get job URL
            try:
                job_link = card.find_element(By.CSS_SELECTOR, 'a.job-card-container__link')
                job_url = job_link.get_attribute('href')
                job_id = job_url.split('/')[-2] if job_url else None
            except:
                job_url = self.driver.current_url
                job_id = hashlib.md5(f"{title}{company}".encode()).hexdigest()[:12]
            
            # Try to get description from detail panel
            description = ""
            try:
                desc_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.jobs-description__content'))
                )
                description = desc_element.text[:500]  # First 500 chars
            except:
                pass
            
            # Check for Easy Apply button
            easy_apply = False
            try:
                self.driver.find_element(By.CSS_SELECTOR, '.jobs-apply-button--top-card')
                easy_apply = True
            except:
                pass
            
            return {
                'job_id': f"linkedin_{job_id}",
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'url': job_url,
                'source': 'linkedin',
                'easy_apply': easy_apply,
                'posted_date': datetime.now().isoformat(),
                'salary': ''  # LinkedIn often doesn't show salary
            }
            
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None
    
    def apply_easy_apply(self, job_url: str, resume_path: str = None) -> Tuple[bool, List[Dict]]:
        """Apply to a job using Easy Apply
        
        Returns:
            Tuple[bool, List[Dict]]: (success, complex_questions)
            - success: Whether application was submitted
            - complex_questions: List of complex questions that need user input
        """
        try:
            self.driver.get(job_url)
            self.random_delay(2, 4)
            
            # Find Easy Apply button
            easy_apply_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.jobs-apply-button'))
            )
            easy_apply_btn.click()
            self.random_delay(2, 3)
            
            # Handle multi-step application
            complex_questions = []
            max_steps = 10
            step_count = 0
            
            while step_count < max_steps:
                step_count += 1
                
                # Check for questions on current page
                detected_complex = self._detect_complex_questions()
                if detected_complex:
                    complex_questions.extend(detected_complex)
                    print(f"⚠️ Detected {len(detected_complex)} complex question(s) - pausing application")
                    return (False, complex_questions)
                
                try:
                    # Look for next/submit button
                    next_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Continue to next step"]')
                    next_btn.click()
                    self.random_delay(1, 2)
                except NoSuchElementException:
                    pass
                
                try:
                    # Look for review button
                    review_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Review your application"]')
                    review_btn.click()
                    self.random_delay(1, 2)
                except NoSuchElementException:
                    pass
                
                try:
                    # Look for submit button
                    submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Submit application"]')
                    submit_btn.click()
                    self.random_delay(2, 3)
                    print("✅ Application submitted!")
                    return (True, [])
                except NoSuchElementException:
                    pass
                
                # Check if we're done or stuck
                try:
                    # Check for success message
                    success = self.driver.find_element(By.CSS_SELECTOR, '.artdeco-modal__header')
                    if 'submitted' in success.text.lower():
                        return (True, [])
                except:
                    pass
                
                # Timeout check
                self.random_delay(1, 2)
                break
                
            return (False, complex_questions)
            
        except Exception as e:
            print(f"Easy Apply error: {e}")
            return (False, [])
    
    def _detect_complex_questions(self) -> List[Dict]:
        """Detect complex questions that require human input
        
        Returns:
            List of complex questions with their details
        """
        complex_questions = []
        
        try:
            # Find all input fields, textareas, and labels
            form_elements = self.driver.find_elements(By.CSS_SELECTOR, 'input, textarea, select, label')
            
            for element in form_elements:
                question_type = self._classify_question(element)
                
                if question_type == 'complex':
                    # Extract question details
                    question_text = self._extract_question_text(element)
                    
                    if question_text:
                        complex_questions.append({
                            'text': question_text,
                            'element_type': element.tag_name,
                            'detected_at': datetime.now().isoformat()
                        })
        
        except Exception as e:
            print(f"Error detecting questions: {e}")
        
        return complex_questions
    
    def _classify_question(self, element) -> str:
        """Classify if a question is simple or complex
        
        Returns:
            'simple', 'complex', or 'unknown'
        """
        try:
            tag = element.tag_name
            
            # Textareas are always complex (long-form answers)
            if tag == 'textarea':
                return 'complex'
            
            # Check input fields
            if tag == 'input':
                input_type = element.get_attribute('type') or 'text'
                
                # Simple types
                if input_type in ['checkbox', 'radio', 'hidden', 'submit', 'button']:
                    return 'simple'
                
                # Text inputs - check for complexity indicators
                if input_type in ['text', 'email', 'tel', 'url']:
                    # Get associated text
                    text = self._extract_question_text(element).lower()
                    
                    # Complex keywords
                    complex_keywords = [
                        'why', 'describe', 'explain', 'tell us', 'tell me',
                        'experience with', 'motivation', 'interest in',
                        'what makes you', 'how would you', 'provide details',
                        'elaborate', 'summary', 'background', 'qualifications'
                    ]
                    
                    if any(keyword in text for keyword in complex_keywords):
                        return 'complex'
                    
                    # Check max length - long inputs suggest complex answers
                    max_length = element.get_attribute('maxlength')
                    if max_length and int(max_length) > 200:
                        return 'complex'
                
                return 'simple'
            
            # Select dropdowns are simple
            if tag == 'select':
                return 'simple'
            
            return 'unknown'
            
        except Exception as e:
            return 'unknown'
    
    def _extract_question_text(self, element) -> str:
        """Extract the question text associated with a form element"""
        try:
            # Try different methods to get question text
            text_sources = [
                element.get_attribute('placeholder'),
                element.get_attribute('aria-label'),
                element.get_attribute('label'),
                element.get_attribute('title')
            ]
            
            # Try to find associated label
            try:
                element_id = element.get_attribute('id')
                if element_id:
                    label = self.driver.find_element(By.CSS_SELECTOR, f'label[for="{element_id}"]')
                    text_sources.append(label.text)
            except:
                pass
            
            # Try parent label
            try:
                parent = element.find_element(By.XPATH, '..')
                if parent.tag_name == 'label':
                    text_sources.append(parent.text)
            except:
                pass
            
            # Return first non-empty text
            for text in text_sources:
                if text and text.strip():
                    return text.strip()
            
            return ''
            
        except Exception as e:
            return ''
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")


def test_linkedin():
    """Test LinkedIn bot"""
    from config import LINKEDIN
    
    bot = LinkedInBot(
        email=LINKEDIN['email'],
        password=LINKEDIN['password'],
        headless=False
    )
    
    if bot.login():
        jobs = bot.search_jobs(
            keywords="Python Developer",
            location="Paris",
            easy_apply_only=True
        )
        
        print(f"\nFound {len(jobs)} jobs:")
        for job in jobs:
            print(f"  - {job['title']} at {job['company']}")
    
    bot.close()


if __name__ == "__main__":
    test_linkedin()
