import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client 
from binance.enums import *
#--------------------- To execute the application --------
# $env:FLASK_APP = "app"
# $env:FLASK_ENV = "development"
# flask run --host=0.0.0.0
# send POST request by e.g., http://135.181.34.197:5000/webhook
# python-binance doc: https://python-binance.readthedocs.io/en/latest/
# Test the API using Insomnia App: https://insomnia.rest/
# To add Heroku CLI to Powershell: $env:Path += ";C:\Program Files\heroku\bin"
# POST request: https://binance-auto-trade-az.herokuapp.com/webhook
#---------------------------------------------------------
app = Flask(__name__)
app.debug = True
client = Client(config.API_KEY, config.API_SECRET)
#--
def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print(f"Sending order {order_type} {side} { quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("An exception occured - {}".format(e))
        return False
    return order
#--
@app.route("/")
def welcome():
    return render_template('index.html')
#--
@app.route("/webhook", methods=['POST'])
def webhook():
    #print(str(request.data))
    data = json.loads(request.data)
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return{
            "code": "error",
            "message": "Invalid passphrase"
        }
    #--
    side     = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    symbol   = data['ticker']
    order_response = order(side, quantity, symbol)
    #--
    if order_response:
        return {
            "code": "success",
            "message": "Order executed!"
        }
    else:
        print("order failed!")
        return {
            "code": "error",
            "message": "Order failed!"
        }
