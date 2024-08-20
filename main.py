from Tseapp import Tseapp
from flask import Flask, redirect, url_for, render_template, request
import unicodedata

app = Flask(__name__)

the_app = Tseapp()

@app.route("/")
def hello_world():
    return render_template('index.html') 


@app.route("/arbitrage", methods=['POST'])
def arbitrage():
    information = None
    if request.method == "POST":
        information = request.form
    min_return = float(information["ar_min_Return"]) if information != None else 0
    min_days_to_mature = int(information["ar_min_days_to_mature"]) if information != None else 0
    min_ROI = float(information["ar_min_ROI"]) if information != None else 0
    
    results = the_app.get_arbitrage_filter(min_return,min_days_to_mature,min_ROI)
    
    return render_template('arbitrage.html', results=results, min_return = min_return,  min_days_to_mature = min_days_to_mature,min_ROI =min_ROI) 


@app.route("/covered_call", methods=['POST'])
def covered_call():
    information = None
    if request.method == "POST":
        information = request.form
    max_risk = float(information["cc_max_risk"]) if information != None else 0
    min_days_to_mature = int(information["cc_min_days_to_mature"]) if information != None else 0
    min_ROI = float(information["cc_min_ROI"]) if information != None else 0
    
    results = the_app.get_covered_call_filter(max_risk,min_days_to_mature,min_ROI)
    
    return render_template('covered_call.html', results=results, max_risk = max_risk,  min_days_to_mature = min_days_to_mature,min_ROI =min_ROI) 

@app.route("/protective_put", methods=['POST'])
def protective_put():
    information = None
    if request.method == "POST":
        information = request.form
    min_dif = float(information["pp_min_dif"]) if information != None else 0
    max_dif = float(information["pp_max_dif"]) if information != None else 0
    min_days_to_mature = int(information["pp_min_days_to_mature"]) if information != None else 0
    min_ROI = float(information["pp_min_ROI"]) if information != None else 0
    
    results = the_app.get_protective_put_filter(min_dif,max_dif, min_ROI,min_days_to_mature)
    
    return render_template('protective_put.html', results=results, min_dif = min_dif, max_dif = max_dif,  min_days_to_mature = min_days_to_mature,min_ROI =min_ROI) 


@app.route("/positions")
def positions():
    information = None
    
    results = the_app.get_current_positions_State()
    
    return render_template('positions.html', results=results) 


@app.route("/add_covered_call_position", methods=["POST"])
def add_covered_call_position():
    information = None
    if request.method == "POST":
        information = request.form
    volume = float(information["cc_volume"]) if information != None else 0
    call_price = int(information["cc_call_price"]) if information != None else 0
    call_name=  str(information["cc_call_name"]) if information != None else 0

    ua_price = float(information["cc_ua_price"]) if information != None else 0
    days_to_mature = int(information["cc_days_to_mature"]) if information != None else 0
    the_app.add_covered_Call_position(call_name, volume, ua_price, call_price, days_to_mature)
    return redirect("/positions")

@app.route("/save_portfolio", methods=["POST"])
def save_portfolio():
    the_app.save_portfolio()
    return redirect("/positions")


app.config['JSON_AS_ASCII'] = True

if __name__ == '__main__':
    # app.run(host='192.168.1.53')
    app.run()
    
    
