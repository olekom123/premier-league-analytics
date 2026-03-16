import streamlit as st
import duckdb

DB_PATH = '/Users/alexkomyshnyi/Desktop/premier-league-analytics/data/pl_analytics.db'

def get_data(query):
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute(query).fetchdf()
    con.close()
    return df

st.set_page_config(page_title="PL Analytics", layout="wide")
st.title("Premier League 2024/25 Analytics")

tab1, tab2, tab3 = st.tabs(["Standings", "Form", "Results"])

with tab1:
    st.subheader("League Table")
    standings = get_data("""
        select
            row_number() over (order by total_points desc, goal_difference desc, goals_for desc) as pos,
            team,
            games_played,
            wins,
            draws,
            losses,
            goals_for,
            goals_against,
            goal_difference,
            total_points as points
        from fct_standings
    """)
    st.dataframe(standings, hide_index=True, width='stretch')

with tab2:
    st.subheader("Team Form (Last 5 Games)")
    form = get_data("""
        select
            team,
            form,
            wins_last_5,
            draws_last_5,
            losses_last_5,
            points_last_5
        from fct_team_form
        order by points_last_5 desc
    """)
    st.dataframe(form, hide_index=True, width='stretch')

with tab3:
    st.subheader("Match Results")
    matchday = st.slider("Matchday", 1, 38, 1)
    results = get_data(f"""
        select
            match_date,
            home_team,
            home_score,
            away_score,
            away_team,
            total_goals
        from stg_matches
        where matchday = {matchday}
        order by match_date
    """)
    st.dataframe(results, hide_index=True, width='stretch')