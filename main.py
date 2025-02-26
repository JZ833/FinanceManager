import yfinance as yf
import pandas as pd


#Update from excel  
import ReadExcel
import InsertDbValues as DB
import GetPrice


def AskUser():
    print("""\nInput a Number, or 0 to Exit
            \n1.Insert One stock into database
            \n2.Insert Excel into database
            \n3.Update Stock quantity in database (log buy or sell)
            \n4.Remove Stock from database
            """)

    UserInput = int(input())

    return UserInput

UserInput = AskUser()



while UserInput > 0:


    if UserInput ==1:
        #get stock info from user
        print("Enter Stock Symbol: < 6 Letters\n")
        Symbol = input()
        print("Enter number of shares\n")
        Quantity = input()
        print("Enter the buy date: YYYY-MM-DD\n")
        date = input()
        print("Enter the total USD you invested\n")
        investment = input()

        #Send to DB
        DB.AddToDatabase(Symbol, Quantity, date, investment)
        
        print(f"Added {Symbol} Stock to DB")
        
        
        
    if UserInput ==2:
        ReadExcel.extract_data()


    if UserInput == 3:
        print("Enter Stock Symbol: < 6 Letters\n")
        Symbol = input()
        
        
        print("Enter new number of shares\n")
        Quantity = float(input())

        #Fetchdata
        OldQuantity = DB.CurrentQuantity(Symbol)
        Investment = DB.FetchTotalInvestment(Symbol)
        CurrentPrice = GetPrice.get_stock_price(Symbol)

        if(Quantity < OldQuantity):
            
            SoldQuantity = OldQuantity - Quantity

            # Calculate old cost basis per share
            OldCostBasis = Investment / OldQuantity 
            
            
            #Calculate the realized gain
            
            Gain = (SoldQuantity * CurrentPrice) - (SoldQuantity * (Investment / OldQuantity))

            # Update the remaining investment amount
            NewInvestment = Investment - (SoldQuantity * OldCostBasis)

            #save gain to UserDB
            DB.UpdateGain(Gain)
            
            

            #Update Total investment and quantity
            DB.AddToDatabase2(Symbol, Quantity, NewInvestment)

            print(f"Updated {Symbol}: New Quantity = {Quantity}, New Investment = ${NewInvestment:.2f}")
            print(f"Realized Gain from Sell: ${Gain:.2f}")
            
            
        else:
            print("Enter how much you payed: \n")
            NewInvestment = float(input())
            NewInvestment += Investment
            #Update Total investment and Quantity
            DB.AddToDatabase2(Symbol, Quantity, NewInvestment)
            
            
            
    if UserInput == 4:
        SellStock = str(input("Enter Stock Name: "))
        CurrentPrice =  GetPrice.get_stock_price(Symbol)
        TotalInvestment = DB.FetchTotalInvestment(SellStock)
        Quantity = DB.CurrentQuantity(SellStock)
        TradeGain = (CurrentPrice * Quantity) - TotalInvestment
        DB.UpdateGain(TradeGain) 
        DB.RemoveRow(SellStock)
        print(f"Removed {SellStock} from database, realized gain/loss: {TradeGain}\n")
        
        
        
        
    UserInput = AskUser()


#Validate inputs
    
        
        
        

