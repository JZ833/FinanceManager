import pymysql.cursors
import datetime as dt
import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt


# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='TeamLlama',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)


style.use('ggplot')

user_id = 1
symbolList = []
weightList = [] 


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
        #Fetch Sum of all investments
        cursor.execute(TotalInvestmentSQL, (user_id,) )
        TotalInvestment = cursor.fetchone()["SUM(`TotalInvestment`)"] or 0
        #Fetch Stock symbols and investment in that stock 
        cursor.execute(FetchTickers, (user_id,))
        result = cursor.fetchall()
        
        #checks if stocks in user database
        if not result:
            print("No stocks found in the database.")
            return
        
        for row in result:
            #Initialize values and calculate weights 
            symbol = row['Symbol'].strip()
            print(f"Fetching data for symbol: {symbol}")
            symbolList.append(symbol)
                        
            Investment = row['TotalInvestment']
            Weight = Investment / TotalInvestment 
            print(f"Symbol: {symbol}\nWeight: {Weight}")
            weightList.append(Weight)

            

def PieChart():
    # Create dataframe for plotting
    df = pd.DataFrame({'Symbol': symbolList, 'Weight': weightList})
    plt.pie(df['Weight'], labels=df['Symbol'], autopct='%1.1f%%')
    plt.title('Investment Distribution')
    plt.ylabel("")  # Optional: removing the ylabel
    plt.show()  # Ensure this line calls plt.show() with parentheses to display the chart

# Call the functions
CalculateWeights()
PieChart()
