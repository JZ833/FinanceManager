import yfinance as yf
import pandas as pd




# Stock price fetching function (current price)
def get_stock_price(symbol: str) -> float:
    ticker = yf.Ticker(symbol)
    price_attrs = ['regularMarketPrice', 'currentPrice', 'price']
    
    for attr in price_attrs:
        if ticker.info.get(attr) is not None:
            return ticker.info.get(attr)
            
    fast_info = ticker.fast_info
    if hasattr(fast_info, 'last_price') and fast_info.last_price is not None:
        return fast_info.last_price
        
    raise Exception(f"Could not find valid price data for {symbol}")

