



class Filter:
    

    def apply_filter(self, stocks_list, call_options_list, put_options_list):
        pass

    def get_roi(self, non_roi_return, duration):
        return (pow((1 + (non_roi_return/100)), 365/duration) -1)*100


class Covered_Call_filter(Filter):


    def __init__(self, _min_roi, _min_confidence_interval, _min_days_to_mature, _sarkhat_or_latest = 'sarkhat'):
        super().__init__()
        self.min_roi = _min_roi
        self.min_confidence_interval = _min_confidence_interval
        self.sarkhat_or_latest = _sarkhat_or_latest
        self. min_day_to_mature = _min_days_to_mature

    def apply_filter(self, stocks_list, call_options_list, put_options_list):
        print("===========================================")
        print("covered call filter result for these specs:")
        print("minimum ROI=", self.min_roi)
        print("minimum confidence interval=", self.min_confidence_interval)
        print("minimum days to mature= ", self.min_day_to_mature)
        print("-------------------------------------------")
        for call_op in call_options_list:
            underlying_asset = call_op.get_underlying_asset()
            total_cost = self.__calculate_total_cost(call_op, underlying_asset)
            expected_return = self.__calculate_expected_return(call_op, underlying_asset)
            profit_percentage = (expected_return / total_cost - 1) * 100
            roi = self.get_roi(profit_percentage, call_op.get_days_till_maturity())
            confidence_interval = self.__calculte_confidence_interval(call_op, underlying_asset)

            if(confidence_interval > self.min_confidence_interval and roi > self.min_roi and call_op.get_days_till_maturity() > self.min_day_to_mature  ):
                print(f'{str(call_op):<15}','roi=',  round(roi, 1), '    confidence interval = ', round(confidence_interval, 1), '  ua price = ', underlying_asset.get_cost(self.sarkhat_or_latest), '      optoins price = ', call_op.get_cost_to_sell( False, self.sarkhat_or_latest))
        print("===========================================")

            

    def __calculate_total_cost(self, call_option, underlying_asset):
        return  underlying_asset.get_cost(self.sarkhat_or_latest) - call_option.get_cost_to_sell( False, self.sarkhat_or_latest)

    def __calculate_expected_return(self, call_option, underlying_asset):
        strike = call_option.get_strike_price()
        return underlying_asset.get_value_at_strike(strike) - call_option.get_value_at_strike(strike)
    
    def __calculte_confidence_interval(self, call_option, underlying_asset):
        return (1- call_option.get_strike_price() / underlying_asset.get_cost(self.sarkhat_or_latest)) * 100
    


# class Maried_Put_Filter(Filter):
#     def __init__(self, _max_risk, _curr_ROI, _min_days_to_mature, _sarkhat_or_latest = 'sarkhat'):
#         super().__init__()
#         self.max_risk = _max_risk
#         self.curr_ROI = _curr_ROI
#         self.sarkhat_or_latest = _sarkhat_or_latest
#         self.min_day_to_mature = _min_days_to_mature
        
#     def apply_filter(self, stocks_list, call_options_list, put_options_list):
#         print("===========================================")
#         print("married put filter result for these specs:")
#         print("current ROI=", self.curr_ROI)
#         print("maximum risk=", self.max_risk)
#         print("minimum days to mature= ", self.min_day_to_mature)
#         print("-------------------------------------------")
#         for put_op in put_options_list:
#             underlying_asset = put_op.get_underlying_asset()
#             total_cost = self.__calculate_total_cost(put_op, underlying_asset)
#             minimum_expected_return = self.__calculate_min_return(put_op, underlying_asset)
#             risk_percentage = (minimum_expected_return / total_cost - 1) * 100
#             calculate_current_return = self.__calculate_curr_return(put_op, underlying_asset)
#             current_return = 
#             roi = self.get_roi(profit_percentage, call_op.get_days_till_maturity())
#             confidence_interval = self.__calculte_confidence_interval(call_op, underlying_asset)

#             if(confidence_interval > self.min_confidence_interval and roi > self.min_roi and call_op.get_days_till_maturity() > self.min_day_to_mature  ):
#                 print(f'{str(call_op):<15}','roi=',  round(roi, 1), '    confidence interval = ', round(confidence_interval, 1), '  ua price = ', underlying_asset.get_cost(self.sarkhat_or_latest), '      optoins price = ', call_op.get_cost_to_sell( False, self.sarkhat_or_latest))
#         print("===========================================")
    