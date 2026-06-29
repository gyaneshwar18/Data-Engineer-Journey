SELECT
    order_id,
    customer_id,
    product_id,
    quantity,
    order_date
FROM {{ source('raw', 'raw_orders') }}
