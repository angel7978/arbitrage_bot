# -*- coding: utf-8 -*-

import ccxt
import json
import super_myinfo


class MyInfo(super_myinfo.MyInfo):
    balance = {}

    def __init__(self):
        with open('config.json') as json_file:
            json_data = json.load(json_file)
            self.title = json_data["title"]
            self.access_key = json_data["api_key"]
            self.secret_key = json_data["secret_key"]
            self.commission = float(json_data["commission"])
            self.min_profit = float(json_data["min_profit"])
            self.min_trade_amount = float(json_data["min_trade_amount"])

        self.exchange = ccxt.bitmex({
            'apiKey': self.access_key,
            'secret': self.secret_key
        })

'''
order {'info': {'symbol': 'XRPBNB', 'orderId': 2312440, 'clientOrderId': 'Pwt2z5PXjqsblNbFXNh6tp', 'transactTime': 1535465088497, 'price': '0.03000000', 'origQty': '50.00000000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY'}, 'id': '2312440', 'timestamp': 1535465088497, 'datetime': '2018-08-28T14:04:48.497Z', 'lastTradeTimestamp': None, 'symbol': 'XRP/BNB', 'type': 'limit', 'side': 'buy', 'price': 0.03, 'amount': 50.0, 'cost': 0.0, 'filled': 0.0, 'remaining': 50.0, 'status': 'open', 'fee': None, 'trades': None}
'''