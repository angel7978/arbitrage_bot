# -*- coding: utf-8 -*-

from binance import myinfo
from binance import orderbook
import super_bot


class BinanceBot(super_bot.SuperBot):
    def getInfo(self):
        return myinfo.MyInfo()

    def getBook(self):
        return orderbook.OrderBook()

    def start(self, count):
        return super().start(count)


for thread in BinanceBot().start(1):
    thread.join()
