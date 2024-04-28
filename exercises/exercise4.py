#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import os
import zipfile
import urllib.request


#download and unzip data

url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
path = "./mowesta-dataset-20221107.zip"
urllib.request.urlretrieve(url, path)

# Extracting CSV file from provided zip
with zipfile.ZipFile(path, 'r') as zip_ref:
    zip_ref.extractall('./')

# Delete the zip file and readme file
os.remove('./mowesta-dataset-20221107.zip')
os.remove('./README.pdf')


#reshaping data

#use columns  "Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", Batterietemperatur in °C", "Geraet aktiv"
df = pd.read_csv("./data.csv", delimiter=";", decimal=",", index_col=False,
                 usecols=["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"])

# Rename  "Temperatur in °C (DWD)" to "Temperatur" and Renaming "Batterietemperatur in °C" to "Batterietemperatur"
df = df.rename(columns={"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C": "Batterietemperatur"})

# transform data

# Transform temperatures in Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32
# converting celcius to Fahrenheit for  Temperatur and Batterietemperatur
df["Temperatur"] = celsius_to_fahrenheit(df["Temperatur"])
df["Batterietemperatur"] = celsius_to_fahrenheit(df["Batterietemperatur"])

# validate data


# Use validations as you see fit, e.g., for “Geraet” to be an id over 0
# Use fitting SQLite types (e.g., BIGINT, TEXT or FLOAT) for all columns


column_types = {
    'Geraet': int,
    'Hersteller': str,
    'Model': str,
    'Monat': int,
    'Temperatur': float,
    'Batterietemperatur': float,
    'Geraet aktiv': str
}
df = df.astype(column_types)

# Writing data into a SQLite database called “temperatures.sqlite”, in the table “temperatures”
df.to_sql('temperatures', 'sqlite:///temperatures.sqlite', if_exists='replace', index=False)
#Delete the CSV file
os.remove('./data.csv')

print ("test successful")
