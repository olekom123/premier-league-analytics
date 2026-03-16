"""
predict_match.py

Predicts the outcome of a Premier League match using the Poisson distribution model.
Takes two team names and a season as input, outputs home win / draw / away win probabilities.

Model logic:
- Uses team season stats from fct_team_season_stats
- Calculates expected goals for each team using attack/defence strength relative to league average
- Uses Poisson distribution to calculate probability of each scoreline up to 10 goals
- Sums scoreline probabilities into home win / draw / away win

Source: https://en.wikipedia.org/wiki/Poisson_distribution
"""

import duckdb
import math

DB_PATH = '/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db'

def get_team_stats(season):
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute(f"""
        select
            team,
            home_avg_scored,
            home_avg_conceded,
            away_avg_scored,
            away_avg_conceded
        from fct_team_season_stats
        where season = '{season}'
    """).fetchdf()
    con.close()
    return df.set_index('team')

def get_league_averages(season):
    con = duckdb.connect(DB_PATH, read_only=True)
    result = con.execute(f"""
        select
            avg(home_avg_scored)    as league_home_avg,
            avg(away_avg_scored)    as league_away_avg
        from fct_team_season_stats
        where season = '{season}'
    """).fetchone()
    con.close()
    return result[0], result[1]

def poisson_prob(lam, k):
    return (math.exp(-lam) * lam**k) / math.factorial(k)

def predict(home_team, away_team, season):
    stats = get_team_stats(season)
    league_home_avg, league_away_avg = get_league_averages(season)

    home = stats.loc[home_team]
    away = stats.loc[away_team]

    home_expected = (home['home_avg_scored'] / league_home_avg) * \
                    (away['away_avg_conceded'] / league_away_avg) * \
                    league_home_avg

    away_expected = (away['away_avg_scored'] / league_away_avg) * \
                    (home['home_avg_conceded'] / league_home_avg) * \
                    league_away_avg

    max_goals = 10
    home_win = draw = away_win = 0.0

    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = poisson_prob(home_expected, h) * poisson_prob(away_expected, a)
            if h > a:
                home_win += p
            elif h == a:
                draw += p
            else:
                away_win += p

    print(f"\n{home_team} vs {away_team} ({season})")
    print(f"Expected goals: {home_team} {home_expected:.2f} - {away_expected:.2f} {away_team}")
    print(f"Home win:  {home_win:.1%}")
    print(f"Draw:      {draw:.1%}")
    print(f"Away win:  {away_win:.1%}")

if __name__ == "__main__":
    season = input("Season (e.g. 2425): ")
    home = input("Home team: ")
    away = input("Away team: ")
    predict(home, away, season)