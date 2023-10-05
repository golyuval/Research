import random
import torch
import torch.nn as nn
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import Data.Generator
import Data.Validator
import Data.Encoder
from Algorithm import PredictionModel


def calc_profit(deals, products):  # Calculate each product's year profit

    f_deals = deals[["Pid", "SellPrice"]].copy(deep=True)
    f_products = products[["Pid", "CostPrice"]].copy(deep=True)

    merged_df = pd.merge(f_deals, f_products, on='Pid', how='outer')  # Merge data by Pid
    merged_df['Profit'] = merged_df['SellPrice'] - merged_df['CostPrice']  # Calculate profit for each sale
    merged_df = merged_df[["Pid", "Profit"]]

    with_id = merged_df.groupby('Pid').sum()
    without_id = with_id["Profit"].tolist()
    descending = with_id.sort_values(by="Profit", ascending=False, inplace=True)

    return with_id, without_id, descending


def predict_profit(new_product, product_df, customer_df, deal_df, model):  # Predict profit for a new product

    product_df = product_df._append(new_product, ignore_index=True) # Add the new product to the dataframe

    # Prepare the data for prediction
    X = product_df.drop(columns=['Pid'])
    X = StandardScaler().fit_transform(X)  # Standardize features
    X = torch.Tensor(X)

    # Use the model to predict profit for all products
    predicted_profits = model(X).detach().numpy()

    # Find the index of the new product in the list of predictions
    new_product_index = product_df.shape[0] - 1

    # Sort the products by predicted profit
    sorted_indices = np.argsort(predicted_profits[:, 0])[::-1]

    # Find the position of the new product in the sorted list
    new_product_position = np.where(sorted_indices == new_product_index)[0][0] + 1

    return predicted_profits[new_product_index][0], new_product_position


# Main function
def main():

    # random seed for equal simulations
    random.seed(14)

    # prepare data
    deal_groups, deal_dates = Data.Generator.deal_details()
    prod_groups, prod_dates = Data.Generator.product_details()
    product_df, customer_df, deal_df = Data.Generator.initiate_tables()
    _, _, _ = Data.Encoder.copies(product_df, deal_df, customer_df)
    x_products = Data.Encoder.encode_product_df(product_df, prod_groups, prod_dates)
    x_deals = Data.Encoder.encode_deals_df(deal_df, deal_dates)

    print("-------------------------------------------------------------------------\n Example: \n")
    print(product_df.iloc[1])
    print("\n--------------------------------------------------------------------------\n")

    # calculate profit (target data)
    _, profit, _ = calc_profit(deal_df, product_df)

    # Initialize and train the profit prediction model
    in_size, model, criterion, optimizer = PredictionModel.init_Model(product_df)

    # Divide (data (100%)) set to    ---------->   (train (80%) , test (20%)) data sets
    X_train, X_test, y_train, y_test = train_test_split(x_products, profit, test_size=0.2, random_state=42)

    # scale and fit Tensor of training data
    X_train = StandardScaler().fit_transform(X_train)
    X_train = torch.Tensor(X_train)
    y_train = torch.Tensor(y_train).view(-1, 1)

    # scale and fit Tensor of test data
    X_test = StandardScaler().fit_transform(X_test)
    X_test = torch.Tensor(X_test)
    y_test = torch.Tensor(y_test).view(-1, 1)

    print("Learning......... \n")
    epochs = 10000
    visual_factor = 1000
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

        if epoch % visual_factor == 0:
            print(f"Loss sample {epoch//visual_factor} / {epochs//visual_factor} :  {loss}")

    print("\nDone !!! \n")

    # Create a new product to predict its profit
    new_product = Data.Generator.initiate_newProduct()
    Data.Encoder.encode_product_df(new_product, prod_groups, prod_dates)

    # Predict profit for the new product and get its position
    predicted_profit, position = predict_profit(new_product, product_df, customer_df, deal_df, model)

    print(f"Predicted Yearly Profit for the New Product: ${predicted_profit:.2f}")
    print(f"Position of the New Product Among Existing Products: {position}")

if __name__ == '__main__':
    main()
