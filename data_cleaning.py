import pandas as pd
import numpy as np
from datetime import datetime

class DataCleaning:
    def __init__(self):
        pass

    def clean_user_data(self,user_df):
        # Drop the 'index' column
        user_df.drop('index', axis=1, inplace=True)
        # Convert 'date_of_birth' column to datetime format
        user_df['date_of_birth'] = pd.to_datetime(user_df['date_of_birth'], format='%Y-%m-%d', errors='coerce')
        # Convert 'join_date' column to datetime format
        user_df['join_date'] = pd.to_datetime(user_df['join_date'], format = '%Y-%m-%d', errors='coerce')
        # Drop rows with null values in important columns
        user_df.dropna(subset=['first_name', 'last_name', 'date_of_birth', 'email_address'], inplace=True)
        # Convert 'phone_number' column to integer
        user_df['phone_number'] = pd.to_numeric(user_df['phone_number'], errors='coerce')
        # Drop rows with incorrect types in important columns
        user_df = user_df[pd.to_numeric(user_df['phone_number'], errors='coerce').notnull()]
        user_df = user_df[pd.to_datetime(user_df['join_date'], errors='coerce').notnull()]
        # Reset index after dropping rows
        user_df.reset_index(drop=True, inplace=True)

        return user_df


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