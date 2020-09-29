import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates

from mplfinance.original_flavor import candlestick_ohlc

import pandas as pd

filename = "data/mbk_w.csv"

plt.style.use("seaborn")

data = pd.read_csv(filename)
ohlc = data.loc[:, ["Data", "Otwarcie", "Najwyzszy", "Najnizszy", "Zamkniecie"]]
ohlc["Data"] = pd.to_datetime(ohlc["Data"])
ohlc["Data"] = ohlc["Data"].apply(mpl_dates.date2num)
ohlc = ohlc.astype(float)

fig, ax = plt.subplots()

candlestick_ohlc(ax, ohlc.values, width=0.6, colorup="green", colordown="red", alpha=0.8)

ax.set_xlabel('Data')
ax.set_ylabel('Cena')
fig.suptitle('mBank')

plt.show()