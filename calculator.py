from datetime import date, datetime
from typing import List, Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from models import Company, Founder, VestingSchedule, FundingRound
from validators import StockValidator

console = Console()
app = typer.Typer(help="Co-founder Stock Calculator with Vesting Schedules")


def create_company() -> Company:
    console.print("[bold blue]Create New Company[/bold blue]")
    
    name = Prompt.ask("Company name")
    total_shares = IntPrompt.ask("Total authorized shares", default=10000000)
    
    return Company(name=name, total_shares=total_shares)


def add_founder(company: Company) -> None:
    console.print(f"\n[bold green]Add Founder to {company.name}[/bold green]")
    
    name = Prompt.ask("Founder name")
    shares = IntPrompt.ask("Shares allocated", default=1000000)
    
    start_date_str = Prompt.ask("Start date (YYYY-MM-DD)", default=date.today().isoformat())
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    except ValueError:
        console.print("[red]Invalid date format. Using today.[/red]")
        start_date = date.today()
    
    founder = Founder(name=name, shares=shares, start_date=start_date)
    
    # Validate before adding
    issues = StockValidator.validate_founder_shares(company, founder)
    if issues:
        console.print("[red]Cannot add founder:[/red]")
        for issue in issues:
            console.print(f"  • {issue}")
        return
    
    company.add_founder(founder)
    console.print(f"[green]Added {name} with {shares:,} shares[/green]")


def display_cap_table(company: Company) -> None:
    if not company.founders:
        console.print("[yellow]No founders added yet.[/yellow]")
        return
    
    table = Table(title=f"{company.name} - Cap Table")
    table.add_column("Founder", style="cyan")
    table.add_column("Shares", style="magenta", justify="right")
    table.add_column("Ownership %", style="green", justify="right")
    table.add_column("Remaining Shares", style="yellow", justify="right")
    
    cap_table = company.get_cap_table()
    for entry in cap_table:
        table.add_row(
            entry['founder'],
            f"{entry['shares']:,}",
            f"{entry['ownership_pct']:.2f}%",
            f"{company.get_remaining_shares():,}"
        )
    
    console.print(table)


def display_vesting_schedule(company: Company) -> None:
    if not company.founders:
        console.print("[yellow]No founders added yet.[/yellow]")
        return
    
    current_date_str = Prompt.ask("Current date for vesting calculation (YYYY-MM-DD)", 
                                 default=date.today().isoformat())
    try:
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d").date()
    except ValueError:
        current_date = date.today()
    
    table = Table(title=f"{company.name} - Vesting Schedule ({current_date})")
    table.add_column("Founder", style="cyan")
    table.add_column("Total Shares", style="magenta", justify="right")
    table.add_column("Vested Shares", style="green", justify="right")
    table.add_column("Unvested Shares", style="red", justify="right")
    table.add_column("Vested %", style="yellow", justify="right")
    
    for founder in company.founders:
        schedule = VestingSchedule(
            founder=founder,
            vesting_start=founder.start_date,
            cliff_months=12,
            vesting_months=48
        )
        
        vested = schedule.calculate_vested_shares(current_date)
        unvested = schedule.calculate_unvested_shares(current_date)
        vested_pct = (vested / founder.shares * 100) if founder.shares > 0 else 0
        
        table.add_row(
            founder.name,
            f"{founder.shares:,}",
            f"{vested:,}",
            f"{unvested:,}",
            f"{vested_pct:.1f}%"
        )
    
    console.print(table)


def simulate_funding_round(company: Company) -> None:
    if not company.founders:
        console.print("[yellow]No founders added yet.[/yellow]")
        return
    
    console.print("\n[bold blue]Simulate Funding Round[/bold blue]")
    
    round_name = Prompt.ask("Round name", default="Series A")
    investment = FloatPrompt.ask("Investment amount ($)", default=2000000.0)
    pre_money = FloatPrompt.ask("Pre-money valuation ($)", default=8000000.0)
    new_shares = IntPrompt.ask("New shares to issue", default=2500000)
    
    funding_round = FundingRound(
        name=round_name,
        investment_amount=investment,
        pre_money_valuation=pre_money,
        new_shares=new_shares
    )
    
    console.print(f"\n[bold]{round_name} Details:[/bold]")
    console.print(f"Investment: ${investment:,.2f}")
    console.print(f"Pre-money: ${pre_money:,.2f}")
    console.print(f"Post-money: ${funding_round.post_money_valuation:,.2f}")
    console.print(f"Price per share: ${funding_round.price_per_share:.4f}")
    
    table = Table(title=f"Dilution Analysis - {round_name}")
    table.add_column("Founder", style="cyan")
    table.add_column("Pre-Round Shares", style="magenta", justify="right")
    table.add_column("Post-Round Shares", style="green", justify="right")
    table.add_column("Pre-Round %", style="yellow", justify="right")
    table.add_column("Post-Round %", style="red", justify="right")
    table.add_column("Dilution %", style="red", justify="right")
    
    total_shares_before = company.get_total_founder_shares()
    total_shares_after = total_shares_before + new_shares
    
    for founder in company.founders:
        original_pct = (founder.shares / total_shares_before * 100) if total_shares_before > 0 else 0
        new_pct = (founder.shares / total_shares_after * 100) if total_shares_after > 0 else 0
        dilution = original_pct - new_pct
        
        table.add_row(
            founder.name,
            f"{founder.shares:,}",
            f"{founder.shares:,}",
            f"{original_pct:.2f}%",
            f"{new_pct:.2f}%",
            f"{dilution:.2f}%"
        )
    
    console.print(table)


@app.command()
def interactive():
    """Interactive mode for step-by-step company setup"""
    console.print(Panel.fit(
        "[bold blue]Co-founder Stock Calculator[/bold blue]\n\n"
        "Welcome to the interactive stock calculator for co-founders.\n"
        "This tool helps you calculate equity splits, vesting schedules,\n"
        "and dilution from funding rounds.",
        border_style="blue"
    ))
    
    company = create_company()
    
    while True:
        console.print("\n[bold]Main Menu:[/bold]")
        console.print("1. Add founder")
        console.print("2. View cap table")
        console.print("3. View vesting schedules")
        console.print("4. Simulate funding round")
        console.print("5. Exit")
        
        choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            add_founder(company)
        elif choice == "2":
            # Validate before display
            issues = StockValidator.validate_company_setup(company)
            if issues:
                console.print("[red]Validation issues:[/red]")
                for issue in issues:
                    console.print(f"  • {issue}")
                continue
            
            display_cap_table(company)
            
            # Show recommendations
            recommendations = StockValidator.get_recommendations(company)
            if recommendations:
                console.print("\n[bold yellow]Recommendations:[/bold yellow]")
                for rec in recommendations:
                    console.print(f"  • {rec}")
        elif choice == "3":
            # Validate before display
            issues = StockValidator.validate_company_setup(company)
            if issues:
                console.print("[red]Validation issues:[/red]")
                for issue in issues:
                    console.print(f"  • {issue}")
                continue
            
            display_vesting_schedule(company)
        elif choice == "4":
            # Validate before funding
            issues = StockValidator.validate_company_setup(company)
            if issues:
                console.print("[red]Validation issues:[/red]")
                for issue in issues:
                    console.print(f"  • {issue}")
                continue
            
            simulate_funding_round(company)
        elif choice == "5":
            console.print("[green]Goodbye![/green]")
            break


@app.command()
def quick_calc(
    company_name: str = typer.Option(..., "--company", "-c", help="Company name"),
    total_shares: int = typer.Option(10000000, "--total", "-t", help="Total authorized shares"),
    founder1_name: str = typer.Option(..., "--f1-name", help="Founder 1 name"),
    founder1_shares: int = typer.Option(..., "--f1-shares", help="Founder 1 shares"),
    founder2_name: str = typer.Option(None, "--f2-name", help="Founder 2 name"),
    founder2_shares: int = typer.Option(0, "--f2-shares", help="Founder 2 shares"),
    founder3_name: str = typer.Option(None, "--f3-name", help="Founder 3 name"),
    founder3_shares: int = typer.Option(0, "--f3-shares", help="Founder 3 shares"),
):
    """Quick calculator for simple equity splits"""
    company = Company(name=company_name, total_shares=total_shares)
    
    founders_data = [
        (founder1_name, founder1_shares),
        (founder2_name, founder2_shares),
        (founder3_name, founder3_shares),
    ]
    
    for name, shares in founders_data:
        if name and shares > 0:
            founder = Founder(name=name, shares=shares, start_date=date.today())
            company.add_founder(founder)
    
    # Validate before display
    issues = StockValidator.validate_company_setup(company)
    if issues:
        console.print("[red]Validation issues:[/red]")
        for issue in issues:
            console.print(f"  • {issue}")
        return
    
    display_cap_table(company)
    
    # Show recommendations
    recommendations = StockValidator.get_recommendations(company)
    if recommendations:
        console.print("\n[bold yellow]Recommendations:[/bold yellow]")
        for rec in recommendations:
            console.print(f"  • {rec}")


if __name__ == "__main__":
    app()