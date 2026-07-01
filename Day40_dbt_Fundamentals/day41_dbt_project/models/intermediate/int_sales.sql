SELECT
    o.order_id,
    o.order_date,

    c.customer_id,
    c.customer_name,
    c.city,

    p.product_id,
    p.product_name,
    p.category,
    p.price,

    o.quantity,

    (o.quantity * p.price) AS total_amount

FROM {{ ref('stg_orders') }} o

JOIN {{ ref('stg_customers') }} c
ON o.customer_id = c.customer_id

JOIN {{ ref('stg_products') }} p
ON o.product_id = p.product_id
