from Tseapp import Tseapp
from flask import Flask, redirect, url_for, render_template, request

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
    min_return = float(information["min_Return"]) if information != None else 0
    min_days_to_mature = int(information["min_days_to_mature"]) if information != None else 0
    min_ROI = float(information["min_ROI"]) if information != None else 0
    print(min_return,min_days_to_mature, min_ROI )
    print(information)
    results = the_app.get_arbitrage_filter(min_return,min_days_to_mature,min_ROI)
    return render_template('arbitrage.html', results=results, min_return = min_return,  min_days_to_mature = min_days_to_mature,min_ROI =min_ROI) 



if __name__ == '__main__':
    app.run(host='192.168.1.50')