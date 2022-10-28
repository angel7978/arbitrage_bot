# -*- coding: utf-8 -*-
import socket

import ccxt
import pyupbit

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

    def start(self, count, simulate=False):
        thread_list = []

        for repeat in range(count):  # API call 횟수 제한 보고 thread 늘릴지 결정, 지금은 2가 적당
            t = threading.Thread(target=self.run, args=(simulate,))
            t.daemon = True
            t.start()
            thread_list.append(t)

        return thread_list

    def run(self, simulate=False):
        chain = ''
        step = 1
        self.info.updateBalance()

        loop = True
        while loop:
            try:
                chain = self.book.getNextChain(step)

                base_coin, profit, cap_arr, profit_log = self.getProfit(chain)

                if profit >= self.info.min_profit:
                    max_volume, cap_log = self.getMaxVolume(base_coin, self.info.getBalance(base_coin), cap_arr)
                    if simulate:
                        print(profit_log + cap_log)
                        continue

                    if max_volume > 0:
                        print(profit_log + cap_log)
                        self.progressChain(max_volume, chain)
                        step = 0
                        self.info.updateBalance()
                        continue

                step = 1
            except IndexError:
                self.book.removeChain(chain)
                step = 0
            except Exception as e:
                print('Exception %s\n%s' % (chain, e))

    def floor(self, num):
        return math.floor(num * 100000000) / 100000000

    def getProfit(self, chain):
        basic_coin = chain.split('-')[0]
        log = '체인 검증 : %s / 기준 : %s' % (chain, basic_coin)
        basic_amount = 10000
        current_amount = basic_amount
        chain_arr = chain.split('-')
        cap_arr = []

        for i in range(len(chain_arr) - 1):
            ticker = self.book.getTicker(chain_arr[i], chain_arr[i + 1])

            bid_position = self.book.isBidPosition(ticker)
            if not bid_position:
                ticker = self.book.getTicker(chain_arr[i + 1], chain_arr[i])

            ask_price, ask_volume, bid_price, bid_volume = self.book.getClosedOrderBook(ticker)
            if ask_price == 0 or bid_price == 0:
                current_amount = 0
                break

            commission = self.info.getCommission(ticker)
            if bid_position:
                # order to ask price/volume
                amount = self.floor(current_amount / ask_price)
                cap_arr.append({
                    'cap': self.floor(ask_price * ask_volume),
                    'coin': chain_arr[i]
                })
                log += '\n  매수 : %s %.8f (%.8f %s) -> (%.8f %s), 캡 %.8f %s, 수수료 : %.8f %s' % (
                    ticker, ask_price, current_amount, chain_arr[i],
                    amount * (1 - commission), chain_arr[i + 1],
                    self.floor(ask_price * ask_volume), chain_arr[i],
                    self.floor(amount * commission), chain_arr[i])

                amount *= (1 - commission)
                if self.info.isUnderMinCap(chain_arr[i + 1], ask_volume):
                    log += '\n  매수 볼륨 부족'
                    current_amount = 0
                    break
            else:
                # order to bid price/volume
                amount = self.floor((current_amount * bid_price) * (1 - commission))
                cap_arr.append({
                    'cap': self.floor(bid_price * bid_volume),
                    'coin': chain_arr[i + 1]
                })
                log += '\n  매도 : %s %.8f (%.8f %s) -> (%.8f %s), 캡 %.8f %s, 수수료 : %.8f %s' % (
                    ticker, bid_price, current_amount, chain_arr[i],
                    self.floor(current_amount * bid_price), chain_arr[i + 1],
                    self.floor(bid_price * bid_volume), chain_arr[i + 1],
                    self.floor((current_amount * bid_price) * commission), chain_arr[i + 1])
                
                if self.info.isUnderMinCap(chain_arr[i + 1], self.floor(bid_price * bid_volume)):
                    log += '\n  매도 볼륨 부족'
                    current_amount = 0
                    break

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
                ticker = self.book.getTicker(base_coin, dic['coin'])
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
            if ask_price == 0 or bid_price == 0:
                current_amount = 0
                break

            commission = self.info.getCommission(ticker)
            if bid_position:
                # order to ask price/volume
                amount = self.floor(current_amount / ask_price)
                print('  매수 예상 : %s %.8f (%.8f %s) -> (%.8f %s), 수수료 : %.8f %s' % (
                    ticker, ask_price, current_amount, chain_arr[i],
                    amount * (1 - commission), chain_arr[i + 1],
                    self.floor(amount * commission), chain_arr[i]))

                ret = self.info.buyCoin(ticker, ask_price, amount, i == len(chain_arr) - 2)
                order_id = self.info.getId(ret)
                if not self.info.isFinished(ret):
                    for j in range(10):
                        ret = self.info.getOrder(order_id, ticker)
                        if self.info.isFinished(ret):
                            break
                if not self.info.isFinished(ret):
                    print('  매수 실패 : %s' % ret)
                    self.info.cancelOrder(order_id, ticker)
                    self.telegram.sendTelegramPush(self.info.title, '체인 실패 %s' % chain, '매수 실패 %s' % ticker)

                    if i >= 1:
                        # 즉시 기준 통화로 판매
                        amount = self.floor((current_amount * bid_price) * (1 - commission))
                        self.info.sellCoin(self.book.getTicker(chain_arr[0], chain_arr[i]), 0, amount, True)
                    return
                else:
                    print('  매수 성공 : %s %.8f (%.8f %s) -> (%.8f %s), 수수료 : %.8f %s' % (
                        ticker, self.info.getContractAverage(ret), self.info.getContractCost(ret), chain_arr[i],
                        self.info.getContractAmount(ret), chain_arr[i + 1],
                        self.info.getContractFee(ret), chain_arr[i + 1]))
                    amount = self.info.getContractAmount(ret) - self.info.getContractFee(ret)
            else:
                # order to bid price/volume
                amount = self.floor((current_amount * bid_price) * (1 - commission))
                print('  매도 예상 : %s %.8f (%.8f %s) -> (%.8f %s), 수수료 : %.8f %s' % (
                    ticker, bid_price, current_amount, chain_arr[i],
                    self.floor(current_amount * bid_price), chain_arr[i + 1],
                    self.floor((current_amount * bid_price) * commission), chain_arr[i + 1]))

                ret = self.info.sellCoin(ticker, bid_price, current_amount, i == len(chain_arr) - 2)
                order_id = self.info.getId(ret)
                if not self.info.isFinished(ret):
                    for j in range(10):
                        ret = self.info.getOrder(order_id, ticker)
                        if self.info.isFinished(ret):
                            break
                if not self.info.isFinished(ret):
                    print('  매도 실패 : %s' % ret)
                    self.info.cancelOrder(order_id, ticker)
                    self.telegram.sendTelegramPush(self.info.title, '체인 실패 %s' % chain, '매도 실패 %s' % ticker)
                    if i >= 1:
                        # 즉시 기준 통화로 판매
                        self.info.sellCoin(self.book.getTicker(chain_arr[0], chain_arr[i]), 0, amount, True)
                    return
                else:
                    print('  매도 성공 : %s %.8f (%.8f %s) -> (%.8f %s), 수수료 : %.8f %s' % (
                        ticker, self.floor(self.info.getContractAverage(ret)),
                        self.info.getContractAmount(ret), chain_arr[i],
                        self.info.getContractCost(ret), chain_arr[i + 1],
                        self.info.getContractFee(ret), chain_arr[i + 1]))
                    amount = self.info.getContractCost(ret) - self.info.getContractFee(ret)

            current_amount = amount
            print('    현재 수량 %.8f %s' % (current_amount, chain_arr[i + 1]))

        profit_rate = current_amount / basic_amount - 1
        print('최종 이익 %.8f, 이익률 %.2f%%\n' % (current_amount - start_amount, profit_rate * 100))

        self.telegram.sendTelegramPush(self.info.title, '체인 성공 %s' % chain, '최종 이익 %.8f, 이익률 %.2f%%' % (current_amount - start_amount, profit_rate * 100))

