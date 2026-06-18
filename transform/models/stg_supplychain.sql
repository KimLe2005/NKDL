{{ config(materialized='view') }}

SELECT
    CAST("Order Id" AS VARCHAR) AS order_id,
    CAST("Order Customer Id" AS VARCHAR) AS customer_id,

    COALESCE(CAST("Sales" AS DOUBLE), 0) AS sales_amount,
    COALESCE(CAST("Benefit per order" AS DOUBLE), 0) AS profit,
    COALESCE(CAST("Order Item Discount" AS DOUBLE), 0) AS discount,

    UPPER(TRIM("Customer Country")) AS customer_country,
    UPPER(TRIM("Order Status")) AS order_status,
    UPPER(TRIM("Type")) AS order_type,

    "Order Id" AS check_id

FROM main.bronze_supplychain_raw
WHERE "Order Id" IS NOT NULL