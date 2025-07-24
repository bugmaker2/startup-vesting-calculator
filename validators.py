from datetime import date
from typing import List, Optional
from models import Company, Founder, FundingRound


class ValidationError(Exception):
    """Custom validation error for stock calculations"""
    pass


class StockValidator:
    """Validates stock calculations and business logic"""
    
    @staticmethod
    def validate_company_setup(company: Company) -> List[str]:
        """Validate company setup and return list of issues"""
        issues = []
        
        if not company.name or not company.name.strip():
            issues.append("Company name cannot be empty")
        
        if company.total_shares <= 0:
            issues.append("Total shares must be greater than 0")
        
        if not company.founders:
            issues.append("At least one founder must be added")
        
        total_founder_shares = sum(f.shares for f in company.founders)
        if total_founder_shares > company.total_shares:
            issues.append(f"Total founder shares ({total_founder_shares:,}) exceeds authorized shares ({company.total_shares:,})")
        
        if total_founder_shares == 0:
            issues.append("Total founder shares cannot be zero")
        
        founder_names = [f.name.strip().lower() for f in company.founders]
        if len(founder_names) != len(set(founder_names)):
            issues.append("Founder names must be unique")
        
        return issues
    
    @staticmethod
    def validate_founder_shares(company: Company, new_founder: Founder) -> List[str]:
        """Validate adding a new founder"""
        issues = []
        
        if not new_founder.name or not new_founder.name.strip():
            issues.append("Founder name cannot be empty")
        
        if new_founder.shares <= 0:
            issues.append("Founder shares must be greater than 0")
        
        existing_names = [f.name.strip().lower() for f in company.founders]
        if new_founder.name.strip().lower() in existing_names:
            issues.append(f"Founder '{new_founder.name}' already exists")
        
        total_shares_after = sum(f.shares for f in company.founders) + new_founder.shares
        if total_shares_after > company.total_shares:
            remaining = company.total_shares - sum(f.shares for f in company.founders)
            issues.append(f"Cannot add {new_founder.shares:,} shares. Only {remaining:,} shares remaining")
        
        return issues
    
    @staticmethod
    def validate_funding_round(company: Company, funding_round: FundingRound) -> List[str]:
        """Validate funding round parameters"""
        issues = []
        
        if not funding_round.name or not funding_round.name.strip():
            issues.append("Round name cannot be empty")
        
        if funding_round.investment_amount <= 0:
            issues.append("Investment amount must be greater than 0")
        
        if funding_round.pre_money_valuation <= 0:
            issues.append("Pre-money valuation must be greater than 0")
        
        if funding_round.new_shares <= 0:
            issues.append("New shares to issue must be greater than 0")
        
        if funding_round.investment_amount > funding_round.pre_money_valuation:
            issues.append("Investment amount exceeds pre-money valuation")
        
        return issues
    
    @staticmethod
    def validate_vesting_schedule(start_date: date, current_date: date) -> List[str]:
        """Validate vesting schedule dates"""
        issues = []
        
        if current_date < start_date:
            issues.append("Current date cannot be before vesting start date")
        
        max_future_date = start_date.replace(year=start_date.year + 10)
        if current_date > max_future_date:
            issues.append("Vesting calculation too far in the future (max 10 years)")
        
        return issues
    
    @staticmethod
    def get_recommendations(company: Company) -> List[str]:
        """Provide business recommendations based on setup"""
        recommendations = []
        
        if len(company.founders) == 1:
            recommendations.append("Consider adding co-founders to distribute risk and expertise")
        
        if len(company.founders) > 4:
            recommendations.append("Large founder teams may face coordination challenges")
        
        total_founder_shares = sum(f.shares for f in company.founders)
        if total_founder_shares < company.total_shares * 0.6:
            recommendations.append("Consider reserving more shares for future employees/investors")
        
        if total_founder_shares > company.total_shares * 0.9:
            recommendations.append("Consider reserving more shares for future funding rounds")
        
        founder_shares = [f.shares for f in company.founders]
        if founder_shares:
            max_shares = max(founder_shares)
            min_shares = min(founder_shares)
            ratio = max_shares / min_shares if min_shares > 0 else float('inf')
            
            if ratio > 5:
                recommendations.append("Large equity disparities may create future conflicts")
        
        return recommendations