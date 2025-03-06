import pymysql.cursors
import datetime as dt
import pandas as pd
import plotly.express as px

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
        # Fetch sum of all investments
        cursor.execute(TotalInvestmentSQL, (user_id,))
        TotalInvestment = cursor.fetchone()["SUM(`TotalInvestment`)"] or 0

        # Fetch stock symbols and investment in each stock
        cursor.execute(FetchTickers, (user_id,))
        result = cursor.fetchall()
        
        # Check if stocks exist for the user
        if not result:
            print("No stocks found in the database.")
            return
        
        for row in result:
            symbol = row['Symbol'].strip()
            print(f"Fetching data for symbol: {symbol}")
            symbolList.append(symbol)
                        
            Investment = row['TotalInvestment']
            Weight = Investment / TotalInvestment 
            print(f"Symbol: {symbol}\nWeight: {Weight}")
            weightList.append(Weight)

def PieChart():
    # Create DataFrame for plotting
    df = pd.DataFrame({'Symbol': symbolList, 'Weight': weightList})
    
    # Create an interactive pie chart using Plotly Express
    fig = px.pie(df, 
                 names='Symbol', 
                 values='Weight',
                 title='Investment Distribution',
                 hole=0)  # Remove or set a value for a donut chart look
    
    fig.show()

# Call the functions
CalculateWeights()
PieChart()
