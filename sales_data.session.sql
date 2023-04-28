-- m3t1
ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid,
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN card_number TYPE VARCHAR(19),
ALTER COLUMN store_code TYPE VARCHAR(12),
ALTER COLUMN product_code TYPE VARCHAR(11),
ALTER COLUMN product_quantity TYPE SMALLINT

--m3t2
UPDATE dim_users
SET country_code = 'GB'
WHERE country_code = 'GGB';
ALTER TABLE dim_users
ALTER COLUMN first_name TYPE VARCHAR(255),
ALTER COLUMN last_name TYPE VARCHAR(255),
ALTER COLUMN date_of_birth TYPE DATE,
ALTER COLUMN country_code TYPE VARCHAR(2),
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN join_date TYPE DATE

--m3t3
ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE FLOAT,
ALTER COLUMN locality TYPE VARCHAR(255),
ALTER COLUMN store_code TYPE VARCHAR(12),
ALTER COLUMN staff_numbers TYPE SMALLINT,
ALTER COLUMN opening_date TYPE DATE,
ALTER COLUMN store_type TYPE VARCHAR(255),
ALTER COLUMN latitude TYPE FLOAT,
ALTER COLUMN country_code TYPE VARCHAR(2),
ALTER COLUMN continent TYPE VARCHAR(255)

--m3t4
-- already removed the £ using python when cleaning
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(255);
ALTER TABLE dim_products
RENAME COLUMN "weight(kg)" TO weight_in_kg;
UPDATE dim_products
SET weight_class =
    CASE
        WHEN weight_in_kg < 2 THEN 'Light'
        WHEN weight_in_kg >= 2 AND weight_in_kg < 40 THEN 'Mid_Sized'
        WHEN weight_in_kg >= 40 AND weight_in_kg < 140 THEN 'Heavy'
        WHEN weight_in_kg >= 140 THEN 'Truck_Required'
        ELSE NULL
    END;

--m3t5
-- already change the column to still available
ALTER TABLE dim_products
RENAME COLUMN "product_price(£)" TO product_price_in_£
ALTER TABLE dim_products
ALTER COLUMN product_price_in_£ TYPE FLOAT,
ALTER COLUMN weight_in_kg TYPE FLOAT,
ALTER COLUMN "EAN" TYPE VARCHAR(17),
ALTER COLUMN product_code TYPE VARCHAR(11),
ALTER COLUMN date_added TYPE DATE,
ALTER COLUMN uuid TYPE uuid USING uuid::uuid,
ALTER COLUMN still_available TYPE BOOL,
ALTER COLUMN weight_class TYPE VARCHAR(14)

--m3t6
--I have already created a single column called datetime
--will now extract data from datetime and create columns
ALTER TABLE dim_date_times ADD COLUMN year INT;
ALTER TABLE dim_date_times ADD COLUMN month INT;
ALTER TABLE dim_date_times ADD COLUMN day INT;

UPDATE dim_date_times
SET year = DATE_PART('year', "DateTime"),
    month = DATE_PART('month', "DateTime"),
    day = DATE_PART('day', "DateTime");


ALTER TABLE dim_date_times
ALTER COLUMN month TYPE VARCHAR(2),
ALTER COLUMN year TYPE VARCHAR(4),
ALTER COLUMN day TYPE VARCHAR(2),
ALTER COLUMN time_period TYPE VARCHAR(10),
ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid;


--m3t7
ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(19),
ALTER COLUMN expiry_date TYPE DATE USING expiry_date::date,
ALTER COLUMN date_payment_confirmed TYPE DATE;
ALTER TABLE dim_card_details
ALTER COLUMN expiry_date TYPE VARCHAR(10);


--m3t8

ALTER TABLE dim_card_details
ADD CONSTRAINT pk_card_number PRIMARY KEY (card_number);
ALTER TABLE dim_date_times
ADD CONSTRAINT pk_date_uuid PRIMARY KEY (date_uuid);
ALTER TABLE dim_users
ADD CONSTRAINT pk_user_uuid PRIMARY KEY (user_uuid);
ALTER TABLE dim_products
ADD CONSTRAINT pk_product_code PRIMARY KEY (product_code);
ALTER TABLE dim_store_details
ADD CONSTRAINT pk_store_code PRIMARY KEY (store_code);

--m3t9
ALTER TABLE orders_table
ADD CONSTRAINT fk_date_uuid
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times (date_uuid);
ALTER TABLE orders_table
ADD CONSTRAINT fk_product_code
FOREIGN KEY (product_code)
REFERENCES dim_products (product_code);
ALTER TABLE orders_table
ADD CONSTRAINT fk_store_code
FOREIGN KEY (store_code)
REFERENCES dim_store_details (store_code);
ALTER TABLE orders_table
ADD CONSTRAINT fk_card_number
FOREIGN KEY (card_number)
REFERENCES dim_card_details (card_number);
ALTER TABLE orders_table
ADD CONSTRAINT fk_user_uuid
FOREIGN KEY (user_uuid)
REFERENCES dim_users (user_uuid);

--m4t1

SELECT country_code, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC;

--m4t2

SELECT locality, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;

--m4t3

SELECT month, SUM(o.product_quantity * p.product_price_in_£) AS total_sales
FROM orders_table o
JOIN dim_date_times d ON o.date_uuid = d.date_uuid
JOIN dim_products p ON o.product_code = p.product_code
GROUP BY month
ORDER BY total_sales DESC;

--m4t4

SELECT 
  COUNT(*) AS numbers_of_sales, 
  SUM(product_quantity) AS product_quantity_count, 
  CASE 
    WHEN s.store_type = 'Web Portal' THEN 'Web'
    ELSE 'Offline'
  END AS location
FROM orders_table o
JOIN dim_products p ON o.product_code = p.product_code
JOIN dim_store_details s ON o.store_code = s.store_code
GROUP BY location;


--m4t5
SELECT s.store_type,
CAST(SUM(o.product_quantity * p.product_price_in_£) AS numeric(10,2)) AS total_sales,
(CAST(SUM(o.product_quantity * p.product_price_in_£) AS numeric(10,2)) / CAST((SELECT SUM(product_quantity * product_price_in_£) FROM orders_table JOIN dim_products ON orders_table.product_code = dim_products.product_code) AS numeric(10,2))) * 100 AS "percentage_total(%)"
FROM orders_table o
JOIN dim_products p ON o.product_code = p.product_code
JOIN dim_store_details s ON o.store_code = s.store_code
GROUP BY s.store_type
ORDER BY total_sales DESC;

--m4t6
SELECT SUM(p.product_price_in_£ * o.product_quantity) AS total_sales,
d.year AS year, d.month AS month
FROM orders_table o
JOIN dim_products p on o.product_code = p.product_code
JOIN dim_date_times d  on o.date_uuid = d.date_uuid
GROUP BY year,month
ORDER BY total_sales DESC
LIMIT 10;

--m4t7

UPDATE dim_store_details
SET country_code = NULL
WHERE store_type = 'Web Portal'
-- doing this because web portal was somehow included in GB

SELECT SUM(staff_numbers) AS total_staff_numbers, country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_staff_numbers DESC;

--m4t8

SELECT SUM(p.product_price_in_£ * o.product_quantity) AS total_sales,
s.store_type, s.country_code
FROM orders_table o
JOIN dim_products p ON o.product_code = p.product_code
JOIN dim_store_details s ON o.store_code = s.store_code
WHERE country_code = 'DE'
GROUP BY s.store_type, s.country_code
ORDER BY total_sales;

--m4t9

ALTER TABLE dim_date_times
RENAME "DateTime" TO datetimee;

SELECT year, AVG(actual_time_taken) as actual_time_taken
FROM (
  SELECT
    EXTRACT(YEAR FROM d.datetimee) AS year,
    LEAD(d.datetimee) OVER (ORDER BY d.datetimee) - d.datetimee AS actual_time_taken
  FROM dim_date_times d
  JOIN orders_table o ON d.date_uuid = o.date_uuid
) subquery
WHERE actual_time_taken IS NOT NULL
GROUP BY year
ORDER BY actual_time_taken DESC
LIMIT 10;

