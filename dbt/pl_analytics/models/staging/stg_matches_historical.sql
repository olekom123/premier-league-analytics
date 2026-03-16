{{ config(materialized='view') }}

select
    season,
    strptime(date, '%d/%m/%Y')::date as match_date,
    hometeam as home_team,
    awayteam as away_team,
    ftr as result,
    htr as ht_result,
    fthg::integer as home_score,
    ftag::integer as away_score,
    hthg::integer as ht_home_score,
    htag::integer as ht_away_score,
    hst::integer as home_shots_target,
    ast::integer as away_shots_target,
    hc::integer as home_corners,
    ac::integer as away_corners,
    hy::integer as home_yellows,
    ay::integer as away_yellows,
    hr::integer as home_reds,
    ar::integer as away_reds,
    b365h::double as odds_home,
    b365d::double as odds_draw,
    b365a::double as odds_away,
    "B365>2.5"::double as odds_over_25,
    "B365<2.5"::double as odds_under_25,
    home_score + away_score as total_goals,
    case
        when result = 'H' then 'home'
        when result = 'A' then 'away'
        else 'draw'
    end as outcome,
    case
        when home_score > away_score then 3
        when home_score = away_score then 1
        else 0
    end as home_points,
    case
        when away_score > home_score then 3
        when home_score = away_score then 1
        else 0
    end as away_points
from raw_matches_historical
where
    date is not null
    and hometeam is not null
    and fthg is not null
