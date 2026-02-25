import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from dateutil.utils import today

dnes = datetime.now()
pred_deseti_lety = datetime.now() - timedelta(days=10*365)
# 1. Stažení dat pro S&P 500 (^GSPC)
ticker = "^GSPC"
data = yf.download(ticker, start=pred_deseti_lety, end=dnes)

# 2. Výpočet klouzavých průměrů (SMA - Simple Moving Average)
data['SMA50'] = data['Close'].rolling(window=50).mean()
data['SMA200'] = data['Close'].rolling(window=200).mean()

# 3. Identifikace signálu
# Golden Cross: SMA50 je nad SMA200 AND v předchozím dni byla pod ním
data['Signal'] = 0.0
data.iloc[200:, data.columns.get_loc('Signal')] = \
    (data['SMA50'][200:] > data['SMA200'][200:]).astype(float)

data['Position'] = data['Signal'].diff()

# 1.0 znamená Golden Cross (nákup), -1.0 znamená Death Cross (prodej)
golden_crosses = data[data['Position'] == 1]
death_crosses = data[data['Position'] == -1]

# 4. Výpis výsledků
print("Nalezené Golden Crossy od roku 2000:")
print(golden_crosses.index.strftime('%Y-%m-%d').tolist())

plt.figure(figsize=(16, 8)) # Nastavíme velikost grafu pro lepší čitelnost

# Vykreslení zavírací ceny
plt.plot(data['Close'], label=ticker + ' Zavírací cena', alpha=0.6)

# Vykreslení klouzavých průměrů
plt.plot(data['SMA50'], label='SMA 50', color='orange')
plt.plot(data['SMA200'], label='SMA 200', color='red')

# Vyznačení Golden Crossů
# Použijeme vertikální čáry pro jasné zobrazení
for date in golden_crosses.index:
    plt.axvline(x=date, color='green', linestyle='--', alpha=0.7, label='Golden Cross' if date == golden_crosses.index[0] else "")

# Vyznačení Death Crossů (volitelné, ale dobré pro kontext)
for date in death_crosses.index:
    plt.axvline(x=date, color='purple', linestyle=':', alpha=0.5, label='Death Cross' if date == death_crosses.index[0] else "")


plt.title(f'{ticker} s klouzavými průměry a Golden/Death Crossy')
plt.xlabel('Datum')
plt.ylabel('Cena')
plt.legend() # Zobrazí legendu s popisky
plt.grid(True) # Přidáme mřížku

plt.show() # Zobrazí graf
