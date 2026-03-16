# PL Analytics

Personal Premier League analytics pipeline built to learn end-to-end data engineering.

## Stack
- **Ingestion**: Python scripts calling football-data.org API
- **Database**: DuckDB (local file at `data/pl_analytics.db`)
- **Transformation**: dbt Core with dbt-duckdb adapter
- **Dashboard**: Streamlit
- **Orchestration**: macOS cron job (daily at noon)

## Project Structure
- `ingestion/` - Python scripts to fetch data from APIs
- `dbt/pl_analytics/` - dbt project with staging and marts models
- `streamlit/` - Streamlit dashboard app
- `logs/` - cron job logs (gitignored)
- `data/` - DuckDB database file (gitignored)

## Running locally
```bash
# Fetch fresh data
python3 ingestion/fetch_matches.py

# Run dbt transformations
cd dbt/pl_analytics
dbt build

# Start dashboard
streamlit run streamlit/app.py

dbt Models

- stg_matches - cleaned match data from raw_matches (view)
- fct_results - one row per team per match with points and outcome (table)
- fct_standings - current league table aggregated from fct_results (table)
- fct_team_form - last 5 results per team with form string (table)

How to work with me

- Walk through everything step by step with explanations
- Explain what each step means before implementing
- Keep solutions simple, no over-engineering