with last_5 as (
    select
        season,
        team,
        match_date,
        outcome,
        points,
        case
            when outcome = 'win'  then 'W'
            when outcome = 'draw' then 'D'
            else                       'L'
        end                             as form_letter,
        row_number() over (
            partition by season, team
            order by match_date desc
        )                               as match_rank
    from {{ ref('fct_results') }}
    qualify row_number() over (partition by season, team order by match_date desc) <= 5
)

select
    season,
    team,
    string_agg(form_letter, ' ' order by match_rank asc)   as form,
    sum(points)                                             as points_last_5,
    count(case when outcome = 'win'  then 1 end)            as wins_last_5,
    count(case when outcome = 'draw' then 1 end)            as draws_last_5,
    count(case when outcome = 'loss' then 1 end)            as losses_last_5
from last_5
group by season, team
order by season desc, points_last_5 desc