{{ config(materialized='table') }}

select
    p.fixture_id,
    p.matchday,
    p.home_team,
    p.away_team,
    p.home_expected,
    p.away_expected,
    p.prob_home_win,
    p.prob_draw,
    p.prob_away_win,
    p.predicted_outcome,
    p.predicted_at,

    -- actual result
    m.home_score,
    m.away_score,
    m.outcome as actual_outcome,

    -- was the prediction correct?
    case
        when m.outcome = p.predicted_outcome then 1
        else 0
    end as was_correct,

    -- probability assigned to the outcome that actually happened
    case
        when m.outcome = 'home' then p.prob_home_win
        when m.outcome = 'draw' then p.prob_draw
        when m.outcome = 'away' then p.prob_away_win
    end as prob_actual_outcome

from {{ source('main', 'raw_predictions') }} as p
inner join {{ ref('stg_matches_historical') }} as m
    on
        p.home_team = m.home_team
        and p.away_team = m.away_team
        and cast(p.utc_date as date) = m.match_date
