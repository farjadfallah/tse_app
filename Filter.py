



class Filter:
    

    def apply_filter(self, stocks_list, call_options_list, put_options_list):
        pass

    def get_roi(self, non_roi_return, duration):
        if(duration+1 == 0 ):
            return -100
        return (pow((1 + (non_roi_return/100))+ 0.000001, 365/(duration+1)) -1)*100


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
        return underlying_asset.get_value_at_price(strike) - call_option.get_value_at_price(strike)
    
    def __calculte_confidence_interval(self, call_option, underlying_asset):
        return (1- call_option.get_strike_price() / underlying_asset.get_cost(self.sarkhat_or_latest)) * 100
    


class Aribitrage_Filter(Filter):
    def __init__(self, _min_return, _min_days_to_mature, _min_roi, _sarkhat_or_latest = 'sarkhat'):
        super().__init__()
        self.min_return = _min_return
        self.min_days_to_mature = _min_days_to_mature
        self.sarkhat_or_latest = _sarkhat_or_latest
        self.min_roi = _min_roi
    
    def apply_filter(self, stocks_list, call_options_list, put_options_list):
        print("===========================================")
        print("Aribitrage filter result for these specs:")
        print("minimum return=", self.min_return)
        print("minimum days to mature= ", self.min_days_to_mature)
        print("-------------------------------------------")
        results = []
        for call_op in call_options_list:
            underlying_asset = call_op.get_underlying_asset()
            opposite_put = call_op.get_similar_option()
            if(opposite_put == None):
                continue

            total_cost = self.__calculate_total_cost(call_op, opposite_put, underlying_asset)
            if(total_cost == None):
                continue
            expected_return = self.__calculate_expected_return(call_op, opposite_put, underlying_asset)
            profit_percentage = (expected_return / total_cost - 1) * 100
            roi = self.get_roi(profit_percentage, call_op.get_days_till_maturity())

            if(profit_percentage > self.min_return and call_op.get_days_till_maturity() > self.min_days_to_mature and roi > self.min_roi ):
                the_result = {"profit": round(profit_percentage, 1),"mature": call_op.get_days_till_maturity(), "roi":round(roi,1), "call_name": str(call_op),  "call_price":call_op.get_cost_to_sell( False, self.sarkhat_or_latest), "put_name": str(opposite_put), "put_price": opposite_put.get_cost_to_buy(  self.sarkhat_or_latest), "ua_price":round(underlying_asset.get_cost(self.sarkhat_or_latest), 0)}
                results.append(the_result)
                print('profit=',  f'{round(profit_percentage, 1):<5}','ROi=',f'{round(roi,1):<6}',  'days=',f'{call_op.get_days_till_maturity():<4}', f'{str(call_op):<10}', f'{call_op.get_cost_to_sell( False, self.sarkhat_or_latest):<10}', f'{str(opposite_put):<10} ',f'{opposite_put.get_cost_to_buy(  self.sarkhat_or_latest):<10}','  ua price = ',f'{round(underlying_asset.get_cost(self.sarkhat_or_latest), 0):<7}')
        print("===========================================")
        return results



    def __calculate_total_cost(self, call_op, put_op, underlying_asset):
        if(put_op.get_cost_to_buy() == 0):
            return None
        return underlying_asset.get_cost(self.sarkhat_or_latest) - call_op.get_cost_to_sell(False) + put_op.get_cost_to_buy()
        
    def __calculate_expected_return(self, call_op, put_op, underlying_asset):
        strike = call_op.get_strike_price()
        return underlying_asset.get_value_at_price(strike) - call_op.get_value_at_price(strike) + put_op.get_value_at_price(strike)
    



class Optimize_Arbitrage_Filter(Filter):
    def __init__(self, _min_difference, min_roi_difference, _min_days_to_mature, _prev_call,_sarkhat_or_latest = 'sarkhat'):
        super().__init__()
        self.is_vialbe = True
        self.min_return = _min_difference
        self.min_days_to_mature = _min_days_to_mature
        self.min_roi = min_roi_difference
        self.sarkhat_or_latest = _sarkhat_or_latest
        self.call_prev = _prev_call
        self.put_prev = self.call_prev.get_similar_option()
        

    def apply_filter(self, stocks_list, call_options_list, put_options_list):
        print("===========================================")
        print("You Should change your arbirage this way:")
        print("-------------------------------------------")
        if(not self.is_vialbe):
            print('cant trade ', self.call_prev, 'at the moment to optimize the strat')
            return
        
        print("SELL")
        # print('profit=',  f'{round(self.prev_expected_return, 1):<5}','ROi=',f'{round(self.prev_roi,1):<6}',  'days=',f'{self.call_prev.get_days_till_maturity():<4}', f'{str(self.call_prev):<10}', f'{self.call_prev.get_cost_to_buy( self.sarkhat_or_latest):<10}', f'{str(self.put_prev):<10} ',f'{self.put_prev.get_cost_to_sell(  self.sarkhat_or_latest):<10}','  ua price = ',f'{round(self.ua_asset_prev.get_cost(self.sarkhat_or_latest), 0):<7}')
        print()
        print("BUY")
        for call_op in call_options_list:
            underlying_asset = call_op.get_underlying_asset()
            opposite_put = call_op.get_similar_option()
            if(opposite_put == None):
                continue

            total_cost = self.__calculate_total_cost(call_op, opposite_put)
            if(total_cost == None):
                continue
            expected_return = self.__calculate_expected_return(call_op, opposite_put)
            profit_percentage = (expected_return / total_cost - 1) * 100
            roi = self.get_roi(profit_percentage, call_op.get_days_till_maturity())

            if(profit_percentage > self.min_return and call_op.get_days_till_maturity() > self.min_days_to_mature and roi > self.min_roi ):
                print('profit=',  f'{round(profit_percentage, 1):<5}','ROi=',f'{round(roi,1):<6}',  'days=',f'{call_op.get_days_till_maturity():<4}', f'{str(call_op):<10}', f'{call_op.get_cost_to_sell( False, self.sarkhat_or_latest):<10}', f'{str(opposite_put):<10} ',f'{opposite_put.get_cost_to_buy(  self.sarkhat_or_latest):<10}')
        print("===========================================")


    def __calculate_total_cost(self, call_op, put_op):
        if(put_op.get_cost_to_buy() == 0):
            return None
        if(self.put_prev.get_cost_to_buy() == 0):
            return None
        return self.call_prev.get_cost_to_buy() - self.put_prev.get_cost_to_sell(False) - call_op.get_cost_to_sell(False) + put_op.get_cost_to_buy()
        
    def __calculate_expected_return(self, call_op, put_op):
        strike = call_op.get_strike_price()
        strike_prev = self.call_prev.get_strike_price()
        return  self.call_prev.get_value_at_price(strike_prev) - self.put_prev.get_value_at_price(strike_prev) - call_op.get_value_at_price(strike) + put_op.get_value_at_price(strike)