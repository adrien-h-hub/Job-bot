"""
Career Path Planner - Long-term career strategy and skill development
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta


class CareerPlanner:
    """Plan career progression and skill development"""
    
    def __init__(self):
        """Initialize career planner"""
        # Career paths by role
        self.career_paths = {
            'junior_developer': {
                'next_roles': ['mid_developer', 'specialist'],
                'timeline': '2-3 years',
                'required_skills': ['Advanced programming', 'System design', 'Code review']
            },
            'mid_developer': {
                'next_roles': ['senior_developer', 'tech_lead', 'specialist'],
                'timeline': '3-5 years',
                'required_skills': ['Architecture', 'Mentoring', 'Project leadership']
            },
            'senior_developer': {
                'next_roles': ['tech_lead', 'architect', 'engineering_manager'],
                'timeline': '3-5 years',
                'required_skills': ['Strategic thinking', 'Team leadership', 'Business acumen']
            },
            'tech_lead': {
                'next_roles': ['architect', 'engineering_manager', 'director'],
                'timeline': '3-5 years',
                'required_skills': ['Cross-team collaboration', 'Technical strategy', 'People management']
            }
        }
        
        # Skill categories
        self.skill_categories = {
            'technical': ['Programming', 'System Design', 'DevOps', 'Security', 'Testing'],
            'soft_skills': ['Communication', 'Leadership', 'Problem Solving', 'Teamwork'],
            'business': ['Product Thinking', 'Project Management', 'Stakeholder Management'],
            'specialized': ['Machine Learning', 'Cloud Architecture', 'Mobile Development']
        }
    
    def create_career_plan(self, current_role: str, target_role: str, 
                          current_skills: List[str], timeline: str = '5 years') -> Dict:
        """
        Create comprehensive career development plan
        
        Args:
            current_role: Current job role
            target_role: Desired future role
            current_skills: List of current skills
            timeline: Time horizon for plan
            
        Returns:
            Dict with career plan, milestones, and skill gaps
        """
        plan = {
            'current_state': {
                'role': current_role,
                'skills': current_skills,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            'target_state': {
                'role': target_role,
                'timeline': timeline
            },
            'progression_path': self._map_progression_path(current_role, target_role),
            'skill_gaps': self._identify_skill_gaps(current_skills, target_role),
            'milestones': self._create_milestones(current_role, target_role, timeline),
            'learning_resources': self._suggest_learning_resources(target_role),
            'action_items': self._generate_action_items(current_role, target_role)
        }
        
        return plan
    
    def _map_progression_path(self, current: str, target: str) -> List[Dict]:
        """Map the progression path from current to target role"""
        # Simplified path mapping
        path = [
            {
                'role': current,
                'duration': '0 years',
                'focus': 'Master current role'
            }
        ]
        
        # Add intermediate steps
        if 'junior' in current.lower() and 'senior' in target.lower():
            path.append({
                'role': 'Mid-Level Developer',
                'duration': '2-3 years',
                'focus': 'Expand technical depth and breadth'
            })
        
        path.append({
            'role': target,
            'duration': '3-5 years',
            'focus': 'Achieve target role'
        })
        
        return path
    
    def _identify_skill_gaps(self, current_skills: List[str], target_role: str) -> List[Dict]:
        """Identify skills needed for target role"""
        # Required skills by role type
        role_requirements = {
            'senior': ['System Design', 'Architecture', 'Mentoring', 'Code Review', 'Technical Leadership'],
            'lead': ['Team Management', 'Project Planning', 'Stakeholder Communication', 'Strategic Thinking'],
            'architect': ['System Architecture', 'Technology Strategy', 'Cross-team Collaboration', 'Documentation'],
            'manager': ['People Management', 'Performance Reviews', 'Hiring', 'Budget Planning', 'Team Building']
        }
        
        # Determine required skills
        required_skills = []
        for key, skills in role_requirements.items():
            if key in target_role.lower():
                required_skills.extend(skills)
        
        # Find gaps
        current_skills_lower = [s.lower() for s in current_skills]
        gaps = []
        
        for skill in required_skills:
            if skill.lower() not in current_skills_lower:
                gaps.append({
                    'skill': skill,
                    'priority': 'High' if skill in required_skills[:3] else 'Medium',
                    'category': self._categorize_skill(skill)
                })
        
        return gaps
    
    def _categorize_skill(self, skill: str) -> str:
        """Categorize a skill"""
        skill_lower = skill.lower()
        
        if any(word in skill_lower for word in ['design', 'architecture', 'programming', 'technical']):
            return 'Technical'
        elif any(word in skill_lower for word in ['management', 'leadership', 'team', 'people']):
            return 'Leadership'
        elif any(word in skill_lower for word in ['communication', 'stakeholder', 'presentation']):
            return 'Communication'
        else:
            return 'General'
    
    def _create_milestones(self, current: str, target: str, timeline: str) -> List[Dict]:
        """Create career milestones"""
        milestones = []
        
        # Parse timeline
        years = int(''.join(filter(str.isdigit, timeline))) if timeline else 5
        
        # 6-month milestones
        for i in range(1, years * 2 + 1):
            months = i * 6
            date = datetime.now() + timedelta(days=months * 30)
            
            milestone = {
                'date': date.strftime('%Y-%m-%d'),
                'timeframe': f'{months} months',
                'goals': self._get_milestone_goals(i, years * 2)
            }
            milestones.append(milestone)
        
        return milestones
    
    def _get_milestone_goals(self, milestone_num: int, total_milestones: int) -> List[str]:
        """Get goals for a specific milestone"""
        progress = milestone_num / total_milestones
        
        if progress <= 0.25:
            return [
                'Master 2-3 new technical skills',
                'Complete relevant certification',
                'Take on stretch project'
            ]
        elif progress <= 0.5:
            return [
                'Lead a small project',
                'Mentor junior team member',
                'Contribute to architecture decisions'
            ]
        elif progress <= 0.75:
            return [
                'Lead cross-functional initiative',
                'Present at team/company meeting',
                'Expand professional network'
            ]
        else:
            return [
                'Demonstrate target role capabilities',
                'Seek promotion or new opportunity',
                'Build leadership portfolio'
            ]
    
    def _suggest_learning_resources(self, target_role: str) -> Dict:
        """Suggest learning resources for target role"""
        resources = {
            'online_courses': [
                'Coursera - System Design',
                'Udemy - Advanced Programming',
                'LinkedIn Learning - Leadership Skills'
            ],
            'certifications': [
                'AWS Certified Solutions Architect',
                'Google Cloud Professional',
                'Certified Scrum Master'
            ],
            'books': [
                'Designing Data-Intensive Applications',
                'The Manager\'s Path',
                'Clean Architecture'
            ],
            'communities': [
                'Local tech meetups',
                'Online developer communities',
                'Professional associations'
            ]
        }
        
        return resources
    
    def _generate_action_items(self, current: str, target: str) -> List[Dict]:
        """Generate immediate action items"""
        actions = [
            {
                'action': 'Identify skill gaps',
                'priority': 'High',
                'timeframe': 'This week',
                'description': 'Compare current skills with target role requirements'
            },
            {
                'action': 'Create learning plan',
                'priority': 'High',
                'timeframe': 'This month',
                'description': 'Select courses and resources to address skill gaps'
            },
            {
                'action': 'Seek mentorship',
                'priority': 'Medium',
                'timeframe': 'This month',
                'description': 'Find someone in target role to mentor you'
            },
            {
                'action': 'Take on stretch project',
                'priority': 'High',
                'timeframe': 'Next quarter',
                'description': 'Volunteer for project requiring target role skills'
            },
            {
                'action': 'Build portfolio',
                'priority': 'Medium',
                'timeframe': 'Ongoing',
                'description': 'Document achievements and projects'
            },
            {
                'action': 'Network actively',
                'priority': 'Medium',
                'timeframe': 'Ongoing',
                'description': 'Attend industry events and connect with peers'
            }
        ]
        
        return actions
    
    def generate_report(self, plan: Dict) -> str:
        """Generate formatted career plan report"""
        report = []
        report.append("=" * 70)
        report.append("CAREER DEVELOPMENT PLAN")
        report.append("=" * 70)
        
        # Current State
        report.append(f"\n📍 CURRENT STATE")
        report.append("-" * 70)
        report.append(f"  Role: {plan['current_state']['role']}")
        report.append(f"  Skills: {', '.join(plan['current_state']['skills'][:5])}")
        report.append(f"  Date: {plan['current_state']['date']}")
        
        # Target State
        report.append(f"\n🎯 TARGET STATE")
        report.append("-" * 70)
        report.append(f"  Role: {plan['target_state']['role']}")
        report.append(f"  Timeline: {plan['target_state']['timeline']}")
        
        # Progression Path
        report.append(f"\n🗺️  PROGRESSION PATH")
        report.append("-" * 70)
        for i, step in enumerate(plan['progression_path'], 1):
            report.append(f"  {i}. {step['role']} ({step['duration']})")
            report.append(f"     Focus: {step['focus']}")
        
        # Skill Gaps
        report.append(f"\n📚 SKILL GAPS TO ADDRESS")
        report.append("-" * 70)
        for gap in plan['skill_gaps'][:10]:
            report.append(f"  • {gap['skill']} ({gap['priority']} priority) - {gap['category']}")
        
        # Milestones
        report.append(f"\n🎯 KEY MILESTONES")
        report.append("-" * 70)
        for milestone in plan['milestones'][:4]:
            report.append(f"\n  {milestone['timeframe']} ({milestone['date']}):")
            for goal in milestone['goals']:
                report.append(f"    • {goal}")
        
        # Learning Resources
        report.append(f"\n📖 LEARNING RESOURCES")
        report.append("-" * 70)
        for category, resources in plan['learning_resources'].items():
            report.append(f"\n  {category.replace('_', ' ').title()}:")
            for resource in resources[:3]:
                report.append(f"    • {resource}")
        
        # Action Items
        report.append(f"\n✅ IMMEDIATE ACTION ITEMS")
        report.append("-" * 70)
        for action in plan['action_items']:
            report.append(f"\n  {action['action']} ({action['priority']} priority)")
            report.append(f"    Timeframe: {action['timeframe']}")
            report.append(f"    {action['description']}")
        
        report.append("\n" + "=" * 70)
        
        return '\n'.join(report)


# Example usage
if __name__ == "__main__":
    planner = CareerPlanner()
    
    current_role = "Mid-Level Python Developer"
    target_role = "Senior Software Architect"
    current_skills = ['Python', 'Django', 'SQL', 'Git', 'REST APIs']
    
    print("Career Path Planner - Test Mode")
    print("=" * 70)
    
    plan = planner.create_career_plan(current_role, target_role, current_skills, '5 years')
    print(planner.generate_report(plan))
