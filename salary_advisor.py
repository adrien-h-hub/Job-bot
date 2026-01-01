"""
Salary Negotiation Advisor - Market data analysis and negotiation strategies
"""

from typing import Dict, List, Optional
import statistics


class SalaryAdvisor:
    """Analyze salary offers and provide negotiation guidance"""
    
    def __init__(self):
        """Initialize salary advisor"""
        # Market data by role and location (simplified - real version would scrape live data)
        self.market_data = {
            'python_developer': {
                'paris': {'min': 45000, 'median': 60000, 'max': 85000},
                'london': {'min': 50000, 'median': 70000, 'max': 100000},
                'new_york': {'min': 80000, 'median': 120000, 'max': 180000}
            },
            'data_scientist': {
                'paris': {'min': 50000, 'median': 70000, 'max': 100000},
                'london': {'min': 60000, 'median': 85000, 'max': 120000},
                'new_york': {'min': 90000, 'median': 130000, 'max': 200000}
            },
            'software_engineer': {
                'paris': {'min': 40000, 'median': 55000, 'max': 80000},
                'london': {'min': 45000, 'median': 65000, 'max': 95000},
                'new_york': {'min': 75000, 'median': 110000, 'max': 170000}
            }
        }
    
    def analyze_offer(self, job: Dict, offer_amount: float, profile: Dict) -> Dict:
        """
        Analyze job offer and suggest negotiation strategy
        
        Args:
            job: Job details
            offer_amount: Offered salary
            profile: User profile with experience
            
        Returns:
            Dict with analysis and recommendations
        """
        # Get market data
        market_data = self._get_market_data(
            title=job.get('title', ''),
            location=job.get('location', ''),
            experience=profile.get('years_experience', 0)
        )
        
        # Calculate position in market
        percentile = self._calculate_percentile(offer_amount, market_data)
        
        # Suggest counter offer
        counter_offer = self._suggest_counter_offer(offer_amount, market_data, profile)
        
        # Generate negotiation script
        script = self._generate_negotiation_script(offer_amount, counter_offer, job)
        
        # Identify leverage points
        leverage = self._identify_leverage(job, profile, market_data)
        
        analysis = {
            'offer_amount': offer_amount,
            'market_data': market_data,
            'percentile': percentile,
            'assessment': self._assess_offer(percentile),
            'counter_offer': counter_offer,
            'negotiation_script': script,
            'leverage_points': leverage,
            'total_comp_considerations': self._get_total_comp_factors(),
            'negotiation_tips': self._get_negotiation_tips()
        }
        
        return analysis
    
    def _get_market_data(self, title: str, location: str, experience: int) -> Dict:
        """Get market salary data for role and location"""
        # Normalize inputs
        role_key = self._normalize_role(title)
        location_key = self._normalize_location(location)
        
        # Get base market data
        if role_key in self.market_data and location_key in self.market_data[role_key]:
            base_data = self.market_data[role_key][location_key]
        else:
            # Default data
            base_data = {'min': 40000, 'median': 60000, 'max': 90000}
        
        # Adjust for experience
        experience_multiplier = 1 + (experience * 0.05)  # 5% per year
        
        adjusted_data = {
            'min': int(base_data['min'] * experience_multiplier),
            'median': int(base_data['median'] * experience_multiplier),
            'max': int(base_data['max'] * experience_multiplier),
            'p25': int(base_data['min'] * 1.15 * experience_multiplier),
            'p75': int(base_data['max'] * 0.85 * experience_multiplier)
        }
        
        return adjusted_data
    
    def _normalize_role(self, title: str) -> str:
        """Normalize job title to match market data"""
        title_lower = title.lower()
        
        if 'python' in title_lower or 'django' in title_lower:
            return 'python_developer'
        elif 'data scientist' in title_lower or 'machine learning' in title_lower:
            return 'data_scientist'
        elif 'software' in title_lower or 'developer' in title_lower:
            return 'software_engineer'
        else:
            return 'software_engineer'  # Default
    
    def _normalize_location(self, location: str) -> str:
        """Normalize location to match market data"""
        location_lower = location.lower()
        
        if 'paris' in location_lower or 'france' in location_lower:
            return 'paris'
        elif 'london' in location_lower or 'uk' in location_lower:
            return 'london'
        elif 'new york' in location_lower or 'nyc' in location_lower:
            return 'new_york'
        else:
            return 'paris'  # Default
    
    def _calculate_percentile(self, offer: float, market_data: Dict) -> int:
        """Calculate which percentile the offer falls into"""
        if offer <= market_data['min']:
            return 10
        elif offer <= market_data['p25']:
            return 25
        elif offer <= market_data['median']:
            return 50
        elif offer <= market_data['p75']:
            return 75
        elif offer <= market_data['max']:
            return 90
        else:
            return 95
    
    def _assess_offer(self, percentile: int) -> str:
        """Assess quality of offer based on percentile"""
        if percentile >= 75:
            return "Excellent offer - above market rate"
        elif percentile >= 50:
            return "Good offer - at market rate"
        elif percentile >= 25:
            return "Fair offer - below market median"
        else:
            return "Low offer - significantly below market"
    
    def _suggest_counter_offer(self, offer: float, market_data: Dict, profile: Dict) -> Dict:
        """Suggest counter offer amount and strategy"""
        # Target 75th percentile or 10-15% above offer
        target_high = market_data['p75']
        target_percentage = offer * 1.15
        
        suggested_counter = min(target_high, target_percentage)
        
        # Minimum acceptable (median)
        minimum_acceptable = market_data['median']
        
        return {
            'suggested_amount': int(suggested_counter),
            'minimum_acceptable': int(minimum_acceptable),
            'negotiation_range': f"€{int(minimum_acceptable):,} - €{int(suggested_counter):,}",
            'strategy': self._get_counter_strategy(offer, suggested_counter)
        }
    
    def _get_counter_strategy(self, offer: float, counter: float) -> str:
        """Get negotiation strategy based on gap"""
        gap_percentage = ((counter - offer) / offer) * 100
        
        if gap_percentage > 20:
            return "Large gap - emphasize value and market data. Be prepared to justify."
        elif gap_percentage > 10:
            return "Moderate gap - highlight specific skills and achievements."
        else:
            return "Small gap - straightforward negotiation likely to succeed."
    
    def _generate_negotiation_script(self, offer: float, counter_data: Dict, job: Dict) -> str:
        """Generate negotiation conversation script"""
        counter = counter_data['suggested_amount']
        
        script = f"""SALARY NEGOTIATION SCRIPT

Opening (Express Gratitude):
"Thank you so much for the offer. I'm very excited about the opportunity to join {job.get('company', 'the team')} as a {job.get('title', 'team member')}."

State Your Case:
"I've done some research on market rates for this role, and based on my {job.get('experience', 'experience')} and the value I can bring, I was hoping we could discuss the compensation."

Make Your Counter:
"Based on my research and the scope of responsibilities, I was thinking more in the range of €{counter:,}. Is there flexibility in the budget?"

Justify Your Ask:
"This is based on:
- Market data for {job.get('title', 'this role')} in {job.get('location', 'this area')}
- My {job.get('experience', 'relevant experience')}
- The additional value I bring through {job.get('skills', 'my specialized skills')}"

If They Can't Meet Your Number:
"I understand budget constraints. Are there other aspects of the compensation package we could discuss? Such as:
- Signing bonus
- Performance bonus structure
- Additional vacation days
- Professional development budget
- Remote work flexibility
- Earlier salary review"

Closing:
"I'm very interested in this role and I'm confident we can find a number that works for both of us. What are your thoughts?"

REMEMBER:
- Stay positive and collaborative
- Don't accept immediately - ask for time to consider
- Get everything in writing
- Be prepared to walk away if needed"""
        
        return script
    
    def _identify_leverage(self, job: Dict, profile: Dict, market_data: Dict) -> List[str]:
        """Identify negotiation leverage points"""
        leverage_points = []
        
        # Experience-based leverage
        if profile.get('years_experience', 0) > 5:
            leverage_points.append(f"Extensive experience ({profile['years_experience']} years)")
        
        # Skills-based leverage
        if profile.get('skills'):
            leverage_points.append(f"Specialized skills: {profile['skills']}")
        
        # Achievement-based leverage
        if profile.get('achievements'):
            leverage_points.append(f"Proven track record: {profile['achievements']}")
        
        # Market-based leverage
        leverage_points.append("Current market demand for this role")
        
        # Other offers (if applicable)
        leverage_points.append("Multiple opportunities (if true)")
        
        # Unique value
        leverage_points.append("Unique combination of skills and experience")
        
        return leverage_points
    
    def _get_total_comp_factors(self) -> List[str]:
        """Get factors to consider beyond base salary"""
        return [
            "Base Salary",
            "Annual Bonus (% of base)",
            "Signing Bonus",
            "Stock Options/Equity",
            "Health Insurance Coverage",
            "Retirement Contributions (401k, pension)",
            "Vacation Days",
            "Remote Work Flexibility",
            "Professional Development Budget",
            "Gym/Wellness Benefits",
            "Commuter Benefits",
            "Meal Allowance",
            "Phone/Internet Reimbursement",
            "Relocation Assistance",
            "Performance Review Schedule"
        ]
    
    def _get_negotiation_tips(self) -> List[str]:
        """Get general negotiation tips"""
        return [
            "Never accept the first offer immediately",
            "Let them make the first number",
            "Always negotiate - most offers have 10-20% flexibility",
            "Use market data to support your ask",
            "Focus on value, not need",
            "Be prepared to walk away",
            "Get everything in writing",
            "Consider total compensation, not just salary",
            "Ask for time to review the offer",
            "Practice your negotiation conversation",
            "Stay professional and positive throughout",
            "Know your minimum acceptable number beforehand",
            "Don't reveal your current salary if possible",
            "Negotiate other benefits if salary is fixed",
            "Time your negotiation well (after receiving offer, before accepting)"
        ]
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate formatted salary analysis report"""
        report = []
        report.append("=" * 70)
        report.append("SALARY NEGOTIATION ANALYSIS")
        report.append("=" * 70)
        
        # Offer Assessment
        report.append(f"\n💰 OFFER ANALYSIS")
        report.append("-" * 70)
        report.append(f"  Offered Amount: €{analysis['offer_amount']:,}")
        report.append(f"  Market Percentile: {analysis['percentile']}th")
        report.append(f"  Assessment: {analysis['assessment']}")
        
        # Market Data
        report.append(f"\n📊 MARKET DATA")
        report.append("-" * 70)
        market = analysis['market_data']
        report.append(f"  Market Range: €{market['min']:,} - €{market['max']:,}")
        report.append(f"  Market Median: €{market['median']:,}")
        report.append(f"  25th Percentile: €{market['p25']:,}")
        report.append(f"  75th Percentile: €{market['p75']:,}")
        
        # Counter Offer
        report.append(f"\n🎯 RECOMMENDED COUNTER OFFER")
        report.append("-" * 70)
        counter = analysis['counter_offer']
        report.append(f"  Suggested Amount: €{counter['suggested_amount']:,}")
        report.append(f"  Minimum Acceptable: €{counter['minimum_acceptable']:,}")
        report.append(f"  Negotiation Range: {counter['negotiation_range']}")
        report.append(f"  Strategy: {counter['strategy']}")
        
        # Leverage Points
        report.append(f"\n💪 YOUR LEVERAGE POINTS")
        report.append("-" * 70)
        for point in analysis['leverage_points']:
            report.append(f"  • {point}")
        
        # Total Compensation
        report.append(f"\n📋 TOTAL COMPENSATION FACTORS")
        report.append("-" * 70)
        for factor in analysis['total_comp_considerations'][:10]:
            report.append(f"  • {factor}")
        
        # Negotiation Script
        report.append(f"\n💬 NEGOTIATION SCRIPT")
        report.append("-" * 70)
        report.append(analysis['negotiation_script'])
        
        # Tips
        report.append(f"\n💡 NEGOTIATION TIPS")
        report.append("-" * 70)
        for tip in analysis['negotiation_tips'][:10]:
            report.append(f"  • {tip}")
        
        report.append("\n" + "=" * 70)
        
        return '\n'.join(report)


# Example usage
if __name__ == "__main__":
    advisor = SalaryAdvisor()
    
    test_job = {
        'title': 'Senior Python Developer',
        'company': 'Tech Corp',
        'location': 'Paris, France'
    }
    
    test_profile = {
        'years_experience': 5,
        'skills': 'Python, Django, AWS, Docker',
        'achievements': 'Led 3 major projects, increased efficiency by 40%'
    }
    
    offer_amount = 55000
    
    print("Salary Negotiation Advisor - Test Mode")
    print("=" * 70)
    
    analysis = advisor.analyze_offer(test_job, offer_amount, test_profile)
    print(advisor.generate_report(analysis))
