# -*- coding: utf-8 -*-

import pyupbit
import json


class MyInfo:
    balance = {}

    def __init__(self):
        with open('config.json') as json_file:
            json_data = json.load(json_file)
            self.access_key = json_data["access_key"]
            self.secret_key = json_data["secret_key"]
            self.commission_krw = float(json_data["commission_krw"])
            self.commission = float(json_data["commission"])
            self.min_profit = float(json_data["min_profit"])
            self.min_trade_amount_krw = float(json_data["min_trade_amount_krw"])
            self.min_trade_amount = float(json_data["min_trade_amount"])

        self.upbit = pyupbit.Upbit(self.access_key, self.secret_key)

    def isUnderMinCap(self, base_coin, min_cap):
        if base_coin == 'KRW' and min_cap < self.min_trade_amount_krw:
            return True
        elif base_coin != 'KRW' and min_cap < self.min_trade_amount:
            return True
        return False

    def getCommission(self, ticker):
        return self.commission_krw if 'KRW' in ticker else self.commission

    def getBalance(self, coin):
        return self.balance[coin]

    def updateBalance(self):
        ret = self.upbit.get_balances()
        for row in ret:
            self.balance[row['currency']] = float(row['balance'])

    def buyCoin(self, ticker, price, volume, immediately=False):
        if immediately:
            ret = self.upbit.buy_limit_order(ticker, price * 2, volume)
        else:
            ret = self.upbit.buy_limit_order(ticker, price, volume)
        return ret

    def sellCoin(self, ticker, price, volume, immediately=False):
        if immediately:
            ret = self.upbit.sell_market_order(ticker, volume)
        else:
            ret = self.upbit.sell_limit_order(ticker, price, volume)
        return ret

    def cancelOrder(self, uuid):
        return self.upbit.cancel_order(uuid)

    def getOrder(self, uuid):
        return self.upbit.get_order(uuid)

    def getId(self, order):
        return order['uuid']

    def isFinished(self, order):
        return order['state'] == 'done'

info = MyInfo()
'''
ret = info.buyCoin('BTC-ARK', 0.00002106, 50)
print(ret)
for i in range(3):
    print(info.getOrder(ret['uuid']))
'''

'''
upbit = pyupbit.Upbit(access_key, secret_key)
print(upbit.get_balances())  # ([{'currency': 'KRW', 'balance': '999106.81706142', 'locked': '0.0', 'avg_krw_buy_price': '0', 'modified': False}], {'group': 'default', 'min': 1799, 'sec': 29})

ret = upbit.buy_limit_order("KRW-XRP", 105, 100)  # price, amount # 8 per sec, 200 per min
print(ret)  # {'uuid': '935afbdc-0fc5-445e-a7ea-af7a9828277e', 'side': 'bid', 'ord_type': 'limit', 'price': '3900.0', 'state': 'wait', 'market': 'KRW-SAND', 'created_at': '2022-03-20T01:16:23+09:00', 'volume': '10.0', 'remaining_volume': '10.0', 'reserved_fee': '19.5', 'remaining_fee': '19.5', 'paid_fee': '0.0', 'locked': '39019.5', 'executed_volume': '0.0', 'trades_count': 0}

ret = upbit.sell_limit_order("KRW-XRP", 1000, 20)
print(ret)  # {'uuid': '1d087688-2125-40b9-a365-00f62be37310', 'side': 'ask', 'ord_type': 'limit', 'price': '3895.0', 'state': 'done', 'market': 'KRW-SAND', 'created_at': '2022-03-20T01:18:31+09:00', 'volume': '10.0', 'remaining_volume': '0.0', 'reserved_fee': '0.0', 'remaining_fee': '0.0', 'paid_fee': '19.475', 'locked': '0.0', 'executed_volume': '10.0', 'trades_count': 1, 'trades': [{'market': 'KRW-SAND', 'uuid': '6bb39640-fe44-40cb-b921-f14f598d1d34', 'price': '3895.0', 'volume': '10.0', 'funds': '38950.0', 'created_at': '2022-03-20T01:18:32+09:00', 'side': 'ask'}]}

ret = upbit.cancel_order('cc52be46-1000-4126-aee7-9bfafb867682')
print(ret)  # 

ret = upbit.get_order('5be8b52d-da1d-4bbd-9358-b8592ce2dca4')
print(ret)  # {'uuid': '935afbdc-0fc5-445e-a7ea-af7a9828277e', 'side': 'bid', 'ord_type': 'limit', 'price': '3900.0', 'state': 'done', 'market': 'KRW-SAND', 'created_at': '2022-03-20T01:16:23+09:00', 'volume': '10.0', 'remaining_volume': '0.0', 'reserved_fee': '19.5', 'remaining_fee': '0.0', 'paid_fee': '19.5', 'locked': '0.0', 'executed_volume': '10.0', 'trades_count': 1, 'trades': [{'market': 'KRW-SAND', 'uuid': 'a02eced7-691c-407a-b54b-cd0317018d9e', 'price': '3900.0', 'volume': '10.0', 'funds': '39000.0', 'created_at': '2022-03-20T01:16:23+09:00', 'side': 'bid'}]}
'''