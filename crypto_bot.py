import requests
import pyodbc
import time
from datetime import datetime

# --- CONFIGURATION ---
# This matches the "localhost" setup in SSMS
DB_CONFIG = {
    'server': 'localhost',
    'database': 'MarketWatch',
    'driver': '{ODBC Driver 17 for SQL Server}'
}

def fetch_crypto_data():
    # 1. EXTRACT: Go to CoinGecko and get live prices
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_market_cap=true"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None

def load_to_sql(data):
    if not data: return

    # 2. LOAD: Connect to the "MarketWatch" database
    conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};Trusted_Connection=yes;"

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        for coin, stats in data.items():
            symbol = coin.upper()
            price = stats['usd']
            cap = stats['usd_market_cap']

            # The SQL Command to insert the row
            query = "INSERT INTO CryptoPrices (Symbol, PriceUSD, MarketCap) VALUES (?, ?, ?)"
            cursor.execute(query, (symbol, price, cap))

        conn.commit()
        print(f"✅ Success! Saved {symbol} at ${price} - {datetime.now()}")
        conn.close()
    except Exception as e:
        print(f"❌ Database Error: {e}")
        print("TIP: If the error mentions the 'Driver', try changing 17 to 18 or 13 in the code.")

# 3. AUTOMATION: Run this loop forever
if __name__ == "__main__":
    print("🚀 Bot started... Press Ctrl+C to stop.")
    while True:
        market_data = fetch_crypto_data()
        load_to_sql(market_data)
        time.sleep(60) # Wait 60 seconds before next check