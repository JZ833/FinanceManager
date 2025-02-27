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
table = "userportfolio"


InsertSQL = f"""INSERT INTO `{table}` (`UserId`, `Symbol`, `Quantity`, `FirstBuyDate`, `TotalInvestment`)
            VALUES(%s, %s, %s, %s, %s)
            ON DUPLICATE KEY
            UPDATE `Quantity` = VALUES(`Quantity`), `TotalInvestment` = VALUES(`TotalInvestment`)
"""

InsertSQL2 = f"""INSERT INTO `{table}` (`UserId`, `Symbol`, `Quantity`, `TotalInvestment`)
            VALUES(%s, %s, %s, %s)
            ON DUPLICATE KEY
            UPDATE `Quantity` = VALUES(`Quantity`), `TotalInvestment` = VALUES(`TotalInvestment`)
"""

CurrentQuantitySQL = f"""SELECT `Quantity`
                            FROM `{table}`
                            WHERE `UserId` = %s AND `Symbol` = %s
"""

TotalInvestmentSQL = f"""
    SELECT `TotalInvestment`
    FROM `{table}`
    WHERE `UserId` = %s AND `Symbol` = %s
"""

RemoveRowSQL = f"""
    DELETE FROM `{table}`
    WHERE `UserId` = %s AND `Symbol` = %s
"""

GainSQL = f"""
    UPDATE `users`
    SET `RealizedGainLoss` = `RealizedGainLoss` + %s
    WHERE `UserId` = %s 
    

"""


def UpdateGain(user_id, gain):
    with connection.cursor() as cursor:
        cursor.execute(GainSQL, (gain, user_id))

    connection.commit()

    
def AddToDatabase(user_id, stock, quantity, date, investment):
    with connection.cursor() as cursor:
        cursor.execute(InsertSQL, (user_id, stock, quantity, date, investment))

    connection.commit()

#same func doesnt need date 
def AddToDatabase2(user_id, stock, quantity, investment):
    with connection.cursor() as cursor:
        cursor.execute(InsertSQL2, (user_id, stock, quantity, investment))

    connection.commit()

def RemoveRow(user_id, stock):
    with connection.cursor() as cursor:
        cursor.execute(RemoveRowSQL, (user_id, stock))

    connection.commit()

def CurrentQuantity(user_id, stock):
    with connection.cursor() as cursor:
        cursor.execute(CurrentQuantitySQL, (user_id, stock))
        result = cursor.fetchone()
        return result["Quantity"] if result and "Quantity" in result else 0 

def FetchTotalInvestment(user_id, stock):
    with connection.cursor() as cursor:
        cursor.execute(TotalInvestmentSQL, (user_id, stock))
        result = cursor.fetchone()
        return result["TotalInvestment"] if result and "TotalInvestment" in result else 0
  

