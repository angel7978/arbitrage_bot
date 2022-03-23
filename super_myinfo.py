# -*- coding: utf-8 -*-

import ccxt
import json


class MyInfo:
    exchange = None

    balance = {}

    title = ''
    access_key = ''
    secret_key = ''
    commission = 0
    min_profit = 0
    min_trade_amount = 0

    def isUnderMinCap(self, base_coin, min_cap):
        return min_cap < self.min_trade_amount

    def getCommission(self, ticker):
        return self.commission

    def getBalance(self, coin):
        if coin not in self.balance:
            return 0
        return self.balance[coin]

    def updateBalance(self):
        ret = self.exchange.fetch_balance()
        for row in ret.keys():
            if type(ret[row]) is not dict or 'free' not in ret[row].keys():
                continue
            self.balance[row] = float(ret[row]['free'])

    def buyCoin(self, ticker, price, volume, immediately=False):
        if immediately:
            order = self.exchange.create_market_buy_order(ticker, volume)
        else:
            order = self.exchange.create_limit_buy_order(ticker, volume, price)
        return order

    def sellCoin(self, ticker, price, volume, immediately=False):
        if immediately:
            order = self.exchange.create_market_sell_order(ticker, volume)
        else:
            order = self.exchange.create_limit_sell_order(ticker, volume, price)
        return order

    def cancelOrder(self, orderid, ticker):
        resp = self.exchange.cancel_order(orderid, ticker)
        return resp

    def getOrder(self, orderid, ticker):
        resp = self.exchange.fetch_order(orderid, ticker)
        return resp

    @staticmethod
    def getId(order):
        return order['id']

    @staticmethod
    def isFinished(order):
        return order['status'] == 'closed'

    @staticmethod
    def getContractAmount(order):
        return order['amount']

    @staticmethod
    def getContractAverage(order):
        return order['average']

    @staticmethod
    def getContractCost(order):
        return order['cost']

    @staticmethod
    def getContractFee(order):
        return order['fee']['cost']


'''
order {'info': {'symbol': 'XRPBNB', 'orderId': 2312440, 'clientOrderId': 'Pwt2z5PXjqsblNbFXNh6tp', 'transactTime': 1535465088497, 'price': '0.03000000', 'origQty': '50.00000000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY'}, 'id': '2312440', 'timestamp': 1535465088497, 'datetime': '2018-08-28T14:04:48.497Z', 'lastTradeTimestamp': None, 'symbol': 'XRP/BNB', 'type': 'limit', 'side': 'buy', 'price': 0.03, 'amount': 50.0, 'cost': 0.0, 'filled': 0.0, 'remaining': 50.0, 'status': 'open', 'fee': None, 'trades': None}
'''