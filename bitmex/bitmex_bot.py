# -*- coding: utf-8 -*-

from bitmex import myinfo
from bitmex import orderbook
import super_bot


class BitmexBot(super_bot.SuperBot):
    def getInfo(self):
        return myinfo.MyInfo()

    def getBook(self):
        return orderbook.OrderBook()

    def start(self, count, simulate=False):
        return super().start(count, simulate)


for thread in BitmexBot().start(1, True):
    thread.join()
