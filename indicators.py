import pandas as pd

def moving_average(df, periods=30):
    # Function calculating Moving Average for given data
    ma = pd.Series(df['Zamkniecie'].rolling(periods, min_periods=periods).mean(), name='MA_' + str(periods))
    df = df.join(ma)
    return df


def exponential_moving_average(df, periods=30):
    # Function calculating Moving Average for given data
    ema = pd.Series(df['Zamkniecie'].ewm(periods, min_periods=periods).mean(), name='EMA_' + str(periods))
    df = df.join(ema)
    return df


def rsi():
    pass


def tsi():
    pass