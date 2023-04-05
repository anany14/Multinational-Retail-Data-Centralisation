-- m3t1
ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid,
ALTER COLUMN user_uuid TYPE uuid USING date_uuid::uuid,
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
SELECT * FROM orders_table;
SELECT * FROM dim_card_details;
SELECT * FROM dim_date_times;
SELECT * FROM dim_users;
SELECT * FROM dim_products;
SELECT * FROM dim_store_details;

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

--not working
ALTER TABLE orders_table
ADD CONSTRAINT fk_user_uuid
FOREIGN KEY (user_uuid)
REFERENCES dim_users (user_uuid);






