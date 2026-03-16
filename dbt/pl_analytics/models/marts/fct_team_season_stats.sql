{{ config(materialized='table') }}

with home_stats as (
    select
        season,
        home_team as team,
        count(*) as home_games,
        sum(home_points) as home_points,
        sum(home_score) as home_goals_scored,
        sum(away_score) as home_goals_conceded,
        avg(home_score) as home_avg_scored,
        avg(away_score) as home_avg_conceded,
        sum(case when outcome = 'home' then 1 else 0 end) as home_wins,
        sum(case when outcome = 'draw' then 1 else 0 end) as home_draws,
        sum(case when outcome = 'away' then 1 else 0 end) as home_losses
    from stg_matches_historical
    group by season, home_team
),

away_stats as (
    select
        season,
        away_team as team,
        count(*) as away_games,
        sum(away_points) as away_points,
        sum(away_score) as away_goals_scored,
        sum(home_score) as away_goals_conceded,
        avg(away_score) as away_avg_scored,
        avg(home_score) as away_avg_conceded,
        sum(case when outcome = 'away' then 1 else 0 end) as away_wins,
        sum(case when outcome = 'draw' then 1 else 0 end) as away_draws,
        sum(case when outcome = 'home' then 1 else 0 end) as away_losses
    from stg_matches_historical
    group by season, away_team
)

select
    h.season,
    h.team,
    h.home_avg_scored,
    h.home_avg_conceded,
    a.away_avg_scored,
    a.away_avg_conceded,
    h.home_wins,
    h.home_draws,
    h.home_losses,
    a.away_wins,
    a.away_draws,
    a.away_losses,
    h.home_games + a.away_games as total_games,
    h.home_points + a.away_points as total_points,
    h.home_goals_scored + a.away_goals_scored as total_goals_scored,
    h.home_goals_conceded + a.away_goals_conceded as total_goals_conceded
from home_stats as h
inner join away_stats as a
    on
        h.season = a.season
        and h.team = a.team
order by h.season desc, total_points desc
