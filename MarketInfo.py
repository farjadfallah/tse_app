
import numpy as np



class MarketInfo:
    def __init__(self):
        self.stocks_list = []
        self.call_options_list = []
        self.put_options_list = []
        self.option_chains_list={}

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


    def find_relations(self):
        self.create_option_chains()
        self.pair_similar_call_and_puts()

    def apply_filter(self, the_filter):
        result = the_filter.apply_filter(self.stocks_list, self.call_options_list, self.put_options_list)
        return result


    def pair_similar_call_and_puts(self):

        for call in self.call_options_list:
            the_strike = call.get_strike_price()
            the_coresponding_chain = self.option_chains_list[str(call.get_underlying_asset())][call.get_days_till_maturity()] 
            for option in the_coresponding_chain:
                if(option.get_type() == 'put' and option.get_strike_price() == the_strike ):
                    call.set_similar_option_to(option)

        for put in self.put_options_list:
            the_strike = put.get_strike_price()
            the_coresponding_chain = self.option_chains_list[str(put.get_underlying_asset())][put.get_days_till_maturity()] 
            for option in the_coresponding_chain:
                if(option.get_type() == 'call' and option.get_strike_price() == the_strike ):
                    put.set_similar_option_to(option)

    def create_option_chains(self):
        for call in self.call_options_list:
            self.__add_option_to_chain(call)

        for put in self.put_options_list:
            self.__add_option_to_chain(put)

    def __add_option_to_chain(self, option): 
        ua_asset = str(option.get_underlying_asset())
        days_till_maturity = option.get_days_till_maturity()
        if(ua_asset not in self.option_chains_list):
                self.option_chains_list[ua_asset] = {}
                self.option_chains_list[ua_asset][days_till_maturity] = []
                self.option_chains_list[ua_asset][days_till_maturity].append(option)
        else:
            if(days_till_maturity not in self.option_chains_list[ua_asset]):
                self.option_chains_list[ua_asset][days_till_maturity] = []
                self.option_chains_list[ua_asset][days_till_maturity].append(option)
            else:
                self.option_chains_list[ua_asset][days_till_maturity].append(option)
