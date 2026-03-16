"""
fetch_matches.py

Downloads current season (2024/25) Premier League match results
from football-data.org API into DuckDB table `raw_matches`.

Runs a full refresh every time (DELETE + reinsert).
Requires FOOTBALL_DATA_API_KEY in .env file.
Source: https://www.football-data.org
"""
import os                                                                                                                                                
import requests 
import duckdb                                                                                                                                            
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

def fetch_matches():
    headers = {"X-Auth-Token": API_KEY}
    url = f"{BASE_URL}/competitions/PL/matches?season=2024"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()["matches"]

def load_to_duckdb(matches):
    con = duckdb.connect("../data/pl_analytics.db")

    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_matches (
            id INTEGER,
            utc_date VARCHAR,
            status VARCHAR,
            matchday INTEGER,
            home_team VARCHAR,
            away_team VARCHAR,
            home_score INTEGER,
            away_score INTEGER
        )
    """)

    con.execute("DELETE FROM raw_matches")

    for match in matches:
        con.execute("""
            INSERT INTO raw_matches VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            match["id"],
            match["utcDate"],
            match["status"],
            match["matchday"],
            match["homeTeam"]["name"],
            match["awayTeam"]["name"],
            match["score"]["fullTime"]["home"],
            match["score"]["fullTime"]["away"]
        ])

    print(f"Loaded {len(matches)} matches into DuckDB")
    con.close()

if __name__ == "__main__":
    matches = fetch_matches()
    load_to_duckdb(matches)