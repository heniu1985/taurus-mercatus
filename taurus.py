import csv

import requests

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

def symbols_file_path():
    """Function download file with instruments symbol

    Returns:
        FILE_PATH: Path to file with instruments symbol
    """
    stooq_symbols = "data/stooq_symbols.csv"  # Path to CSV file with instruments symbol
    symbols_url_path = "https://stooq.pl/db/l/?g=6"

    symbols = requests.get(symbols_url_path)

    try:
        symbols.raise_for_status()
    except Exception:
        print("Wrong path!!!")

    symbols_file = open(stooq_symbols, "wb")
    
    for fragment in symbols.iter_content(100000):
        symbols_file.write(fragment)
    
    symbols_file.close()

    return stooq_symbols

def list_of_symbols(file_path):
    """Function make list with short instruments symbols

    Args:
        file_path (FILE_PATH): Path of file with instruments symbols

    Returns:
        list: List with short instruments symbols
    """
    symbols_list = []

    with open(symbols_file_path()) as s:
        reader = csv.reader(s)

        for row in reader:
            symbols_list.append(row[0][:3])
    
    symbols_list.remove("<TI")
    symbols_list = set(symbols_list)

    return symbols_list