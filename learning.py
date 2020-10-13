import os
import zipfile
import csv

import datetime

import requests

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import indicators

# def symbols_file_path():
#     """Function download file with instruments symbol

#     Returns:
#         FILE_PATH: Path to file with instruments symbol
#     """
#     STOOQ_SYMBOLS = "data/stooq_symbols.csv"  # Path to CSV file with instruments symbol
#     SYMBOLS_URL_PATH = "https://stooq.pl/db/l/?g=6"

#     symbols = requests.get(SYMBOLS_URL_PATH)

#     try:
#         symbols.raise_for_status()
#     except Exception:
#         print("Wrong path!!!")

#     symbols_file = open(STOOQ_SYMBOLS, "wb")
    
#     for fragment in symbols.iter_content(100000):
#         symbols_file.write(fragment)
    
#     symbols_file.close()

#     return STOOQ_SYMBOLS

# def list_of_symbols(file_path):
#     """Function make list with short instruments symbols

#     Args:
#         file_path (FILE_PATH): Path of file with instruments symbols

#     Returns:
#         list: List with short instruments symbols
#     """
#     symbols_list = []

#     with open(symbols_file_path()) as s:
#         reader = csv.reader(s)

#         for row in reader:
#             symbols_list.append(row[0][:3])
    
#     symbols_list.remove("<TI")
#     symbols_list = set(symbols_list)

#     return symbols_list

# def links_to_quotes():
#     """Function make a text file with links to files with qoutes
#     """
#     path = symbols_file_path()

#     FILE_PATH = "data/links.txt"

#     with open(FILE_PATH, "w") as F:
        
#         for row in list_of_symbols(path):
#             F.write(f"https://stooq.pl/q/d/l/?s={row.lower()}&i=w\n")

# def download_qoutes():

#     LINKS_PATH = "data/links.txt"
    
#     path = symbols_file_path()

#     with open(LINKS_PATH, "r") as L:
#         for line in L:
#             for row in list_of_symbols(path):
#                 filename = f"data/{row.lower()}.csv"

#                 link = requests.get(line)

#                 try:
#                     link.raise_for_status()
#                 except Exception:
#                     print("Bad link!!!")

#                 quote = open(filename, "wb")
#                 for chunk in link.iter_content(100000):
#                     quote.write(chunk)

#                 quote.close()

"""
    Tworzenie wykresu
"""

# # plt.figure(figsize=[15,10])
# # plt.grid(True)
# # plt.plot(df["Zamkniecie"], label="close")
# # plt.plot(df["MA_30"], label="MA_30")
# # plt.plot(df["EMA_30"], label="EMA_30")
# # plt.legend(loc=2)

# # plt.show()

"""
    Zmiana nazw plików
"""

# path = "data/daily/pl/wse stocks/"

# filenames = os.listdir(path)

# print(filenames)

# for filename in filenames:
#     os.rename(path + filename, path + filename[:-4] + ".csv")

"""
    Odczytywanie pliku z danymi
    Wyliczanie wskaźników
"""

# df = pd.read_csv(filename)
# df = df[["Data", "Zamkniecie"]]

# df = indicators.moving_average(df)
# df = indicators.exponential_moving_average(df)

# print(df)

"""
    Zmiana pliku csv na słownik
"""

# filename = "data/daily/pl/wse stocks/1at.csv"

# with open(filename, "r") as csvfile:
#     datas_dict = []
#     reader = csv.DictReader(csvfile)
#     for line in reader:
#         datas_dict.append(line)

# print(datas_dict)