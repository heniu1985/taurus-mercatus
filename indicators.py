# This file contains technical analisys indicators that I use in my strategies

import pandas as pd
import numpy as np

def moving_average(df, periods=30):
    """Function calculating Moving Average (MA) for given data

    Args:
        df (pandas.DataFrame): Quotes with closing prices
        periods (int, optional): The number of periods from which MA is calculated. Defaults to 30.

    Returns:
        pandas.DataFrame: Quotes extended by the calculated MA
    """
    ma = pd.Series(df['<CLOSE>'].rolling(periods, min_periods=periods).mean(), name='MA_' + str(periods))
    df = df.join(ma.round(4))

    return df


def exponential_moving_average(df, periods=30):
    """Function calculating Exponential Moving Average (EMA) for given data

    Args:
        df (pandas.DataFrame): Quotes with closing prices
        periods (int, optional): The number of periods from which EMA is calculated. Defaults to 30.

    Returns:
        pandas.DataFrame: Quotes extended by the calculated EMA
    """
    ema = pd.Series(df['<CLOSE>'].ewm(periods, min_periods=periods).mean(), name='EMA_' + str(periods))
    df = df.join(ema.round(4))

    return df


def rsi(df, periods=14):
    
    prices = df["<CLOSE>"].tolist()

    i = 0
    up_prices = []
    down_prices = []
    
    while i < len(prices):
        if i == 0:
            up_prices.append(0)
            down_prices.append(0)
        else:
            if (prices[i] - prices[i-1]) > 0:
                up_prices.append(round(prices[i] - prices[i-1], 2))
                down_prices.append(0)
            else:
                down_prices.append(round(prices[i] - prices[i-1], 2))
                up_prices.append(0)
        i += 1

    p = 0
    s = 0
    avg_gain = []
    avg_loss = []

    while p < len(prices):
        if p < periods:
            avg_gain.append(0)
            avg_loss.append(0)
        else:
            sum_of_gains = sum(up_prices[s:p])
            sum_of_loss = sum(down_prices[s:p])
            avg_gain.append(round(sum_of_gains / periods, 2))
            avg_loss.append(abs(round(sum_of_loss / periods, 2)))
            s += 1
        p += 1
    
    p = 0
    rs = []
    rsi = []

    while p < len(prices):
        if p < periods:
            rs.append(0)
            rsi.append(0)
        else:
            try:
                rs_value = round(avg_gain[p] / avg_loss[p], 4)
                rs.append(rs_value)
                rsi_value = round(100 - 100 / (1 + rs_value), 4)
                rsi.append(rsi_value)
            except ZeroDivisionError:
                rs.append(rs[p-1])
                rsi.append(rsi[p-1])
        p += 1

    df = df.assign(RSI = rsi)
    df.replace(0, np.nan, inplace=True)

    return df

def tsi():
    
    pass