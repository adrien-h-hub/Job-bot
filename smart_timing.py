"""
Smart Application Timing - Apply at optimal times for better visibility
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import pytz
from config import DATABASE


class SmartTiming:
    """Determine optimal application times based on industry and location"""
    
    # Best days to apply (0=Monday, 6=Sunday)
    OPTIMAL_DAYS = [1, 2, 3]  # Tuesday, Wednesday, Thursday
    
    # Best hours to apply (company local time)
    OPTIMAL_HOURS = {
        'tech': range(8, 11),        # 8am-10am
        'finance': range(9, 12),     # 9am-11am
        'healthcare': range(7, 10),  # 7am-9am
        'retail': range(10, 13),     # 10am-12pm
        'default': range(8, 11)      # 8am-10am
    }
    
    # Timezone mapping for major cities
    CITY_TIMEZONES = {
        'paris': 'Europe/Paris',
        'london': 'Europe/London',
        'new york': 'America/New_York',
        'san francisco': 'America/Los_Angeles',
        'berlin': 'Europe/Berlin',
        'tokyo': 'Asia/Tokyo',
        'sydney': 'Australia/Sydney',
    }
    
    def __init__(self):
        pass
    
    def get_optimal_apply_time(self, job: Dict) -> datetime:
        """
        Calculate the best time to apply for a job
        
        Args:
            job: Job dictionary with title, company, location
            
        Returns:
            datetime: Optimal time to submit application
        """
        # Get company timezone
        company_tz = self._get_company_timezone(job.get('location', ''))
        
        # Determine industry from job title
        industry = self._detect_industry(job.get('title', ''))
        
        # Get optimal hours for this industry
        optimal_hours = self.OPTIMAL_HOURS.get(industry, self.OPTIMAL_HOURS['default'])
        
        # Start from current time in company timezone
        now = datetime.now(company_tz)
        next_optimal = now
        
        # Find next optimal time slot
        max_iterations = 168  # Don't search more than a week ahead
        iterations = 0
        
        while iterations < max_iterations:
            # Check if current time is optimal
            if (next_optimal.weekday() in self.OPTIMAL_DAYS and 
                next_optimal.hour in optimal_hours):
                # Found optimal time
                return next_optimal
            
            # Move to next hour
            next_optimal += timedelta(hours=1)
            iterations += 1
        
        # If no optimal time found in a week, return next business day morning
        while next_optimal.weekday() not in self.OPTIMAL_DAYS:
            next_optimal += timedelta(days=1)
        
        next_optimal = next_optimal.replace(hour=9, minute=0, second=0, microsecond=0)
        return next_optimal
    
    def _get_company_timezone(self, location: str) -> pytz.timezone:
        """
        Determine company timezone from location string
        
        Args:
            location: Location string (e.g., "Paris, France")
            
        Returns:
            pytz.timezone: Company timezone
        """
        location_lower = location.lower()
        
        # Check for known cities
        for city, tz_name in self.CITY_TIMEZONES.items():
            if city in location_lower:
                return pytz.timezone(tz_name)
        
        # Check for countries/regions
        if 'france' in location_lower or 'paris' in location_lower:
            return pytz.timezone('Europe/Paris')
        elif 'uk' in location_lower or 'london' in location_lower:
            return pytz.timezone('Europe/London')
        elif 'germany' in location_lower or 'berlin' in location_lower:
            return pytz.timezone('Europe/Berlin')
        elif 'usa' in location_lower or 'united states' in location_lower:
            return pytz.timezone('America/New_York')
        
        # Default to UTC
        return pytz.UTC
    
    def _detect_industry(self, job_title: str) -> str:
        """
        Detect industry from job title
        
        Args:
            job_title: Job title string
            
        Returns:
            str: Industry category
        """
        title_lower = job_title.lower()
        
        # Tech keywords
        tech_keywords = ['developer', 'engineer', 'programmer', 'software', 
                        'data', 'devops', 'cloud', 'python', 'java', 'tech']
        if any(keyword in title_lower for keyword in tech_keywords):
            return 'tech'
        
        # Finance keywords
        finance_keywords = ['analyst', 'finance', 'banking', 'investment', 
                           'accountant', 'financial']
        if any(keyword in title_lower for keyword in finance_keywords):
            return 'finance'
        
        # Healthcare keywords
        healthcare_keywords = ['nurse', 'doctor', 'medical', 'healthcare', 
                              'clinical', 'physician']
        if any(keyword in title_lower for keyword in healthcare_keywords):
            return 'healthcare'
        
        # Retail keywords
        retail_keywords = ['retail', 'sales', 'store', 'customer service']
        if any(keyword in title_lower for keyword in retail_keywords):
            return 'retail'
        
        return 'default'
    
    def should_apply_now(self, job: Dict) -> bool:
        """
        Check if current time is optimal for applying
        
        Args:
            job: Job dictionary
            
        Returns:
            bool: True if should apply now, False if should queue
        """
        optimal_time = self.get_optimal_apply_time(job)
        now = datetime.now(optimal_time.tzinfo)
        
        # If optimal time is within next 2 hours, apply now
        time_diff = (optimal_time - now).total_seconds() / 3600
        
        return time_diff <= 2
    
    def get_time_until_optimal(self, job: Dict) -> timedelta:
        """
        Get time remaining until optimal application time
        
        Args:
            job: Job dictionary
            
        Returns:
            timedelta: Time until optimal application time
        """
        optimal_time = self.get_optimal_apply_time(job)
        now = datetime.now(optimal_time.tzinfo)
        
        return optimal_time - now
    
    def format_optimal_time(self, job: Dict) -> str:
        """
        Get human-readable optimal application time
        
        Args:
            job: Job dictionary
            
        Returns:
            str: Formatted optimal time string
        """
        optimal_time = self.get_optimal_apply_time(job)
        time_until = self.get_time_until_optimal(job)
        
        # Format the time
        formatted = optimal_time.strftime('%A, %B %d at %I:%M %p %Z')
        
        # Add relative time
        hours = int(time_until.total_seconds() / 3600)
        if hours < 1:
            relative = "now"
        elif hours < 24:
            relative = f"in {hours} hours"
        else:
            days = hours // 24
            relative = f"in {days} days"
        
        return f"{formatted} ({relative})"


# Example usage and testing
if __name__ == "__main__":
    timing = SmartTiming()
    
    # Test jobs
    test_jobs = [
        {
            'title': 'Python Developer',
            'company': 'Tech Corp',
            'location': 'Paris, France'
        },
        {
            'title': 'Financial Analyst',
            'company': 'Bank Inc',
            'location': 'London, UK'
        },
        {
            'title': 'Sales Manager',
            'company': 'Retail Co',
            'location': 'New York, USA'
        }
    ]
    
    print("Smart Application Timing - Test Results")
    print("=" * 60)
    
    for job in test_jobs:
        print(f"\nJob: {job['title']} at {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Optimal time: {timing.format_optimal_time(job)}")
        print(f"Apply now? {timing.should_apply_now(job)}")
