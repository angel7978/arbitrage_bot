# -*- coding: utf-8 -*-

from bitmart import myinfo
from bitmart import orderbook
import super_bot


class BitmartBot(super_bot.SuperBot):
    def getInfo(self):
        return myinfo.MyInfo()

    def getBook(self):
        return orderbook.OrderBook()

    def start(self, count, simulate=False):
        return super().start(count, simulate)


for thread in BitmartBot().start(1):
    thread.join()
# 170.13636701 (USDT)
# 169.78000000 (USDC)

