# -*- coding: utf-8 -*-

from ascendex import myinfo
from ascendex import orderbook
import super_bot


class AscendexBot(super_bot.SuperBot):
    def getInfo(self):
        return myinfo.MyInfo()

    def getBook(self):
        return orderbook.OrderBook()

    def start(self, count, simulate=False):
        return super().start(count, simulate)


for thread in AscendexBot().start(1):
    thread.join()
# 161.94 USDT

