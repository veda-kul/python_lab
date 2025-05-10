# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    option = ""
    while option != "0":
        print("Add Stock ---")
        ticker_symbol = input("Enter Ticker Symbol: ").strip().upper()
        company_name = input("Enter Company Name: ")
        number_of_shares = input("Enter Number of Shares: ")
        new_stock = Stock(ticker_symbol, company_name, int(number_of_shares))
        stock_list.append(new_stock)
        option = input("Stock Added --- Enter to Add Another Stock or 0 to Stop: ")
    
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    print("Update Shares ---")
    option = ""
    while option != "0":
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option:")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)

# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print_all_stocks(stock_list)
    stock_to_buy = input("Which stock do you want to buy? ").strip().upper()
    selected_stock = find_stock_in_stock_list(stock_to_buy, stock_list)
    if selected_stock is None:
        print(f"{stock_to_buy} could not be found")
    else:
        try:
            number_of_shares_to_buy = int(input("How many shares do you want to buy? "))
            selected_stock.buy(number_of_shares_to_buy)
        except ValueError:
            print("Please enter a valid number")
    input("Press Enter to Continue")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print_all_stocks(stock_list)
    stock_to_sell = input("Which stock do you want to sell? ").strip().upper()
    selected_stock = find_stock_in_stock_list(stock_to_sell, stock_list)
    if selected_stock is None:
        print(f"{stock_to_sell} could not be found")
    else:
        try:
            number_of_shares_to_sell = int(input("How many shares do you want to sell? "))
            selected_stock.sell(number_of_shares_to_sell)
        except ValueError:
            print("Please enter a valid number")
    input("Press Enter to Continue")

# Print all stock symbols    
def print_all_stocks(stock_list):
    print("Stock List:[" + ", ".join(stock.symbol for stock in stock_list) + "]")

# Remove stock and all daily data
def delete_stock(stock_list,):
    print("Delete Stock ---")
    print_all_stocks(stock_list)
    original_stock_list_length = len(stock_list)
    stock_to_delete = input("Which stock do you want to delete? ").strip().upper()
    stock_list[:] = [ stock for stock in stock_list if stock.symbol != stock_to_delete]
    if(len(stock_list) < original_stock_list_length):
        print(f"{stock_to_delete} Stock Deleted")
    input("Press Enter to Continue")

# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Stock List ---")
    print(f"{'SYMBOL':<10} {'NAME':<25} {'SHARES':>8}")
    print("=" * 45)
    for stock in stock_list:
        print(f"{stock.symbol:<10} {stock.name:<25} {stock.shares:>8}")
    input("Press Enter to continue")

def find_stock_in_stock_list(stock_symbol, stock_list):
    for stock in stock_list:
        if stock.symbol == stock_symbol:
            return stock
    return None

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ---")
    print_all_stocks(stock_list)
    user_input_stock = input("Which stock do you want to use?:").strip()
    stock_to_update = find_stock_in_stock_list(user_input_stock, stock_list)
    if stock_to_update is None:
        print(f"{user_input_stock} Entered stock could not be found")
    else:
        print(f"""Ready to add data for: {stock_to_update}
                Enter Data Separated by Commas - Do Not Use Spaces
                Enter a Blank Line to Quit
                Enter Date,Price, Volum
                Example: 8/28/20,47.85, 10550 
            """)
        user_input=input("Enter Date,Price,Volume:")
        try:
            record_date_string, price, volume = [item.strip() for item in user_input.split(",")]
            #We can also check if entered date is in correct format
            record_date = datetime.strptime(record_date_string, "%m/%d/%y")
            newDailyData = DailyData(record_date, price, volume)
            stock_to_update.add_data(newDailyData)
            print(f"Daily Data Stock Data added for {user_input_stock}")
        except ValueError:
             print("Invalid date format! Please enter the date as MM/DD/YY (e.g., 8/28/20).")
        except Exception as exc:
                print(f"Please enter data as Date,Price,Volume. {exc}")
    input("Press Enter to continue")

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_data:
        print(f"Report for: {stock.symbol} {stock.name}")
        data_list = stock.DataList
        if len(data_list) == 0:
            print("*** No Daily history")
        else:
            print(f"{'Date':<12} {'Close':>10} {'Volume':>12}")
            print("-" * 36)
            for item in data_list:
                print(f"{(item._date.strftime("%m/%d/%y")):<12} {float(item._close):>10.2f} {int(item._volume):>12,}")
        print()
    print("--- Report Complete ---")
    input("Press ENTER to Continue")

# Display Chart
def display_chart(stock_list):
    print_all_stocks(stock_list)
    symbol = input("Which stock do you want to use?: ").strip()
    stock_to_update = find_stock_in_stock_list(symbol, stock_list)
    if stock_to_update is None:
        print(f"{symbol} Entered stock could not be found")
    else:
        display_stock_chart(stock_list, symbol)
    input("Press Enter to Continue")


# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Manage Data ---")
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            input("Press Enter to continue")
        elif option == "2":
            stock_data_result = stock_data.load_stock_data(stock_list)
            input("Press Enter to continue")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
    
# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("""Retrieving  Stock Data from Yahoo! Finance ---
              This will retrieve data from all stocks in your stock list.
    """)
    try:
        start_date = input("Enter starting date: (MM/DD/YY): ")
        end_date = input("Enter ending date: (MM/DD/YY): ")
        datetime.strptime(start_date, "%m/%d/%y")
        datetime.strptime(end_date, "%m/%d/%y")
        stock_data.retrieve_stock_web(start_date, end_date, stock_list)
    except ValueError:
        print("Invalid date format! Please use MM/DD/YY")  
    input("Press Enter to Continue")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV file from Yahoo! Finance ---")
    print_all_stocks(stock_list)
    user_input_stock_symbol = input("Which stock do you want to use?:").strip()
    stock_to_update = find_stock_in_stock_list(user_input_stock_symbol, stock_list)
    if stock_to_update is None:
        print(f"{user_input_stock_symbol} Entered stock could not be found")
    else:
        csv_file_name = input("Enter filename:")
        stock_data.import_stock_web_csv(stock_list, user_input_stock_symbol, csv_file_name)
        print("CSV File Imported")
    input("Press ENTER to Continue")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    # Clear Database()
    stock_data.clear_database()
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()