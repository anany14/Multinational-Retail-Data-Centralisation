import yaml
from sqlalchemy import create_engine,text

class DatabaseConnector:
    def __init__(self):
        pass

    def read_db_creds(self, yaml_path='db_creds.yaml'): 

        with open(yaml_path, 'r') as f: # Load the credentials from the YAML file
            creds = yaml.safe_load(f) 
        return creds #returning the credentials as a dictionary 

    def init_db_engine(self): 
        creds = self.read_db_creds()
        engine = create_engine(f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        #initialised the engine above with creds from yaml
        return engine #returning the engine after initialising it

    def list_db_tables(self):

        engine = self.init_db_engine()
        with engine.connect() as conn:
            tables = conn.execute(text("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'public';")).fetchall()
            table_names = [table[0] for table in tables]
        return table_names
    
    def upload_to_db(self,cleaned_data,table_name='dim_users'):
        
        new_engine = create_engine(f"postgresql+psycopg2://postgres:wuMBRELLA!2@localhost:5432/sales_data")
        connection = new_engine.connect()
        cleaned_data.to_sql(table_name, connection, if_exists='replace', index=False)
        connection.close()


db_connector = DatabaseConnector()
creds = db_connector.read_db_creds()
engine = db_connector.init_db_engine()
table_names = db_connector.list_db_tables()
print(creds, "\n", engine,"\n", table_names)

from data_extraction import DataExtractor
dataextractor = DataExtractor()
df = dataextractor.read_rds_table(engine,table_names)
print(df.head())

from data_cleaning import DataCleaning 
datacleaning = DataCleaning()
cleaned_data = datacleaning.clean_user_data(df)
print(cleaned_data.head())

#db_connector.upload_to_db(cleaned_data, table_name='dim_users')

pdf_df = dataextractor.retrieve_pdf_data()
clean_card_df = datacleaning.clean_card_data(pdf_df)
print(clean_card_df.head())
print(clean_card_df.describe())
print(clean_card_df.info())
#db_connector.upload_to_db(clean_card_df, table_name='dim_card_details')
