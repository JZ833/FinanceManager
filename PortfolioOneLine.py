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
stock_data = {}        # To hold each stock's profit percentage DataFrame
stock_investment = {}  # To hold each stock's TotalInvestment

def getData(symbol, StartDate):
    # Download historical data for the symbol
    df = yf.download(symbol, start=StartDate, end=EndDate)
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
    # Fetch the portfolio stocks along with their investment and first buy date
    FetchTickers = """
        SELECT `Symbol`, `TotalInvestment`, `FirstBuyDate`
        FROM `userportfolio`
        WHERE `UserId` = %s
        ORDER BY `FirstBuyDate` ASC
        LIMIT 1000;
    """

    with connection.cursor() as cursor:
        cursor.execute(FetchTickers, (user_id,))
        result = cursor.fetchall()

        if not result:
            print("No stocks found in the database.")
            return

        for row in result:
            symbol = row['Symbol'].strip()
            investment = row['TotalInvestment']
            first_buy_date = row['FirstBuyDate']
            print(f"Fetching data for symbol: {symbol}")

            symbolList.append(symbol)
            stock_investment[symbol] = investment

            # Fetch the historical data starting at the first buy date
            data = getData(symbol, first_buy_date)
            # Calculate profit percentages for this stock
            dfProfit = calculate_profit_percentage(data)
            stock_data[symbol] = dfProfit

def CalculatePortfolioProfit():
    # Build a master date range from the earliest purchase date among all stocks to today
    earliest_dates = [df['Date'].min() for df in stock_data.values()]
    master_start_date = min(earliest_dates)
    master_dates = pd.date_range(start=master_start_date, end=EndDate)

    # Initialize Series to hold the cumulative value and cumulative initial investment per day
    total_values = pd.Series(0, index=master_dates)
    total_investment = pd.Series(0, index=master_dates)

    for symbol in symbolList:
        dfProfit = stock_data[symbol].copy()
        investment = stock_investment[symbol]

        # Compute the Value series for the stock:
        # Value = investment * (1 + Profit_Percentage/100)
        dfProfit['Value'] = investment * (1 + dfProfit['Profit_Percentage'] / 100)
        dfProfit.set_index('Date', inplace=True)
        dfProfit = dfProfit.sort_index()

        # Reindex to master_dates, forward fill the Value for dates after the first buy date
        dfValue = dfProfit['Value'].reindex(master_dates, method='ffill')

        # For dates before the stock was acquired, set the value to 0.
        first_date = dfProfit.index.min()
        dfValue[dfValue.index < first_date] = 0

        # Build an investment Series: from first_date onward, the initial investment counts; before that, it's 0.
        inv_series = pd.Series(0.0, index=master_dates)
        inv_series[inv_series.index >= first_date] = investment

        # Add to the cumulative totals
        total_values += dfValue
        total_investment += inv_series

    # Compute portfolio profit percentage:
    # (total portfolio value / total invested capital - 1) * 100
    portfolio_profit_percentage = (total_values / total_investment - 1) * 100
    # For days with no investment yet (total_investment == 0), set profit percentage to 0
    portfolio_profit_percentage[total_investment == 0] = 0

    portfolio_df = pd.DataFrame({
        'Date': master_dates,
        'Portfolio_Profit_Percentage': portfolio_profit_percentage
    })

    return portfolio_df

def PlotPortfolio():
    portfolio_df = CalculatePortfolioProfit()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=portfolio_df['Date'],
            y=portfolio_df['Portfolio_Profit_Percentage'],
            mode='lines',
            name='Portfolio Profit'
        )
    )

    fig.update_layout(
        title="Portfolio: Profit Percentage Over Time",
        xaxis_title="Date",
        yaxis_title="Profit Percentage (%)",
        template="plotly_dark",
        font=dict(size=14),
        autosize=True,
        width=1000,
        height=600
    )
    fig.show()

# Execute the functions in order
CalculatePercent()
PlotPortfolio()
