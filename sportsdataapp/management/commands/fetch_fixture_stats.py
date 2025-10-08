from django.core.management.base import BaseCommand
from apiscripts.general import fetch_fixture_stats  # import the above function

class Command(BaseCommand):
    help = "Fetch fixture statistics"

    def add_arguments(self, parser):
        parser.add_argument("year", type=int, help="Year of the season")
        parser.add_argument("team_name", type=str, help="Team name")
        parser.add_argument("competition_name", nargs="?", type=str, help="Competition name (optional)")

    def handle(self, *args, **options):
        year = options["year"]
        team_name = options["team_name"]
        competition_name = options.get("competition_name")

        fetch_fixture_stats(year, team_name, competition_name)
