import pandas as pd
import yfinance as yf
import os
from conditional import condition_manager
from dataset_manager import *
import matplotlib.pyplot as plt

class simulation():
    def __init__(self, symbol):
        self.symbol = symbol
        self.stock_data = get_symbol(self.symbol)
        self.entry_mng = condition_manager()
        self.exit_mng = condition_manager()
        
    def add_factor_to_dataset(self, factor):
        add_factor(self.symbol, factor)
        self.stock_data = fetch_updated_data(self.symbol)
    
    def add_entry_condition(self, factor, argument):
        self.entry_mng.add_condition(factor, argument)

    def add_exit_condition(self, factor, argument):
        self.exit_mng.add_condition(factor, argument)
    
    def crop_dataset(self, start_date, end_date):
        self.stock_data = crop_data(self.symbol, start_date, end_date)

    def simulate(self):
        balance = 100
        balances = []
        invested = False

        for i in range(len(self.stock_data)):
            row = self.stock_data.iloc[i]
            if not invested:
                invested = self.entry_mng.check_conditions(row)
                self.entry_price = row['Close']
            else:
                invested = not self.exit_mng.check_conditions(row)
                if not invested:
                    balance *= row['Close']/self.entry_price
            balances.append(balance*(row['Close']/self.entry_price))
        self.stock_data = add_balances(self.symbol, balances)

    def plot_sim(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.stock_data['Date'], self.stock_data['Balance'], label='Portfolio Balance')
        # Adjusting x-axis ticks to show specific dates
        xticks = self.stock_data['Date'][::len(self.stock_data)//10]  # Show only 10 evenly spaced dates
        plt.xticks(ticks=xticks, labels=xticks, rotation=45, ha='right')

        plt.xlabel('Date')
        plt.ylabel('Balance ($)')
        plt.title(f"Investment Strategy Performance on {self.symbol}")
        plt.legend()
        plt.tight_layout()
        plt.show()


