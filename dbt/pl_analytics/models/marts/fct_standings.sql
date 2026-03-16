{{ config(materialized='table') }}

select
    season,
    team,
    count(*)                                                    as games_played,
    sum(case when outcome = 'win'  then 1 else 0 end)           as wins,
    sum(case when outcome = 'draw' then 1 else 0 end)           as draws,
    sum(case when outcome = 'loss' then 1 else 0 end)           as losses,
    sum(goals_scored)                                           as goals_for,
    sum(goals_conceded)                                         as goals_against,
    sum(goals_scored) - sum(goals_conceded)                     as goal_difference,
    sum(points)                                                 as total_points
from {{ ref('fct_results') }}
group by season, team
order by season desc, total_points desc, goal_difference desc, goals_for desc
