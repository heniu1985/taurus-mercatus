import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

filename = "data/mbk_w.csv"

mbank = pd.read_csv(filename)
mbank = mbank[["Data", "Zamkniecie"]]
mbank["MA 30"] = mbank.iloc[:, 1].rolling(window=30).mean()

plt.figure(figsize=[15,10])
plt.grid(True)
plt.plot(mbank["Zamkniecie"], label="close")
plt.plot(mbank["MA 30"], label="MA 30")
plt.legend(loc=2)

plt.show()