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
    database='TeamLlama',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

user_id = 1

def Dividends():
    FetchTickers = """
        SELECT `Symbol`, `FirstBuyDate`, `Quantity` 
        FROM `userportfolio`
        WHERE `UserId` = %s
    """

    UpdateDividends = """
        UPDATE `userportfolio`
        SET `DividendsReceived` = %s
        WHERE `Symbol` = %s AND `UserId` = %s
    """
    
    with connection.cursor() as cursor:

        cursor.execute(FetchTickers, (user_id,))
        result = cursor.fetchall()

        for row in result:
            Stock = row['Symbol'].strip()
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

            cursor.execute(UpdateDividends, (total_dividends, Stock, user_id))
            print(f"{Stock}: Dividends Updated in SQL") 

        connection.commit()

Dividends()
