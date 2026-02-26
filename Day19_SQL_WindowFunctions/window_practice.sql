----1️⃣ ROW_NUMBER() — Unique row numbering

SELECT order_id,
       customer_id,
       amount,
       ROW_NUMBER() OVER (ORDER BY amount DESC) AS row_num
FROM orders;

---- 2️⃣ RANK() — Ranking with gaps

select order_id,
        customer_id,
        amount,
        RANK() over(order by amount desc) AS  rank_position
from orders;

------ 3️⃣ DENSE_RANK() — Ranking without gaps
select order_id,
        customer_id,
        amount,
        DENSE_RANK() over(order by amount desc) AS  rank_position
from orders;

---- 4️⃣ Row number per customer

with Rank_order AS (
    select *, ROW_NUMBER() OVER (
                PARTITION by customer_id
                order by amount DESC)
                as rn  
    from orders)
select * from Rank_order
where rn=1;
