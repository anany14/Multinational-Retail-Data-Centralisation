import pandas as pd
import numpy as np
from datetime import datetime
import re

class DataCleaning:
    def __init__(self):
        pass

    def clean_user_data(self,user_df):

        user_df['country_code'] = user_df['country_code'].str.replace('GGB','GB')
        user_df = user_df[user_df['country_code'].astype(str).str.match('(GB)|(DE)|(US)')]
        user_df['country_code'] = user_df['country_code'].astype('category')
        user_df.drop('index',axis=1,inplace=True)
        user_df['date_of_birth'] = pd.to_datetime(user_df['date_of_birth'],format='%Y-%m-%d',errors='coerce')
        user_df['join_date'] = pd.to_datetime(user_df['join_date'],format='%Y-%m-%d',errors='coerce')
        user_df['email_address'] = user_df['email_address'].str.replace('@@','@',regex=True)
        user_df['address'] = user_df['address'].str.replace('\n','',regex=True)
        user_df['country'] = user_df['country'].astype('category')
        user_df['country_code'] = user_df['country_code'].astype('category')
        user_df['company'] = user_df['company'].astype('category')


     
        return user_df


    def clean_card_data(self,card_df):
        
        #converting datatype to datetime 
        card_df['expiry_date'] = pd.to_datetime(card_df['expiry_date'], format='%m/%y', errors='coerce')
        card_df['date_payment_confirmed'] = pd.to_datetime(card_df['date_payment_confirmed'],format='%Y-%m-%d', errors='coerce')
        #converting column datatype to category
        card_df['card_provider'] = card_df['card_provider'].fillna('Unknown').astype('category')
        #creating a mask where the column only accepts the correct card categories
        mask = card_df['card_provider'].isin(['Diners Club / Carte Blanche', 'American Express', 'JCB 16 digit','JCB 15 digit', 'Maestro', 'Mastercard', 'Discover','VISA 19 digit', 'VISA 16 digit', 'VISA 13 digit'])
        #applying the mask so erroneous values are removed
        card_df = card_df.loc[mask]
        #converting card_number to 'str' and removing "?" from some values
        card_df['card_number'] = card_df['card_number'].astype(str)
        card_df['card_number'] = card_df['card_number'].str.replace('?','',regex=True)
        #some card_numbers contain the expiry date in the card_number column, so making a separate df to store these rows
        fix = card_df[card_df['card_number'].str.contains('[^0-9 ]')]
        #making the df clean by removing the rows earlier mentioned
        card_df = card_df[~card_df['card_number'].str.contains('[^0-9 ]')]
        #extracting the expiry date values from card_number column to the expiry_date column
        fix['expiry_date'] = fix['card_number'].str[-5:]
        fix['card_number'] = fix['card_number'].str[:-6]
        #merging the dataframes into a sinlge df
        merge = pd.concat([card_df,fix],ignore_index=True)
        #converting the data_type to correct types
        merge['expiry_date'] = pd.to_datetime(merge['expiry_date'], format='%m/%y', errors='coerce')
        merge['date_payment_confirmed'] = pd.to_datetime(merge['date_payment_confirmed'],format='%Y-%m-%d', errors='coerce')
        merge['card_number'] = merge['card_number'].astype(str)
        merge['card_provider'] = merge['card_provider'].astype('category')
        
        return merge
    


    def clean_store_data(self,stores_df):

        # checking to make sure all the store codes are in the correct form
        pattern = r'^[A-Z]{2,3}-[A-Z0-9]{6,8}$'
        stores_df = stores_df[stores_df['store_code'].astype('str').str.match(pattern)]

        stores_df.drop('lat', axis=1,inplace=True)
        stores_df.drop('index', axis=1,inplace=True)

        #converting to correct datetime format
        stores_df['opening_date'] = pd.to_datetime(stores_df['opening_date'],format='%Y-%m-%d',errors='coerce')

        #converting the column country_code,locality, continent and store_type into a category
        stores_df['locality'] = stores_df['locality'].astype('category')
        stores_df['country_code'] = stores_df['country_code'].fillna('Unknown').astype('category')
        stores_df['continent'] = stores_df['continent'].astype('category')
        stores_df['store_type'] = stores_df['store_type'].astype('category')
        stores_df['staff_numbers'] = pd.to_numeric(stores_df['staff_numbers'], errors='coerce')

        # Convert longitude and latitude columns to numeric
        stores_df['longitude'] = pd.to_numeric(stores_df['longitude'], errors='coerce')
        stores_df['latitude'] = pd.to_numeric(stores_df['latitude'], errors='coerce')
        #stores_df = (stores_df['longitude'].astype('float') >= -180) & (stores_df['longitude'].astype('float') <= 180)
        #stores_df = (stores_df['latitude'].astype('float') >= -90) & (stores_df['latitude'].astype('float') <= 90)

        # Replace \n in the addresses with a space
        stores_df['address'] = stores_df['address'].astype('str').replace('\n', ' ', regex=True)
        stores_df['address'] = stores_df['address'].str.strip()

        return stores_df
    

    def clean_products_data(self,products_df):

        #using product code to remove all the unnecessary rows
        products_df['product_code'] = products_df['product_code'].astype(str)
        products_df['product_code'] = products_df['product_code'].str.upper()
        product_code_pattern = r'^[A-Z0-9]{2}-[A-Z0-9]{6,8}$'
        products_df = products_df[products_df['product_code'].str.match(product_code_pattern)]

        #weight column cleaned and converted to float
        products_df = products_df.rename(columns={'product_price': 'product_price(£)'})
        products_df['product_price(£)'] = products_df['product_price(£)'].str.replace("£","")
        products_df['product_price(£)'] = pd.to_numeric(products_df['product_price(£)'],errors='coerce')

        products_df['category'] = products_df['category'].astype('category')
        products_df['date_added'] = pd.to_datetime(products_df['date_added'],format='%Y-%m-%d',errors='coerce')

        # Rename the column to "still_available"
        products_df = products_df.rename(columns={'removed': 'still_available'})
        # Replace "Still_available" values with True and "Removed" values with False
        products_df['still_available'] = products_df['still_available'].replace({'Still_avaliable': True, 'Removed': False})
        products_df['still_available'] = products_df['still_available'].astype(bool)

        products_df.drop('Unnamed: 0',axis=1,inplace=True)

        return products_df


    def convert_product_weights(self,products_df):

        products_df['weight'] = products_df['weight'].astype('str')
        for idx, row in products_df.iterrows():
            weight = re.sub('[^0-9.]', '', row['weight'])
            if 'kg' in row['weight']:
                weight = float(weight)
            elif 'ml' in row['weight']:
                weight = float(weight) / 1000
            elif 'g' in row['weight']:
                weight = float(weight) / 1000
            elif 'oz' in row['weight']:
                weight = float(weight) / 35.72
            products_df.at[idx, 'weight'] = weight
        products_df = products_df.rename(columns={'weight':'weight(kg)'})

        return products_df

    def clean_orders_data(self,orders_df):

        orders_df.drop('first_name',axis=1,inplace=True)
        orders_df.drop('last_name',axis=1,inplace=True)
        orders_df.drop('1',axis=1,inplace=True)
        orders_df.drop('level_0',axis=1,inplace=True)
        orders_df.drop('index',axis=1,inplace=True)
        orders_df['card_number'] = pd.to_numeric(orders_df['card_number'])
        orders_df['product_quantity'] = pd.to_numeric(orders_df['product_quantity'])
        orders_df['product_code'] = orders_df['product_code'].str.upper()
        store_code_pattern = r'^[A-Z]{2,3}-[A-Z0-9]{5,8}$'
        orders_df = orders_df[orders_df['store_code'].astype('str').str.match(store_code_pattern)]
        product_code_pattern = r'^[A-Z0-9]{2}-[A-Z0-9]{6,8}$'
        orders_df = orders_df[orders_df['product_code'].str.match(product_code_pattern)]

        return orders_df
    

    def clean_events(self,events_df):

        events_df = events_df[~pd.to_numeric(events_df['month'], errors='coerce').isna()]
        events_df['DateTime'] = pd.to_datetime(events_df['year'].astype(str) + '-' + events_df['month'].astype(str) + '-' + events_df['day'].astype(str) + ' ' + events_df['timestamp'])
        events_df['time_period'] = events_df['time_period'].astype('category')
        events_df.drop('timestamp',axis=1,inplace=True)
        events_df.drop('month',axis=1,inplace=True)
        events_df.drop('year',axis=1,inplace=True)
        events_df.drop('day',axis=1,inplace=True)

        return events_df
