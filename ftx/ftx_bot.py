# -*- coding: utf-8 -*-

from ftx import myinfo
from ftx import orderbook
import super_bot


class FTXBot(super_bot.SuperBot):
    def getInfo(self):
        return myinfo.MyInfo()

    def getBook(self):
        return orderbook.OrderBook()

    def start(self, count, simulate=False):
        return super().start(count, simulate)


for thread in FTXBot().start(1):
    thread.join()
# 170.02 USD
# 168.78 USDT

