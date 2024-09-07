


class Stock:
    def __init__(self, _ticker, _full_name, _close, _high, _low, _last, _volume, _best_kharid, _best_foroosh, _spread):
        self.ticker = _ticker
        self.full_name = _full_name
        self.close = _close
        self.high = _high
        self.low = _low
        self.last = _last
        self.volume = _volume
        self.best_kharid = _best_kharid
        self.best_foroosh = _best_foroosh
        self.spread = _spread

    def check_name(self, chosen_ticker):
        if(chosen_ticker == self.ticker):
            return True
        return False

    def get_close_price(self):
        return self.close
    
    def get_cost(self, sarkhat_or_latest = 'sarkhat'):
        return (self.best_foroosh if sarkhat_or_latest == 'sarkhat' else self.last) * (1+self.spread/100)
    
    def get_cost_to_sell(self, sarkhat_or_latest = 'sarkhat'):
        return (self.best_kharid if sarkhat_or_latest == 'sarkhat' else self.last) 
  
    def get_value_at_price(self, final_price):
        return final_price
       

    def __repr__(self) -> str:
        return self.ticker