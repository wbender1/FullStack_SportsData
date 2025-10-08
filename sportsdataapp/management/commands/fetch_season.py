from django.core.management.base import BaseCommand
from apiscripts.general import fetch_season  # import your function

class Command(BaseCommand):
    help = "Fetch season data from API and store it in the database"

    def add_arguments(self, parser):
        parser.add_argument("competition", type=str, help="Name of the competition")
        parser.add_argument("year", type=int, help="Year of the season")

    def handle(self, *args, **options):
        competition = options["competition"]
        year = options["year"]
        fetch_season(competition, year)
        self.stdout.write(self.style.SUCCESS(f"Finished fetching data for {year} {competition}"))
