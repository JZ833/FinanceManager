import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# Define the start and end dates
start = dt.datetime(1990, 1, 1)
end = dt.datetime.now()

# Define the commodity names and their corresponding ticker symbols
commodities = {
    'Palladium': 'PA=F',
    'Platinum': 'PL=F',
    'Gold': 'GC=F',
    'Silver': 'SI=F',
    'Copper': 'HG=F',
    'Oil': 'CL=F',
    'Gas': 'RB=F',
    'Natural Gas': 'NG=F',
    'Coffee': 'KC=F',
    'Lean Hogs': 'HE=F',
    'Corn': 'ZC=F'
}

def get_commodity_data():
    """
    Downloads historical data for each commodity.
    Returns a dictionary mapping the commodity name to its DataFrame.
    """
    data_dict = {}
    for name, ticker in commodities.items():
        print(f"Downloading data for {name}...")
        df = yf.download(ticker, start=start, end=end)
        data_dict[name] = df
    return data_dict

def calculate_profit_percentage(df):
    """
    Calculates the profit percentage for a given DataFrame that has a 'Close' column.
    The profit percentage is computed relative to the first available closing price.
    Returns a DataFrame with 'Date' and 'Profit_Percentage' columns.
    """
    if 'Close' not in df.columns:
        raise ValueError("The DataFrame does not contain a 'Close' column.")
    start_close = df['Close'].iloc[0]
    df['Profit_Percentage'] = ((df['Close'] - start_close) / start_close) * 100
    df_profit = df.reset_index()[['Date', 'Profit_Percentage']]
    return df_profit

def plot_profit_percentages(commodity_profit_dict):
    """
    Plots the profit percentages for all commodities using Plotly.
    Each commodity's profit percentage is plotted as a separate line.
    """
    fig = go.Figure()
    
    for commodity, df_profit in commodity_profit_dict.items():
        fig.add_trace(
            go.Scatter(
                x=df_profit['Date'],
                y=df_profit['Profit_Percentage'],
                mode='lines',
                name=commodity
            )
        )
        
    fig.update_layout(
        title="Commodity Price Profit Percentage Over Time",
        xaxis_title="Date",
        yaxis_title="Profit Percentage (%)",
        template="plotly_dark",
        width=1200,
        height=700
    )
    
    fig.show()

def main():
    # Download data for all commodities
    data_dict = get_commodity_data()
    
    # Calculate profit percentages for each commodity
    profit_dict = {}
    for commodity, df in data_dict.items():
        if df.empty:
            print(f"No data for {commodity}, skipping...")
            continue
        profit_dict[commodity] = calculate_profit_percentage(df)
    
    # Plot all the profit percentage lines
    plot_profit_percentages(profit_dict)

if __name__ == "__main__":
    main()
