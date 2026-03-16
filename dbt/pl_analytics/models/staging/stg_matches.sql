{{ config(materialized='view') }}

with source as (
      select * from raw_matches
),

renamed as (
      select
          id as match_id,
          cast(utc_date as timestamp) as match_date,
          status,
          matchday,
          home_team,
          away_team,
          home_score,
          away_score,
          home_score + away_score as total_goals,
          case
              when home_score > away_score then 'home'
              when away_score > home_score then 'away'
              else 'draw'
          end as result
      from source
      where status = 'FINISHED'
  )

  select * from renamed