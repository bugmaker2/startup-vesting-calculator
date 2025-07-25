# Co-founder Stock Calculator

A comprehensive CLI tool for calculating co-founder equity, vesting schedules, and dilution from funding rounds.

## Features

- **Equity Distribution**: Calculate fair equity splits among co-founders
- **Vesting Schedules**: 4-year vesting with 1-year cliff by default
- **Funding Round Simulation**: Model dilution from investment rounds
- **Interactive Mode**: Step-by-step guided setup
- **Quick Calculations**: Fast calculations via command-line arguments
- **Validation**: Comprehensive business logic validation
- **Rich Reporting**: Beautiful tables and visualizations

## Installation

```bash
# Using uv (recommended)
uv sync

# Using pip
pip install -e .
```

## Quick Start

### Interactive Mode
```bash
python main.py interactive
```

### Quick Calculation
```bash
python main.py quick-calc --company "TechCorp" --total 10000000 \
  --f1-name "Alice" --f1-shares 4000000 \
  --f2-name "Bob" --f2-shares 3500000 \
  --f3-name "Charlie" --f3-shares 2500000
```

## Usage Examples

### 1. Basic Equity Split
```bash
# Create a company with 3 founders
python main.py interactive

# Steps:
# 1. Enter company name: "TechCorp"
# 2. Total shares: 10,000,000
# 3. Add founders with their respective shares
# 4. View the cap table showing ownership percentages
```

### 2. Vesting Schedule Calculation
```bash
# After adding founders, select option 3 from the menu
# Enter current date to see vested vs unvested shares
# Example output:
# ┌─────────┬──────────────┬──────────────┬────────────────┬──────────┐
# │ Founder │ Total Shares │ Vested Shares │ Unvested Shares │ Vested % │
# ├─────────┼──────────────┼──────────────┼────────────────┼──────────┤
# │ Alice   │ 4,000,000    │ 2,000,000     │ 2,000,000       │ 50.0%    │
# │ Bob     │ 3,500,000    │ 1,750,000     │ 1,750,000       │ 50.0%    │
# │ Charlie │ 2,500,000    │ 1,250,000     │ 1,250,000       │ 50.0%    │
# └─────────┴──────────────┴──────────────┴────────────────┴──────────┘
```

### 3. Funding Round Simulation
```bash
# After setting up founders, select option 4 from the menu
# Enter funding round details:
# - Round name: "Series A"
# - Investment: $2,000,000
# - Pre-money: $8,000,000
# - New shares: 2,500,000

# Output shows dilution analysis:
# ┌─────────┬──────────────────┬────────────────────┬──────────────┬──────────────┬──────────────┐
# │ Founder │ Pre-Round Shares │ Post-Round Shares  │ Pre-Round %   │ Post-Round %  │ Dilution %   │
# ├─────────┼──────────────────┼────────────────────┼──────────────┼──────────────┼──────────────┤
# │ Alice   │ 4,000,000        │ 4,000,000         │ 40.00%        │ 32.00%        │ 8.00%        │
# │ Bob     │ 3,500,000        │ 3,500,000         │ 35.00%        │ 28.00%        │ 7.00%        │
# │ Charlie │ 2,500,000        │ 2,500,000         │ 25.00%        │ 20.00%        │ 5.00%        │
# └─────────┴──────────────────┴────────────────────┴──────────────┴──────────────┴──────────────┘
```

## Data Models

### Company
- `name`: Company name
- `total_shares`: Total authorized shares
- `founders`: List of Founder objects

### Founder
- `name`: Founder's name
- `shares`: Number of shares allocated
- `start_date`: Vesting start date

### VestingSchedule
- `cliff_months`: Default 12 months (1 year)
- `vesting_months`: Default 48 months (4 years)
- Calculates vested/unvested shares based on current date

### FundingRound
- `name`: Round name (Series A, Seed, etc.)
- `investment_amount`: Investment in dollars
- `pre_money_valuation`: Pre-money valuation
- `new_shares`: Shares to issue to investors

## Validation Rules

The tool validates:
- Company name is not empty
- Total shares > 0
- At least one founder exists
- Founder shares don't exceed total authorized shares
- Founder names are unique
- Investment amounts are positive
- Vesting calculations are within reasonable bounds

## Business Recommendations

Based on your setup, the tool provides recommendations such as:
- Consider adding co-founders to distribute risk
- Large founder teams may face coordination challenges
- Reserve shares for future employees/investors
- Avoid large equity disparities to prevent conflicts

## Development

### Requirements
- Python 3.12+
- Dependencies listed in pyproject.toml

### Running Tests
```bash
# Install development dependencies
uv sync --dev

# Run the application
python main.py --help
```

### Project Structure
```
StockCalculator/
├── main.py              # Entry point
├── calculator.py        # CLI interface
├── models.py           # Data models
├── validators.py       # Validation logic
├── pyproject.toml      # Project configuration
└── README.md          # This file
```

## Command Reference

### Interactive Mode
```
python main.py interactive
```

### Quick Calculator
```
python main.py quick-calc [OPTIONS]

Options:
  -c, --company TEXT      Company name [required]
  -t, --total INTEGER     Total authorized shares [default: 10000000]
  --f1-name TEXT          Founder 1 name [required]
  --f1-shares INTEGER     Founder 1 shares [required]
  --f2-name TEXT          Founder 2 name
  --f2-shares INTEGER     Founder 2 shares [default: 0]
  --f3-name TEXT          Founder 3 name
  --f3-shares INTEGER     Founder 3 shares [default: 0]
  --help                  Show this message and exit.
```

## License

MIT License - see LICENSE file for details.