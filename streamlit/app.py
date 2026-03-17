import streamlit as st
import duckdb
from datetime import datetime

DB_PATH = '/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db'

def get_data(query):
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute(query).fetchdf()
    con.close()
    return df

def get_seasons():
    df = get_data("SELECT DISTINCT season FROM fct_standings ORDER BY season DESC")
    return df['season'].tolist()

def get_current_season():
    now = datetime.now()
    year = now.year if now.month >= 8 else now.year - 1
    return str(year)[2:] + str(year + 1)[2:]

st.set_page_config(page_title="PL Analytics", layout="wide")
st.title("Premier League Analytics")

seasons = get_seasons()
current_season = get_current_season()
default_idx = seasons.index(current_season) if current_season in seasons else 0
selected_season = st.sidebar.selectbox("Season", seasons, index=default_idx)

tab1, tab2, tab3, tab4 = st.tabs(["Standings", "Form", "Results", "Predictions"])

with tab1:
    st.subheader(f"League Table — {selected_season}")
    standings = get_data(f"""
        select
            row_number() over (
                order by total_points desc, goal_difference desc, goals_for desc
            )                   as pos,
            team,
            games_played,
            wins,
            draws,
            losses,
            goals_for,
            goals_against,
            goal_difference,
            total_points        as points
        from fct_standings
        where season = '{selected_season}'
    """)
    st.dataframe(standings, hide_index=True, width='stretch')

with tab2:
    st.subheader(f"Team Form (Last 5) — {selected_season}")
    form = get_data(f"""
        select
            team,
            form,
            wins_last_5,
            draws_last_5,
            losses_last_5,
            points_last_5
        from fct_team_form
        where season = '{selected_season}'
        order by points_last_5 desc
    """)
    st.dataframe(form, hide_index=True, width='stretch')

with tab3:
    st.subheader(f"Match Results — {selected_season}")
    results = get_data(f"""
        select
            date(match_date) as match_date,
            home_team,
            home_score,
            away_score,
            away_team,
            total_goals
        from stg_matches_historical
        where season = '{selected_season}'
        order by match_date desc
    """)
    results['match_date'] = results['match_date'].astype(str)
    st.dataframe(results, hide_index=True, width='stretch')

with tab4:
    st.subheader("Upcoming Fixtures & Predictions")
    predictions = get_data("""
        select
            date(utc_date) as utc_date,
            matchday,
            home_team,
            away_team,
            round(prob_home_win * 100, 1)   as home_win_pct,
            round(prob_draw * 100, 1)        as draw_pct,
            round(prob_away_win * 100, 1)    as away_win_pct,
            predicted_outcome
        from raw_predictions
        order by utc_date
    """)
    predictions['utc_date'] = predictions['utc_date'].astype(str)
    st.dataframe(predictions, hide_index=True, width='stretch')