"""
predict_match.py

Predicts outcomes for all upcoming Premier League fixtures using the Poisson model.
Reads upcoming fixtures from raw_fixtures and team stats from fct_team_season_stats.
Stores predictions in DuckDB table `raw_predictions`.

Model logic:
- Uses team season stats from fct_team_season_stats
- Calculates expected goals using attack/defence strength relative to league average
- Uses Poisson distribution to calculate home win / draw / away win probabilities

Source: https://en.wikipedia.org/wiki/Poisson_distribution
"""

import duckdb
import math
from datetime import datetime

DB_PATH = '/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db'

def get_current_season():
    now = datetime.now()
    return str(now.year if now.month >= 8 else now.year - 1)[2:] + \
            str(now.year + 1 if now.month >= 8 else now.year)[2:]

def get_team_stats(con, season):
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
    return df.set_index('team')

def get_league_averages(con, season):
    result = con.execute(f"""
        select
            avg(home_avg_scored)    as league_home_avg,
            avg(away_avg_scored)    as league_away_avg
        from fct_team_season_stats
        where season = '{season}'
    """).fetchone()
    return result[0], result[1]

def get_fixtures(con):
    return con.execute("""
        select id, utc_date, matchday, home_team, away_team
        from raw_fixtures
        order by utc_date
    """).fetchdf()

def poisson_prob(lam, k):
    return (math.exp(-lam) * lam**k) / math.factorial(k)

def calculate_probabilities(home_expected, away_expected, max_goals=10):
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
    return home_win, draw, away_win

def predict_all_fixtures(con, fixtures, stats, league_home_avg, league_away_avg):
    predictions = []

    for _, fixture in fixtures.iterrows():
        home_team = fixture['home_team']
        away_team = fixture['away_team']

        if home_team not in stats.index or away_team not in stats.index:
            print(f"WARNING: missing stats for {home_team} vs {away_team} — skipping")
            continue

        home = stats.loc[home_team]
        away = stats.loc[away_team]

        home_expected = (home['home_avg_scored'] / league_home_avg) * \
                        (away['away_avg_conceded'] / league_away_avg) * \
                        league_home_avg

        away_expected = (away['away_avg_scored'] / league_away_avg) * \
                        (home['home_avg_conceded'] / league_home_avg) * \
                        league_away_avg

        home_win, draw, away_win = calculate_probabilities(home_expected, away_expected)

        predictions.append({
            'fixture_id':       fixture['id'],
            'utc_date':         fixture['utc_date'],
            'matchday':         fixture['matchday'],
            'home_team':        home_team,
            'away_team':        away_team,
            'home_expected':    round(home_expected, 3),
            'away_expected':    round(away_expected, 3),
            'prob_home_win':    round(home_win, 4),
            'prob_draw':        round(draw, 4),
            'prob_away_win':    round(away_win, 4),
            'predicted_outcome': 'home' if home_win > draw and home_win > away_win
                                else 'draw' if draw > away_win
                                else 'away',
            'predicted_at':     datetime.now().isoformat()
        })

    return predictions

def load_to_duckdb(con, predictions):
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_predictions (
            fixture_id          INTEGER,
            utc_date            VARCHAR,
            matchday            INTEGER,
            home_team           VARCHAR,
            away_team           VARCHAR,
            home_expected       DOUBLE,
            away_expected       DOUBLE,
            prob_home_win       DOUBLE,
            prob_draw           DOUBLE,
            prob_away_win       DOUBLE,
            predicted_outcome   VARCHAR,
            predicted_at        VARCHAR
        )
    """)

    existing_ids = set(
        row[0] for row in con.execute("SELECT fixture_id FROM raw_predictions").fetchall()
    )

    new_predictions = [p for p in predictions if p['fixture_id'] not in existing_ids]

    for p in new_predictions:
        con.execute("""
            INSERT INTO raw_predictions VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, list(p.values()))

    print(f"Stored {len(new_predictions)} new predictions ({len(predictions) - len(new_predictions)} already existed)")

if __name__ == "__main__":
    con = duckdb.connect(DB_PATH)
    season = get_current_season()
    print(f"Generating predictions for season {season}")

    stats = get_team_stats(con, season)
    league_home_avg, league_away_avg = get_league_averages(con, season)
    fixtures = get_fixtures(con)

    predictions = predict_all_fixtures(con, fixtures, stats, league_home_avg, league_away_avg)
    load_to_duckdb(con, predictions)
    con.close()