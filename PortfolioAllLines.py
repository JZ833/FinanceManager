import yfinance as yf
import pymysql.cursors
import datetime as dt
import pandas as pd
import plotly.graph_objects as go

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='TeamLlama',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

user_id = 1
EndDate = dt.datetime.now()

symbolList = []
stock_data = {}  

def getData(Name, StartDate):
    # Download historical data for the symbol
    df = yf.download(Name, start=StartDate, end=EndDate)
    return df

def calculate_profit_percentage(df):
    # Ensure the DataFrame is not empty and has the 'Close' column
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    if 'Close' not in df.columns:
        raise ValueError("The DataFrame does not contain a 'Close' column.")

    # Get the close price on the start date
    start_close = df['Close'].iloc[0]

    # Calculate profit percentage
    df['Profit_Percentage'] = ((df['Close'] - start_close) / start_close) * 100

    # Return the DataFrame with Date and Profit_Percentage columns
    dfProfit = df.reset_index()[['Date', 'Profit_Percentage']]

    return dfProfit

def CalculatePercent():
    FetchTickers = """
        SELECT `Symbol`, `TotalInvestment`, `FirstBuyDate`
        FROM `userportfolio`
        WHERE `UserId` = %s
        ORDER BY `FirstBuyDate` ASC
        LIMIT 1000;
    """

    with connection.cursor() as cursor:
        # Fetch Variables
        cursor.execute(FetchTickers, (user_id,))
        result = cursor.fetchall()

        # Check if stocks are in the user database
        if not result:
            print("No stocks found in the database.")
            return

        for row in result:
            symbol = row['Symbol'].strip()
            print(f"Fetching data for symbol: {symbol}")
            symbolList.append(symbol)
            
            # Get the start date for the stock
            StartDate = row['FirstBuyDate']

            # Fetch the data for the stock
            data = getData(symbol, StartDate)

            # Calculate profit percentages using the calculate_profit_percentage function
            dfProfit = calculate_profit_percentage(data)

            # Store dfProfit for this symbol in the stock_data dictionary
            stock_data[symbol] = dfProfit


def Plot():
    # Initialize a Plotly figure
    fig = go.Figure()

    for symbol in symbolList:
        # Use the dfProfit stored in stock_data for each symbol
        dfProfit = stock_data.get(symbol)  

        if dfProfit is not None:
            # Plot the profit percentage over time for the current symbol
            fig.add_trace(
                go.Scatter(
                    x=dfProfit['Date'],
                    y=dfProfit['Profit_Percentage'],
                    mode='lines',
                    name=symbol
                )
            )

    fig.update_layout(
        title=f"Portfolio: Profit Percentage Over Time",
        xaxis_title="Date",
        yaxis_title="Profit Percentage (%)",
        legend_title="Stock Symbols",
        template="plotly_dark",  
        font=dict(
            size=14
        ),
        autosize=True,
        width=1000,
        height=600
    )

    # Show the plot
    fig.show()

# Call the functions
CalculatePercent()
Plot()
