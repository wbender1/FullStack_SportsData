# Import libraries
from rich.console import Console
from tabulate import tabulate

# Import Functions
from apiscripts.helpers import (make_country, fetch_competitions, fetch_teams, fetch_venues,
                                make_season, fetch_standings, fetch_fixtures, make_meta_join_table,
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


# Fetch Season
def fetch_season(competition_name: str, year: int):
    # Find or Make Season
    season, competition = make_season(competition_name, year)
    if competition.type == 'League':
        fetch_standings(season, competition)
    else:
        console.print(f'No Standings Data for League Competitions.', style="yellow")
    # Find Fixtures
    fetch_fixtures(season, competition)
    # Make Team-Season Join Table Entries
    make_meta_join_table(season)


