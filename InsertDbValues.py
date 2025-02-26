#sql libs
import pymysql.cursors
import datetime as dt

#excel data
#import ReadExcel

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='TeamLlama',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)



#define user portfolio (need login to identify) 
table = "userportfolio1"


InsertSQL = f"""INSERT INTO `{table}` (`Symbol`, `Quantity`, `FirstBuyDate`, `TotalInvestment`)
            VALUES(%s, %s, %s, %s)
            ON DUPLICATE KEY
            UPDATE `Quantity` = VALUES(`Quantity`), `TotalInvestment` = VALUES(`TotalInvestment`)

"""

InsertSQL2 = f"""INSERT INTO `{table}` (`Symbol`, `Quantity`, `TotalInvestment`)
            VALUES(%s, %s, %s)
            ON DUPLICATE KEY
            UPDATE `Quantity` = VALUES(`Quantity`), `TotalInvestment` = VALUES(`TotalInvestment`)

"""



CurrentQuantitySQL = f"""SELECT `Quantity`
                            FROM `{table}`
                            WHERE `Symbol` = %s

"""

TotalInvestmentSQL = f"""
    SELECT `TotalInvestment`
    FROM `{table}`
    WHERE `Symbol` = %s

"""

RemoveRowSQL = f"""
    DELETE FROM `{table}`
    WHERE `Symbol` = %s
"""

GainSQL = f"""
    UPDATE `users`
    SET `RealizedGainLoss` = `RealizedGainLoss` + %s
    WHERE `Id` = 1
    

"""


def UpdateGain(gain):
    with connection.cursor() as cursor:
        cursor.execute(GainSQL, (gain,))

    connection.commit()



def AddToDatabase(stock, quantity, date, investment):
    with connection.cursor() as cursor:
        cursor.execute(InsertSQL, (stock, quantity, date, investment))

    connection.commit()

#same func doesnt need date 
def AddToDatabase2(stock, quantity, investment):
    with connection.cursor() as cursor:
        cursor.execute(InsertSQL2, (stock, quantity, investment))

    connection.commit()
    
def RemoveRow(stock):
    with connection.cursor() as cursor:
        cursor.execute(RemoveRowSQL, (stock,))

    connection.commit()


#Fetches the curent quantity of the given stock        
def CurrentQuantity(stock):
    with connection.cursor() as cursor:
        cursor.execute(CurrentQuantitySQL, (stock,))
        result = cursor.fetchone()

        return result["Quantity"] if result and "Quantity" in result else 0 

#Fetches the curent total investment of the given stock        
def FetchTotalInvestment(stock):
    with connection.cursor() as cursor:
        cursor.execute(TotalInvestmentSQL, (stock,))
        result = cursor.fetchone()

        return result["TotalInvestment"] if result and "TotalInvestment" in result else 0

    
  

