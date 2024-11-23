
  create view "data_engineering_test"."public"."calculate_comissions__dbt_tmp"
    
    
  as (
    WITH orders_with_salesowners AS (
    SELECT
        o.order_id,
        round(i.gross_value / 100.0, 2) AS gross_value_in_euros,

        -- Converting the gross value into net value by taking the vat out in a non-lineal way.
        round((i.gross_value / 100.0) / (1 + i.vat / 100.0), 2) AS net_value_in_euros,
        string_to_array(o.salesowners, ', ') AS salesowners_array
    FROM
        public.orders o
    JOIN
        public.invoicing_data i ON o.order_id = i.order_id
),
salesowners AS (
    SELECT
        ows.order_id,
        ows.net_value_in_euros,
        so.salesowner,
        so.ordinality AS salesowner_position
    FROM
        orders_with_salesowners ows,
        unnest(ows.salesowners_array) WITH ORDINALITY AS so(salesowner, ordinality) -- unnests the array and assigns the order for each sales person in the order that it comes from the file
),
commission_calc AS (
    SELECT
        order_id,
        salesowner,
        CASE 
            WHEN salesowner_position = 1 THEN net_value_in_euros * 0.06    -- Main owner - 6%
            WHEN salesowner_position = 2 THEN net_value_in_euros * 0.025   -- Co-owner 1 - 2.5%
            WHEN salesowner_position = 3 THEN net_value_in_euros * 0.0095  -- Co-owner 2 - 0.95%
            ELSE 0  -- No comission
        END AS commission
    FROM salesowners
)
SELECT
    salesowner,
    ROUND(SUM(commission), 2) AS total_commission
FROM commission_calc
GROUP BY salesowner
ORDER BY total_commission DESC
  );