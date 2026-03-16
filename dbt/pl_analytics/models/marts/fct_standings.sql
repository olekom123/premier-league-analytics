{{ config(materialized='table') }}

select
    team,
    count(*) as games_played,
    sum(case when outcome = 'win' then 1 else 0 end) as wins,
    sum(case when outcome = 'draw' then 1 else 0 end) as draws,
    sum(case when outcome = 'loss' then 1 else 0 end) as losses,
    sum(goals_scored) as goals_for,
    sum(goals_conceded) as goals_against,
    sum(goals_scored) - sum(goals_conceded) as goal_difference,
    sum(points) as total_points
from fct_results
group by team
order by total_points desc, goal_difference desc, goals_for desc
