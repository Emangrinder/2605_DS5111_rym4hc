-- stg_youtube_transcripts was CREATE OR REPLACE VIEW; now a dbt view model
-- filename itself is the view name, so no explicit name needed
{{ config(materialized='view') }}

SELECT
    JSON_PAYLOAD:video_id::STRING AS VIDEO_ID,
    JSON_PAYLOAD:cleaned_text::STRING AS CLEANED_TEXT,
    JSON_PAYLOAD:tech_terms AS TECH_TERMS_ARRAY,
    JSON_PAYLOAD:book_names AS BOOK_NAMES_ARRAY,
    INSERTED_AT
-- raw_transcripts is a lowest-level raw source table, NOT a dbt model,
-- so it stays a plain FROM reference rather than {{ ref() }}
FROM raw_transcripts
