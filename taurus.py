# Imports

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
ZIP_UNPACK_PATH = "data/daily/pl/wse stocks/"

def download_datas():

    link = requests.get(DOWNLOAD_PATH)

    try:
        link.raise_for_status()
    except Exception:
        print("Datas not downloded!!!")
        
    with open(ARCHIVE_PATH, "wb") as TP:
        for chunk in link.iter_content(100000):
            TP.write(chunk)

def unpack_datas():

    packed_datas = zipfile.ZipFile(ARCHIVE_PATH)

    for file in packed_datas.namelist():
        if file.startswith(ZIP_UNPACK_PATH):
            packed_datas.extract(file)