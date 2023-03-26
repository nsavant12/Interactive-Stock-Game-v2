#imports
import tkinter as tk
import yfinance as yf
#Creating the Portfolio section
class Portfolio(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Stock Game")
        self.stocks = {}
        self.create_widgets()
#populating the window
    def create_widgets(self):
        symbol_label = tk.Label(self.master, text="Stock Symbol:")
        symbol_label.grid(row=0, column=0, padx=5, pady=5)

        shares_label = tk.Label(self.master, text="Shares:")
        shares_label.grid(row=1, column=0, padx=5, pady=5)

        self.symbol_entry = tk.Entry(self.master)
        self.symbol_entry.grid(row=0, column=1, padx=5, pady=5)

        self.shares_entry = tk.Entry(self.master)
        self.shares_entry.grid(row=1, column=1, padx=5, pady=5)

        buy_button = tk.Button(self.master, text="Buy", command=self.on_buy_button_click)
        buy_button.grid(row=2, column=0, padx=5, pady=5)

        sell_button = tk.Button(self.master, text="Sell", command=self.on_sell_button_click)
        sell_button.grid(row=2, column=1, padx=5, pady=5)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        portfolio_label = tk.Label(self.master, text="Portfolio:")
        portfolio_label.grid(row=4, column=0, padx=1, pady=1)

        self.portfolio_list = tk.Listbox(self.master, width=50)
        self.portfolio_list.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
#setting up the buy stock function
    def add_stock(self, symbol, shares):
        stock_data = yf.Ticker(symbol).info
        if "regularMarketPrice" in stock_data:
            price = stock_data["regularMarketPrice"]
            value = shares * price
            if symbol in self.stocks:
                self.stocks[symbol]["shares"] += shares
                self.stocks[symbol]["value"] += value
            else:
                self.stocks[symbol] = {"shares": shares, "value": value, "price": price}
            self.update_portfolio()
        else:
            self.status_label.configure(text=f"{symbol} is not a valid stock symbol")
#setting up the remove stock function
    def remove_stock(self, symbol, shares):
        if symbol in self.stocks:
            if shares > self.stocks[symbol]["shares"]:
                self.status_label.configure(text=f"You do not own {shares} shares of {symbol}")
            else:
                self.stocks[symbol]["shares"] -= shares
                self.stocks[symbol]["value"] -= shares * self.stocks[symbol]["price"]
                if self.stocks[symbol]["shares"] == 0:
                    del self.stocks[symbol]
                self.update_portfolio()
        else:
            self.status_label.configure(text=f"You do not own {symbol}")
#displaying previously bought stocks w/ key info
    def update_portfolio(self):
        self.portfolio_list.delete(0, tk.END)
        total_value = 0
        for symbol, stock_data in self.stocks.items():
            shares = stock_data["shares"]
            price = stock_data["price"]
            value = stock_data["value"]
            self.portfolio_list.insert(tk.END, f"{symbol}: {shares} shares at a price of {price:.2f}  Total Value:{value:.2f}")
            total_value += value
        self.portfolio_list


#set up the buy stock function
    def on_buy_button_click(self):
        symbol = self.symbol_entry.get().upper()
        shares = int(self.shares_entry.get())
        self.add_stock(symbol, shares)
#set up the sell stock function
    def on_sell_button_click(self):
        symbol = self.symbol_entry.get().upper()
        shares = int(self.shares_entry.get())
        self.remove_stock(symbol, shares)
#set up the window
if __name__ == "__main__":
    root = tk.Tk()
    app = Portfolio(root)
    app.mainloop()
