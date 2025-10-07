from django.core.management.base import BaseCommand
from apiscripts.general import fetch_country  # import your function

class Command(BaseCommand):
    help = "Fetch country data from API and store it in the database"

    def add_arguments(self, parser):
        parser.add_argument("country_name", type=str, help="Name of the country")

    def handle(self, *args, **options):
        country_name = options["country_name"]
        fetch_country(country_name)
        self.stdout.write(self.style.SUCCESS(f"Finished fetching data for {country_name}"))
