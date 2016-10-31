import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests as req


#################################################################################
# Data Fetching
#################################################################################


def data_path(symbol):
    return "./data/{}.csv".format(symbol)

def pull_historical_data(symbol):
    table_url = "http://ichart.finance.yahoo.com/table.csv?s=" + symbol
    file_path = data_path(symbol)
    response = req.get(table_url)
    response_data = response.text if response.ok else None
    if response_data:
        outfile = open(file_path, "w")
        outfile.write(response_data)
        outfile.close()
        return file_path
    return False

def get_or_fetch_data_frame(symbol, read_csv_args={}):
    """
    We try to get the file if it exists, but if it doesn't we'll
    go fetch it and then pull in the data.
    
    Returns a dataframe from the Yahoo Data csv export
    """
    try:
        df = pd.read_csv(data_path(symbol), **read_csv_args)
    except FileNotFoundError:
        df = pd.read_csv(pull_historical_data(symbol), **read_csv_args)
    return df

#################################################################################
# Data Frame Manipulation Functions
#################################################################################


def get_max_close(symbol):
    df = pd.read_csv(data_path(symbol))
    return df['Close'].max()

def get_mean_vol(symbol):
    df = pd.read_csv(data_path(symbol))
    return df['Volume'].mean()

def plot_high_prices(symbol):
    df = pd.read_csv(data_path(symbol))
    plt.plot(df["High"])
    plt.show()

def mk_empty_df():
    start_date = '2010-01-22'
    end_date   = '2010-01-26'
    dates      = pd.date_range(start_date, end_date)
    df1        = pd.DataFrame(index=dates)
    return df1

def mk_SPY_df(cols=None):
    return get_or_fetch_data_frame("SPY",
                {"index_col": "Date",
                 "usecols": cols,
                 "na_values": ["NaN"],
                 "parse_dates": True})

def market_dates():
    return mk_SPY_df(["Date"])


our_symbols = ['GOOG', 'IBM', 'GLD']

def get_data(symbols, dates=None):
    """
    Read stock data (adjusted close) for given symbols from CSV files.
    """
    df = dates or market_dates()
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        tmpdf = get_or_fetch_data_frame(symbol,
                    {"index_col": "Date",
                     "usecols": ["Date", "Adj Close"],
                     "na_values": ["NaN"],
                     "parse_dates": True}).rename(columns={'Adj Close': symbol})
        df = df.join(tmpdf, how='inner')
    return df.sort_index()

def index_stocks_on_SPY(sybols, dates=None):
    pass


def test_run():
    df1   = mk_empty_df()
    dfSPY = pd.read_csv("data/SPY.csv",
                        index_col="Date",
                        usecols=["Date", "Adj Close"],
                        na_values=["NaN"],
                        parse_dates=True).rename(columns={'Adj Close': 'SPY'})
    df1 = df1.join(dfSPY, how='inner')
    return df1

def normalize_data(df):
    return df/df.ix[0,:]

#################################################################################
# Numpy Array Work
#################################################################################




#################################################################################
# PLOTTING FUNCTIONS
#################################################################################


def plot_data(df, title="Stock Prices", normalize=False):
    """
    Plot the stock Prices for given data frames
    """
    df = normalize_data(df) if normalize else df
    ax = df.plot(title=title, fontsize=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()
