#!/bin/bash

python3 /Users/alexkomyshnyi/Desktop/premier-league-analytics/ingestion/fetch_historical.py

cd /Users/alexkomyshnyi/Desktop/premier-league-analytics/dbt/pl_analytics
dbt build