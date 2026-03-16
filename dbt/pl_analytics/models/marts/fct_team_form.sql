{{ config(materialized='table') }}

with last_5 as (
    select
        team,
        match_date,
        matchday,
        outcome,
        points,
        case
            when outcome = 'win' then 'W'
            when outcome = 'draw' then 'D'
            else 'L'
        end as form_letter,
        row_number() over (
            partition by team
            order by match_date desc
        ) as match_rank
    from fct_results
    qualify row_number() over (partition by team order by match_date desc) <= 5
)

select
    team,
    string_agg(form_letter, ' ' order by match_rank asc) as form,
    sum(points) as points_last_5,
    count(case when outcome = 'win' then 1 end) as wins_last_5,
    count(case when outcome = 'draw' then 1 end) as draws_last_5,
    count(case when outcome = 'loss' then 1 end) as losses_last_5
from last_5
group by team
order by points_last_5 desc
