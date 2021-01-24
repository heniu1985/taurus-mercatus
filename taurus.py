# Imports

import os
import shutil
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
POSITION_TO_DELETE = ["<TICKER>", "<PER>", "<TIME>", "<VOL>", "<OPENINT>"]

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

def check_files():

    filenames = os.listdir(QUOTES_PATH)

    for filename in filenames:
        if len(filename) != 7:
            os.remove(QUOTES_PATH + filename)
            print(filename + " DELETED")

def move_files():

    filenames = os.listdir(QUOTES_PATH)

    for filename in filenames:
        os.rename(QUOTES_PATH + filename, DATA_PATH + filename)
    
    shutil.rmtree("data/daily")

def change_extensions():
    """Function change file extensions from txt to csv
    """
    filenames = os.listdir(DATA_PATH)

    for filename in filenames:
        if filename.endswith("txt"):
            os.rename(DATA_PATH + filename, DATA_PATH + filename[:-3] + "csv")
        else:
            os.remove(DATA_PATH + filename)
            print(filename + " DELETED")

def paths_to_file():
    """Function return list of csv files paths with quotation datas

    Returns:
        list: List of csv files paths with quotation datas
    """
    filenames = os.listdir(DATA_PATH)
    files_paths = []

    for filename in filenames:
        files_paths.append(DATA_PATH + filename)

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
    df["<CLOSE>"] = df["<CLOSE>"]
    df = df.resample("W").last()

    return df

def buy_signal(df):
    """Function calculates signal to open long position

    Args:
        df (pandas.DataFrame): pandas.DataFrame

    Returns:
        string: return "Buy" if condition is met else False
    """
    tsi = df["TSI"]
    tsi_ma = df["TSI_MA"]
    signal = ""

    if ((tsi[-2] < 0 and tsi_ma[-1] < 0) and (tsi[-1] > tsi_ma[-1] and tsi[-2] < tsi_ma[-2])) or (tsi[-1] > 0 and tsi[-2] < 0):
        signal = "Buy"
    else:
        signal = False

    return signal

def sell_signal(df):
    """Function calculates signal to open short position

    Args:
        df (pandas.DataFrame): pandas.DataFrame

    Returns:
        string: return "Sell" if condition is met else False
    """
    tsi = df["TSI"]
    tsi_ma = df["TSI_MA"]
    signal = ""

    if (tsi[-1] > 0 and tsi_ma[-1] > 0) and (tsi[-1] < tsi_ma[-1] and tsi[-2] > tsi_ma[-2]):
        signal = "Sell"
    else:
        signal = False

    return signal

def close_long_position(df):
    """Function calculates signal to close long position

    Returns:
        string: return "Close long position" if condition is met else False
    """
    close_price = df["<CLOSE>"]
    ma = df["MA"]
    clp = ""

    if close_price[-1] < ma[-1] and close_price[-2] > ma[-2]:
        clp = "Close long position"
    else:
        clp = False

    return clp

def close_short_position(df):
    """Function calculates signal to close short position

    Returns:
        string: return "Close short position" if condition is met else False
    """
    close_price = df["<CLOSE>"]
    ma = df["MA"]
    csp = ""

    if close_price[-1] > ma[-1] and close_price[-2] < ma[-2]:
        csp = "Close short position"
    else:
        csp = False

    return csp

def count_signals():
    """Function counts transaction signals

    Returns:
        list: list of dictionaries with signals
        1. Dictionary for buy signals
        2. Dictionary for sell signals
        3. Dictionary for close long position
        4. Dictionary for close short position
    """
    filenames = os.listdir(DATA_PATH)
    signals = []
    buy = {}
    sell = {}
    close_long = {}
    close_short = {}

    for filename in filenames:
        f = DATA_PATH + filename
        df = csv_to_df(f)
        df = indicators.moving_average(df)
        df = indicators.exponential_moving_average(df)
        df = indicators.rsi(df)
        df = indicators.tsi(df)
        df = indicators.tsi_moving_average(df)
        b = buy_signal(df)
        s = sell_signal(df)        
        cl = close_long_position(df)
        cs = close_short_position(df)
        if b == "Buy":
            buy[filename[:3]] = b
        else:
            pass

        if s == "Sell":
            sell[filename[:3]] = s
        else:
            pass

        if cl == "Close long position":
            close_long[filename[:3]] = cl
        else:
            pass
        
        if cs == "Close short position":
            close_short[filename[:3]] = cs
        else:
            pass
    
    signals.append(buy)
    signals.append(sell)
    signals.append(close_long)
    signals.append(close_short)

    return signals

def send_buy_signals_email():
    """Function send "BUY" signals
    """
    buy_dict = count_signals()[0]
    signal = "BUY"
    
    if len(buy_dict) == 0:
        emails.no_signals(signal)
    else:
        emails.buy_signals(buy_dict)

def send_sell_signals_email():
    """Function send "SELL" signals
    """
    sell_dict = count_signals()[1]
    signal = "SELL"
    
    if len(sell_dict) == 0:
        emails.no_signals(signal)
    else:
        emails.sell_signals(sell_dict)

def send_close_long_signals_email():
    """Function send close long posiotion signals
    """
    close_long_dict = count_signals()[2]
    signal = "CLOSE LONG POSITION"
    
    if len(close_long_dict) == 0:
        emails.no_signals(signal)
    else:
        emails.close_long_signals(close_long_dict)

def send_close_short_signals_email():
    """Function send close short position signals
    """
    close_short_dict = count_signals()[3]
    signal = "CLOSE SHORT POSITION"
    
    if len(close_short_dict) == 0:
        emails.no_signals(signal)
    else:
        emails.close_short_signals(close_short_dict)

def main():

    """Data download"""

    try:

        download_datas()
        unpack_datas()
        check_files()
        move_files()
        change_extensions()
    
        emails.files_downloaded()
    except:
        emails.download_error()

    """Data format"""

    for path in paths_to_file():
        ftdl = file_to_dicts_lists(path)
        duk = del_unnecessary_keys(ftdl)
        cddf = change_dicts_dates_format(duk)
        back_to_file(path, cddf)

    """Signal counting and mailing"""

    l = count_signals()
    send_buy_signals_email()
    send_sell_signals_email()
    send_close_long_signals_email()
    send_close_short_signals_email()
    print(l)

if __name__ == "__main__":
    main()