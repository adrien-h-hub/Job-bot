"""
Glassdoor Bot - Search jobs on Glassdoor with company reviews
"""

import time
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import requests


class GlassdoorBot:
    """Scrape jobs from Glassdoor with company ratings"""
    
    def __init__(self, headless: bool = True):
        """
        Initialize Glassdoor bot
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver = None
        self.base_url = "https://www.glassdoor.com"
    
    def setup_driver(self):
        """Setup Selenium WebDriver"""
        if self.driver:
            return
        
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def search_jobs(self, keywords: str, location: str, 
                   posted_within_days: int = 7) -> List[Dict]:
        """
        Search for jobs on Glassdoor
        
        Args:
            keywords: Job search keywords
            location: Job location
            posted_within_days: Filter by posting date
            
        Returns:
            List of job dictionaries with company ratings
        """
        self.setup_driver()
        
        jobs = []
        
        try:
            # Build search URL
            search_url = f"{self.base_url}/Job/jobs.htm?sc.keyword={keywords.replace(' ', '+')}&locT=C&locId=&locKeyword={location.replace(' ', '+')}"
            
            print(f"Searching Glassdoor: {keywords} in {location}")
            self.driver.get(search_url)
            time.sleep(3)
            
            # Handle cookie consent if present
            try:
                cookie_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-test="close-gdpr"]')
                cookie_btn.click()
                time.sleep(1)
            except:
                pass
            
            # Scroll to load more jobs
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Extract job listings
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, 'li[data-test="jobListing"]')
            
            for card in job_cards[:20]:  # Limit to 20 jobs
                try:
                    job_data = self._extract_job_data(card)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    print(f"Error extracting job: {e}")
                    continue
            
            print(f"Found {len(jobs)} jobs on Glassdoor")
            
        except Exception as e:
            print(f"Glassdoor search error: {e}")
        
        return jobs
    
    def _extract_job_data(self, card) -> Optional[Dict]:
        """Extract job data from a job card element"""
        try:
            # Job title
            title_elem = card.find_element(By.CSS_SELECTOR, 'a[data-test="job-link"]')
            title = title_elem.text.strip()
            url = title_elem.get_attribute('href')
            
            # Company name
            company_elem = card.find_element(By.CSS_SELECTOR, 'div[data-test="employer-name"]')
            company = company_elem.text.strip()
            
            # Location
            try:
                location_elem = card.find_element(By.CSS_SELECTOR, 'div[data-test="emp-location"]')
                location = location_elem.text.strip()
            except:
                location = "Not specified"
            
            # Salary (if available)
            salary = None
            try:
                salary_elem = card.find_element(By.CSS_SELECTOR, 'div[data-test="detailSalary"]')
                salary = salary_elem.text.strip()
            except:
                pass
            
            # Company rating
            rating = None
            try:
                rating_elem = card.find_element(By.CSS_SELECTOR, 'span[data-test="rating"]')
                rating = float(rating_elem.text.strip())
            except:
                pass
            
            # Job description preview
            try:
                desc_elem = card.find_element(By.CSS_SELECTOR, 'div[data-test="job-description"]')
                description = desc_elem.text.strip()
            except:
                description = ""
            
            # Generate unique job ID
            job_id = f"glassdoor_{hash(url)}"
            
            job_data = {
                'job_id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'description': description,
                'url': url if url.startswith('http') else f"{self.base_url}{url}",
                'source': 'glassdoor',
                'company_rating': rating,
                'posted_date': 'Recent',
                'easy_apply': False  # Glassdoor doesn't have easy apply
            }
            
            return job_data
            
        except Exception as e:
            print(f"Error parsing job card: {e}")
            return None
    
    def get_company_reviews(self, company_name: str) -> Dict:
        """
        Get company reviews and ratings
        
        Args:
            company_name: Company name
            
        Returns:
            Dict with company ratings and reviews
        """
        try:
            # Search for company
            search_url = f"{self.base_url}/Search/results.htm?keyword={company_name.replace(' ', '+')}"
            
            self.setup_driver()
            self.driver.get(search_url)
            time.sleep(2)
            
            # Click on first company result
            try:
                company_link = self.driver.find_element(By.CSS_SELECTOR, 'a[data-test="employer-link"]')
                company_link.click()
                time.sleep(3)
            except:
                return {'error': 'Company not found'}
            
            # Extract ratings
            reviews_data = {
                'company_name': company_name,
                'overall_rating': None,
                'culture_rating': None,
                'work_life_balance': None,
                'career_opportunities': None,
                'compensation': None,
                'recommend_to_friend': None,
                'ceo_approval': None,
                'total_reviews': 0
            }
            
            # Overall rating
            try:
                rating_elem = self.driver.find_element(By.CSS_SELECTOR, 'div[data-test="rating"]')
                reviews_data['overall_rating'] = float(rating_elem.text.strip())
            except:
                pass
            
            # Review count
            try:
                count_elem = self.driver.find_element(By.CSS_SELECTOR, 'div[data-test="review-count"]')
                count_text = count_elem.text.strip()
                reviews_data['total_reviews'] = int(''.join(filter(str.isdigit, count_text)))
            except:
                pass
            
            return reviews_data
            
        except Exception as e:
            print(f"Error getting company reviews: {e}")
            return {'error': str(e)}
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None


# Example usage
if __name__ == "__main__":
    bot = GlassdoorBot(headless=False)
    
    try:
        # Search for jobs
        jobs = bot.search_jobs("Python Developer", "Paris, France")
        
        print("\n" + "="*60)
        print("GLASSDOOR JOB SEARCH RESULTS")
        print("="*60)
        
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            if job.get('company_rating'):
                print(f"   Rating: ⭐ {job['company_rating']}/5.0")
            print(f"   Location: {job['location']}")
            if job.get('salary'):
                print(f"   Salary: {job['salary']}")
            print(f"   URL: {job['url'][:60]}...")
        
        # Get company reviews for first job
        if jobs:
            company = jobs[0]['company']
            print(f"\n\nGetting reviews for {company}...")
            reviews = bot.get_company_reviews(company)
            
            if 'error' not in reviews:
                print(f"\nCompany: {reviews['company_name']}")
                print(f"Overall Rating: {reviews['overall_rating']}/5.0")
                print(f"Total Reviews: {reviews['total_reviews']}")
    
    finally:
        bot.close()
