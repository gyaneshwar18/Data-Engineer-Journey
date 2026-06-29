SELECT
    customer_id,
    customer_name,
    city,
    email
FROM {{ source('raw', 'raw_customers') }}
