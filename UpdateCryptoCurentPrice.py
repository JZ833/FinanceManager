import pymysql.cursors
import krakenex
from Names import ticker_dict  # Import the mapping dictionary from your Names.py

def get_kraken_symbol(traditional_symbol):
    """
    Converts a traditional symbol (e.g., 'BTCUSD') into Kraken's symbol using ticker_dict.
    If the symbol ends with 'USD', it extracts the base asset (e.g., 'BTC') and looks up the Kraken symbol.
    Returns the Kraken symbol (e.g., 'XBTUSD') or None if no mapping is found.
    """
    if traditional_symbol.endswith("USD"):
        base_asset = traditional_symbol[:-3]  # Remove the 'USD' suffix
    else:
        base_asset = traditional_symbol
    kraken_symbol = ticker_dict.get(base_asset)
    if kraken_symbol is None:
        print(f"No Kraken symbol found for base asset: {base_asset}")
    return kraken_symbol

def fetch_kraken_ticker(kraken_symbol):
    """
    Uses krakenex to query the Kraken API for ticker data.
    Args:
        kraken_symbol (str): The Kraken symbol for the crypto (e.g., "XBTUSD").
    Returns:
        dict or None: A dictionary containing ticker data if successful,
                      or None if an error occurred or data is missing.
    """
    api = krakenex.API()
    # Make sure the API key file path is correct for your system.
    api.load_key(r"C:\Users\Tarv\Desktop\KrakenAPI\KrakenAPI_Keys.txt")
    
    try:
        response = api.query_public('Ticker', {'pair': kraken_symbol})
        if response.get("error"):
            print(f"Kraken API error for {kraken_symbol}: {response['error']}")
            return None
        
        result = response.get("result", {})
        if not result:
            print(f"No result returned from Kraken for {kraken_symbol}")
            return None
        
        # The result is a dictionary where the first key holds the pair data.
        pair_data = list(result.values())[0]
        return {
            "last_trade_price": float(pair_data["c"][0]),
            "ask_price": float(pair_data["a"][0]),
            "bid_price": float(pair_data["b"][0]),
            "volume_24h": float(pair_data["v"][1])
        }
    except Exception as e:
        print(f"Exception fetching ticker for {kraken_symbol}: {e}")
        return None

# Database connection parameters—adjust as necessary.
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='TeamLlama',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

user_id = 1

def update_crypto_price():
    fetch_symbols_query = """
        SELECT `Symbol` FROM `cryptoportfolio`
        WHERE `UserId` = %s
    """
    
    update_price_query = """
        UPDATE `cryptoportfolio`
        SET `CurrentPrice` = %s
        WHERE `Symbol` = %s AND `UserId` = %s
    """
    
    with connection.cursor() as cursor:
        cursor.execute(fetch_symbols_query, (user_id,))
        rows = cursor.fetchall()

        if not rows:
            print("No crypto symbols found in the database.")
            return

        for row in rows:
            traditional_symbol = row['Symbol'].strip()
            print(f"Processing symbol: {traditional_symbol}")
            
            # Map the traditional symbol to Kraken's symbol using the imported ticker_dict.
            kraken_symbol = get_kraken_symbol(traditional_symbol)
            if not kraken_symbol:
                print(f"No Kraken mapping found for {traditional_symbol}. Skipping update.")
                continue

            # Fetch ticker data using the Kraken symbol.
            ticker_info = fetch_kraken_ticker(kraken_symbol)
            if ticker_info is None:
                print(f"Krakenex did not return data for {traditional_symbol} (mapped as {kraken_symbol}).")
                continue

            # Use the last trade price as the current price.
            current_price = ticker_info.get("last_trade_price")
            print(f"Fetched price for {traditional_symbol} ({kraken_symbol}): {current_price}")

            try:
                cursor.execute(update_price_query, (current_price, traditional_symbol, user_id))
            except Exception as e:
                print(f"Error updating price for {traditional_symbol}: {e}")

        # Commit all updates to the database.
        connection.commit()

if __name__ == "__main__":
    update_crypto_price()
