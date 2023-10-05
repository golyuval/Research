import datetime
import numpy as np
import pandas as pd


def copies(prod, deal, customer):

    in_product = prod.copy(deep=True)
    in_deal = deal.copy(deep=True)
    in_customer = customer.copy(deep=True)

    return in_product, in_deal, in_customer


def encode_deals_df(deals, filters):

    # filter data by given scope (by days)
    for name, scope in filters.items():
        filter_date(deals, name, scope)

    return deals.drop(columns=['Pid'], inplace=False)





def encode_product_df(products, groups, dates):

    # 1-hot code each classification column
    for name, group in groups.items():
        encode_group(products, name, group)

    # transform each date into numeric indicator (num of days from the given limit)
    for name, limit in dates.items():
        encode_date(products, name, limit)

    return products.drop(columns=['Pid'], inplace=False)



def encode_date(df,col_name,days): # turn column of dates into column of numeric integer values

    # df : data frame to encode
    # col_name : column in df to encode
    # days : lower bound date by days
    # low_bound : lower bound by datetime
    # new_col : new list which indicate the amount of days passed from col_name date from delta

    low_bound = datetime.datetime.now() - datetime.timedelta(days=days)
    new_col = np.zeros(len(df[col_name]))

    for i in range(len(df[col_name])):
        new_col[i] = (df[col_name][i] - low_bound).days

    df.drop(columns=[col_name], inplace=True)
    df[col_name] = new_col.tolist()


def encode_group(df, col_name, tokens):  # turn multiple tokens column into binary columns

    # df : data frame to encode
    # col_name : column in df to 1-hot code
    # tokens : the options in df["col_name"]
    # map_Tokens : map token to index
    # binary_Tokens : dictionary of {token1 : <indicator_list>, ...}


    binary_Tokens = [np.zeros(len(df[col_name])) for _ in range(len(tokens))]
    map_Tokens = {}

    for i, token in enumerate(tokens): # initiates map_Tokens
        map_Tokens[token] = i

    for i, token in enumerate(df[col_name]): # initiates binary_Tokens
        binary_Tokens[map_Tokens[token]][i] = 1

    for i, token in enumerate(map_Tokens): # add all tokens as indicator columns to df
        df[token] = binary_Tokens[i].tolist()

    df.drop(columns=[col_name], inplace=True) # remove col_name column from df



def filter_date(df, col, delta=365):

    # df : data frame to filter
    # col : date column to filter by
    # delta : amount of time to show in timedelta terms

    current_date = datetime.datetime.now()
    limit = current_date - datetime.timedelta(days=delta)

    df.drop(df.loc[df[col] < limit].index, inplace=True)  # remove each row that [col] value is smaller than the limit


"""

import pandas as pd
import random
from datetime import datetime, timedelta

# Create a list of 100 random dates within a date range
start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()
date_list = [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(100)]

# Create a list of 100 random colors
colors = ["red", "blue", "black"]
color_list = [random.choice(colors) for _ in range(100)]

# Create a DataFrame
df = pd.DataFrame({'hi': date_list, 'color': color_list})

# Print the DataFrame
print(df)

encode_date(df,"hi",365)
print(df)

encode_str(df,"color",colors)
print(df)"""

