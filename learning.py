import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import indicators

filename = "data/mbk_w.csv"

df = pd.read_csv(filename)
df = df[["Data", "Zamkniecie"]]

df = indicators.moving_average(df)
df = indicators.exponential_moving_average(df)

# print(df)

plt.figure(figsize=[15,10])
plt.grid(True)
plt.plot(df["Zamkniecie"], label="close")
plt.plot(df["MA_30"], label="MA_30")
plt.plot(df["EMA_30"], label="EMA_30")
plt.legend(loc=2)

plt.show()