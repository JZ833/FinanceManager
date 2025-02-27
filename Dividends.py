#sql libs
import pymysql.cursors
import datetime as dt

#API lib
import yfinance as yf
import pandas as pd




# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='TeamLlamas',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)


def Dividends():
    FetchTickers = """
        SELECT `Stock`, `FirstBuyDate`, `Quantity` FROM `portfoliodata`
    """

    UpdateDividends = """
        UPDATE `portfoliodata`
        SET `TotalDividend` = %s
        WHERE `Stock` = %s
    """
    
    with connection.cursor() as cursor:

        cursor.execute(FetchTickers)
        result = cursor.fetchall()

        for row in result:
            Stock = row['Stock'].strip()
            StartDate = row['FirstBuyDate']
            Quantity = row['Quantity'] 

            #print(StartDate)
            total_dividends = 0.0 

            CallYF = yf.Ticker(Stock)
            try:
                hist = CallYF.history(start=StartDate)
                
                # Filter the data to include only dividend payments
                if 'Dividends' in hist.columns and not hist['Dividends'].empty:
                    total_dividends = hist['Dividends'].sum()
                    
                else:
                    total_dividends = 0.0  # No dividend data available
            except Exception as e:
                print(f"Error fetching dividend history for {Stock}: {e}")

            total_dividends = total_dividends * Quantity

            cursor.execute(UpdateDividends, (total_dividends, Stock))
            print(f"{Stock}: Dividends Updated in SQL") 

        connection.commit()
