



class Filter:
    

    def apply_filter(self, stocks_list, call_options_list, put_options_list):
        pass

    def get_roi(self, non_roi_return, duration):
        if(duration+1 <= 0 ):
            return -100
        return (pow((1 + (non_roi_return/100))+ 0.000001, 365/(duration+1)) -1)*100

    def sort_results_by(self, key, results):
        for i in range(len(results)):
            for j in range(i, len(results)):
                if(results[i][key] < results[j][key]):
                    tmp = results[i]
                    results[i] = results[j]
                    results[j] = tmp
        return results

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
        results = []
        for call_op in call_options_list:
            try:
                underlying_asset = call_op.get_underlying_asset()
                total_cost = self.__calculate_total_cost(call_op, underlying_asset)
                expected_return = self.__calculate_expected_return(call_op, underlying_asset)
                if(total_cost == 0):
                    continue
                profit_percentage = (expected_return / total_cost - 1) * 100
                roi = self.get_roi(profit_percentage, call_op.get_days_till_maturity())
                confidence_interval = self.__calculte_confidence_interval(call_op, underlying_asset)

                if(confidence_interval > self.min_confidence_interval and roi > self.min_roi and call_op.get_days_till_maturity() > self.min_day_to_mature  ):
                    the_result = {"max_risk": round(confidence_interval, 1),"mature": call_op.get_days_till_maturity(), "roi":round(roi,1), "call_name": str(call_op),  "call_price":call_op.get_cost_to_sell( False, self.sarkhat_or_latest), "ua_price":round(underlying_asset.get_cost(self.sarkhat_or_latest), 0)}
                    results.append(the_result)
                    print(f'{str(call_op):<15}','roi=',  round(roi, 1), '    confidence interval = ', round(confidence_interval, 1), '  ua price = ', underlying_asset.get_cost(self.sarkhat_or_latest), '      optoins price = ', call_op.get_cost_to_sell( False, self.sarkhat_or_latest))
        
            except  OverflowError as err:
                print(err)
        print("===========================================")
        return self.sort_results_by('roi', results)

            

    def __calculate_total_cost(self, call_option, underlying_asset):
        return  underlying_asset.get_cost(self.sarkhat_or_latest) - call_option.get_cost_to_sell( False, self.sarkhat_or_latest)

    def __calculate_expected_return(self, call_option, underlying_asset):
        strike = call_option.get_strike_price()
        return underlying_asset.get_value_at_price(strike) - call_option.get_value_at_price(strike)
    
    def __calculte_confidence_interval(self, call_option, underlying_asset):
        return (1- call_option.get_strike_price() / (underlying_asset.get_cost(self.sarkhat_or_latest)+ 0.0001)) * 100
    


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

        return self.sort_results_by('roi', results)



    def __calculate_total_cost(self, call_op, put_op, underlying_asset):
        if(put_op.get_cost_to_buy() == 0):
            return None
        return underlying_asset.get_cost(self.sarkhat_or_latest) - call_op.get_cost_to_sell(False) + put_op.get_cost_to_buy()
        
    def __calculate_expected_return(self, call_op, put_op, underlying_asset):
        strike = call_op.get_strike_price()
        return underlying_asset.get_value_at_price(strike) - call_op.get_value_at_price(strike) + put_op.get_value_at_price(strike)
    

class Protective_Put_Filter(Filter):
    def __init__(self, _min_diff, _max_diff, _min_days_to_mature, _min_roi, _sarkhat_or_latest = 'sarkhat'):
        super().__init__()
        self.min_diff = _min_diff
        self.max_diff = _max_diff
        self.min_days_to_mature = _min_days_to_mature
        self.min_roi = _min_roi
        self.sarkhat_or_latest = _sarkhat_or_latest
    
    def apply_filter(self, stocks_list, call_options_list, put_options_list):
        print("===========================================")
        print("Protective put filter result for these specs:")
        print("minimum ROI=", self.min_roi)
        print("min and max differnce:", self.min_diff, self.max_diff)
        print("minimum days to mature= ", self.min_days_to_mature)
        print("-------------------------------------------")
        results = []
        for put_op in put_options_list:
            underlying_asset = put_op.get_underlying_asset()

            total_cost = self.__calculate_total_cost(put_op, underlying_asset)
            if(total_cost == None):
                continue
            min_expected_return = self.__calculate_expected_return(put_op, underlying_asset)
            profit_percentage = (min_expected_return / total_cost - 1) * 100
            roi = self.get_roi(profit_percentage, put_op.get_days_till_maturity())

            difference = self.__calculate_difference_to_strike(put_op, underlying_asset)

            if(roi >= self.min_roi and difference >= self.min_diff and difference <= self.max_diff  and put_op.get_days_till_maturity() > self.min_days_to_mature):
                the_result = {"difference": round(difference, 1),"mature": put_op.get_days_till_maturity(), "roi":round(roi,1), "put_name": str(put_op), "put_price": put_op.get_cost_to_buy(  self.sarkhat_or_latest), "ua_price":round(underlying_asset.get_cost(self.sarkhat_or_latest), 0)}
                results.append(the_result)
                print('difference=',  f'{round(difference, 1):<5}','ROi=',f'{round(roi,1):<6}',  'days=',f'{put_op.get_days_till_maturity():<4}', f'{str(put_op):<10} ',f'{put_op.get_cost_to_buy(  self.sarkhat_or_latest):<10}','  ua price = ',f'{round(underlying_asset.get_cost(self.sarkhat_or_latest), 0):<7}')
        print("===========================================")

        return self.sort_results_by('roi', results)



    def __calculate_total_cost(self, put_op, underlying_asset):
        if(put_op.get_cost_to_buy() <=0):
            return None
        return underlying_asset.get_cost(self.sarkhat_or_latest) + put_op.get_cost_to_buy()
        
    def __calculate_expected_return(self, put_op, underlying_asset):
        strike = put_op.get_strike_price()
        return underlying_asset.get_value_at_price(strike) + put_op.get_value_at_price(strike)
    
    def __calculate_difference_to_strike(self, put_op, underlyting_asset):
        return (put_op.get_strike_price() / underlyting_asset.get_cost(self.sarkhat_or_latest) - 1) * 100