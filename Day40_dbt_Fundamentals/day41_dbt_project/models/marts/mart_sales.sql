SELECT
    city,
    category,

    COUNT(order_id) AS total_orders,

    SUM(quantity) AS total_quantity,

    SUM(total_amount) AS total_revenue,

    AVG(total_amount) AS average_order_value

FROM {{ ref('int_sales') }}

GROUP BY
    city,
    category
