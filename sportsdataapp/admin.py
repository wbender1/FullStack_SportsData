from django.contrib import admin
from .models import Country, Team, Season, Competition, Venue, Fixture, FixtureStats



class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "num_competitions", "code", "flag")
    search_fields = ("name",)
admin.site.register(Country, CountryAdmin)


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("api_id", "country_name", "name", "type", "logo")
    def country_name(self, obj):
        return obj.country.name
    country_name.admin_order_field = "country__name"
    country_name.short_description = "Country"
    search_fields = ("api_id", "country__name", "name", "type")
    list_filter = ("country__name", "type")
admin.site.register(Competition, CompetitionAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ("api_id", "name", "short_name", "country_name",
                    "founded", "national", "logo_url")
    def country_name(self, obj):
        return obj.country.name

    country_name.admin_order_field = "country__name"
    country_name.short_description = "Country"
    search_fields = ("api_id", "name", "country__name", "national")
    list_filter = ("country__name", "national")
admin.site.register(Team, TeamAdmin)


class VenueAdmin(admin.ModelAdmin):
    list_display = ("api_id", "name", "address", "city", "country_name",
                    "capacity", "surface", "image")
    def country_name(self, obj):
        return obj.country.name
    country_name.admin_order_field = "country__name"
    country_name.short_description = "Country"
    search_fields = ("api_id", "name", "country__name")
    list_filter = ("country__name",)
admin.site.register(Venue, VenueAdmin)


class SeasonAdmin(admin.ModelAdmin):
    list_display = ("id", "year", "competition_name")
    def competition_name(self, obj):
        return obj.competition.name
    competition_name.admin_order_field = "competition__name"
    competition_name.short_description = "Competition"
    search_fields = ("year", "competition__name")
    list_filter = ("year", "competition__name")
admin.site.register(Season, SeasonAdmin)


class FixtureAdmin(admin.ModelAdmin):
    list_display = ("id", "season_year", "season_competition_name",
                    "home_team", "away_team", "venue_name", "referee",
                    "date", "round", "home_goals", "away_goals")
    def season_year(self, obj):
        return obj.season.year
    season_year.admin_order_field = "season__year"
    season_year.short_description = "Season"
    def venue_name(self, obj):
        return obj.venue.name
    venue_name.admin_order_field = "venue__name"
    venue_name.short_description = "Venue"
    def season_competition_name(self, obj):
        return obj.season.competition.name
    season_competition_name.admin_order_field = "season__competition__name"
    season_competition_name.short_description = "Competition"
    search_fields = ("season__year", "season__competition__name")
    list_filter = ("season__year", "season__competition__name")
admin.site.register(Fixture, FixtureAdmin)


class FixtureStatsAdmin(admin.ModelAdmin):
    list_display = ("id", "fixture_season_year",
                    "fixture_season_competition_name",
                    "fixture_home_team", "fixture_away_team")
    def fixture_season_year(self, obj):
        return obj.fixture.season.year
    fixture_season_year.admin_order_field = "fixture__season__year"
    fixture_season_year.short_description = "Season"
    def fixture_season_competition_name(self, obj):
        return obj.fixture.season.competition.name
    fixture_season_competition_name.admin_order_field = "fixture__season__competition__name"
    fixture_season_competition_name.short_description = "Competition"
    def fixture_home_team(self, obj):
        return obj.fixture.home_team.name
    fixture_home_team.admin_order_field = "fixture__home_team__name"
    fixture_home_team.short_description = "Team"
    def fixture_away_team(self, obj):
        return obj.fixture.away_team.name
    fixture_away_team.admin_order_field = "fixture__away_team__name"
    fixture_away_team.short_description = "Team"
    search_fields = ("fixture__season__year", "fixture__season__competition__name")
    list_filter = ("fixture__season__year", "fixture__season__competition__name")
admin.site.register(FixtureStats, FixtureStatsAdmin)