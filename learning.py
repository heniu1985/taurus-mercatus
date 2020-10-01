import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

filename = "data/mbk_w.csv"

df = pd.read_csv(filename)
df = df[["Data", "Zamkniecie"]]
MA = pd.Series(df['Zamkniecie'].rolling(30).mean(), name='MA_' + str("30"))
df = df.join(MA)

print(df)

# plt.figure(figsize=[15,10])
# plt.grid(True)
# plt.plot(mbank["Zamkniecie"], label="close")
# plt.plot(mbank["MA 30"], label="MA 30")
# plt.legend(loc=2)

# plt.show()