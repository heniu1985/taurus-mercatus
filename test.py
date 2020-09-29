import csv

from datetime import datetime

import matplotlib.pyplot as plt

filename = "data/mbk_w.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    dates, closes = [], []
    for row in reader:
        current_date = datetime.strptime(row[0], "%Y-%m-%d")
        close = float(row[4])
        dates.append(current_date)
        closes.append(close)

plt.style.use("seaborn")
fig, ax = plt.subplots()
ax.plot(dates, closes, c="blue")

ax.set_title("mBank", fontsize=24)
ax.set_xlabel("", fontsize=16)
ax.set_ylabel("Price", fontsize=16)
ax.tick_params(axis="both", which="major", labelsize=16)

plt.show()