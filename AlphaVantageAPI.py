import requests

class DayTrader:
    def __init__(self):
        self.bank_account = 10000
        self.num_of_shares = 0

    def __str__(self):
        return "Bank account balance $" + str("{:.2f}".format(self.bank_account)) + " and You own {} shares".format(self.num_of_shares)

    def buy(self, shares, price):
        if shares * price > self.bank_account:
            print("Sorry not enough cash in your bank account.")
        else:
            self.bank_account -= shares * price
            self.num_of_shares += shares
            return True

    def sell(self, shares, price):
        if shares > self.num_of_shares:
            print("You dont have {} shares to sell".format(shares))
        else:
            self.bank_account += shares * price
            self.num_of_shares -= shares
            return True


MYFUNCTION = "TIME_SERIES_DAILY" # "GLOBAL_QUOTE"
MYKEY = "A7SW5BBTJ4PNLKAK"
MYSYMBOL = "IBM"

r = requests.get("https://www.alphavantage.co/query?function="+ MYFUNCTION +"&symbol=IBM&apikey=" + MYKEY)
data = r.json()

load_prices = []
counter = 0
for k , v in data["Time Series (Daily)"].items():
    load_prices.append(float(v["4. close"]))
    counter += 1
    if counter == 30:
        break
    #print("Date: ", k ," price ", v["4. close"])

print("Price Load complete... Lets play")


day_counter = 1
load_prices.reverse()

trader = DayTrader()

for todays_price in load_prices:
    print("\n Day#", day_counter, trader)
    print("\nPrice of one IBM stock is: $",todays_price)
    choice_is_valid = True

    while choice_is_valid:
        choice = input("What would you like to do  ? Buy (B) / Sell (S)  / Hold (H) ").lower()
        if choice not in ["b", "s", "h"]:
            print("invalid entry...")
            continue
        if choice == "b":
            print("How many shares would you like to buy ? Max you can efford ", int(trader.bank_account / todays_price), " : ")
            buy = int(input())
            if trader.buy(buy, todays_price):
                choice_is_valid = False
        elif choice == "s":
            sell = int(input("How many shares would you like to sell ? : "))
            if trader.sell(sell, todays_price):
                choice_is_valid = False
        else:
            day_counter += 1
            choice_is_valid = False
            continue
        day_counter += 1

print("\n Game over \nYou started with $ 10000.00")
print("Today you have : $", "{:.2f}".format(trader.bank_account + trader.num_of_shares * load_prices[-1]))
