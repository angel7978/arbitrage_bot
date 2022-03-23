# -*- coding: utf-8 -*-

import pyupbit
import time;


class OrderBook:
    idx = 0
    chain_list = []
    book_archive = {}

    def __init__(self):
        self.krw_tickers = pyupbit.get_tickers(fiat="KRW")
        self.btc_tickers = pyupbit.get_tickers(fiat="BTC")
        self.usdt_tickers = pyupbit.get_tickers(fiat="USDT")

        # make triangle chain (KRW-BTC-XXX-KRW) and (KRW-XXX-BTC-KRW)
        for ticker in self.btc_tickers:
            coin_name = ticker.split('-')[1]
            replace_ticker = ticker.replace('BTC', 'KRW')
            if replace_ticker in self.krw_tickers:
                chain = 'KRW-BTC-' + coin_name + '-KRW'
                self.chain_list.append(chain)
                # print(chain)

                chain = 'KRW-' + coin_name + '-BTC-KRW'
                self.chain_list.append(chain)
                # print(chain)

        # make triangle chain (USDT-BTC-XXX-USDT) and (USDT-XXX-BTC-USDT)
        for ticker in self.btc_tickers:
            coin_name = ticker.split('-')[1]
            replace_ticker = ticker.replace('BTC', 'USDT')
            if replace_ticker in self.usdt_tickers:
                chain = 'USDT-BTC-' + coin_name + '-USDT'
                self.chain_list.append(chain)
                # print(chain)

                chain = 'USDT-' + coin_name + '-BTC-USDT'
                self.chain_list.append(chain)
                # print(chain)

        print('chain count : %d' % len(self.chain_list))

    def getTicker(self, base_coin, target_coin):
        return base_coin + '-' + target_coin

    def getPrice(self, ticker):
        return pyupbit.get_current_price(ticker)

    def getClosedOrderBook(self, ticker, forced=False):
        ms = time.time() * 1000.0
        if ticker not in self.book_archive:
            self.book_archive[ticker] = {
                'time': 0,
                'data': ''
            }

        book_data = self.book_archive[ticker]
        if not forced and ms < book_data['time'] + 1000:
            closed_bids_asks = book_data['data']
        else:
            orderbook = pyupbit.get_orderbook(ticker)
            closed_bids_asks = orderbook['orderbook_units'][0]
            self.book_archive[ticker] = {
                'time': ms,
                'data': closed_bids_asks
            }

        return closed_bids_asks['ask_price'], closed_bids_asks['ask_size'], closed_bids_asks['bid_price'], closed_bids_asks['bid_size']

    def removeChain(self, chain):
        self.chain_list.remove(chain)

    def getNextChain(self, step=1):
        self.idx = (self.idx + step) % len(self.chain_list)
        return self.chain_list[self.idx]

    def isBidPosition(self, ticker):
        return ticker in self.krw_tickers or ticker in self.btc_tickers or ticker in self.usdt_tickers




'''
print(pyupbit.Upbit)

tickers = pyupbit.get_tickers()
print(tickers)  # ['KRW-BTC', 'KRW-ETH', 'BTC-ETH', 'BTC-LTC', 'BTC-XRP', 'BTC-ETC', 'BTC-OMG', 'BTC-CVC', 'BTC-DGB', 'BTC-SC', 'BTC-SNT', 'BTC-WAVES', 'BTC-NMR', 'BTC-XEM', 'BTC-QTUM', 'BTC-BAT', 'BTC-LSK', 'BTC-STEEM', 'BTC-DOGE', 'BTC-BNT', 'BTC-XLM', 'BTC-ARDR', 'BTC-ARK', 'BTC-STORJ', 'BTC-GRS', 'BTC-REP', 'BTC-RLC', 'USDT-BTC', 'USDT-ETH', 'USDT-LTC', 'USDT-XRP', 'USDT-ETC', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-ADA', 'BTC-ADA', 'BTC-MANA', 'USDT-OMG', 'KRW-SBD', 'BTC-SBD', 'KRW-POWR', 'BTC-POWR', 'KRW-BTG', 'USDT-ADA', 'BTC-DNT', 'BTC-ZRX', 'BTC-TRX', 'BTC-TUSD', 'BTC-LRC', 'KRW-ICX', 'KRW-EOS', 'USDT-TUSD', 'KRW-TRX', 'BTC-POLY', 'USDT-SC', 'USDT-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'BTC-BCH', 'USDT-BCH', 'KRW-BCH', 'BTC-MFT', 'BTC-LOOM', 'KRW-BAT', 'KRW-IOST', 'BTC-RFR', 'KRW-RFR', 'USDT-DGB', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'BTC-RVN', 'BTC-GO', 'BTC-UPP', 'BTC-ENJ', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'BTC-MTL', 'KRW-UPP', 'KRW-ELF', 'USDT-DOGE', 'USDT-ZRX', 'USDT-RVN', 'USDT-BAT', 'KRW-KNC', 'BTC-MOC', 'BTC-ZIL', 'KRW-BSV', 'BTC-BSV', 'BTC-IOST', 'KRW-THETA', 'BTC-DENT', 'KRW-QKC', 'BTC-ELF', 'KRW-BTT', 'BTC-IOTX', 'BTC-SOLVE', 'BTC-NKN', 'BTC-META', 'KRW-MOC', 'BTC-ANKR', 'BTC-CRO', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'BTC-ORBS', 'BTC-AERGO', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'BTC-ATOM', 'BTC-STPT', 'KRW-MBL', 'BTC-EOS', 'BTC-LUNA', 'BTC-DAI', 'BTC-MKR', 'BTC-BORA', 'KRW-WAXP', 'BTC-WAXP', 'KRW-HBAR', 'KRW-MED', 'BTC-MED', 'BTC-MLK', 'KRW-MLK', 'KRW-STPT', 'BTC-VET', 'KRW-ORBS', 'BTC-CHZ', 'KRW-VET', 'BTC-FX', 'BTC-OGN', 'KRW-CHZ', 'BTC-XTZ', 'BTC-HIVE', 'BTC-HBD', 'BTC-OBSR', 'BTC-DKA', 'KRW-STMX', 'BTC-STMX', 'BTC-AHT', 'BTC-PCI', 'KRW-DKA', 'BTC-LINK', 'KRW-HIVE', 'KRW-KAVA', 'BTC-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'BTC-JST', 'BTC-CHR', 'BTC-DAD', 'BTC-TON', 'KRW-JST', 'BTC-CTSI', 'BTC-DOT', 'KRW-CRO', 'BTC-COMP', 'BTC-SXP', 'BTC-HUNT', 'KRW-TON', 'BTC-ONIT', 'BTC-CRV', 'BTC-ALGO', 'BTC-RSR', 'KRW-SXP', 'BTC-OXT', 'BTC-PLA', 'KRW-HUNT', 'BTC-MARO', 'BTC-SAND', 'BTC-SUN', 'KRW-PLA', 'KRW-DOT', 'BTC-SRM', 'BTC-QTCON', 'BTC-MVL', 'KRW-SRM', 'KRW-MVL', 'BTC-REI', 'BTC-AQT', 'BTC-AXS', 'BTC-STRAX', 'KRW-STRAX', 'KRW-AQT', 'BTC-GLM', 'KRW-GLM', 'BTC-FCT2', 'BTC-SSX', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', 'BTC-FIL', 'BTC-UNI', 'BTC-BASIC', 'BTC-INJ', 'BTC-PROM', 'BTC-VAL', 'BTC-PSG', 'BTC-JUV', 'BTC-CBK', 'BTC-FOR', 'KRW-CBK', 'BTC-BFC', 'BTC-LINA', 'BTC-HUM', 'BTC-CELO', 'KRW-SAND', 'KRW-HUM', 'BTC-IQ', 'BTC-STX', 'KRW-DOGE', 'BTC-NEAR', 'BTC-AUCTION', 'BTC-DAWN', 'BTC-FLOW', 'BTC-STRK', 'KRW-STRK', 'BTC-PUNDIX', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-DAWN', 'KRW-AXS', 'KRW-STX', 'BTC-GRT', 'BTC-SNX', 'BTC-USDP', 'KRW-XEC', 'KRW-SOL', 'BTC-SOL', 'KRW-MATIC', 'BTC-MATIC', 'KRW-NU', 'BTC-NU', 'KRW-AAVE', 'KRW-1INCH', 'BTC-AAVE', 'BTC-1INCH', 'BTC-MASK', 'KRW-ALGO', 'BTC-AUDIO', 'KRW-NEAR', 'BTC-YGG', 'BTC-GTC', 'BTC-OCEAN', 'BTC-CTC', 'BTC-LPT', 'KRW-WEMIX', 'BTC-WEMIX', 'KRW-AVAX', 'BTC-AVAX', 'BTC-IMX', 'BTC-RNDR', 'BTC-RLY', 'KRW-T', 'BTC-T', 'KRW-CELO']

tickers = pyupbit.get_tickers(fiat="KRW")
print(tickers)  # ['KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-STRAX', 'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-DAWN', 'KRW-AXS', 'KRW-STX', 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-NU', 'KRW-AAVE', 'KRW-1INCH', 'KRW-ALGO', 'KRW-NEAR', 'KRW-WEMIX', 'KRW-AVAX', 'KRW-T', 'KRW-CELO']

price = pyupbit.get_current_price("BTC-XRP")
print("%.8f" % price)  # 0.00001923

price = pyupbit.get_current_price(["BTC-XRP", "KRW-XRP"])
print(price)  # {'BTC-XRP': 1.923e-05, 'KRW-XRP': 962.0}

orderbook = pyupbit.get_orderbook("KRW-XRP")
print(orderbook)  # {'market': 'KRW-XRP', 'timestamp': 1647605844475, 'total_ask_size': 7968820.29132141, 'total_bid_size': 7882158.52608623, 'orderbook_units': [{'ask_price': 963.0, 'bid_price': 962.0, 'ask_size': 135376.99006716, 'bid_size': 146231.84895152}, {'ask_price': 964.0, 'bid_price': 961.0, 'ask_size': 359296.15891841, 'bid_size': 559271.3269234}, {'ask_price': 965.0, 'bid_price': 960.0, 'ask_size': 207801.35308605, 'bid_size': 988201.24362968}, {'ask_price': 966.0, 'bid_price': 959.0, 'ask_size': 270516.94467568, 'bid_size': 605176.89753836}, {'ask_price': 967.0, 'bid_price': 958.0, 'ask_size': 337116.12955518, 'bid_size': 725560.41828806}, {'ask_price': 968.0, 'bid_price': 957.0, 'ask_size': 726492.68418605, 'bid_size': 297277.70050552}, {'ask_price': 969.0, 'bid_price': 956.0, 'ask_size': 470734.7378047, 'bid_size': 432033.07370768}, {'ask_price': 970.0, 'bid_price': 955.0, 'ask_size': 667823.69270081, 'bid_size': 569547.93208353}, {'ask_price': 971.0, 'bid_price': 954.0, 'ask_size': 311008.03145032, 'bid_size': 171156.48636712}, {'ask_price': 972.0, 'bid_price': 953.0, 'ask_size': 293999.59306643, 'bid_size': 207083.5376007}, {'ask_price': 973.0, 'bid_price': 952.0, 'ask_size': 249321.43289513, 'bid_size': 291774.26338741}, {'ask_price': 974.0, 'bid_price': 951.0, 'ask_size': 789207.47347897, 'bid_size': 600397.51780924}, {'ask_price': 975.0, 'bid_price': 950.0, 'ask_size': 1239696.11922387, 'bid_size': 1757910.37845602}, {'ask_price': 976.0, 'bid_price': 949.0, 'ask_size': 940838.60502241, 'bid_size': 275418.08535994}, {'ask_price': 977.0, 'bid_price': 948.0, 'ask_size': 969590.34519024, 'bid_size': 255117.81547805}]}

bids_asks = orderbook['orderbook_units'][0]
print(bids_asks)  # {'ask_price': 963.0, 'bid_price': 962.0, 'ask_size': 135376.99006716, 'bid_size': 146231.84895152}
'''