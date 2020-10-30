# Imports

import os
import zipfile
import csv

import requests

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import smtplib
import emails

import indicators

# Constants

DOWNLOAD_PATH = "https://static.stooq.pl/db/h/d_pl_txt.zip"
ARCHIVE_PATH = "data/all_data.zip"
QUOTES_PATH = "data/daily/pl/wse stocks/"
DATA_PATH = "data/datafiles/"
POSITION_TO_DELETE = ["<TICKER>", "<PER>", "<TIME>", "<OPEN>", "<HIGH>", "<LOW>", "<VOL>", "<OPENINT>"]

# Functions

def download_datas():
    """Function download data from DOWNLOAD_PATH
    Data comes from website Stooq - https://stooq.pl/
    """
    link = requests.get(DOWNLOAD_PATH)

    try:
        link.raise_for_status()
    except Exception:
        print("Datas not downloded!!!")
        
    with open(ARCHIVE_PATH, "wb") as AP:
        for chunk in link.iter_content(100000):
            AP.write(chunk)

def unpack_datas():
    """Function unzip archive with datas
    """
    packed_datas = zipfile.ZipFile(ARCHIVE_PATH)

    for file in packed_datas.namelist():
       if file.startswith(QUOTES_PATH):
            packed_datas.extract(file)

    os.remove(ARCHIVE_PATH)

def change_extensions():
    """Function change file extensions from txt to csv
    """
    filenames = os.listdir(QUOTES_PATH)

    for filename in filenames:
        os.rename(QUOTES_PATH + filename, QUOTES_PATH + filename[:-4] + ".csv")

def paths_to_file():
    """Function return list of csv files paths with quotation datas

    Returns:
        list: List of csv files paths with quotation datas
    """
    filenames = os.listdir(QUOTES_PATH)
    files_paths = []

    for file in filenames:
        files_paths.append(QUOTES_PATH + file)

    return files_paths

def file_to_dicts_lists(file_path):
    """Function make list of dictionaries with quotes from given file

    Args:
        file_path (str): Path to file with qoutes

    Returns:
        list: List with dictionaries with qoutes
    """
    with open(file_path, "r") as f:
        dicts_list = []
        reader = csv.DictReader(f)

        for line in reader:
            dicts_list.append(line)
    
    return dicts_list

def del_unnecessary_keys(list_of_dicts):
    """Function delete unnecessary keys from dictionaries with quotes

    Args:
        list_of_dicts (list): List with dictionaries with qoutes

    Returns:
        list: Formated list with dictionaries
    """
    for position in list_of_dicts:
        for key in POSITION_TO_DELETE:
            if key in position:
                del position[key]
    
    return list_of_dicts

def change_dicts_dates_format(list_of_dicts):
    """Function change dates format in all dictionaries on list

    Args:
        list_of_dicts (list): List of dictionaries with dates to correct

    Returns:
        list: List of dictionaries with corrected dates format
    """
    for dictionary in list_of_dicts:
        date = dictionary["<DATE>"]
        year = date[:4]
        month = date[4:6]
        day = date[6:]
        date = f"{year}-{month}-{day}"
        dictionary["<DATE>"] = date

    return list_of_dicts

def back_to_file(file_path, list_of_dicts):
    """Function create new datafiles which program will use later

    Args:
        file_path (string): Path to downloaded file with quotes
        list_of_dicts (list): List of dictionaries with qoutes
    """
    filename = DATA_PATH + file_path[-7:]

    keys = list_of_dicts[0].keys()

    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(list_of_dicts)

def csv_to_df(filename):
    """Function create pandas.DataFrame from giving csv file

    Args:
        filename (string): Path to csv file with quotes

    Returns:
        pandas.DataFrame: pandas.DataFrame from giving csv file
    """
    df = pd.read_csv(filename)
    df["<DATE>"] = pd.to_datetime(df["<DATE>"])
    df.set_index("<DATE>", inplace=True)
    df["<CLOSE>"] = df["<CLOSE>"].round(2)
    df = df.resample("W").last()

    return df

def main():

    """Data download"""

    # download_datas()
    # unpack_datas()
    # change_extensions()

    """Data format"""

    # for path in paths_to_file():
        # ftdl = file_to_dicts_lists(path)
        # duk = del_unnecessary_keys(ftdl)
        # cddf = change_dicts_dates_format(duk)
        # back_to_file(path, cddf)

    """Pandas DataFrame"""

    # filename = DATA_PATH + "cdr.csv"
    # df = csv_to_df(filename)
    # df = indicators.moving_average(df)
    # df = indicators.exponential_moving_average(df)
    # df = indicators.rsi(df)
    # df = indicators.tsi(df)

if __name__ == "__main__":
    main()