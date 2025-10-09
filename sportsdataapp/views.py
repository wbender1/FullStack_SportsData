from django.shortcuts import render
from django.db.models import Q
from .models import Competition, Country, Fixture, FixtureStats, Season, Standing, Team, Venue

# Create your views here.


# Index View
def index(request):
    return render(request, "sportsdataapp/index.html")


# Search Competitions View
def competitions_view(request):
    if request.method == 'GET':
        competitions = Competition.objects.all()
        country_query = request.GET.get("country", '')
        competition_query = request.GET.get("type")
        if country_query and competition_query:
            competitions = competitions.filter(
                country__name__icontains=country_query,
                type=competition_query).order_by('name')
            return render(request, 'sportsdataapp/competitions.html', {'competitions': competitions})
        if competition_query:
            competitions = competitions.filter(type=competition_query).order_by('country__name', 'name')
            return render(request, 'sportsdataapp/competitions.html', {'competitions': competitions})
        if country_query:
            competitions = competitions.filter(country__name__icontains=country_query).order_by('name')
            return render(request, 'sportsdataapp/competitions.html', {'competitions': competitions})
        else:
            competitions = competitions.order_by('country__name', 'name')
            return render(request, 'sportsdataapp/competitions.html', {'competitions': competitions})
    return render(request, 'sportsdataapp/competitions.html',)
