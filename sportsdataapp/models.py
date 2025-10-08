from django.db import models

# Define Country Model
class Country(models.Model):
    name = models.CharField(max_length=100)
    num_competitions = models.IntegerField()
    code = models.CharField(max_length=10, null=True, blank=True)
    flag = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

# Define Competition Model
class Competition(models.Model):
    api_id = models.IntegerField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=15)
    logo = models.URLField()

    class Meta:
        verbose_name = "Competition"
        verbose_name_plural = "Competitions"

    def __str__(self):
        return self.name

# Define Team Model
class Team(models.Model):
    api_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    founded = models.IntegerField(null=True, blank=True)
    national = models.BooleanField(default=False)
    logo_url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name

# Define Venue Model
class Venue(models.Model):
    api_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    capacity = models.IntegerField(null=True, blank=True)
    surface = models.CharField(max_length=50, null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Venue"
        verbose_name_plural = "Venues"

    def __str__(self):
        return self.name

# Define Season Model
class Season(models.Model):
    year = models.IntegerField()
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"

    def __str__(self):
        return f'{self.year} {self.competition}'

# Define TeamSeasonCompetition Model
class TeamSeasonCompetition(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)


# Define Standings Model
class Standing(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    position = models.IntegerField()
    points = models.IntegerField()
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    goal_diff = models.IntegerField()
    played = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()
    home_goals_for = models.IntegerField()
    home_goals_against = models.IntegerField()
    home_goal_diff = models.IntegerField()
    home_played = models.IntegerField()
    home_wins = models.IntegerField()
    home_draws = models.IntegerField()
    home_losses = models.IntegerField()
    away_goals_for = models.IntegerField()
    away_goals_against = models.IntegerField()
    away_goal_diff = models.IntegerField()
    away_played = models.IntegerField()
    away_wins = models.IntegerField()
    away_draws = models.IntegerField()
    away_losses = models.IntegerField()

    class Meta:
        verbose_name = "Standings"
        verbose_name_plural = "Standings\'"

    def __str__(self):
        return f'{self.team} {self.season} (Position: {self.position})'

# Define Fixture Model
class Fixture(models.Model):
    api_id = models.IntegerField(primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_fixtures', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_fixtures', on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    referee = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    short_status = models.CharField(max_length=15)
    elapsed = models.IntegerField(null=True, blank=True)
    round = models.CharField(max_length=100)
    home_goals = models.IntegerField(null=True, blank=True)
    away_goals = models.IntegerField(null=True, blank=True)
    half_home_goals = models.IntegerField(null=True, blank=True)
    half_away_goals = models.IntegerField(null=True, blank=True)
    full_home_goals = models.IntegerField(null=True, blank=True)
    full_away_goals = models.IntegerField(null=True, blank=True)
    et_home_goals = models.IntegerField(null=True, blank=True)
    et_away_goals = models.IntegerField(null=True, blank=True)
    pen_home_goals = models.IntegerField(null=True, blank=True)
    pen_away_goals = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Fixture"
        verbose_name_plural = "Fixtures"

    def __str__(self):
        return f'{self.season}: {self.home_team} vs. {self.away_team}'


# Define FixtureStats Model
class FixtureStats(models.Model):
    fixture = models.OneToOneField(Fixture, on_delete=models.CASCADE, related_name="stats")
    home_sh_on_goal = models.IntegerField(null=True, blank=True)
    home_sh_off_goal = models.IntegerField(null=True, blank=True)
    home_total_sh = models.IntegerField(null=True, blank=True)
    home_blocked_sh = models.IntegerField(null=True, blank=True)
    home_sh_inside = models.IntegerField(null=True, blank=True)
    home_sh_outside = models.IntegerField(null=True, blank=True)
    home_fouls = models.IntegerField(null=True, blank=True)
    home_corners = models.IntegerField(null=True, blank=True)
    home_offsides = models.IntegerField(null=True, blank=True)
    home_possession = models.CharField(max_length=20, null=True, blank=True)
    home_yellows = models.IntegerField(null=True, blank=True)
    home_reds = models.IntegerField(null=True, blank=True)
    home_saves = models.IntegerField(null=True, blank=True)
    home_tot_passes = models.IntegerField(null=True, blank=True)
    home_accurate_pass = models.IntegerField(null=True, blank=True)
    home_percent_pass = models.CharField(max_length=20, null=True, blank=True)
    home_ex_goals = models.CharField(max_length=20, null=True, blank=True)
    away_sh_on_goal = models.IntegerField(null=True, blank=True)
    away_sh_off_goal = models.IntegerField(null=True, blank=True)
    away_total_sh = models.IntegerField(null=True, blank=True)
    away_blocked_sh = models.IntegerField(null=True, blank=True)
    away_sh_inside = models.IntegerField(null=True, blank=True)
    away_sh_outside = models.IntegerField(null=True, blank=True)
    away_fouls = models.IntegerField(null=True, blank=True)
    away_corners = models.IntegerField(null=True, blank=True)
    away_offsides = models.IntegerField(null=True, blank=True)
    away_possession = models.CharField(max_length=20, null=True, blank=True)
    away_yellows = models.IntegerField(null=True, blank=True)
    away_reds = models.IntegerField(null=True, blank=True)
    away_saves = models.IntegerField(null=True, blank=True)
    away_tot_passes = models.IntegerField(null=True, blank=True)
    away_accurate_pass = models.IntegerField(null=True, blank=True)
    away_percent_pass = models.CharField(max_length=20, null=True, blank=True)
    away_ex_goals = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Fixture Stats"
        verbose_name_plural = "Fixture Stats"
