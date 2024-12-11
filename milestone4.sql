-- task 1
SELECT country_code AS country, 
       COUNT(store_code) AS total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC;

-- task 2
SELECT locality, 
       COUNT(store_code) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC;

-- task 3
SELECT 
    SUM(dim_products.product_price * orders_table.product_quantity) AS total_sales,
    dim_date_times.month
FROM orders_table
JOIN dim_products ON orders_table.product_code = dim_products.product_code
JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY dim_date_times.month
ORDER BY total_sales DESC;

-- task 4
SELECT 
    COUNT(orders_table.index) AS numbers_of_sales,
    SUM(orders_table.product_quantity) AS product_quantity_count,
    CASE 
        WHEN dim_store_details.store_type = 'Web Portal' THEN 'Web'
        ELSE 'Offline'
    END AS location
FROM orders_table
JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY location
ORDER BY location DESC;

-- task 5
WITH store_sales AS (
    SELECT 
        s.store_type,
        SUM(p.product_price * o.product_quantity) AS total_sales,
        COUNT(o.index) AS total_sales_count
    FROM orders_table o
    JOIN dim_store_details s ON o.store_code = s.store_code
    JOIN dim_products p ON o.product_code = p.product_code
    GROUP BY s.store_type
),
total_sales AS (
    SELECT SUM(p.product_price * o.product_quantity) AS total_revenue
    FROM orders_table o
    JOIN dim_store_details s ON o.store_code = s.store_code
    JOIN dim_products p ON o.product_code = p.product_code
)
SELECT 
    store_type,
    total_sales,
    ROUND((total_sales / (SELECT total_revenue FROM total_sales)) * 100, 2) AS sales_made_percentage
FROM store_sales
ORDER BY total_sales DESC;

-- task 6
WITH sales_data AS (
    SELECT 
        dd.year,
        dd.month,
        SUM(dp.product_price * o.product_quantity) AS total_sales
    FROM 
        orders_table o
    JOIN 
        dim_date_times dd ON o.date_uuid = dd.date_uuid
    JOIN 
        dim_products dp ON o.product_code = dp.product_code
    GROUP BY 
        dd.year, dd.month
)
SELECT 
    ROUND(total_sales, 2) AS total_sales,
    year,
    month
FROM 
    sales_data
ORDER BY 
    total_sales DESC
LIMIT 10;


-- task 7
SELECT 
    SUM(s.staff_numbers) AS total_staff_numbers, 
    s.country_code
FROM dim_store_details s
GROUP BY s.country_code
ORDER BY total_staff_numbers DESC;

-- task 8
SELECT 
    SUM(o.product_quantity * p.product_price) AS total_sales,
    s.store_type,
    s.country_code
FROM 
    orders_table o
JOIN 
    dim_store_details s ON o.store_code = s.store_code
JOIN 
    dim_products p ON o.product_code = p.product_code
WHERE 
    s.country_code = 'DE'  -- Filter for Germany (DE)
GROUP BY 
    s.store_type, s.country_code
ORDER BY 
    total_sales ASC;

-- task 9
WITH full_timestamps AS (
    SELECT
        d.date_uuid,
        TO_TIMESTAMP(CONCAT(d.year, '-', d.month, '-', d.day, ' ', d.timestamp), 'YYYY-MM-DD HH24:MI:SS') AS full_timestamp
    FROM
        dim_date_times d
),
sales_with_time_difference AS (
    SELECT
        EXTRACT(YEAR FROM ft.full_timestamp) AS year,
        ft.full_timestamp AS current_sale_time,
        LEAD(ft.full_timestamp) OVER (PARTITION BY EXTRACT(YEAR FROM ft.full_timestamp) ORDER BY ft.full_timestamp) AS next_sale_time
    FROM
        orders_table o
    JOIN
        full_timestamps ft ON o.date_uuid = ft.date_uuid
),
time_differences AS (
    SELECT
        year,
        EXTRACT(EPOCH FROM (next_sale_time - current_sale_time)) AS time_difference_seconds
    FROM
        sales_with_time_difference
    WHERE
        next_sale_time IS NOT NULL  -- Exclude the last sale for each year
),
average_time_by_year AS (
    SELECT
        year,
        AVG(time_difference_seconds) AS avg_time_seconds
    FROM
        time_differences
    GROUP BY
        year
)
SELECT
    year,
    json_build_object(
        'hours', FLOOR(avg_time_seconds / 3600),
        'minutes', FLOOR((avg_time_seconds % 3600) / 60),
        'seconds', FLOOR(avg_time_seconds % 60),
        'milliseconds', FLOOR((avg_time_seconds - FLOOR(avg_time_seconds)) * 1000)
    ) AS actual_time_taken
FROM
    average_time_by_year
ORDER BY
    year;
