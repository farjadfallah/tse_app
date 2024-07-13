import mplcursors
import matplotlib.pyplot as plt
import numpy as np


class Portfolio:
    def __init__(self, _shares = {}, _call_options={}, _put_options={}, _darmad_sabets={}):
        self.shares = _shares
        self.call_options = _call_options
        self.put_options = _put_options
        self.daramad_sabets = _darmad_sabets

    def get_value_at_strike(self, final_price, days_till_maturity):
        final_value = 0
        for share in self.shares:
            final_value += (share.get_value_at_strike(final_price) * self.shares[share])
        for call in self.call_options:
            final_value += (call.get_value_at_strike(final_price) * self.call_options[call])
        for put in self.put_options:
            final_value += (put.get_value_at_strike(final_price) * self.put_options[put])
        for daramad_sabet in self.daramad_sabets:
            final_value += (daramad_sabet.get_value_at_strike(days_till_maturity) * self.daramad_sabets[daramad_sabet])

        return final_value

    def get_total_cost(self):
        total_cost = 0
        for share in self.shares:
            total_cost += (share.get_cost() * self.shares[share])
        for call in self.call_options:
            price = call.get_cost_to_buy(False) if self.call_options[call] > 0 else call.get_cost_to_sell(False)
            total_cost += (price * self.call_options[call])
        for put in self.put_options:
            price = put.get_cost_to_buy(False) if self.put_options[put] > 0 else put.get_cost_to_sell(False)
            total_cost += (price * self.put_options[put])
        for daramad_sabet in self.daramad_sabets:
            total_cost += (daramad_sabet.get_cost() * self.daramad_sabets[daramad_sabet])
        return total_cost

    def add_call(self, call, amount):
        if(call in self.call_options):
            self.call_options[call] += amount
        else:
            self.call_options[call] = amount

    
    def add_put(self, put, amount):
        if(put in self.put_options):
            self.put_options[put] += amount
        else:
            self.put_options[put] = amount

    def add_share(self, share, amount):
        if(share in self.shares):
            self.shares[share] += amount
        else:
            self.shares[share] = amount

    def add_daramad_sabet(self, daramad_sabet, amount):
        if(daramad_sabet in self.daramad_sabets):
            self.daramad_sabets[daramad_sabet] += amount
        else:
            self.daramad_sabets[daramad_sabet] = amount

    def plot_chart(self, change, curr_price):
        the_linespace =  np.linspace(curr_price*(1-change), curr_price*(1+change),100)
        y = [((self.get_value_at_strike(x,110) - self.get_total_cost())/(self.get_total_cost()))+1 for x in the_linespace]
        for i in range(len(the_linespace)-1):
            if y[i] < 1:
                plt.plot([the_linespace[i], the_linespace[i + 1]], [y[i], y[i + 1]], color='r')  
            else:
                plt.plot([the_linespace[i], the_linespace[i + 1]], [y[i], y[i + 1]], color='g')  
        mplcursors.cursor(hover=True)
        plt.show()