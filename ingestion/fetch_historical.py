"""
fetch_historical.py

Downloads Premier League match data from football-data.co.uk for 20+ seasons.
Loads the following into DuckDB table `raw_matches_historical`:
- Match results (full time + half time)
- Match stats (shots on target, corners, cards)
- Bet365 odds (home/draw/away + over/under 2.5)

Runs a full refresh every time (DROP + recreate).
Source: https://www.football-data.co.uk
"""
import os
import requests
import duckdb
import pandas as pd
from io import StringIO

DB_PATH = '/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db'

SEASONS = [
    '2526', '2425', '2324', '2223', '2122', '2021',
    '1920', '1819', '1718', '1617', '1516', '1415',
    '1314', '1213', '1112', '1011', '0910', '0809',
    '0708', '0607', '0506'
]

COLUMNS = [
    'Div', 'Date', 'HomeTeam', 'AwayTeam',
    'FTHG', 'FTAG', 'FTR',
    'HTHG', 'HTAG', 'HTR',
    'HST', 'AST',
    'HC', 'AC',
    'HY', 'AY',
    'HR', 'AR',
    'B365H', 'B365D', 'B365A',
    'B365>2.5', 'B365<2.5'
]

def fetch_season(season):
    url = f'https://www.football-data.co.uk/mmz4281/{season}/E0.csv'
    response = requests.get(url)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text), usecols=lambda c: c in COLUMNS)
    df['season'] = season
    df = df.dropna(subset=['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'])
    print(f"Season {season}: {len(df)} matches loaded")
    return df

def load_to_duckdb(df):
    con = duckdb.connect(DB_PATH)
    con.execute("DROP TABLE IF EXISTS raw_matches_historical")
    con.execute("""
        CREATE TABLE raw_matches_historical AS
        SELECT * FROM df
    """)
    print(f"Total: {len(df)} matches loaded into raw_matches_historical")
    con.close()

if __name__ == "__main__":
    all_seasons = []
    for season in SEASONS:
        try:
            df = fetch_season(season)
            all_seasons.append(df)
        except Exception as e:
            print(f"Season {season} failed: {e}")

    combined = pd.concat(all_seasons, ignore_index=True)
    load_to_duckdb(combined)