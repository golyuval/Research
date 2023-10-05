
def valid_test_train(customer_df):
    # Check if there are enough data points for training and testing
    if customer_df.shape[0] < 2:
        print("Insufficient data points for training and testing.")
        return