from django.shortcuts import render
from django.db.models import Q
from .models import Competition, Country, Fixture, FixtureStats, Season, Standing, Team, TeamSeasonCompetition, Venue

# Create your views here.


# Index View
def index(request):
    return render(request, "sportsdataapp/index.html")


# Competitions View
def competitions_view(request):
    if request.method == 'GET':
        competitions = Competition.objects.all()
        name_query = request.GET.get("name", '')
        country_query = request.GET.get("country", '')
        competition_query = request.GET.get("type")
        # Filter Competitions
        if name_query:
            competitions = competitions.filter(name__icontains=name_query)
        if competition_query:
            competitions = competitions.filter(type=competition_query)
        if country_query:
            competitions = competitions.filter(country__name__icontains=country_query)
    # Order Competitions
    competitions = competitions.order_by('country__name', '-type', 'name')
    total = competitions.count()
    return render(request, 'sportsdataapp/competitions.html', {'competitions': competitions, 'total': total})


# Competitions View
def countries_view(request):
    countries = Country.objects.all().order_by('name')
    total = countries.count()
    return render(request, 'sportsdataapp/countries.html', {'countries': countries, 'total': total})

# Fixtures View
def fixtures_view(request):
    return 0

# Fixture Stats View
def fixture_stats_view(request):
    return 0

# Seasons View
def seasons_view(request):
    if request.method == 'GET':
        seasons = Season.objects.all()
        year_query = request.GET.get("year", '')
        country_query = request.GET.get("country", '')
        competition_query = request.GET.get("competition", '')
        competition_type_query = request.GET.get("type")
        # Filter Seasons
        if year_query:
            seasons = seasons.filter(year__icontains=year_query)
        if country_query:
            seasons = seasons.filter(competition__country__name__icontains=country_query)
        if competition_query:
            seasons = seasons.filter(competition__name__icontains=competition_query)
        if competition_type_query:
            seasons = seasons.filter(competition__type=competition_type_query)
    # Order Seasons
    seasons = seasons.order_by('year', 'competition__country__name', '-competition__type', 'competition__name')
    total = seasons.count()
    return render(request, 'sportsdataapp/seasons.html', {'seasons': seasons, 'total': total})

# Standings View
def standings_view(request):
    return 0

# Teams View
def teams_view(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        name_query = request.GET.get("name", '')
        country_query = request.GET.get("country", '')
        short_name_query = request.GET.get("short_name", '')
        national_query = request.GET.get("type", '')
        competition_query = request.GET.get("competition", '')
        # Filter Teams
        if name_query:
            teams = teams.filter(name__icontains=name_query)
        if country_query:
            teams = teams.filter(country__name__icontains=country_query)
        if short_name_query:
            teams = teams.filter(short_name__icontains=short_name_query)
        if competition_query:
            teams = teams.filter(teamseasoncompetition__competition__name__icontains=competition_query)
        if national_query:
            if national_query == "true":
                teams = teams.filter(national=True)
            if national_query == "false":
                teams = teams.filter(national=False)
    # Order Teams
    teams = teams.order_by('country__name', 'teamseasoncompetition__competition__name', 'national', 'name')
    total = teams.count()
    return render(request, 'sportsdataapp/teams.html', {'teams': teams, 'total': total},)

# Venues View
def venues_view(request):
    if request.method == 'GET':
        venues = Venue.objects.all().distinct()
        name_query = request.GET.get("name", '')
        city_query = request.GET.get("city", '')
        country_query = request.GET.get("country", '')
        surface_query = request.GET.get("surface", '')
        competition_query = request.GET.get("competition", '')
        # Filter Venues
        if name_query:
            venues = venues.filter(name__icontains=name_query)
        if city_query:
            venues = venues.filter(city__icontains=city_query)
        if country_query:
            venues = venues.filter(country__name__icontains=country_query)
        if surface_query:
            venues = venues.filter(surface__icontains=surface_query)
        if competition_query:
            venues = venues.filter(teamseasoncompetition__competition__name__icontains=competition_query)
    # Order Venues
    venues = venues.order_by('country__name', 'teamseasoncompetition__competition__name', 'name')
    total = venues.count()
    return render(request, 'sportsdataapp/venues.html', {'venues': venues, 'total': total}, )