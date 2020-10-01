#  Imports. I think I can remove that in the future.
import pandas as pd


def moving_average(df, periods=30):
    # Function calculating Moving Average for given data
    ma = pd.Series(df['Zamkniecie'].rolling(periods).mean(), name='MA_' + str(periods))
    df = df.join(ma)
    return df


def rsi():
    pass


def tsi():
    pass