# This file contains technical analisys indicators that I use in my strategies

import pandas as pd

def moving_average(df, periods=30):
    """Function calculating Moving Average (MA) for given data

    Args:
        df (pandas.DataFrame): Quotes with closing prices
        periods (int, optional): The number of periods from which MA is calculated. Defaults to 30.

    Returns:
        pandas.DataFrame: Quotes extended by the calculated MA
    """
    ma = pd.Series(df['Zamkniecie'].rolling(periods, min_periods=periods).mean(), name='MA_' + str(periods))
    df = df.join(ma)
    return df


def exponential_moving_average(df, periods=30):
    """Function calculating Exponential Moving Average (EMA) for given data

    Args:
        df (pandas.DataFrame): Quotes with closing prices
        periods (int, optional): The number of periods from which EMA is calculated. Defaults to 30.

    Returns:
        pandas.DataFrame: Quotes extended by the calculated EMA
    """
    ema = pd.Series(df['Zamkniecie'].ewm(periods, min_periods=periods).mean(), name='EMA_' + str(periods))
    df = df.join(ema)
    return df


def rsi():
    pass


def tsi():
    pass