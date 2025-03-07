import pymysql.cursors
import yfinance as yf
import datetime as dt
import pandas as pd
import plotly.graph_objects as go

# Define the start and end dates
start = dt.datetime(2023, 1, 1)
end = dt.datetime.now()

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='TeamLlama',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

def get_data(symbol):
    # Download historical data for the given symbol
    df = yf.download(symbol, start=start, end=end)
    return df

def calculate_profit_percentage(df):
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    if 'Close' not in df.columns:
        raise ValueError("The DataFrame does not contain a 'Close' column.")

    start_close = df['Close'].iloc[0]
    df['Profit_Percentage'] = ((df['Close'] - start_close) / start_close) * 100
    return df.reset_index()[['Date', 'Profit_Percentage']]

def aggregate_sector_profit(symbols):
    profit_series = []
    
    for symbol in symbols:
        print(f"Processing {symbol}")
        data = get_data(symbol)
        if data.empty:
            print(f"No data for {symbol}")
            continue
        try:
            profit_df = calculate_profit_percentage(data)
            profit_df = profit_df.set_index('Date')
            profit_series.append(profit_df['Profit_Percentage'].rename(symbol))
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
    
    if not profit_series:
        return None
    
    combined = pd.concat(profit_series, axis=1)
    combined['Sector_Avg'] = combined.mean(axis=1)
    combined = combined.reset_index()[['Date', 'Sector_Avg']]
    return combined

def get_sector_symbols(sector):
    # Removed the outer connection context manager to keep the connection open
    with connection.cursor() as cursor:
        sql = "SELECT `Symbol` FROM `allstocks` WHERE `Sector`=%s"
        cursor.execute(sql, (sector,))
        result = cursor.fetchall()
        return [row['Symbol'] for row in result]

def plot_sector_aggregates(sector_data_dict):
    fig = go.Figure()
    
    for sector, df in sector_data_dict.items():
        if df is None or df.empty:
            print(f"No data to plot for {sector}")
            continue
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Sector_Avg'],
            mode='lines',
            name=sector
        ))
    
    fig.update_layout(
        title="Sector Aggregated Profit Percentage Over Time",
        xaxis_title="Date",
        yaxis_title="Profit Percentage (%)",
        legend_title="Sectors",
        template="plotly_dark",
        font=dict(size=14),
        autosize=True,
        width=1000,
        height=600
    )
    
    fig.show()

def main():
    Sectors = ["Healthcare", "Financials", "Technology",
               "Energy", "Industrials", "Communication Services",  
               "Consumer Discretionary", "Materials", "Real Estate",
               "Utilities", "Consumer Staples"]
    
    sector_data = {}
    
    for sector in Sectors:
        print(f"\nProcessing sector: {sector}")
        symbols = get_sector_symbols(sector)
        print(f"Found {len(symbols)} symbols for {sector}")
        
        aggregated = aggregate_sector_profit(symbols)
        if aggregated is not None:
            sector_data[sector] = aggregated
        else:
            print(f"No aggregated data for sector: {sector}")
    
    plot_sector_aggregates(sector_data)
    # Optionally, close the connection after processing
    connection.close()

if __name__ == '__main__':
    main()
