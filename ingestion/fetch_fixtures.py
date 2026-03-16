"""
fetch_fixtures.py

Fetches upcoming Premier League fixtures from football-data.org API.
Loads into DuckDB table `raw_fixtures`.

Season is calculated dynamically based on current month.
Requires FOOTBALL_DATA_API_KEY in .env file.
Source: https://www.football-data.org
"""

import os
import requests
import duckdb
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
DB_PATH = '/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db'

def get_current_season():
    now = datetime.now()
    return now.year if now.month >= 8 else now.year - 1

def fetch_fixtures(season):
    headers = {"X-Auth-Token": API_KEY}
    url = f"{BASE_URL}/competitions/PL/matches?season={season}&status=SCHEDULED"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()["matches"]

def load_to_duckdb(matches):
    if len(matches) == 0:
        print("WARNING: 0 upcoming fixtures loaded. Season may be finished or API issue.")
        return

    con = duckdb.connect(DB_PATH)

    con.execute("DROP TABLE IF EXISTS raw_fixtures")
    con.execute("""
        CREATE TABLE raw_fixtures (
            id INTEGER,
            utc_date VARCHAR,
            matchday INTEGER,
            home_team VARCHAR,
            away_team VARCHAR
        )
    """)

    for match in matches:
        con.execute("""
            INSERT INTO raw_fixtures VALUES (?, ?, ?, ?, ?)
        """, [
            match["id"],
            match["utcDate"],
            match["matchday"],
            match["homeTeam"]["name"],
            match["awayTeam"]["name"]
        ])

    print(f"Loaded {len(matches)} upcoming fixtures into DuckDB")
    con.close()

if __name__ == "__main__":
    season = get_current_season()
    print(f"Fetching fixtures for season {season}/{str(season+1)[-2:]}")
    fixtures = fetch_fixtures(season)
    load_to_duckdb(fixtures)