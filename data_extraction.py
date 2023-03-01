import pandas as pd
from sqlalchemy import text
import tabula


class DataExtractor:
    def __init__(self):
        pass

    def read_rds_table(self,engine,table_names):
        table_name = [name for name in table_names if "user" in name][0]
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name};")).fetchall()
            print_tables = conn.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}';")).fetchall()
            [print(x) for x in print_tables]
            df = pd.DataFrame(result)
        return df

    def retrieve_pdf_data(self,link="https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"):

        pdf_dfs = tabula.read_pdf(link,pages='all')
        pdf_df = pd.concat(pdf_dfs)  #as tabula returns a list of pandas dataframe which is 1 df every page of the pdf
        return pdf_df   #we use concat to merge all the ist of dfs into a single df
    



        
    

