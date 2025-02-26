import pandas as pd
import os
import yfinance as yf
from openpyxl import Workbook
import pymysql.cursors

import InsertDbValues as DB


#Create function for downloading and selecting excel file from user  
FILE_PATH = r"C:\Users\Tarv\Desktop\Data\PortfolioData.xlsx"

# Read the Excel file with error handling for missing columns
try:
    df = pd.read_excel(FILE_PATH, parse_dates=["FirstBuyDate"], engine="openpyxl")
except ValueError:
    df = pd.read_excel(FILE_PATH, engine="openpyxl")
    if "FirstBuyDate" not in df.columns:
        df["FirstBuyDate"] = pd.NaT




def extract_data():
    """Extract the Stock and Quantity columns as arrays and print them."""
    # Normalize the "Stock" column
    df["Stock"] = df["Stock"].astype(str).str.strip().str.upper()
    
    stock_data = df["Stock"].to_numpy()
    quantity_data = df["Quantity"].to_numpy()
    first_buy_date = df["FirstBuyDate"]
    total_investment = df["TotalInvestment"].to_numpy()
    i = 0 #iterator
    FixedDate = []
    
    # Print stock quantity and date line by line
    print("\nStock Data:\n\nSymbol\tQuantity\tFirst Buy Date\n")

    
    for stock, quantity, date, investment in zip(stock_data, quantity_data, first_buy_date, total_investment):
        #fix date for sql 
        FixedDate.append(date.strftime("%Y-%m-%d"))
        
        #print values from excel
        print(f"{stock}:\t{quantity}\t{FixedDate[i]}")

        #insert into SQL DB
        DB.AddToDatabase(stock, quantity, FixedDate[i], investment)
        print("\t\tAdded to DB\n")

        
        i = i +1
        
    print("DB updated with excel values") 

    

#extract_data()





