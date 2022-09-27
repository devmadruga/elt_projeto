{{
    config(
        materialized = 'incremental',
        on_schema_change='fail'
    )
}}


WITH src_reviews AS (
SELECT * FROM {{ ref('src_reviews') }}
)
SELECT * FROM src_reviews
WHERE review_text is not null

/*if para o inscremento. Nota a facilidade de color {{ this }} e ele já saber
 que é sobre 'fct_reviews' */
{% if is_incremental() %}
AND review_date > (select max(review_date) from {{ this }})
{% endif %}