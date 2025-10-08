# Import libraries
from rich.console import Console
from datetime import datetime

# Import Models
from sportsdataapp.models import (Country, Competition, Team, Venue,
                                  Season, Standing, Fixture, TeamSeasonCompetition)

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


# Make Season
def make_season(competition_name: str, year: int):
    # Find Competition
    competition = Competition.objects.filter(name=competition_name).first()
    if not competition:
        raise ValueError(f'{competition_name} not found.')
    # Find Season ID
    season = Season.objects.filter(competition=competition, year=year).first()
    if not season:
        season = Season(year=year, competition=competition)
        season.save()
        console.print(f'Created new season. {year} {competition_name} (Competition ID: {competition.api_id}).',
                      style="green")
    else:
        console.print(f'Found season for {year} {competition_name} (Competition ID: {competition.api_id}).',
                      style="green")

    return season, competition

# Fetch Standings
def fetch_standings(season: Season, competition: Competition):
    console.print(f'Fetching standings data for {season.year} {competition.name} (Competition ID: {competition.api_id}) season.',
                  style="blue")
    # API Request Setup
    url = "https://v3.football.api-sports.io/standings"
    params = {'league': competition.api_id, 'season': season.year}
    # API Request
    standings_data = api_request(url, params)
    standings_response = standings_data['response'][0]['league']['standings'][0]
    # Process each Standing in Response
    new_standings = []
    for team_entry in standings_response:
        team_info = team_entry['team']
        stats = team_entry['all']
        home_stats = team_entry['home']
        away_stats = team_entry['away']
        # Find Team
        team = Team.objects.filter(api_id=team_info['id']).first()
        # Find or create the Standing
        standing = Standing.objects.filter(team=team, season=season).first()
        if not standing:
            # Create standings entry
            standing = Standing(
                team=team,
                season=season,
                position=team_entry['rank'],
                points=team_entry['points'],
                goals_for=stats['goals']['for'],
                goals_against=stats['goals']['against'],
                goal_diff=(stats['goals']['for'] - stats['goals']['against']),
                played=stats['played'],
                wins=stats['win'],
                draws=stats['draw'],
                losses=stats['lose'],
                home_goals_for=home_stats['goals']['for'],
                home_goals_against=home_stats['goals']['against'],
                home_goal_diff=(home_stats['goals']['for'] - home_stats['goals']['against']),
                home_played=home_stats['played'],
                home_wins=home_stats['win'],
                home_draws=home_stats['draw'],
                home_losses=home_stats['lose'],
                away_goals_for=away_stats['goals']['for'],
                away_goals_against=away_stats['goals']['against'],
                away_goal_diff=(away_stats['goals']['for'] - away_stats['goals']['against']),
                away_played=away_stats['played'],
                away_wins=away_stats['win'],
                away_draws=away_stats['draw'],
                away_losses=away_stats['lose'],
            )
            new_standings.append(standing)

    if new_standings:
        Standing.objects.bulk_create(new_standings)
        console.print(f'New standings were added!', style="bold green")
    else:
        console.print(f'No new standings were added!', style="bold red")


# Fetch Fixtures
def fetch_fixtures(season: Season, competition: Competition):
    console.print(f'Fetching fixture data for {season.year} season with league ID {competition.api_id}.',
                  style="blue")
    # API Request Setup
    url = "https://v3.football.api-sports.io/fixtures"
    params = {'league': competition.api_id, 'season': season.year}
    # API Request
    fixture_data = api_request(url, params)
    fixtures_response = fixture_data['response']
    # Process each Fixture in Response
    new_fixtures = []
    for entry in fixtures_response:
        fixture_id = entry['fixture']['id']
        fixture_data = entry['fixture']
        venue = Venue.objects.filter(api_id = fixture_data['venue']['id']).first()
        if not venue:
            # Create Venue
            country = Country.objects.filter(name = entry['league']['country']).first()
            if fixture_data['venue']['id']:
                venue = Venue(
                    api_id=fixture_data['venue']['id'],
                    name=fixture_data['venue']['name'],
                    address=None,
                    city=fixture_data['venue']['city'],
                    country=country,
                    capacity=None,
                    surface=None,
                    image=None
                )
                venue.save()
                console.print(f'Created new venue: {venue.name}.', style="green")
        # Find or create the Fixture
        fixture = Fixture.objects.filter(api_id=fixture_id).first()
        if not fixture:
            # Create fixture entry
            date_str = fixture_data.get('date')
            date_value = datetime.fromisoformat(date_str) if date_str else None
            fixture = Fixture(
                api_id=fixture_id,
                season=season,
                home_team_id=entry['teams']['home']['id'],
                away_team_id=entry['teams']['away']['id'],
                venue=venue,
                competition=competition,
                referee=fixture_data['referee'],
                date=date_value,
                short_status=fixture_data['status']['short'],
                elapsed=fixture_data['status']['elapsed'],
                round=entry['league']['round'],
                home_goals=entry['goals']['home'],
                away_goals=entry['goals']['away'],
                half_home_goals=entry['score']['halftime']['home'],
                half_away_goals=entry['score']['halftime']['away'],
                full_home_goals=entry['score']['fulltime']['home'],
                full_away_goals=entry['score']['fulltime']['away'],
                et_home_goals=entry['score']['extratime']['home'],
                et_away_goals=entry['score']['extratime']['away'],
                pen_home_goals=entry['score']['penalty']['home'],
                pen_away_goals=entry['score']['penalty']['away']
            )
            new_fixtures.append(fixture)
    if new_fixtures:
        Fixture.objects.bulk_create(new_fixtures)
        console.print(f'{len(new_fixtures)} new fixtures were added!', style="bold green")
    else:
        console.print(f'No new fixtures were added!', style="bold red")


# Make MetaData join table
def make_meta_join_table(season: Season):
    # Find Fixtures
    fixtures = Fixture.objects.filter(season=season).all()
    home_venue = []
    for fixture in fixtures:
        home_venue.append((
            fixture.home_team_id,
            fixture.venue_id
        ))
    unique_home_venue = set(home_venue)
    new_meta_entries = []
    for pair in unique_home_venue:
        # Find or Make Meta Instance

        team = Team.objects.filter(api_id=pair[0]).first()
        meta_instance = TeamSeasonCompetition.objects.filter(season=season, team=team).first()
        if not meta_instance:
            meta_instance = TeamSeasonCompetition(
                team=team,
                season=season,
                competition=season.competition,
                venue_id=pair[1]
            )
            new_meta_entries.append(meta_instance)
            console.print(f'Created new meta instance: {pair}.', style="green")
    if new_meta_entries:
        TeamSeasonCompetition.objects.bulk_create(new_meta_entries)
        console.print(f'Successfully added {len(new_meta_entries)} meta instances!', style="bold green")
    else:
        console.print(f'No new meta instances were added!', style="bold red")