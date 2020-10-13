# Imports

import os
import zipfile
import csv

import requests

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import indicators

# Constants

DOWNLOAD_PATH = "https://static.stooq.pl/db/h/d_pl_txt.zip"
ARCHIVE_PATH = "data/all_data.zip"
QUOTES_PATH = "data/daily/pl/wse stocks/"
POSITION_TO_DELETE = ["<PER>", "<TIME>", "<OPEN>", "<HIGH>", "<LOW>", "<OPENINT>"]

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

def change_extension():
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

def file_to_dict(file_path):
    """Function make list of dictionaries wiht quotes from given file

    Args:
        file_path (str): Path to file with qoutes

    Returns:
        list: List with dictionaries with qoutes
    """
    with open(file_path, "r") as f:
        quotes_dict = []
        reader = csv.DictReader(f)

        for line in reader:
            quotes_dict.append(line)
    
    return quotes_dict

# path = paths_to_file()[5]
# dicts_list = file_to_dict(path)
# filename = "output.txt"

# for position in dicts_list:
#     del position["<PER>"]
#     del position["<TIME>"]
#     del position["<OPEN>"]
#     del position["<HIGH>"]
#     del position["<LOW>"]
#     del position["<OPENINT>"]

# with open(filename, "w") as f:
#     print(dicts_list, file=f)