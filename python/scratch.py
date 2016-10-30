import pandas as pd
import matplotlib.pyplot as plt
import requests as req

def pull_historical_data(symbol):
    table_url = "http://ichart.finance.yahoo.com/table.csv?s=" + symbol
    file_name = "./data/" + symbol + ".csv"
    response = req.get(table_url)
    response_data = response.text if response.ok else None
    if response_data:
        outfile = open(file_name, "w")
        outfile.write(response_data)
        outfile.close()
        return file_name
    return False

def get_max_close(symbol):
    df = pd.read_csv("./data/{}.csv".format(symbol))
    return df['Close'].max()

def get_mean_vol(symbol):
    df = pd.read_csv("./data/{}.csv".format(symbol))
    return df['Volume'].mean()

def plot_high_prices(symbol):
    df = pd.read_csv("./data/{}.csv".format(symbol))
    plt.plot(df["High"])
    plt.show()
