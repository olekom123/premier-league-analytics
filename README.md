# Premier League Analytics

A full end-to-end data engineering project analysing 21 seasons of Premier League data with match outcome predictions.

## What it does
- Pulls 21 seasons of PL match data (7,900+ matches) from football-data.co.uk
- Fetches upcoming fixtures from football-data.org API
- Transforms raw data using dbt with full test coverage
- Predicts match outcomes using the Poisson statistical model
- Displays everything in an interactive Streamlit dashboard with season filtering

## Tech stack
| Tool | Purpose |
|------|---------|
| Python | Data ingestion scripts |
| DuckDB | Local database (free Snowflake alternative) |
| dbt Core | Data transformations and testing |
| Streamlit | Interactive dashboard |
| macOS cron | Daily automated refresh |

## Project structure

    premier-league-analytics/
    ├── ingestion/
    │   ├── fetch_historical.py   # 21 seasons of match data + odds
    │   ├── fetch_fixtures.py     # upcoming fixtures
    │   └── predict_match.py      # Poisson prediction model
    ├── dbt/pl_analytics/
    │   ├── models/
    │   │   ├── staging/          # stg_matches_historical
    │   │   └── marts/            # fct_results, fct_standings, fct_team_form, fct_team_season_stats
    │   └── seeds/
    │       └── team_name_mapping.csv
    ├── streamlit/
    │   └── app.py                # dashboard
    ├── data/                     # DuckDB database (gitignored)
    ├── logs/                     # cron job logs (gitignored)
    └── refresh.sh                # daily refresh script

## Dashboard tabs
- **Standings** — league table for any season (2005/06 to present)
- **Form** — last 5 results per team
- **Results** — match results for any season
- **Predictions** — upcoming fixtures with win/draw/loss probabilities

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/olekom123/premier-league-analytics.git
cd premier-league-analytics

2. Install dependencies

pip3 install -r requirements.txt

3. Get a free API key

Sign up at football-data.org and create a .env file:
FOOTBALL_DATA_API_KEY=your_key_here

4. Run ingestion

python3 ingestion/fetch_historical.py
python3 ingestion/fetch_fixtures.py

5. Run dbt

cd dbt/pl_analytics
dbt seed
dbt build

6. Generate predictions

python3 ingestion/predict_match.py

7. Start dashboard

streamlit run streamlit/app.py

Automated refresh

A cron job runs daily at noon to fetch fresh data and rebuild all models:
chmod +x refresh.sh
crontab -e
# add: 0 12 * * * /path/to/refresh.sh >> /path/to/logs/refresh.log 2>&1

Data sources

- football-data.co.uk — historical match results and odds (free)
- football-data.org — upcoming fixtures API (free tier)