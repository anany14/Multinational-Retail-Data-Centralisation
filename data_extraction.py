import pandas as pd
from sqlalchemy import text
import tabula
import requests
import boto3
from io import StringIO


class DataExtractor:
    def __init__(self):
        pass

    def read_rds_table(self,engine,table_name):
        
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name};")).fetchall()
            df = pd.DataFrame(result)
        
        return df

    def retrieve_pdf_data(self,link="https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"):
        
        pdf_dfs = tabula.read_pdf(link,pages='all')
        pdf_df = pd.concat(pdf_dfs)  #as tabula returns a list of pandas dataframe which is 1 df every page of the pdf
        
        return pdf_df   #we use concat to merge all the list of dfs into a single df
    
    def list_number_of_stores(self,endpoint='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores',header={'x-api-key' :'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
        
        number_of_stores = requests.get(f'{endpoint}',headers=header)
        
        return number_of_stores.json()['number_stores']

    def retrieve_stores_data(self,store_numbers,endpoint='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'):
        
        i = 0 
        stores=[]
        while i < store_numbers:
            store = requests.get(f'{endpoint}{i}',headers={'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'})
            stores.append(store.json())
            i+=1 
        
        df = pd.DataFrame(stores)
        
        return df

    def extract_from_s3(self,s3_address ='s3://data-handling-public/products.csv'):
        
        bucket_name, object_key = s3_address.replace("s3://", "").split("/", 1)
        # Create a connection to the S3 resource
        s3 = boto3.resource('s3')
        print(bucket_name, object_key)
        # Get the object from the bucket
        obj = s3.Object(bucket_name, object_key)
        # Read the contents of the object as a string
        file_content = obj.get()['Body'].read().decode('utf-8')
        # was unable to read file content using pandas so had to create a file like object
        # Create a file-like object from the string contents
        file_obj = StringIO(file_content)
        # Read the CSV data from the file-like object
        df = pd.read_csv(file_obj)
        
        return df
    

    def extract_timestamp(self,link="https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"):
        
        response = requests.get(link)
        data = response.json()
        events_df = pd.DataFrame(data)
        events_dfcopy = events_df.copy()
    
        return events_dfcopy
    