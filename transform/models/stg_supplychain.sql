{{ config(materialized='view') }}

SELECT
    -- 1. Định danh
    CAST("Order Id" AS VARCHAR) AS order_id,
    CAST("Order Customer Id" AS VARCHAR) AS customer_id,
    
    
    -- 3. Số liệu tài chính (Xử lý NULL)
    COALESCE(CAST("Sales" AS DOUBLE), 0) AS sales_amount,
    COALESCE(CAST("Benefit per order" AS DOUBLE), 0) AS profit,
    COALESCE(CAST("Order Item Discount" AS DOUBLE), 0) AS discount,
    
    -- 4. Thông tin phân loại (Chuẩn hóa chữ hoa/thường)
    UPPER(TRIM("Customer Country")) AS customer_country,
    UPPER(TRIM("Order Status")) AS order_status,
    UPPER(TRIM("Type")) AS order_type,
    
    -- 5. Lọc dữ liệu: Chỉ lấy đơn hàng có Order Id hợp lệ
    "Order Id" AS check_id

FROM {{ source('main', 'bronze_supplychain_raw') }}
WHERE "Order Id" IS NOT NULL