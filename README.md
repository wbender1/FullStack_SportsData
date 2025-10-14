# FullStack SportsData

This project is a full-stack Django web application designed to fetch, store, and display comprehensive football (soccer) data. It utilizes the [API-SPORTS](https://www.api-football.com/) service to populate a PostgreSQL database and presents the information through a user-friendly, filterable web interface.

## Features

*   **Data Aggregation:** Fetches and stores data for countries, competitions (leagues and cups), teams, venues, seasons, and fixtures.
*   **Detailed Statistics:** Retrieves detailed league standings and in-depth match statistics, including shots, passes, fouls, cards, and expected goals (xG).
*   **Django Backend:** Built with a robust Django framework, leveraging its ORM for database interactions.
*   **PostgreSQL Database:** Uses PostgreSQL for efficient and scalable data storage.
*   **Web Interface:** A clean, navigable frontend built with HTML and Bootstrap for viewing and filtering the collected sports data.
*   **Custom Management Commands:** Provides command-line tools to easily populate the database with data from the API.

## Tech Stack

*   **Backend:** Python, Django
*   **Database:** PostgreSQL
*   **Frontend:** HTML, Bootstrap CSS
*   **Core Python Libraries:**
    *   `requests`: For making HTTP requests to the API.
    *   `python-decouple`: For managing environment variables.
    *   `psycopg2-binary`: PostgreSQL adapter for Python.
    *   `rich`, `tabulate`: For formatted console output in management commands.

## Setup and Installation

### 1. Prerequisites

*   Python 3.x
*   PostgreSQL installed and running.
*   An API key from [API-SPORTS](https://www.api-football.com/).

### 2. Clone the Repository

```bash
git clone https://github.com/wbender1/FullStack_SportsData.git
cd FullStack_SportsData
```

### 3. Set up a Virtual Environment

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install django psycopg2-binary python-decouple requests rich tabulate
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory of the project and add the following, replacing the placeholder values with your actual credentials:

```
SECRET_KEY='your-django-secret-key'
FOOTBALL_API_KEY='your-api-sports-key'
DATABASE_PASSWORD='your-postgresql-password'
```

### 6. Database Setup

1.  Open your PostgreSQL command-line tool (e.g., `psql`).
2.  Create a new user and database. The application is configured by default to use:
    *   Database Name: `sportsstats`
    *   User: `sportsuser`
    *   Password: The one you set in your `.env` file.

    ```sql
    CREATE DATABASE sportsstats;
    CREATE USER sportsuser WITH PASSWORD 'your-postgresql-password';
    ALTER ROLE sportsuser SET client_encoding TO 'utf8';
    ALTER ROLE sportsuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE sportsuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE sportsstats TO sportsuser;
    ```

### 7. Apply Database Migrations

Run the following command to create the database tables based on the Django models:

```bash
python manage.py migrate
```

## Usage

### 1. Populating the Database

Data is fetched from the API using custom Django management commands. The process is sequential: you must fetch a country before fetching its seasons, and you must fetch a season before fetching fixture stats.

**A. Fetch Country Data**
This command fetches all competitions, teams, and venues for a given country.

```bash
python manage.py fetch_country "England"
```

**B. Fetch Season Data**
This command fetches standings (for leagues) and all fixtures for a specific competition and year.

```bash
# For a league
python manage.py fetch_season "Premier League" 2023

# For a cup
python manage.py fetch_season "FA Cup" 2023
```

**C. Fetch Fixture Statistics**
This command fetches detailed match-by-match statistics for a specific team in a given year. You can optionally narrow it down to a single competition.

```bash
# For all competitions in a year
python manage.py fetch_fixture_stats 2023 "Manchester United"

# For a specific competition in a year
python manage.py fetch_fixture_stats 2023 "Manchester United" "Premier League"
```
*Note: The API has a rate limit, and fetching fixture stats can be slow as each fixture requires a separate API call.*

### 2. Running the Web Application

Start the Django development server:

```bash
python manage.py runserver
```

Open your web browser and navigate to `http://127.0.0.1:8000/`.

### 3. Web Interface

The web interface provides several views to explore the data:

*   **Home:** The main entry point with links to all data tables.
*   **Countries:** Lists all countries in the database.
*   **Competitions:** View all leagues and cups, with filters for name, country, and type (League/Cup).
*   **Teams:** Browse all teams, filterable by name, country, competition, and type (Club/National).
*   **Venues:** See venue information with filters for name, city, country, and surface.
*   **Seasons:** A list of all competition seasons, filterable by year, country, and competition.
*   **Standings:** Search for and view league standings for a specific competition and year.
*   **Fixtures:** Search for match results and schedules. You can filter by season and team(s).
*   **Fixture Stats:** From the fixtures view, click "View" on any match to see a detailed breakdown of team statistics, including a box score and performance metrics.