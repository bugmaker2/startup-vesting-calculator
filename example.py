#!/usr/bin/env python3
"""
Example usage of the co-founder stock calculator
"""

from datetime import date, timedelta
from models import Company, Founder, VestingSchedule, FundingRound
from validators import StockValidator

# Example 1: Basic company setup
print("=== Example 1: Basic Company Setup ===")
company = Company(name="TechCorp", total_shares=10_000_000)

# Add founders
founders = [
    Founder(name="Alice", shares=4_000_000, start_date=date(2024, 1, 1)),
    Founder(name="Bob", shares=3_500_000, start_date=date(2024, 1, 1)),
    Founder(name="Charlie", shares=2_500_000, start_date=date(2024, 1, 1)),
]

for founder in founders:
    company.add_founder(founder)

# Display cap table
print("\nCap Table:")
for entry in company.get_cap_table():
    print(f"{entry['founder']}: {entry['shares']:,} shares ({entry['ownership_pct']:.1f}%)")

# Example 2: Vesting calculation
print("\n=== Example 2: Vesting Calculation ===")
current_date = date(2024, 7, 1)  # 6 months after start

print(f"Vesting status as of {current_date}:")
for founder in company.founders:
    schedule = VestingSchedule(
        founder=founder,
        vesting_start=founder.start_date,
        cliff_months=12,
        vesting_months=48
    )
    
    vested = schedule.calculate_vested_shares(current_date)
    unvested = schedule.calculate_unvested_shares(current_date)
    vested_pct = (vested / founder.shares) * 100
    
    print(f"{founder.name}: {vested:,} vested, {unvested:,} unvested ({vested_pct:.1f}%)")

# Example 3: Funding round simulation
print("\n=== Example 3: Series A Funding Round ===")
funding_round = FundingRound(
    name="Series A",
    investment_amount=2_000_000,
    pre_money_valuation=8_000_000,
    new_shares=2_500_000
)

print(f"Funding Round: {funding_round.name}")
print(f"Investment: ${funding_round.investment_amount:,.0f}")
print(f"Pre-money: ${funding_round.pre_money_valuation:,.0f}")
print(f"Post-money: ${funding_round.post_money_valuation:,.0f}")
print(f"Price per share: ${funding_round.price_per_share:.4f}")

print("\nDilution Analysis:")
total_shares_before = company.get_total_founder_shares()
total_shares_after = total_shares_before + funding_round.new_shares

for founder in company.founders:
    original_pct = (founder.shares / total_shares_before) * 100
    new_pct = (founder.shares / total_shares_after) * 100
    dilution = original_pct - new_pct
    
    print(f"{founder.name}: {original_pct:.1f}% → {new_pct:.1f}% (dilution: {dilution:.1f}%)")

# Example 4: Validation and recommendations
print("\n=== Example 4: Validation ===")
issues = StockValidator.validate_company_setup(company)
if issues:
    print("Validation issues:")
    for issue in issues:
        print(f"  • {issue}")
else:
    print("✓ Company setup is valid")

recommendations = StockValidator.get_recommendations(company)
if recommendations:
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"  • {rec}")

print("\n=== Usage Examples ===")
print("Interactive mode: python main.py interactive")
print("Quick calculation: python main.py quick-calc --help")

if __name__ == "__main__":
    print("\nRun 'python main.py interactive' for interactive mode!")