-- Split out of the old 03_fct_entities.sql (Step 3b: book mentions flatten)
-- One model file = one table in dbt, so this is now its own file
{{ config(materialized='table') }}

SELECT
    VIDEO_ID,
    f.value::STRING AS BOOK_NAME,
    INSERTED_AT AS PROCESSED_AT
FROM {{ ref('stg_youtube_transcripts') }},
LATERAL FLATTEN(input => BOOK_NAMES_ARRAY) f
