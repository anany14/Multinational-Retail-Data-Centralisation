# Multinational Retail-Data Centralization

The goal of the project is to create a system that centralizes the multinational company's sales data, making it easily accessible and analyzable by the team. This involves storing the company's sales data in a database using postgreSQL and Python, the database will serve as the single source of truth for sales data. Once the database is set up, the team will be able to query it to obtain up-to-date metrics that will inform their decision-making processes and help them become more data-driven. Ultimately, the project aims to improve the company's efficiency and effectiveness in managing and analyzing its sales data.

## Installation

1. Clone this repository to your local machine using `git clone https://github.com/<username>/multinational-sales-data-centralization.git`
2. Ensure that you have Python 3.8 or higher installed
3. Ensure that you have PostgreSQL installed 

## Usage

1. Run `python database_utils.py` to create the necessary database tables in the PostgreSQL server. This script requires that you have access to a PostgreSQL server and have provided the necessary credentials. The other 2 scripts are imported in this script as this is the main script and the only one you need to run. 
2. `python data_extraction.py` extracts data from the various data sources. This script requires that you have access to the necessary data sources. Data extraction methods were created in this script to extract data from different sources such as CSV files, an API, and an S3 bucket. The methods contained are tailored to extract data from a specific data source.
3. `python data_cleaning.py` cleans and transforms the data in the database. This script standardizes data formats and removes duplicates or irrelevant information, making the data more usable for analysis.
4. Use the SQL query `sales_data_sessions.sql` to query the database and obtain up-to-date metrics for the business. This script contains queries to extract sales data by country, product, and time period.

## Files

- `database_utils.py`: Contains functions to create, connect and upload to the PostgreSQL database, as well as create the necessary tables in the database.
- `data_extraction.py`: Contains functions to extract data from various data sources.
- `data_cleaning.py`: Contains functions to clean and transform the data in the PostgreSQL database.
- `sales_data_sessions.sql`: Contains SQL queries to obtain sales data from the PostgreSQL database.

## Dependencies

- `psycopg2`: PostgreSQL adapter for the Python programming language.
- `pandas`: Data manipulation library for Python.
- `sqlalchemy`: SQL toolkit and Object-Relational Mapping (ORM) library for Python.

## Contributing

This project is not currently accepting contributions.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.


## Milestone 1: Set-up GitHub Repo

## Milestone 2: Extracted and Cleaned the data from different sources

## Milestone 3: Created the Database Schema : Developed a STAR Based Schema of the Database, ensuring that the columns are of the correct types. 

## Milestone 4: Queried the data to answer questions such as - 
### How Many stores does the store have and in which countries?
| country_code  | total_no_stores |
|-------|-----|
| GB  | 265  |
| DE | 141  |
| US  | 34  |
| NULL | 1  |

1 of the stores is a Web Portal 

### Which Locations currently have the most stores? 

|     locality      | total_no_stores |
|-------------------|-----------------|
| Chapletown        |              14 |
| Belper            |              13 |
| Bushley           |              12 |
| Exeter            |              11 |
| High Wycombe      |              10 |
| Arbroath          |              10 |
| Rutherglen        |              10 |

### Which Months produce the average highest cost of sales typically? 

| total_sales | month |
|-------------|-------|
|673295.67999 |     8 |
|668041.44999 |     1 |
|657335.83999 |    10 |
|650321.42999 |     5 |
|645741.69999 |     7 |
|645462.99999 |     3 |
|635578.98999 |     6 |
|635329.08999 |    12 |
|633993.61999 |     9 |
|630757.07999 |    11 |

### How many sales are coming from online? 

|numbers_of_sales|product_quantity_count|location|
|----------------|----------------------|--------|
|93166|374047|Offline|
|26957|107739|Web|

### What Percentage of sales come through each type of store?

| store_type  | total_sales | percentage_total(%) |
|-------------|-------------|---------------------|
| Local       |  3440896.52 |             44.5577 |
| Web portal  |  1726547.05 |             22.3578 |
| Super Store |  1224293.65 |             15.8539 |
| Mall Kiosk  |   698791.61 |             9.04896 |
| Outlet      |   631804.81 |             8.18152 |

### Which month in each year produced the highest cost of sales?

| total_sales | year | month |
|-------------|------|-------|
|    27936.77 | 1994 |     3 |
|    27356.14 | 2019 |     1 |
|    27091.67 | 2009 |     8 |
|    26679.98 | 1997 |    11 |
|    26310.97 | 2018 |    12 |
|    26277.72 | 2019 |     8 |
|    26236.67 | 2017 |     9 |
|    25798.12 | 2010 |     5 |
|    25648.29 | 1996 |     8 |
|    25614.54 | 2000 |     1 |

### What is the staff headcount? 

|total_staff_numbers|country_code|
|-------------------|------------|
|12807|GB|
|6054|DE|
|1304|US|
|325|NULL|

### Which German type store is selling the most?

|total_sales|store_type|country_code|
|-----------|----------|------------|
|198373.57000000027|Outlet|DE|
|247634.20000000042|Mall Kiosk|DE|
|384625.02999999863|Super Store|DE|
|1109909.5899999605|Local|DE|

### How quickly is the company making sales?

|year|actual_time_taken|
|----|-----------------|
|2013|{""hours"":2,""minutes"":17,""seconds"":15,""milliseconds"":655.442}|
|1993|{""hours"":2,""minutes"":15,""seconds"":40,""milliseconds"":129.515}|
|2002|{""hours"":2,""minutes"":13,""seconds"":49,""milliseconds"":478.228}|
|2008|{""hours"":2,""minutes"":13,""seconds"":3,""milliseconds"":532.442}|
|2022|{""hours"":2,""minutes"":13,""seconds"":2,""milliseconds"":3.698}|
|1995|{""hours"":2,""minutes"":12,""seconds"":59,""milliseconds"":84.514}|
|2016|{""hours"":2,""minutes"":12,""seconds"":58,""milliseconds"":99.167}|
|2011|{""hours"":2,""minutes"":12,""seconds"":29,""milliseconds"":826.536}|
|2020|{""hours"":2,""minutes"":12,""seconds"":10,""milliseconds"":518.667}|
|2021|{""hours"":2,""minutes"":11,""seconds"":48,""milliseconds"":370.733}|
