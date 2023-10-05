import datetime
import random

import pandas as pd

def initiate_newProduct():

    new_product = {
        'Pid': 501,
        'RealPrice': 1761,
        'CostPrice': 184,
            'Color': "Yellow",
        'EngineSize': 26.7,
        'ProdDate': datetime.datetime(2020, 1, 1),
        'CompName': "Company B"
    }
    return pd.DataFrame(new_product, index=[0])

def initiate_tables():

    product_data = {
        'Pid': range(1, 501),  # Product IDs from 1 to 100
        'RealPrice': [random.randint(500, 2000) for _ in range(500)],  # Random real prices
        'CostPrice': [random.randint(100, 500) for _ in range(500)],  # Random cost prices
            'Color': [random.choice(['Red', 'Blue', 'Green', 'Yellow']) for _ in range(500)],  # Random colors
        'EngineSize': [round(random.uniform(1.0, 30.0), 1) for _ in range(500)],  # Random engine sizes
        'ProdDate': [datetime.datetime(random.randint(2010, 2023), 1, 1) for _ in range(500)], # Random production dates
        'CompName': [random.choice(['Company A', 'Company B', 'Company C']) for _ in range(500)]  # Random company names
    }


    customer_data = {
        'Cid': range(1, 1001),  # Customer IDs from 101 to 200
        'Age': [random.randint(18, 70) for _ in range(1000)],  # Random sell prices
        'District': [random.choice(["south","west","north","east"]) for _ in range(1000)]  # Random sell dates
    }

    deal_data = {
        'Did': range(1,5001),  # Customer IDs from 101 to 200
        'Pid': [random.randint(1, 500) for _ in range(5000)],  # Random product IDs
        'Cid': [random.randint(1,1000) for _ in range(5000)],  # Customer IDs
        'SellPrice': [random.randint(600, 2500) for _ in range(5000)],  # Random sell prices
        'SellDate': [datetime.datetime(random.randint(2019, 2023), random.randint(1, 12), random.randint(1, 28)) for _
                     in range(5000)]  # Random sell dates
    }

    product_df = pd.DataFrame(product_data)
    customer_df = pd.DataFrame(customer_data)
    deal_df = pd.DataFrame(deal_data)

    return product_df, customer_df, deal_df

def product_details():

    # return product_groups dictionary (represents all columns with const number of options)
    # return product_dates dictionary (represents all columns with const datetime representation)

    product_groups = {
        "Color": ['Red', 'Blue', 'Green', 'Yellow'],
        "CompName": ['Company A', 'Company B', 'Company C']
    }

    product_dates = {
        "ProdDate": 6000
    }

    return product_groups, product_dates

def deal_details():

    # return deal_groups dictionary (represents all columns with const number of options)
    # return deal_dates dictionary (represents all columns with const datetime representation)

    deal_groups = {

    }

    deal_dates = {
        "SellDate": 365
    }

    return deal_groups, deal_dates
