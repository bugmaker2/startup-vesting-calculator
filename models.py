from datetime import date, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class Founder(BaseModel):
    name: str
    shares: int = Field(gt=0, description="Number of shares allocated")
    start_date: date = Field(description="Start date for vesting")
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class VestingSchedule(BaseModel):
    founder: Founder
    cliff_months: int = Field(default=12, ge=0, le=48)
    vesting_months: int = Field(default=48, ge=12, le=60)
    vesting_start: date
    
    def calculate_vested_shares(self, current_date: date) -> int:
        if current_date < self.vesting_start:
            return 0
            
        months_elapsed = (current_date.year - self.vesting_start.year) * 12 + \
                        (current_date.month - self.vesting_start.month)
        
        if months_elapsed < self.cliff_months:
            return 0
            
        if months_elapsed >= self.vesting_months:
            return self.founder.shares
            
        vested_portion = (months_elapsed - self.cliff_months) / (self.vesting_months - self.cliff_months)
        return int(self.founder.shares * vested_portion)
    
    def calculate_unvested_shares(self, current_date: date) -> int:
        return self.founder.shares - self.calculate_vested_shares(current_date)


class Company(BaseModel):
    name: str = Field(min_length=1, description="Company name")
    total_shares: int = Field(gt=0, description="Total authorized shares")
    founders: List[Founder] = Field(default_factory=list)
    
    def add_founder(self, founder: Founder) -> None:
        self.founders.append(founder)
    
    def get_total_founder_shares(self) -> int:
        return sum(f.shares for f in self.founders)
    
    def get_remaining_shares(self) -> int:
        return self.total_shares - self.get_total_founder_shares()
    
    def get_cap_table(self) -> List[dict]:
        total_founder_shares = self.get_total_founder_shares()
        return [
            {
                'founder': f.name,
                'shares': f.shares,
                'ownership_pct': (f.shares / total_founder_shares * 100) if total_founder_shares > 0 else 0
            }
            for f in self.founders
        ]


class FundingRound(BaseModel):
    name: str
    investment_amount: float = Field(gt=0)
    pre_money_valuation: float = Field(gt=0)
    new_shares: int = Field(gt=0)
    
    @property
    def post_money_valuation(self) -> float:
        return self.pre_money_valuation + self.investment_amount
    
    @property
    def price_per_share(self) -> float:
        return self.pre_money_valuation / self.new_shares
    
    def calculate_dilution(self, original_shares: int, original_percentage: float) -> dict:
        total_shares_after = original_shares + self.new_shares
        new_percentage = (original_shares / total_shares_after) * 100
        dilution = original_percentage - new_percentage
        
        return {
            'original_shares': original_shares,
            'new_shares': new_shares,
            'total_shares_after': total_shares_after,
            'original_percentage': original_percentage,
            'new_percentage': new_percentage,
            'dilution_percentage': dilution
        }