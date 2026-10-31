import os
import json
import datetime
import requests
from bs4 import BeautifulSoup
import yfinance as yf

def fetch_commodities():
    tickers = {
        "silver_usd_oz": "SI=F",
        "copper_usd_lb": "HG=F",
        "aluminum_usd_mt": "ALI=F",
        "usd_inr": "USDINR=X"
    }
    data = {}
    for key, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            if not hist.empty:
                data[key] = round(float(hist['Close'].iloc[-1]), 2)
        except Exception as e:
            print(f"Failed to fetch {symbol}: {e}")
            data[key] = None
    return data

def main():
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    output = {
        "timestamp": today,
        "commodities": fetch_commodities(),
        "status": "success"
    }
    
    os.makedirs('data', exist_ok=True)
    file_path = f'data/latest_prices.json'
    with open(file_path, 'w') as f:
        json.dump(output, f, indent=2)
        
    print(f"Data collection complete. Output saved to {file_path}")

if __name__ == "__main__":
    main()
