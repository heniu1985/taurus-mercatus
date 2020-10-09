import csv

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import indicators

import requests

"""
    Pobieranie pliku z symbolami
"""

# filename = "data/stooq_symbole.csv"

# res = requests.get("https://stooq.pl/db/l/?g=6")

# try:
#     res.raise_for_status()
# except Exception:
#     print("Zła strona!!!")

# stooq_symbole = open(filename, "wb")

# for fragment in res.iter_content(100000):
#     stooq_symbole.write(fragment)

# stooq_symbole.close()

"""
    Utworzenie listy z symbolami instrumentów
"""

# symbole = []
# with open(filename) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         symbole.append(row[0][:3])

# symbole.remove("<TI")
# print(symbole)

"""
Pobieranie notowań
"""
# filename = "data/pkn_w.csv"

# res = requests.get("https://stooq.pl/q/d/l/?s=pkn&i=w")

# try:
#     res.raise_for_status()
# except Exception:
#      print("Zła strona!!!")

# pobrany_plik = open(filename, "wb")

# for chunk in res.iter_content(100000):
#     pobrany_plik.write(chunk)

# pobrany_plik.close()

"""
    Odczytywanie pliku z danymi
    Wyliczanie wskaźników
"""
filename = "data/wic.csv"

try:
    df = pd.read_csv(filename)
    df = df[["Data", "Zamkniecie"]]

    df = indicators.moving_average(df)
    df = indicators.exponential_moving_average(df)

    print(df)
except KeyError:
    print("Bad datas!!!")
except FileNotFoundError:
    print("File not found!!!")

"""
    Tworzenie wykresu
"""

# plt.figure(figsize=[15,10])
# plt.grid(True)
# plt.plot(df["Zamkniecie"], label="close")
# plt.plot(df["MA_30"], label="MA_30")
# plt.plot(df["EMA_30"], label="EMA_30")
# plt.legend(loc=2)

# plt.show()