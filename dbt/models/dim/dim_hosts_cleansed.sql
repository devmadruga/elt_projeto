{{
    config(
        materialized = 'view',
    )
}}

WITH src_hosts AS
    (SELECT *
    FROM {{ ref('src_hosts') }})
SELECT 
    created_at,
    host_id,
    is_superhost,
    updated_at,
    CASE
        WHEN host_name is NULL THEN 'Anonymous'
        ELSE host_name
    END AS host_name
FROM src_hosts