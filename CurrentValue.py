import pymysql.cursors
import datetime as dt

#
import yfinance as yf
import pandas as pd

import CurrentPrice as CP 


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

def CurrentValue():
    FetchTickers = """
        SELECT `Symbol`, `Quantity` FROM `userportfolio`
        WHERE `UserId` = %s
    """

    UpdateCurrentValue = """
        UPDATE `userportfolio`
        SET `CurrentValue` = %s
        WHERE `Symbol` = %s AND `UserId` = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(FetchTickers, (user_id,))
        result = cursor.fetchall()

        if not result:
            print("No stocks found in the database.")
            return

        for row in result:
            symbol = row['Symbol'].strip()
            print(f"Fetching data for symbol: {symbol}")
            quantity = row['Quantity']

            try:
                # Fetch the current price
                Price = CP.get_stock_price(symbol)
                print(f"Price for {symbol}: {Price}")

                Price = round(Price * quantity, 2)

                # Update the database
                cursor.execute(UpdateCurrentValue, (Price, symbol, user_id))
            except Exception as e:
                print(f"Error fetching price for {symbol}: {e}")

        # Commit the changes
        connection.commit()
        

CurrentValue()




    
