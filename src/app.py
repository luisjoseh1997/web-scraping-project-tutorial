import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#Descargar HTML con BeautifulSoup

url="https://en.wikipedia.org/wiki/List_of_Spotify_streaming_records"
headers={
   "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

response=requests.get(url, time.sleep(10), headers=headers)

#Transformar el HTML

if response:
    soup=BeautifulSoup(response.text, 'html')

tablas = soup.find_all("table", class_="wikitable sortable plainrowheaders")

filas = tablas[0].find_all('tr')
data = []

for fila in filas:
    celdas = fila.find_all(['th', 'td'])
    celdas_clean = []
    for c in celdas:
        celdas_clean.append(c.text.strip())
    data.append(celdas_clean)

#creamos y limpiamos el DataFrame
df = pd.DataFrame(data[1:], columns = data[0])
df = df.drop(100)
df["Streams(billions)"] = pd.to_numeric(df["Streams(billions)"])
df["Rank"] = pd.to_numeric(df["Rank"])

#Almacenando los datos en sqlite
con = sqlite3.connect("webscraping.db")

df.to_sql('tabla', con, if_exists='replace', index=False)
con.commit()