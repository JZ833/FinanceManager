import krakenex

api = krakenex.API()
asset_pairs = api.query_public('AssetPairs')['result']

# Example: Create a dictionary mapping the common symbol (e.g., BTC) to Kraken's ticker symbol (e.g., XBTUSD)
ticker_dict = {}
for pair, data in asset_pairs.items():
    # data['altname'] often gives a cleaner ticker symbol
    ticker = data['altname']
    # You might need to process the ticker to extract the base asset (e.g., "BTC" from "XBTUSD")
    # This step may involve mapping Kraken's naming conventions (like "XBT" to "BTC")
    # For example:
    if ticker.startswith('XBT'):
        base_asset = 'BTC'
    else:
        base_asset = ticker[:-3]  # a simple heuristic if the pair ends with a 3-letter quote currency
    ticker_dict[base_asset] = ticker

print(ticker_dict)

count = 0

for ticker in ticker_dict:
    count = count + 1
    #print(ticker)

print(f"Number of crypto tickers avalible: {count}\n")
