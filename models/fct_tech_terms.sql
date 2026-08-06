-- Split out of the old 03_fct_entities.sql (Step 3a: tech terms flatten)
-- One model file = one table in dbt, so this is now its own file
{{ config(materialized='table') }}

SELECT
    VIDEO_ID,
    f.value::STRING AS TECH_TERM,
    INSERTED_AT AS PROCESSED_AT
FROM {{ ref('stg_youtube_transcripts') }},
LATERAL FLATTEN(input => TECH_TERMS_ARRAY) f
