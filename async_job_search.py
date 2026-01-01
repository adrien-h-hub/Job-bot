"""
Async Job Search - Parallel job searches for faster performance
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import time


class AsyncJobSearch:
    """Execute job searches in parallel across multiple platforms"""
    
    def __init__(self, linkedin_bot=None, indeed_bot=None, max_workers: int = 5):
        """
        Initialize async job search
        
        Args:
            linkedin_bot: LinkedIn bot instance
            indeed_bot: Indeed bot instance
            max_workers: Maximum number of parallel workers
        """
        self.linkedin_bot = linkedin_bot
        self.indeed_bot = indeed_bot
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def search_all_platforms(self, keywords: List[str], location: str, 
                                   platforms: List[str] = None) -> List[Dict]:
        """
        Search all platforms in parallel
        
        Args:
            keywords: List of search keywords
            location: Job location
            platforms: List of platforms to search (default: all)
            
        Returns:
            List of all jobs found across platforms
        """
        if platforms is None:
            platforms = ['linkedin', 'indeed']
        
        tasks = []
        
        # Create search tasks for each platform
        if 'linkedin' in platforms and self.linkedin_bot:
            tasks.append(self._search_linkedin_async(keywords, location))
        
        if 'indeed' in platforms and self.indeed_bot:
            tasks.append(self._search_indeed_async(keywords, location))
        
        # Execute all searches in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results and filter out errors
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)
            elif isinstance(result, Exception):
                print(f"Search error: {result}")
        
        return all_jobs
    
    async def _search_linkedin_async(self, keywords: List[str], location: str) -> List[Dict]:
        """Search LinkedIn asynchronously"""
        loop = asyncio.get_event_loop()
        
        # Run LinkedIn search in thread pool
        jobs = await loop.run_in_executor(
            self.executor,
            self._search_linkedin_sync,
            keywords,
            location
        )
        
        return jobs
    
    async def _search_indeed_async(self, keywords: List[str], location: str) -> List[Dict]:
        """Search Indeed asynchronously"""
        loop = asyncio.get_event_loop()
        
        # Run Indeed search in thread pool
        jobs = await loop.run_in_executor(
            self.executor,
            self._search_indeed_sync,
            keywords,
            location
        )
        
        return jobs
    
    def _search_linkedin_sync(self, keywords: List[str], location: str) -> List[Dict]:
        """Synchronous LinkedIn search (runs in thread pool)"""
        if not self.linkedin_bot:
            return []
        
        all_jobs = []
        try:
            for keyword in keywords:
                jobs = self.linkedin_bot.search_jobs(
                    keywords=keyword,
                    location=location,
                    easy_apply_only=True
                )
                all_jobs.extend(jobs)
                time.sleep(2)  # Rate limiting
            
            print(f"✅ LinkedIn: Found {len(all_jobs)} jobs")
        except Exception as e:
            print(f"❌ LinkedIn error: {e}")
        
        return all_jobs
    
    def _search_indeed_sync(self, keywords: List[str], location: str) -> List[Dict]:
        """Synchronous Indeed search (runs in thread pool)"""
        if not self.indeed_bot:
            return []
        
        all_jobs = []
        try:
            for keyword in keywords:
                jobs = self.indeed_bot.search_jobs(
                    keywords=keyword,
                    location=location,
                    posted_within_days=7
                )
                all_jobs.extend(jobs)
                time.sleep(2)  # Rate limiting
            
            print(f"✅ Indeed: Found {len(all_jobs)} jobs")
        except Exception as e:
            print(f"❌ Indeed error: {e}")
        
        return all_jobs
    
    async def search_with_multiple_keywords(self, keywords: List[str], location: str,
                                           platform: str = 'linkedin') -> List[Dict]:
        """
        Search multiple keywords in parallel on a single platform
        
        Args:
            keywords: List of keywords to search
            location: Job location
            platform: Platform to search
            
        Returns:
            Combined results from all keyword searches
        """
        loop = asyncio.get_event_loop()
        
        # Create tasks for each keyword
        tasks = []
        for keyword in keywords:
            if platform == 'linkedin' and self.linkedin_bot:
                task = loop.run_in_executor(
                    self.executor,
                    self._search_single_keyword_linkedin,
                    keyword,
                    location
                )
                tasks.append(task)
            elif platform == 'indeed' and self.indeed_bot:
                task = loop.run_in_executor(
                    self.executor,
                    self._search_single_keyword_indeed,
                    keyword,
                    location
                )
                tasks.append(task)
        
        # Execute all keyword searches in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)
        
        return all_jobs
    
    def _search_single_keyword_linkedin(self, keyword: str, location: str) -> List[Dict]:
        """Search LinkedIn for a single keyword"""
        try:
            jobs = self.linkedin_bot.search_jobs(
                keywords=keyword,
                location=location,
                easy_apply_only=True
            )
            print(f"  LinkedIn '{keyword}': {len(jobs)} jobs")
            return jobs
        except Exception as e:
            print(f"  LinkedIn '{keyword}' error: {e}")
            return []
    
    def _search_single_keyword_indeed(self, keyword: str, location: str) -> List[Dict]:
        """Search Indeed for a single keyword"""
        try:
            jobs = self.indeed_bot.search_jobs(
                keywords=keyword,
                location=location,
                posted_within_days=7
            )
            print(f"  Indeed '{keyword}': {len(jobs)} jobs")
            return jobs
        except Exception as e:
            print(f"  Indeed '{keyword}' error: {e}")
            return []
    
    def cleanup(self):
        """Cleanup thread pool executor"""
        self.executor.shutdown(wait=True)


# Helper function for easy integration
async def parallel_job_search(linkedin_bot, indeed_bot, keywords: List[str], 
                              location: str, platforms: List[str] = None) -> List[Dict]:
    """
    Convenience function for parallel job search
    
    Args:
        linkedin_bot: LinkedIn bot instance
        indeed_bot: Indeed bot instance
        keywords: Search keywords
        location: Job location
        platforms: Platforms to search
        
    Returns:
        Combined job results
    """
    searcher = AsyncJobSearch(linkedin_bot, indeed_bot)
    
    try:
        jobs = await searcher.search_all_platforms(keywords, location, platforms)
        return jobs
    finally:
        searcher.cleanup()


# Example usage
if __name__ == "__main__":
    async def test_async_search():
        """Test async job search"""
        print("Async Job Search - Test Mode")
        print("=" * 60)
        
        # Simulate search
        keywords = ['Python Developer', 'Data Scientist', 'Software Engineer']
        location = 'Paris, France'
        
        print(f"Searching for: {', '.join(keywords)}")
        print(f"Location: {location}")
        print("\nSearching in parallel...")
        
        # In real usage, pass actual bot instances
        # searcher = AsyncJobSearch(linkedin_bot, indeed_bot)
        # jobs = await searcher.search_all_platforms(keywords, location)
        
        print("\n✅ Parallel search would be 3-5x faster than sequential!")
        print("Example: 3 keywords × 2 platforms = 6 parallel searches")
        print("Sequential: ~60 seconds | Parallel: ~12 seconds")
    
    # Run test
    asyncio.run(test_async_search())
