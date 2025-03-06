import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import yfinance as yf
from fredapi import Fred

FredKey = "db3bf9c729b0ac45151b940bcfb1179c"
fred = Fred(api_key=FredKey)

style.use('ggplot')

# Define the start and end dates
start = dt.datetime(1990, 1, 1)
end = dt.datetime.now()

def get_gold_data():
    # Download historical data for gold
    dfGold = yf.download("GC=F", start=start, end=end)
    dfGold.to_csv("GC=F.csv")
    return dfGold

def calculate_profit_percentage(dfGold):
    # Ensure the DataFrame has the 'Close' column
    if 'Close' not in dfGold.columns:
        raise ValueError("The DataFrame does not contain a 'Close' column.")

    # Get the close price on the start date
    start_close = dfGold['Close'].iloc[0]

    # Calculate profit percentage
    dfGold['Profit_Percentage'] = ((dfGold['Close'] - start_close) / start_close) * 100

    # Create a new DataFrame with date and profit percentage
    dfProfit = dfGold.reset_index()[['Date', 'Profit_Percentage']]

    return dfProfit

def plot_profit_percentage(dfProfit):
    # Plot the profit percentage over time
    plt.figure(figsize=(10, 6))
    plt.plot(dfProfit['Date'], dfProfit['Profit_Percentage'], label='Profit %', color='gold')
    plt.title("Gold Price Profit Percentage Over Time")
    plt.xlabel("Date")
    plt.ylabel("Profit Percentage (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

df = get_gold_data()
df2 = calculate_profit_percentage(df)
plot_profit_percentage(df2)

