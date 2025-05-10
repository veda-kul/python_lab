#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    ## Sort the stock list
    pass


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        length = len(stock.DataList)

        for i in range(length):
            for j in range(0, length-i-1):
                if stock.DataList[j].date > stock.DataList[j + 1].date:
                    stock.DataList[j], stock.DataList[j + 1] = stock.DataList[j + 1], stock.DataList[j]
    
    return stock_list

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    stock_to_plot = None
    for stock in stock_list:
        if symbol == stock.symbol:
            stock_to_plot = stock
            break
    if stock_to_plot is None:
        print("Input stock could not be found")
        input("Press Enter to Continue")
    else:
        if not stock.DataList:
            print(f"No daily data available for {symbol}")
            input("Press Enter to Continue")
        else:
            sortDailyData(stock_list)
            dates = [data.date for data in stock.DataList]
            prices = [data.close for data in stock.DataList]

            plt.figure(figsize=(10,5))
            plt.plot(dates, prices, marker = 'o', linestyle = '-', label=f"{symbol} Closing Price")
            plt.title(f"{stock.name} ({stock.symbol}) - Closing Price Over Time")
            plt.xlabel("Date")
            plt.ylabel("Closing Price")
            plt.legend()
            plt.tight_layout()
            plt.show()