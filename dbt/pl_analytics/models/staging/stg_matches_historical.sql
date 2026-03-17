{{ config(materialized='view') }}

select
    m.season,
    strptime(m.date, '%d/%m/%Y')::date as match_date,
    m.ftr as result,
    m.htr as ht_result,
    (m.fthg)::integer as home_score,
    (m.ftag)::integer as away_score,
    (m.hthg)::integer as ht_home_score,
    (m.htag)::integer as ht_away_score,
    (m.hst)::integer as home_shots_target,
    (m.ast)::integer as away_shots_target,
    (m.hc)::integer as home_corners,
    (m.ac)::integer as away_corners,
    (m.hy)::integer as home_yellows,
    (m.ay)::integer as away_yellows,
    (m.hr)::integer as home_reds,
    (m.ar)::integer as away_reds,
    (m.b365h)::double as odds_home,
    (m.b365d)::double as odds_draw,
    (m.b365a)::double as odds_away,
    (m."B365>2.5")::double as odds_over_25,
    (m."B365<2.5")::double as odds_under_25,
    coalesce(ht.standard_name, m.hometeam) as home_team,
    coalesce(atm.standard_name, m.awayteam) as away_team,
    home_score + away_score as total_goals,
    case
        when m.ftr = 'H' then 'home'
        when m.ftr = 'A' then 'away'
        else 'draw'
    end as outcome,
    case
        when m.fthg > m.ftag then 3
        when m.fthg = m.ftag then 1
        else 0
    end as home_points,
    case
        when m.ftag > m.fthg then 3
        when m.fthg = m.ftag then 1
        else 0
    end as away_points
from {{ source('main', 'raw_matches_historical') }} as m
left join
    {{ ref('team_name_mapping') }} as ht
    on m.hometeam = ht.historical_name
left join
    {{ ref('team_name_mapping') }} as atm
    on m.awayteam = atm.historical_name
where
    m.date is not null
    and m.hometeam is not null
    and m.fthg is not null
