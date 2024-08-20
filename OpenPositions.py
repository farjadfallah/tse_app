
import pandas as pd

class OpenPostionsRecords:

    def __init__(self, _market_info):
        self.covered_calls_list = []
        self.arbitrages_list = []
        self.protective_puts_list =[]
        self.market_info = _market_info

   
    

    def add_covered_call(self, covered_call):
        self.covered_calls_list.append(covered_call)

    def get_current_state(self):
        final_result =[[],[],[]]
        for covered_call in self.covered_calls_list:
            final_result[0].append(covered_call.get_current_state())
        print(final_result)
        return final_result
    
    def save_file(self):
        the_list = []
        for record in self.covered_calls_list:
            the_list.append(record.save_file_output())

        df = pd.DataFrame(the_list, columns=['call_name', 'volume', 'ua_asset_price', 'call_price', 'days_to_mature'])
        df.to_csv('my_portfolio.csv', index=False, encoding="utf8")
    
    def load_file(self):
        df = pd.read_csv('my_portfolio.csv', encoding="utf8")
        for index, row in df.iterrows():
            new_covered_Call =Covered_Call_Position_Record(self.market_info, row['call_name'],row['call_price'],row['ua_asset_price'],row['volume'],row['days_to_mature'] )
            self.add_covered_call(new_covered_Call)
           

        
class Record():
     def get_roi(self, non_roi_return, duration):
        if(duration+1 <= 0 ):
            return -100
        return (pow((1 + (non_roi_return/100))+ 0.000001, 365/(duration+1)) -1)*100 
     
class Covered_Call_Position_Record(Record):

    def __init__(self, market_info, _call_name, call_price, ua_price, _volume, _days_to_mature_when_enter ):
        super().__init__()
        self.call_name = _call_name
        self.market_info = market_info
        self.call_op = self.market_info.find_option_with_name(_call_name)
        self.ua_asset = self.call_op.get_underlying_asset()
        self.call_entry_price = call_price
        self.ua_entry_price = ua_price
        self.volume = _volume

        self.strike_price = self.call_op.get_strike_price()
        self.days_to_mature_when_enter = _days_to_mature_when_enter
        self.expected_ROI = self.__calculate__ROI(self.ua_entry_price, self.call_entry_price, self.days_to_mature_when_enter)
        self.expected_untill_loss = self.__calculte_confidence_interval(self.ua_entry_price)

    

    def get_current_state(self):
        self.call_op = self.market_info.find_option_with_name(self.call_name)
        self.ua_asset = self.call_op.get_underlying_asset()
        new_untill_loss = self.__calculte_confidence_interval(self.ua_asset.get_cost())
        new_roi = self.__calculate__ROI(self.ua_asset.get_cost(), self.call_op.get_cost_to_buy(), self.call_op.get_days_till_maturity())
        taken_profit = self.__get_taken_profit()
        taken_ROI = self.get_roi(taken_profit, self.days_to_mature_when_enter-self.call_op.get_days_till_maturity())

       
        result = self.__make_result(new_untill_loss, new_roi, taken_profit, taken_ROI)
        return result
        
    def save_file_output(self):
        the_list = [self.call_name, self.volume, self.ua_entry_price, self.call_entry_price, self.days_to_mature_when_enter]
        return the_list
        

    def __make_result(self, new_untill_loss, new_roi, taken_profit, taken_ROI):
        the_result = {"call_name": str(self.call_op)}
        the_result["volume"] = self.volume
        the_result["ex_days_to_mature"] = self.days_to_mature_when_enter
        the_result["ex_till_loss"] = round(self.expected_untill_loss, 1)
        the_result["ex_ROI"] = round(self.expected_ROI, 1)
        the_result["days_to_mature"] = self.call_op.get_days_till_maturity()
        the_result["ua_price"] = round(self.ua_asset.get_cost())
        the_result["call_price"] = self.call_op.get_cost_to_buy()
        the_result["till_loss"] = round(new_untill_loss, 1)
        the_result["taken_profit"] = round(taken_profit, 1)
        the_result["taken_ROI"] = round(taken_ROI, 1)
        the_result["new_ROI"] = round(new_roi, 1)
        return the_result

    def __calculate__ROI(self, ua_value, call_op_value, days_to_maturity):
        total_cost = self.__calculate_total_cost(ua_value, call_op_value)
        expected_return = self.__calculate_expected_return(self.call_op, self.ua_asset)
        profit_percentage = (expected_return / total_cost - 1) * 100
        roi = self.get_roi(profit_percentage, days_to_maturity)
        return roi
                
    def __calculate_total_cost(self, ua_value, call_op_value):
        return  ua_value - call_op_value

    def __calculate_expected_return(self, call_option, underlying_asset):
        strike = call_option.get_strike_price()
        return underlying_asset.get_value_at_price(strike) - call_option.get_value_at_price(strike)
    
    def __calculte_confidence_interval(self, ua_asset_price):
        return ((self.ua_entry_price- self.call_entry_price)/ ua_asset_price-1) * 100

    def __get_taken_profit(self):
        return ((self.ua_asset.get_cost() -self.call_op.get_cost_to_buy() ) / (self.ua_entry_price - self.call_entry_price) - 1)*100