import datetime as dt
import pandas as pd
import yfinance as yf
from fredapi import Fred
import plotly.graph_objects as go

# FRED API key and connection
FredKey = "db3bf9c729b0ac45151b940bcfb1179c"
fred = Fred(api_key=FredKey)

# Define the start and end dates
start = dt.datetime(1960, 1, 1)
end = dt.datetime.now()

# Fetch Historical data for bonds (spread between 10Y and 2Y yields)
def get_Bond_data(): 
    data = fred.get_series('T10Y2Y', observation_start=start, observation_end=end)
    dfBond = pd.DataFrame(data, columns=['10 Year Bond - 2 Year Bond'])
    dfBond.index.name = 'Date'
    print(dfBond)
    return dfBond 

# Fetch Historical data for the Federal Funds Rate
def get_FRED_data(): 
    data = fred.get_series('FEDFUNDS',observation_start=start, observation_end=end)
    dfFRED = pd.DataFrame(data, columns=['Federal Funds Rate'])
    dfFRED.index.name = 'Date'
    print(dfFRED)
    return dfFRED

# Fetch Historical data for 30-Year Mortgage Rates
def get_Mortgage_data(): 
    data = fred.get_series('MORTGAGE30US', observation_start=start, observation_end=end)
    dfMortgage = pd.DataFrame(data, columns=['30 Year Mortgage Rate'])
    dfMortgage.index.name = 'Date'
    print(dfMortgage)
    return dfMortgage

def CallFunc():
    print("\n\nwhat the banks are making in reserves\n\n") 
    dfFRED = get_FRED_data()

    print("\n\nwhat the banks are making on Mortgages\n\n") 
    dfMortgage = get_Mortgage_data()

    print("\n\npeople thoughts for the future (spread in %)\n\n")
    dfBond = get_Bond_data()

    # Reset index to turn the DatetimeIndex into a column
    dfFRED.reset_index(inplace=True)
    dfMortgage.reset_index(inplace=True)
    dfBond.reset_index(inplace=True)

    # Rename the index column to 'Date' if necessary
    dfFRED.rename(columns={'index': 'Date'}, inplace=True)
    dfMortgage.rename(columns={'index': 'Date'}, inplace=True)
    dfBond.rename(columns={'index': 'Date'}, inplace=True)

    # Merge the datasets using inner join to get common dates.
    print("Merging data...\n")
    dfMerge2 = pd.merge(dfMortgage, dfBond, on='Date', how='inner')  # Merge Mortgage and Bond data
    dfMerge = pd.merge(dfMerge2, dfFRED, on='Date', how='inner')       # Add FRED data

    # Plotting with Plotly
    print("Plotting data with Plotly...\n")
    fig = go.Figure()
    
    # Plot each column except 'Date'
    for column in dfMerge.columns:
        if column != 'Date':
            fig.add_trace(
                go.Scatter(
                    x=pd.to_datetime(dfMerge['Date']),
                    y=dfMerge[column],
                    mode='lines',
                    name=column
                )
            )

    # Customize the layout
    fig.update_layout(
        title="Merged Data Plot",
        xaxis_title="Date",
        yaxis_title="Values in percent",
        width=1400,
        height=700,
        template="plotly_dark"
    )
    
    # Display the plot in your browser or interactive window
    fig.show()

CallFunc()
