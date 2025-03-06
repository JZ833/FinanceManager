import krakenex

def fetch_kraken_ticker(pair):
    """
    Fetch ticker information for a given pair from Kraken API.
    Args:
        pair (str): The trading pair symbol (e.g., 'XBTUSD' for Bitcoin/USD).
    Returns:
        dict: Readable ticker information including price, volume, etc.
    """
    api = krakenex.API()
    api.load_key(r"C:\Users\Tarv\Desktop\KrakenAPI\KrakenAPI_Keys.txt")  # Adjust path as needed

    try:
        # Query the ticker data
        response = api.query_public('Ticker', {'pair': pair})
        
        # Check for errors
        if response.get("error"):
            print(f"Error from Kraken API: {response['error']}")
            return None
        
        # Extract data for the given pair
        result = response.get("result", {})
        pair_data = list(result.values())[0]  # Extract the first (and only) pair's data
        
        # Make the data more readable
        return {
            "symbol": "BTC/USD",
            "ask_price": float(pair_data["a"][0]),  # Ask price
            "bid_price": float(pair_data["b"][0]),  # Bid price
            "last_trade_price": float(pair_data["c"][0]),  # Last trade price
            "24h_volume": float(pair_data["v"][1])  # Volume over 24 hours
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Main script
if __name__ == "__main__":
    pair = "BTCUSD"  # Kraken uses XBT instead of BTC
    ticker_info = fetch_kraken_ticker(pair)
    
    if ticker_info:
        print("\n=== BTC/USD Ticker Information ===")
        print(f"Symbol: {ticker_info['symbol']}")
        print(f"Ask Price: ${ticker_info['ask_price']:.2f}")
        print(f"Bid Price: ${ticker_info['bid_price']:.2f}")
        print(f"Last Trade Price: ${ticker_info['last_trade_price']:.2f}")
        print(f"24h Volume: {ticker_info['24h_volume']:.6f} BTC")
