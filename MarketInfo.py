
import numpy as np



class MarketInfo:
    def __init__(self):
        self.stocks_list = []
        self.call_options_list = []
        self.put_options_list = []
        

    def find_stock_with_name(self, stock_name):
        for stock in self.stocks_list:
            if(stock.check_name(stock_name)):
                return stock
        return None
            
    def find_option_with_name(self, option_name):
        for option in self.call_options_list:
            if(option.check_name(option_name)):
                return option
            
        for option in self.put_options_list:
            if(option.check_name(option_name)):
                return option
        
        return None
            
    def add_stock(self, stock):
        self.stocks_list.append(stock)

    def add_call_option(self, call_option):
        self.call_options_list.append(call_option)

    def add_put_option(self, put_option):
        self.put_options_list.append(put_option)


    def apply_filter(self, the_filter):
        the_filter.apply_filter(self.stocks_list, self.call_options_list, self.put_options_list)