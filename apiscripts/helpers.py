# Import libraries
from rich.console import Console


# Import Models
from sportsdataapp.models import (Country, Competition, Team, Venue,
                                  )

# Import Functions
from apiscripts.api_request import api_request

console = Console()

# Fetch Country
def make_country(input_country_name: str):
    # Create or get Country
    country = Country.objects.filter(name=input_country_name).first()
    if not country:
        # Fetch Competitions with Country
        console.print(f'Fetching {input_country_name} competitions data from API.', style="blue")
        # API Request Setup
        url = "https://v3.football.api-sports.io/leagues"
        params = {'country': input_country_name}
        # API Request
        comps_data = api_request(url, params)
        comps = comps_data['response']
        # Process Data
        country = Country(name= comps_data['parameters']['country'],
                          num_competitions=comps_data['results'],
                          code=comps_data['response'][0]['country']['code'],
                          flag=comps_data['response'][0]['country']['flag'])
        country.save()
        console.print(f'Created new Country: {comps_data['parameters']['country']}.', style="green")
    else:
        console.print(f'Country found in records: {input_country_name}.', style="green")


# Fetch Competitions
def fetch_competitions(input_country_name: str):
    # Get Country
    country = Country.objects.filter(name=input_country_name).first()
    # Fetch Competitions with Country
    console.print(f'Fetching {input_country_name} competitions data from API.', style="blue")
    # API Request Setup
    url = "https://v3.football.api-sports.io/leagues"
    params = {'country': input_country_name}
    # API Request
    comps_data = api_request(url, params)
    comps = comps_data['response']
    new_comps = []
    for comp_entry in comps:
        # Find or create Competition
        comp = Competition.objects.filter(api_id=comp_entry['league']['id']).first()
        if not comp:
            comp = Competition(
                api_id=comp_entry['league']['id'],
                country=country,
                name=comp_entry['league']['name'],
                type=comp_entry['league']['type'],
                logo=comp_entry['league']['logo']
            )
            new_comps.append(comp)
            console.print(f'Created new Competition: {comp.name}', style="green")
    if new_comps:
        Competition.objects.bulk_create(new_comps)
        console.print(f'Successfully added {len(new_comps)} competitions!', style="bold green")
    else:
        console.print(f'No new competitions were added!', style="bold red")

    return len(new_comps)


# Fetch Teams
def fetch_teams(input_country_name: str):
    # Get Country
    country = Country.objects.filter(name=input_country_name).first()
    # Fetch Teams with Country
    console.print(f'Fetching {input_country_name} Teams data from API.', style="blue")
    # API Request Setup
    url = "https://v3.football.api-sports.io/teams"
    params = {'country': input_country_name}
    # API Request
    teams_data = api_request(url, params)
    teams_response = teams_data['response']
    # Process each Team in Response
    new_teams = []
    for entry in teams_response:
        team_data = entry['team']
        # Find or create Team
        team = Team.objects.filter(api_id=team_data['id']).first()
        if not team:
            team = Team(
                api_id=team_data['id'],
                name=team_data['name'],
                short_name=team_data['code'],
                country=country,
                founded=team_data['founded'],
                national=team_data['national'],
                logo_url=team_data['logo'],
            )
            new_teams.append(team)
            console.print(f'Created new team: {team.name}.', style="green")
    if new_teams:
        Team.objects.bulk_create(new_teams)
        console.print(f'Successfully added {len(new_teams)} teams!', style="bold green")
    else:
        console.print(f'No new teams were added!', style="bold red")

    return len(new_teams)


# Fetch Venues
def fetch_venues(input_country_name: str):
    # Get Country
    country = Country.objects.filter(name=input_country_name).first()
    # Fetch Venues with Country
    console.print(f'Fetching {input_country_name} Venues data from API.', style="blue")
    # API Request Setup
    url = "https://v3.football.api-sports.io/venues"
    params = {'country': input_country_name}
    # API Request
    venues_data = api_request(url, params)
    venues_response = venues_data['response']
    # Process each Venue in Response
    new_venues = []
    for entry in venues_response:
        venue = Venue.objects.filter(api_id=entry['id'])
        if not venue:
            # Create Venue
            venue = Venue(
                api_id=entry['id'],
                name=entry['name'],
                address=entry['address'],
                city=entry['city'],
                country=country,
                capacity=entry['capacity'],
                surface=entry['surface'],
                image=entry['image']
            )
            new_venues.append(venue)
            console.print(f'Created new venue: {venue.name}.', style="green")
    if new_venues:
        Venue.objects.bulk_create(new_venues)
        console.print(f'Successfully added {len(new_venues)} venues!', style="bold green")
    else:
        console.print(f'No new venues were added!', style="bold red")

    return len(new_venues)