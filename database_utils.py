import yaml
from sqlalchemy import create_engine,text
from data_extraction import DataExtractor
from data_cleaning import DataCleaning 


class DatabaseConnector:
    def __init__(self):
        pass

    def read_db_creds(self, yaml_path='db_creds.yaml'): 

        with open(yaml_path, 'r') as f: # Load the credentials from the YAML file
            creds = yaml.safe_load(f) 
        return creds #returning the credentials as a dictionary 

    def init_db_engine(self,creds): 
        engine = create_engine(f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        #initialised the engine above with creds from yaml
        return engine #returning the engine after initialising it

    def list_db_tables(self,engine):

        with engine.connect() as conn:
            tables = conn.execute(text("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'public';")).fetchall()
            table_names = [table[0] for table in tables]
        return table_names
    
    def upload_to_db(self,cleaned_data,table_name):

        with open('pass.yaml', 'r') as t: # Load the credentials from the YAML file
            pas = yaml.safe_load(t) 
        new_engine = create_engine(f"postgresql+psycopg2://postgres:{pas['PASS']}@localhost:5432/sales_data")
        cleaned_data.to_sql(table_name, new_engine, if_exists='replace', index=False)
        
db_connector = DatabaseConnector()
dataextractor = DataExtractor()
datacleaning = DataCleaning()

creds = db_connector.read_db_creds()               
engine = db_connector.init_db_engine(creds)
table_names = db_connector.list_db_tables(engine)
user_table = [name for name in table_names if "user" in name][0]
user_df = dataextractor.read_rds_table(engine,user_table)
user_df.to_csv('user_unclean.csv')
dim_users = datacleaning.clean_user_data(user_df)
dim_users.to_csv('user_clean.csv')
db_connector.upload_to_db(dim_users, table_name='dim_users')   #m2t3

pdf_df = dataextractor.retrieve_pdf_data()
pdf_df.to_csv('unclean_card.csv')
dim_card_details = datacleaning.clean_card_data(pdf_df)
dim_card_details.to_csv('clean_card.csv')
db_connector.upload_to_db(dim_card_details, table_name='dim_card_details')   #m2t4

number_of_stores = dataextractor.list_number_of_stores()
stores_df = dataextractor.retrieve_stores_data(number_of_stores)
dim_store_details = datacleaning.clean_store_data(stores_df)
db_connector.upload_to_db(dim_store_details,table_name='dim_store_details')   #m2t5

products_df = dataextractor.extract_from_s3()
clean_products_df  = datacleaning.clean_products_data(products_df)
dim_products = datacleaning.convert_product_weights(clean_products_df)
db_connector.upload_to_db(dim_products,table_name='dim_products')    #m2t6

orders_table_name = [name for name in table_names if "orders" in name][0]
orders_df = dataextractor.read_rds_table(engine,orders_table_name)
orders_table = datacleaning.clean_orders_data(orders_df)
db_connector.upload_to_db(orders_table,table_name='orders_table')   #m2t7

events_df = dataextractor.extract_timestamp()
dim_date_times = datacleaning.clean_events(events_df)
db_connector.upload_to_db(dim_date_times,table_name='dim_date_times') #m2t8
