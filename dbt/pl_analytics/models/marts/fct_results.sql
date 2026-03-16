{{ config(materialized='table') }}

select
    match_id,
    match_date,
    matchday,
    home_team as team,
    away_team as opponent,
    home_score as goals_scored,
    away_score as goals_conceded,
    total_goals,
    'home' as venue,
    case
        when result = 'home' then 3
        when result = 'draw' then 1
        else 0
    end as points,
    case
        when result = 'home' then 'win'
        when result = 'draw' then 'draw'
        else 'loss'
    end as outcome,
    case when home_score = 0 then 1 else 0 end as clean_sheet,
    case
        when
            home_score > 0
            and away_score > 0 then 1
        else 0
    end as btts
from stg_matches

union all

select
    match_id,
    match_date,
    matchday,
    away_team as team,
    home_team as opponent,
    away_score as goals_scored,
    home_score as goals_conceded,
    total_goals,
    'away' as venue,
    case
        when result = 'away' then 3
        when result = 'draw' then 1
        else 0
    end as points,
    case
        when result = 'away' then 'win'
        when result = 'draw' then 'draw'
        else 'loss'
    end as outcome,
    case when away_score = 0 then 1 else 0 end as clean_sheet,
    case
        when
            home_score > 0
            and away_score > 0 then 1
        else 0
    end as btts
from stg_matches
