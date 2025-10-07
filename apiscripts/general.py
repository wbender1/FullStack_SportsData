# Import libraries
from rich.console import Console
from tabulate import tabulate

# Import Functions
from apiscripts.helpers import (make_country, fetch_competitions, fetch_teams, fetch_venues,
                                )


console = Console()

# Fetch Country
def fetch_country(input_country_name: str):
    console.print(f'Fetching all data for {input_country_name}', style="blue")

    make_country(input_country_name)
    comps_added = fetch_competitions(input_country_name)
    teams_added = fetch_teams(input_country_name)
    venues_added = fetch_venues(input_country_name)

    summary_table = [
        ("Competitions Added", comps_added),
        ("Teams Added", teams_added),
        ("Venues Added", venues_added)
    ]
    headers = ["Entity", "Added Count"]
    console.print(f"\n[bold]Data added for[/bold] [green]{input_country_name}")
    print(tabulate(summary_table, headers=headers, tablefmt="pretty"))