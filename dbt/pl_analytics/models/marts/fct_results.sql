{{ config(materialized='table') }}

select
    season,
    match_date,
    home_team                                           as team,
    away_team                                           as opponent,
    home_score                                          as goals_scored,
    away_score                                          as goals_conceded,
    total_goals,
    'home'                                              as venue,
    home_points                                         as points,
    case
        when outcome = 'home' then 'win'
        when outcome = 'draw' then 'draw'
        else 'loss'
    end                                                 as outcome,
    case when home_score = 0 then 1 else 0 end          as clean_sheet,
    case when home_score > 0
        and away_score > 0 then 1 else 0 end           as btts

from {{ ref('stg_matches_historical') }}

union all

select
    season,
    match_date,
    away_team                                           as team,
    home_team                                           as opponent,
    away_score                                          as goals_scored,
    home_score                                          as goals_conceded,
    total_goals,
    'away'                                              as venue,
    away_points                                         as points,
    case
        when outcome = 'away' then 'win'
        when outcome = 'draw' then 'draw'
        else 'loss'
    end                                                 as outcome,
    case when away_score = 0 then 1 else 0 end          as clean_sheet,
    case when home_score > 0
        and away_score > 0 then 1 else 0 end           as btts

from {{ ref('stg_matches_historical') }}