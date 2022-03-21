# -*- coding: utf-8 -*-

import telegram_module
import threading
import math
import json
import traceback
from abc import *


class SuperBot(metaclass=ABCMeta):

    def __init__(self):
        self.info = self.getInfo()
        self.book = self.getBook()
        self.telegram = telegram_module.Telegram()

    @abstractmethod
    def getInfo(self):
        pass

    @abstractmethod
    def getBook(self):
        pass

    def start(self, count):
        thread_list = []

        for repeat in range(count):  # API call 횟수 제한 보고 thread 늘릴지 결정, 지금은 2가 적당
            t = threading.Thread(target=self.run)
            t.daemon = True
            t.start()
            thread_list.append(t)

        return thread_list

    def run(self):
        chain = ''
        step = 1
        self.info.updateBalance()

        while True:
            try:
                chain = self.book.getNextChain(step)

                base_coin, profit, cap_arr, profit_log = self.getProfit(chain)

                if profit >= self.info.min_profit:
                    max_volume, cap_log = self.getMaxVolume(base_coin, self.info.getBalance(base_coin), cap_arr)
                    if max_volume > 0:
                        print(profit_log + cap_log)
                        self.progressChain(max_volume, chain)
                        step = 0
                        self.info.updateBalance()
                        continue

                step = 1
            except json.decoder.JSONDecodeError:
                pass
            except IndexError:
                self.book.removeChain(chain)
                step = 0
            except Exception as e:
                print('%s %s' % (chain, e))
                traceback.print_exc()

    def floor(self, num):
        return math.floor(num * 100000000) / 100000000

    def getProfit(self, chain):
        basic_coin = chain.split('-')[0]
        log = '체인 검증 : %s / 기준 : %s' % (chain, basic_coin)
        basic_amount = 10000000 if 'KRW' in chain else 10000
        current_amount = basic_amount
        chain_arr = chain.split('-')
        cap_arr = []

        for i in range(len(chain_arr) - 1):
            ticker = self.book.getTicker(chain_arr[i], chain_arr[i + 1])

            bid_position = self.book.isBidPosition(ticker)
            if not bid_position:
                ticker = self.book.getTicker(chain_arr[i + 1], chain_arr[i])

            ask_price, ask_volume, bid_price, bid_volume = self.book.getClosedOrderBook(ticker)

            commission = self.info.getCommission(ticker)
            if bid_position:
                # order to ask price/volume
                amount = self.floor(current_amount * (1 - commission) / ask_price)
                cap_arr.append({
                    'cap': self.floor(ask_price * ask_volume),
                    'coin': chain_arr[i]
                })
                log += '\n  매수 : %s %.8f (%.8f %s) -> (%.8f %s), 캡 %.8f %s, 수수료 : %.8f %s' % (
                    ticker, ask_price, current_amount, chain_arr[i], amount, chain_arr[i + 1],
                    self.floor(ask_price * ask_volume), chain_arr[i],
                    self.floor(current_amount * commission), chain_arr[i])
            else:
                # order to bid price/volume
                amount = self.floor((current_amount * bid_price) * (1 - commission))
                cap_arr.append({
                    'cap': self.floor(bid_price * bid_volume),
                    'coin': chain_arr[i + 1]
                })
                log += '\n  매도 : %s %.8f (%.8f %s) -> (%.8f %s), 캡 %.8f %s, 수수료 : %.8f %s' % (
                    ticker, bid_price, current_amount, chain_arr[i], self.floor(current_amount * bid_price),
                    chain_arr[i + 1], self.floor(bid_price * bid_volume), chain_arr[i + 1],
                    self.floor((current_amount * bid_price) * commission), chain_arr[i + 1])

            current_amount = amount
            log += '\n    현재 수량 %.8f %s' % (current_amount, chain_arr[i + 1])

        profit_rate = current_amount / basic_amount - 1
        log += '\n최종 이익률 %.2f%%\n' % (profit_rate * 100)

        return basic_coin, profit_rate, cap_arr, log

    def getMaxVolume(self, base_coin, init_balance, cap_arr):
        min_cap = init_balance
        log = '최초 캡 : %.8f %s' % (min_cap, base_coin)

        for dic in cap_arr:
            if dic['coin'] != base_coin:
                ticker = self.book.getTicker(dic['coin'], base_coin)
                price = self.book.getPrice(ticker)
                cap = self.floor(dic['cap'] * price)

                log += '\n  캡 : %.8f %s -> %.8f %s' % (dic['cap'], dic['coin'], cap, base_coin)
            else:
                cap = dic['cap']
                log += '\n  캡 : %.8f %s' % (dic['cap'], dic['coin'])

            if cap < min_cap:
                min_cap = cap

        log += '\n최종 캡 : %.8f %s\n' % (min_cap, base_coin)
        if self.info.isUnderMinCap(base_coin, min_cap):
            return 0, log

        return min_cap, log

    def progressChain(self, start_amount, chain):
        basic_coin = chain.split('-')[0]
        print('체인 시작 : %s / 기준 : %s' % (chain, basic_coin))
        basic_amount = start_amount
        current_amount = basic_amount
        chain_arr = chain.split('-')

        for i in range(len(chain_arr) - 1):
            ticker = self.book.getTicker(chain_arr[i], chain_arr[i + 1])

            bid_position = self.book.isBidPosition(ticker)
            if not bid_position:
                ticker = self.book.getTicker(chain_arr[i + 1], chain_arr[i])

            ask_price, ask_volume, bid_price, bid_volume = self.book.getClosedOrderBook(ticker, True)

            commission = self.info.getCommission(ticker)
            if bid_position:
                # order to ask price/volume
                amount = self.floor(current_amount * (1 - commission) / ask_price)
                print('  매수 예상 : %s %.8f (%.8f %s) -> (%.8f %s), 캡 %.8f %s, 수수료 : %.8f %s' % (
                    ticker, ask_price, current_amount, chain_arr[i], amount, chain_arr[i + 1],
                    self.floor(ask_price * ask_volume), chain_arr[i],
                    self.floor(current_amount * commission), chain_arr[i]))

                ret = self.info.buyCoin(ticker, ask_price, amount, i == len(chain_arr) - 2)
                order_id = self.info.getId(ret)
                if not self.info.isFinished(ret):
                    for j in range(10):
                        ret = self.info.getOrder(order_id)
                        if self.info.isFinished(ret):
                            break
                if not self.info.isFinished(ret):
                    print('  매수 실패 : %s' % ret)
                    self.info.cancelOrder(order_id)
                    self.telegram.sendTelegramPush('매수 실패, 체인 %s, 현재 단계 %s' % (chain, ticker))
                    return
                else:
                    print('  매수 성공 : %s' % ret)
            else:
                # order to bid price/volume
                amount = self.floor((current_amount * bid_price) * (1 - commission))
                print('  매도 예상 : %s %.8f (%.8f %s) -> (%.8f %s), 캡 %.8f %s, 수수료 : %.8f %s' % (
                    ticker, bid_price, current_amount, chain_arr[i], self.floor(current_amount * bid_price),
                    chain_arr[i + 1], self.floor(bid_price * bid_volume), chain_arr[i + 1],
                    self.floor((current_amount * bid_price) * commission), chain_arr[i + 1]))

                ret = self.info.sellCoin(ticker, bid_price, current_amount, i == len(chain_arr) - 2)
                order_id = self.info.getId(ret)
                if not self.info.isFinished(ret):
                    for j in range(10):
                        ret = self.info.getOrder(order_id)
                        if self.info.isFinished(ret):
                            break
                if not self.info.isFinished(ret):
                    print('  매도 실패 : %s' % ret)
                    self.info.cancelOrder(order_id)
                    self.telegram.sendTelegramPush('매도 실패, 체인 %s, 현재 단계 %s' % (chain, ticker))
                    return
                else:
                    print('  매도 성공 : %s' % ret)

            current_amount = amount
            print('    현재 수량 %.8f %s' % (current_amount, chain_arr[i + 1]))

        profit_rate = current_amount / basic_amount - 1
        print('최종 이익 %.8f, 이익률 %.2f%%\n' % (current_amount - start_amount, profit_rate * 100))

        self.telegram.sendTelegramPush('최종 이익 %.8f, 이익률 %.2f%%' % (current_amount - start_amount, profit_rate * 100))

