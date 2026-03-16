{{ config(materialized='table') }}

with base as (
    select * from {{ ref('fct_prediction_results') }}
),

overall as (
    select
        'overall'                               as segment,
        'all'                                   as segment_value,
        count(*)                                as total_predictions,
        sum(was_correct)                        as correct_predictions,
        round(avg(was_correct) * 100, 1)        as accuracy_pct,
        round(avg(prob_actual_outcome) * 100, 1) as avg_confidence_pct
    from base
),

by_predicted_outcome as (
    select
        'predicted_outcome'                     as segment,
        predicted_outcome                       as segment_value,
        count(*)                                as total_predictions,
        sum(was_correct)                        as correct_predictions,
        round(avg(was_correct) * 100, 1)        as accuracy_pct,
        round(avg(prob_actual_outcome) * 100, 1) as avg_confidence_pct
    from base
    group by predicted_outcome
),

by_actual_outcome as (
    select
        'actual_outcome'                        as segment,
        actual_outcome                          as segment_value,
        count(*)                                as total_predictions,
        sum(was_correct)                        as correct_predictions,
        round(avg(was_correct) * 100, 1)        as accuracy_pct,
        round(avg(prob_actual_outcome) * 100, 1) as avg_confidence_pct
    from base
    group by actual_outcome
)

select * from overall
union all
select * from by_predicted_outcome
union all
select * from by_actual_outcome
order by segment, segment_value
