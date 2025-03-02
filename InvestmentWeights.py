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

def CalculateWeights():
    FetchTickers = """
        SELECT `Symbol`, `TotalInvestment` FROM `userportfolio`
        WHERE `UserId` = %s
    """

    TotalInvestmentSQL = """
        SELECT SUM(`TotalInvestment`) FROM `userportfolio`
        WHERE `UserId` = %s

    """
    


    with connection.cursor() as cursor:
        
        cursor.execute(TotalInvestmentSQL, (user_id,) )
        TotalInvestment = cursor.fetchone()["SUM(`TotalInvestment`)"] or 0
        
        cursor.execute(FetchTickers, (user_id,))
        result = cursor.fetchall()

        

        if not result:
            print("No stocks found in the database.")
            return

        for row in result:
            symbol = row['Symbol'].strip()
            print(f"Fetching data for symbol: {symbol}")
            
            Investment = row['TotalInvestment']

            Weight = Investment / TotalInvestment 

            print(f"Symbol: {symbol}\nWeight: {Weight}")

            
            
            
CalculateWeights()
