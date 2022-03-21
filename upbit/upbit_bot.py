# -*- coding: utf-8 -*-

from upbit import myinfo
from upbit import orderbook
import super_bot


class UpbitBot(super_bot.SuperBot):

    def getInfo(self):
        return myinfo.MyInfo()

    def getBook(self):
        return orderbook.OrderBook()

    def start(self, count):
        return super().start(count)


for thread in UpbitBot().start(1):
    thread.join()

