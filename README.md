# Multinational-Retail-Data-Centralisation

The goal of the project is to create a system that centralizes the multinational company's sales data, making it easily accessible and analyzable by the team. This involves storing the company's sales data in a database using postgreSQL and Python, the database will serve as the single source of truth for sales data. Once the database is set up, the team will be able to query it to obtain up-to-date metrics that will inform their decision-making processes and help them become more data-driven. Ultimately, the project aims to improve the company's efficiency and effectiveness in managing and analyzing its sales data.

## Milestone 1: Set-up GitHub Repo

## Milestone 2: Extracting and Cleaning the data from different sources

### Task 1: Set up a Database called **"sales_data"** using *pgadmin4*

### Task 2: Initialised 3 Project Classes -

**DataExtractor** - This class was created in the **data_extraction.py** script. Data extraction methods were created in this class to extract data from different sources such as CSV files, an API, and an S3 bucket. The methods contained are tailored to extract data from a specific data source. This class was used as a utility class.

**DataCleaning** - This class was created in the **data_cleaning.py** script. This class was used to clean the data extracted.

**DatabaseConnector** - This class was created in the **database_utils.py** script. This class was used to connect and upload data to the database.

### Task 3: Extracting and cleaning data

Used all the 3 scripts to extract data from an AWS RDS Database.

**Step 1:** I stored the AWS credentials of the in the file **db_creds.yaml** file. 

**Step 2:** Created a method read_db_creds which read the credentials yaml file and returned a dictionary of the credentials.
```
def read_db_creds(self, yaml_path='db_creds.yaml'):
    import yaml
    with open(yaml_path, 'r') as f: 
        creds = yaml.safe_load(f)
    return creds 
```

**Step 3:** created a method init_db_engine which read the credentials from the return of read_db_creds and initialised and returned an sqlalchemy database engine.
```
def init_db_engine(self): 
    from sqlalchemy import create_engine
    creds = self.read_db_creds()
    engine = create_engine(f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
    return engine 
```

**Step 4:** Used the engine from init_db_engine and created a method list_db_tables to list all the tables in the database to know which tables data can be extracted from.
```
def list_db_tables(self):
    engine = self.init_db_engine()
    with engine.connect() as conn:
        tables = conn.execute(text("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'public';")).fetchall()
        table_names = [table[0] for table in tables]
    return table_names
```

**Step 5:** Developed a method called read_rds_table in DataExtractor class which extracted the database table to a pandas DataFrame.
```
def read_rds_table(self,engine,table_names):
    table_name = [name for name in table_names if "user" in name][0]
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table_name};")).fetchall()
        print_tables = conn.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}';")).fetchall()
        [print(x) for x in print_tables]
        df = pd.DataFrame(result)
    return df
```

**Step 6:** Created a method called clean_user_data in the DataCleaning class which performed the cleaning of the user data.
```
def clean_user_data(self,user_df):
    user_df.drop('index', axis=1, inplace=True)
    user_df['date_of_birth'] = pd.to_datetime(user_df['date_of_birth'], format='%Y-%m-%d', errors='coerce')
    user_df['join_date'] = pd.to_datetime(user_df['join_date'], format = '%Y-%m-%d', errors='coerce')
    user_df.dropna(subset=['first_name', 'last_name', 'date_of_birth', 'email_address'], inplace=True)
    user_df['phone_number'] = pd.to_numeric(user_df['phone_number'], errors='coerce')
    user_df = user_df[pd.to_numeric(user_df['phone_number'], errors='coerce').notnull()]
    user_df = user_df[pd.to_datetime(user_df['join_date'], errors='coerce').notnull()]
    user_df.reset_index(drop=True, inplace=True)
    return user_df
```

**Step 7:** Created a method in DatabaseConnector class called upload_to_db. This method takes in a Pandas DataFrame and table name to upload to as an argument.
```
def upload_to_db(self,cleaned_data,table_name):

    with open('pass.yaml', 'r') as t: # Load the credentials from the YAML file
        pas = yaml.safe_load(t) 
    new_engine = create_engine(f"postgresql+psycopg2://postgres:{pas['PASS']}@localhost:5432/sales_data")
    cleaned_data.to_sql(table_name, new_engine, if_exists='replace', index=False)
```

**Step 8:** Used the upload_to_db method to store the data in my sales_Data database in a table named dim_users.
```
db_connector = DatabaseConnector()
db_connector.upload_to_db(clean_card_df, table_name='dim_card_details')
```

### Task 4: Extracted,cleaned and uploaded card details into sales_data database which were stored in a PDF document in an AWS S3 bucket using Tabula.
- Installed the package **Tabular-py** using pip on bash
- Created a method into the **DataExtractor** Class called **retrieve_pdf_data** to extract details.
```
def retrieve_pdf_data(self,link="https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"):
    pdf_dfs = tabula.read_pdf(link,pages='all')
    pdf_df = pd.concat(pdf_dfs)  #as tabula returns a list of pandas dataframe which is 1 df every page of the pdf
    return pdf_df   #we use concat to merge all the ist of dfs into a single df
```
- Created a method called **clean_card_data** in **DataCleaning** Class.
```
def clean_card_data(self,card_df):
    
    #dropping any rows will null values
    card_df = card_df.dropna()
    #removing any columns with erroneous values
    card_df = card_df[~card_df['card_number'].astype(str).str.contains('[^0-9]')]
    card_df = card_df[~card_df['card_provider'].str.contains('[^a-zA-Z0-9 /]')]
    #cleaing up any formatting issues in expiry_date column
    card_df['expiry_date'] = pd.to_datetime(card_df['expiry_date'], format='%m/%y', errors='coerce')
    card_df = card_df.dropna()
    # Clean up formatting errors in date_payment_confirmed column
    card_df['date_payment_confirmed'] = pd.to_datetime(card_df['date_payment_confirmed'], format='%Y-%m-%d', errors='coerce')
    card_df = card_df.dropna()
    # Convert the 'card_number' column to the Int64 data type
    card_df['card_number'] = pd.to_numeric(card_df['card_number'], errors='coerce').astype('Int64')
    #convert card_provider column to category data type
    card_df['card_provider'] = card_df['card_provider'].fillna('Unknown').astype('category')

    return card_df
```
- Uploaded to my **sales_data** database as a table called **dim_card_details**

### Task 5: 