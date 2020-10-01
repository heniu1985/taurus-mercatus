#  Imports. I think I can remove that in the future.
import pandas as pd


def moving_average(company, period=30):
    # Function will calculate moving avarage of given period
    ma = company.iloc[:, 1].rolling(window=period).mean()
    return ma


def rsi():
    pass


def tsi():
    pass