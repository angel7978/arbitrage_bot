# -*- coding: utf-8 -*-

import ccxt
import time


class OrderBook:
    idx = 0
    chain_list = []
    book_archive = {}

    def __init__(self):
        self.binance = ccxt.binance()
        self.tickers = self.binance.fetch_tickers()

        base_coin = ['USDT', 'USDC', 'BUSD', 'DAI']
        for base in base_coin:
            # make triangle chain (BASE-XXX-YYY-BASE or BASE-YYY-XXX-BASE)
            for first_ticker in self.tickers:
                if ('/%s' % base) not in first_ticker:
                    continue

                first_coin_name = first_ticker.split('/')[0]

                for second_ticker in self.tickers:
                    if first_ticker == second_ticker:
                        continue

                    second_coin_name = second_ticker.replace('/', '').replace(first_coin_name, '')

                    last_ticker = self.getTicker(second_coin_name, base)
                    if last_ticker not in self.tickers:
                        continue

                    middle_ticker = self.getTicker(first_coin_name, second_coin_name)
                    middle_ticker_reverse = self.getTicker(first_coin_name, second_coin_name)
                    if middle_ticker not in self.tickers and middle_ticker_reverse not in self.tickers:
                        continue

                    # print('%s-%s-%s-%s' % (base, second_coin_name, first_coin_name, base))
                    self.chain_list.append('%s-%s-%s-%s' % (base, first_coin_name, second_coin_name, base))

                    # print('%s-%s-%s-%s' % (base, second_coin_name, first_coin_name, base))
                    self.chain_list.append('%s-%s-%s-%s' % (base, second_coin_name, first_coin_name, base))

        print('chain count : %d' % len(self.chain_list))

    def getTicker(self, base_coin, target_coin):
        return base_coin + '/' + target_coin

    def getPrice(self, ticker):
        return self.binance.fetch_ticker(ticker)['close']

    def getClosedOrderBook(self, ticker, forced=False):
        ms = time.time() * 1000.0
        if ticker not in self.book_archive:
            self.book_archive[ticker] = {
                'time': 0,
                'data': ''
            }

        book_data = self.book_archive[ticker]
        if not forced and ms < book_data['time'] + 1000:
            orderbook = book_data['data']
        else:
            orderbook = self.binance.fetch_order_book(ticker)
            self.book_archive[ticker] = {
                'time': ms,
                'data': orderbook
            }

        return orderbook['asks'][0][0], orderbook['asks'][0][1], orderbook['bids'][0][0], orderbook['bids'][0][1]

    def getNextChain(self, step=1):
        self.idx = (self.idx + step) % len(self.chain_list)
        return self.chain_list[self.idx]

    def removeChain(self, chain):
        self.chain_list.remove(chain)

    def isBidPosition(self, ticker):
        return ticker in self.tickers

'''
binance = ccxt.binance()
markets = binance.fetch_tickers()
print(markets.keys())  # dict_keys(['ETH/BTC', 'LTC/BTC', 'BNB/BTC', 'NEO/BTC', 'QTUM/ETH', 'EOS/ETH', 'SNT/ETH', 'BNT/ETH', 'BCC/BTC', 'GAS/BTC', 'BNB/ETH', 'BTC/USDT', 'ETH/USDT', 'HSR/BTC', 'OAX/ETH', 'DNT/ETH', 'MCO/ETH', 'ICN/ETH', 'MCO/BTC', 'WTC/BTC', 'WTC/ETH', 'LRC/BTC', 'LRC/ETH', 'QTUM/BTC', 'YOYOW/BTC', 'OMG/BTC', 'OMG/ETH', 'ZRX/BTC', 'ZRX/ETH', 'STRAT/BTC', 'STRAT/ETH', 'SNGLS/BTC', 'SNGLS/ETH', 'BQX/BTC', 'BQX/ETH', 'KNC/BTC', 'KNC/ETH', 'FUN/BTC', 'FUN/ETH', 'SNM/BTC', 'SNM/ETH', 'NEO/ETH', 'IOTA/BTC', 'IOTA/ETH', 'LINK/BTC', 'LINK/ETH', 'XVG/BTC', 'XVG/ETH', 'SALT/BTC', 'SALT/ETH', 'MDA/BTC', 'MDA/ETH', 'MTL/BTC', 'MTL/ETH', 'SUB/BTC', 'SUB/ETH', 'EOS/BTC', 'SNT/BTC', 'ETC/ETH', 'ETC/BTC', 'MTH/BTC', 'MTH/ETH', 'ENG/BTC', 'ENG/ETH', 'DNT/BTC', 'ZEC/BTC', 'ZEC/ETH', 'BNT/BTC', 'AST/BTC', 'AST/ETH', 'DASH/BTC', 'DASH/ETH', 'OAX/BTC', 'ICN/BTC', 'BTG/BTC', 'BTG/ETH', 'EVX/BTC', 'EVX/ETH', 'REQ/BTC', 'REQ/ETH', 'VIB/BTC', 'VIB/ETH', 'HSR/ETH', 'TRX/BTC', 'TRX/ETH', 'POWR/BTC', 'POWR/ETH', 'ARK/BTC', 'ARK/ETH', 'YOYOW/ETH', 'XRP/BTC', 'XRP/ETH', 'MOD/BTC', 'MOD/ETH', 'ENJ/BTC', 'ENJ/ETH', 'STORJ/BTC', 'STORJ/ETH', 'BNB/USDT', 'VEN/BNB', 'YOYOW/BNB', 'POWR/BNB', 'VEN/BTC', 'VEN/ETH', 'KMD/BTC', 'KMD/ETH', 'NULS/BNB', 'RCN/BTC', 'RCN/ETH', 'RCN/BNB', 'NULS/BTC', 'NULS/ETH', 'RDN/BTC', 'RDN/ETH', 'RDN/BNB', 'XMR/BTC', 'XMR/ETH', 'DLT/BNB', 'WTC/BNB', 'DLT/BTC', 'DLT/ETH', 'AMB/BTC', 'AMB/ETH', 'AMB/BNB', 'BCC/ETH', 'BCC/USDT', 'BCC/BNB', 'BAT/BTC', 'BAT/ETH', 'BAT/BNB', 'BCPT/BTC', 'BCPT/ETH', 'BCPT/BNB', 'ARN/BTC', 'ARN/ETH', 'GVT/BTC', 'GVT/ETH', 'CDT/BTC', 'CDT/ETH', 'GXS/BTC', 'GXS/ETH', 'NEO/USDT', 'NEO/BNB', 'POE/BTC', 'POE/ETH', 'QSP/BTC', 'QSP/ETH', 'QSP/BNB', 'BTS/BTC', 'BTS/ETH', 'BTS/BNB', 'XZC/BTC', 'XZC/ETH', 'XZC/BNB', 'LSK/BTC', 'LSK/ETH', 'LSK/BNB', 'TNT/BTC', 'TNT/ETH', 'FUEL/BTC', 'FUEL/ETH', 'MANA/BTC', 'MANA/ETH', 'BCD/BTC', 'BCD/ETH', 'DGD/BTC', 'DGD/ETH', 'IOTA/BNB', 'ADX/BTC', 'ADX/ETH', 'ADX/BNB', 'ADA/BTC', 'ADA/ETH', 'PPT/BTC', 'PPT/ETH', 'CMT/BTC', 'CMT/ETH', 'CMT/BNB', 'XLM/BTC', 'XLM/ETH', 'XLM/BNB', 'CND/BTC', 'CND/ETH', 'CND/BNB', 'LEND/BTC', 'LEND/ETH', 'WABI/BTC', 'WABI/ETH', 'WABI/BNB', 'LTC/ETH', 'LTC/USDT', 'LTC/BNB', 'TNB/BTC', 'TNB/ETH', 'WAVES/BTC', 'WAVES/ETH', 'WAVES/BNB', 'GTO/BTC', 'GTO/ETH', 'GTO/BNB', 'ICX/BTC', 'ICX/ETH', 'ICX/BNB', 'OST/BTC', 'OST/ETH', 'OST/BNB', 'ELF/BTC', 'ELF/ETH', 'AION/BTC', 'AION/ETH', 'AION/BNB', 'NEBL/BTC', 'NEBL/BNB', 'BRD/BTC', 'BRD/ETH', 'BRD/BNB', 'MCO/BNB', 'EDO/BTC', 'EDO/ETH', 'WINGS/BTC', 'WINGS/ETH', 'NAV/BTC', 'NAV/ETH', 'NAV/BNB', 'LUN/BTC', 'LUN/ETH', 'TRIG/BTC', 'TRIG/ETH', 'TRIG/BNB', 'APPC/BTC', 'APPC/ETH', 'APPC/BNB', 'VIBE/BTC', 'VIBE/ETH', 'RLC/BTC', 'RLC/ETH', 'RLC/BNB', 'INS/BTC', 'INS/ETH', 'PIVX/BTC', 'PIVX/BNB', 'IOST/BTC', 'IOST/ETH', 'CHAT/BTC', 'CHAT/ETH', 'STEEM/BTC', 'STEEM/ETH', 'STEEM/BNB', 'NANO/BTC', 'NANO/ETH', 'NANO/BNB', 'VIA/BTC', 'VIA/ETH', 'VIA/BNB', 'BLZ/BTC', 'BLZ/ETH', 'BLZ/BNB', 'AE/BTC', 'AE/ETH', 'AE/BNB', 'RPX/BTC', 'RPX/ETH', 'RPX/BNB', 'NCASH/BTC', 'NCASH/ETH', 'NCASH/BNB', 'POA/BTC', 'POA/ETH', 'POA/BNB', 'ZIL/BTC', 'ZIL/ETH', 'ZIL/BNB', 'ONT/BTC', 'ONT/ETH', 'ONT/BNB', 'STORM/BTC', 'STORM/ETH', 'STORM/BNB', 'QTUM/BNB', 'QTUM/USDT', 'XEM/BTC', 'XEM/ETH', 'XEM/BNB', 'WAN/BTC', 'WAN/ETH', 'WAN/BNB', 'WPR/BTC', 'WPR/ETH', 'QLC/BTC', 'QLC/ETH', 'SYS/BTC', 'SYS/ETH', 'SYS/BNB', 'QLC/BNB', 'GRS/BTC', 'GRS/ETH', 'ADA/USDT', 'ADA/BNB', 'CLOAK/BTC', 'CLOAK/ETH', 'GNT/BTC', 'GNT/ETH', 'GNT/BNB', 'LOOM/BTC', 'LOOM/ETH', 'LOOM/BNB', 'XRP/USDT', 'BCN/BTC', 'BCN/ETH', 'BCN/BNB', 'REP/BTC', 'REP/BNB', 'BTC/TUSD', 'TUSD/BTC', 'ETH/TUSD', 'TUSD/ETH', 'TUSD/BNB', 'ZEN/BTC', 'ZEN/ETH', 'ZEN/BNB', 'SKY/BTC', 'SKY/ETH', 'SKY/BNB', 'EOS/USDT', 'EOS/BNB', 'CVC/BTC', 'CVC/ETH', 'CVC/BNB', 'THETA/BTC', 'THETA/ETH', 'THETA/BNB', 'XRP/BNB', 'TUSD/USDT', 'IOTA/USDT', 'XLM/USDT', 'IOTX/BTC', 'IOTX/ETH', 'QKC/BTC', 'QKC/ETH', 'AGI/BTC', 'AGI/ETH', 'AGI/BNB', 'NXS/BTC', 'NXS/ETH', 'NXS/BNB', 'ENJ/BNB', 'DATA/BTC', 'DATA/ETH', 'ONT/USDT', 'TRX/BNB', 'TRX/USDT', 'ETC/USDT', 'ETC/BNB', 'ICX/USDT', 'SC/BTC', 'SC/ETH', 'NPXS/BTC', 'NPXS/ETH', 'VEN/USDT', 'KEY/BTC', 'KEY/ETH', 'NAS/BTC', 'NAS/ETH', 'NAS/BNB', 'MFT/BTC', 'MFT/ETH', 'MFT/BNB', 'DENT/BTC', 'DENT/ETH', 'ARDR/BTC', 'ARDR/ETH', 'ARDR/BNB', 'NULS/USDT', 'HOT/BTC', 'HOT/ETH', 'VET/BTC', 'VET/ETH', 'VET/USDT', 'VET/BNB', 'DOCK/BTC', 'DOCK/ETH', 'POLY/BTC', 'POLY/BNB', 'PHX/BTC', 'PHX/ETH', 'PHX/BNB', 'HC/BTC', 'HC/ETH', 'GO/BTC', 'GO/BNB', 'PAX/BTC', 'PAX/BNB', 'PAX/USDT', 'PAX/ETH', 'RVN/BTC', 'DCR/BTC', 'DCR/BNB', 'USDC/BNB', 'MITH/BTC', 'MITH/BNB', 'BCH/BTC', 'BSV/BTC', 'BCH/USDT', 'BSV/USDT', 'BNB/PAX', 'BTC/PAX', 'ETH/PAX', 'XRP/PAX', 'EOS/PAX', 'XLM/PAX', 'REN/BTC', 'REN/BNB', 'BNB/TUSD', 'XRP/TUSD', 'EOS/TUSD', 'XLM/TUSD', 'BNB/USDC', 'BTC/USDC', 'ETH/USDC', 'XRP/USDC', 'EOS/USDC', 'XLM/USDC', 'USDC/USDT', 'ADA/TUSD', 'TRX/TUSD', 'NEO/TUSD', 'TRX/XRP', 'XZC/XRP', 'PAX/TUSD', 'USDC/TUSD', 'USDC/PAX', 'LINK/USDT', 'LINK/TUSD', 'LINK/PAX', 'LINK/USDC', 'WAVES/USDT', 'WAVES/TUSD', 'WAVES/PAX', 'WAVES/USDC', 'BCH/TUSD', 'BCH/PAX', 'BCH/USDC', 'BSV/TUSD', 'BSV/PAX', 'BSV/USDC', 'LTC/TUSD', 'LTC/PAX', 'LTC/USDC', 'TRX/PAX', 'TRX/USDC', 'BTT/BTC', 'BTT/BNB', 'BTT/USDT', 'BNB/USDS', 'BTC/USDS', 'USDS/USDT', 'USDS/PAX', 'USDS/TUSD', 'USDS/USDC', 'BTT/PAX', 'BTT/TUSD', 'BTT/USDC', 'ONG/BNB', 'ONG/BTC', 'ONG/USDT', 'HOT/BNB', 'HOT/USDT', 'ZIL/USDT', 'ZRX/BNB', 'ZRX/USDT', 'FET/BNB', 'FET/BTC', 'FET/USDT', 'BAT/USDT', 'XMR/BNB', 'XMR/USDT', 'ZEC/BNB', 'ZEC/USDT', 'ZEC/PAX', 'ZEC/TUSD', 'ZEC/USDC', 'IOST/USDT', 'CELR/BNB', 'CELR/BTC', 'CELR/USDT', 'ADA/PAX', 'ADA/USDC', 'NEO/PAX', 'NEO/USDC', 'DASH/BNB', 'DASH/USDT', 'NANO/USDT', 'OMG/BNB', 'OMG/USDT', 'THETA/USDT', 'ENJ/USDT', 'MITH/USDT', 'MATIC/BNB', 'MATIC/BTC', 'MATIC/USDT', 'ATOM/BNB', 'ATOM/BTC', 'ATOM/USDT', 'ATOM/USDC', 'ATOM/PAX', 'ATOM/TUSD', 'ETC/USDC', 'ETC/PAX', 'ETC/TUSD', 'BAT/USDC', 'BAT/PAX', 'BAT/TUSD', 'PHB/BNB', 'PHB/BTC', 'PHB/USDC', 'PHB/TUSD', 'PHB/PAX', 'TFUEL/BNB', 'TFUEL/BTC', 'TFUEL/USDT', 'TFUEL/USDC', 'TFUEL/TUSD', 'TFUEL/PAX', 'ONE/BNB', 'ONE/BTC', 'ONE/USDT', 'ONE/TUSD', 'ONE/PAX', 'ONE/USDC', 'FTM/BNB', 'FTM/BTC', 'FTM/USDT', 'FTM/TUSD', 'FTM/PAX', 'FTM/USDC', 'BTCB/BTC', 'BCPT/TUSD', 'BCPT/PAX', 'BCPT/USDC', 'ALGO/BNB', 'ALGO/BTC', 'ALGO/USDT', 'ALGO/TUSD', 'ALGO/PAX', 'ALGO/USDC', 'USDSB/USDT', 'USDSB/USDS', 'GTO/USDT', 'GTO/PAX', 'GTO/TUSD', 'GTO/USDC', 'ERD/BNB', 'ERD/BTC', 'ERD/USDT', 'ERD/PAX', 'ERD/USDC', 'DOGE/BNB', 'DOGE/BTC', 'DOGE/USDT', 'DOGE/PAX', 'DOGE/USDC', 'DUSK/BNB', 'DUSK/BTC', 'DUSK/USDT', 'DUSK/USDC', 'DUSK/PAX', 'BGBP/USDC', 'ANKR/BNB', 'ANKR/BTC', 'ANKR/USDT', 'ANKR/TUSD', 'ANKR/PAX', 'ANKR/USDC', 'ONT/PAX', 'ONT/USDC', 'WIN/BNB', 'WIN/BTC', 'WIN/USDT', 'WIN/USDC', 'COS/BNB', 'COS/BTC', 'COS/USDT', 'TUSDB/TUSD', 'NPXS/USDT', 'NPXS/USDC', 'COCOS/BNB', 'COCOS/BTC', 'COCOS/USDT', 'MTL/USDT', 'TOMO/BNB', 'TOMO/BTC', 'TOMO/USDT', 'TOMO/USDC', 'PERL/BNB', 'PERL/BTC', 'PERL/USDC', 'PERL/USDT', 'DENT/USDT', 'MFT/USDT', 'KEY/USDT', 'STORM/USDT', 'DOCK/USDT', 'WAN/USDT', 'FUN/USDT', 'CVC/USDT', 'BTT/TRX', 'WIN/TRX', 'CHZ/BNB', 'CHZ/BTC', 'CHZ/USDT', 'BAND/BNB', 'BAND/BTC', 'BAND/USDT', 'BNB/BUSD', 'BTC/BUSD', 'BUSD/USDT', 'BEAM/BNB', 'BEAM/BTC', 'BEAM/USDT', 'XTZ/BNB', 'XTZ/BTC', 'XTZ/USDT', 'REN/USDT', 'RVN/USDT', 'HC/USDT', 'HBAR/BNB', 'HBAR/BTC', 'HBAR/USDT', 'NKN/BNB', 'NKN/BTC', 'NKN/USDT', 'XRP/BUSD', 'ETH/BUSD', 'BCH/BUSD', 'LTC/BUSD', 'LINK/BUSD', 'ETC/BUSD', 'STX/BNB', 'STX/BTC', 'STX/USDT', 'KAVA/BNB', 'KAVA/BTC', 'KAVA/USDT', 'BUSD/NGN', 'BNB/NGN', 'BTC/NGN', 'ARPA/BNB', 'ARPA/BTC', 'ARPA/USDT', 'TRX/BUSD', 'EOS/BUSD', 'IOTX/USDT', 'RLC/USDT', 'MCO/USDT', 'XLM/BUSD', 'ADA/BUSD', 'CTXC/BNB', 'CTXC/BTC', 'CTXC/USDT', 'BCH/BNB', 'BTC/RUB', 'ETH/RUB', 'XRP/RUB', 'BNB/RUB', 'TROY/BNB', 'TROY/BTC', 'TROY/USDT', 'BUSD/RUB', 'QTUM/BUSD', 'VET/BUSD', 'VITE/BNB', 'VITE/BTC', 'VITE/USDT', 'FTT/BNB', 'FTT/BTC', 'FTT/USDT', 'BTC/TRY', 'BNB/TRY', 'BUSD/TRY', 'ETH/TRY', 'XRP/TRY', 'USDT/TRY', 'USDT/RUB', 'BTC/EUR', 'ETH/EUR', 'BNB/EUR', 'XRP/EUR', 'EUR/BUSD', 'EUR/USDT', 'OGN/BNB', 'OGN/BTC', 'OGN/USDT', 'DREP/BNB', 'DREP/BTC', 'DREP/USDT', 'BULL/USDT', 'BULL/BUSD', 'BEAR/USDT', 'BEAR/BUSD', 'ETHBULL/USDT', 'ETHBULL/BUSD', 'ETHBEAR/USDT', 'ETHBEAR/BUSD', 'TCT/BNB', 'TCT/BTC', 'TCT/USDT', 'WRX/BNB', 'WRX/BTC', 'WRX/USDT', 'ICX/BUSD', 'BTS/USDT', 'BTS/BUSD', 'LSK/USDT', 'BNT/USDT', 'BNT/BUSD', 'LTO/BNB', 'LTO/BTC', 'LTO/USDT', 'ATOM/BUSD', 'DASH/BUSD', 'NEO/BUSD', 'WAVES/BUSD', 'XTZ/BUSD', 'EOSBULL/USDT', 'EOSBULL/BUSD', 'EOSBEAR/USDT', 'EOSBEAR/BUSD', 'XRPBULL/USDT', 'XRPBULL/BUSD', 'XRPBEAR/USDT', 'XRPBEAR/BUSD', 'BAT/BUSD', 'ENJ/BUSD', 'NANO/BUSD', 'ONT/BUSD', 'RVN/BUSD', 'STRAT/BUSD', 'STRAT/BNB', 'STRAT/USDT', 'AION/BUSD', 'AION/USDT', 'MBL/BNB', 'MBL/BTC', 'MBL/USDT', 'COTI/BNB', 'COTI/BTC', 'COTI/USDT', 'ALGO/BUSD', 'BTT/BUSD', 'TOMO/BUSD', 'XMR/BUSD', 'ZEC/BUSD', 'BNBBULL/USDT', 'BNBBULL/BUSD', 'BNBBEAR/USDT', 'BNBBEAR/BUSD', 'STPT/BNB', 'STPT/BTC', 'STPT/USDT', 'BTC/ZAR', 'ETH/ZAR', 'BNB/ZAR', 'USDT/ZAR', 'BUSD/ZAR', 'BTC/BKRW', 'ETH/BKRW', 'BNB/BKRW', 'WTC/USDT', 'DATA/BUSD', 'DATA/USDT', 'XZC/USDT', 'SOL/BNB', 'SOL/BTC', 'SOL/USDT', 'SOL/BUSD', 'BTC/IDRT', 'BNB/IDRT', 'USDT/IDRT', 'BUSD/IDRT', 'CTSI/BTC', 'CTSI/USDT', 'CTSI/BNB', 'CTSI/BUSD', 'HIVE/BNB', 'HIVE/BTC', 'HIVE/USDT', 'CHR/BNB', 'CHR/BTC', 'CHR/USDT', 'BTCUP/USDT', 'BTCDOWN/USDT', 'GXS/USDT', 'ARDR/USDT', 'ERD/BUSD', 'LEND/USDT', 'HBAR/BUSD', 'MATIC/BUSD', 'WRX/BUSD', 'ZIL/BUSD', 'MDT/BNB', 'MDT/BTC', 'MDT/USDT', 'STMX/BTC', 'STMX/ETH', 'STMX/USDT', 'KNC/BUSD', 'KNC/USDT', 'REP/BUSD', 'REP/USDT', 'LRC/BUSD', 'LRC/USDT', 'IQ/BNB', 'IQ/BUSD', 'PNT/BTC', 'PNT/USDT', 'BTC/GBP', 'ETH/GBP', 'XRP/GBP', 'BNB/GBP', 'GBP/BUSD', 'DGB/BTC', 'DGB/BUSD', 'BTC/UAH', 'USDT/UAH', 'COMP/BTC', 'COMP/BNB', 'COMP/BUSD', 'COMP/USDT', 'BTC/BIDR', 'ETH/BIDR', 'BNB/BIDR', 'BUSD/BIDR', 'USDT/BIDR', 'BKRW/USDT', 'BKRW/BUSD', 'SC/USDT', 'ZEN/USDT', 'SXP/BTC', 'SXP/BNB', 'SXP/BUSD', 'SNX/BTC', 'SNX/BNB', 'SNX/BUSD', 'SNX/USDT', 'ETHUP/USDT', 'ETHDOWN/USDT', 'ADAUP/USDT', 'ADADOWN/USDT', 'LINKUP/USDT', 'LINKDOWN/USDT', 'VTHO/BNB', 'VTHO/BUSD', 'VTHO/USDT', 'DCR/BUSD', 'DGB/USDT', 'GBP/USDT', 'STORJ/BUSD', 'SXP/USDT', 'IRIS/BNB', 'IRIS/BTC', 'IRIS/BUSD', 'MKR/BNB', 'MKR/BTC', 'MKR/USDT', 'MKR/BUSD', 'DAI/BNB', 'DAI/BTC', 'DAI/USDT', 'DAI/BUSD', 'RUNE/BNB', 'RUNE/BTC', 'RUNE/BUSD', 'MANA/BUSD', 'DOGE/BUSD', 'LEND/BUSD', 'ZRX/BUSD', 'DCR/USDT', 'STORJ/USDT', 'XRP/BKRW', 'ADA/BKRW', 'BTC/AUD', 'ETH/AUD', 'AUD/BUSD', 'FIO/BNB', 'FIO/BTC', 'FIO/BUSD', 'BNBUP/USDT', 'BNBDOWN/USDT', 'XTZUP/USDT', 'XTZDOWN/USDT', 'AVA/BNB', 'AVA/BTC', 'AVA/BUSD', 'USDT/BKRW', 'BUSD/BKRW', 'IOTA/BUSD', 'MANA/USDT', 'XRP/AUD', 'BNB/AUD', 'AUD/USDT', 'BAL/BNB', 'BAL/BTC', 'BAL/BUSD', 'YFI/BNB', 'YFI/BTC', 'YFI/BUSD', 'YFI/USDT', 'BLZ/BUSD', 'KMD/BUSD', 'BAL/USDT', 'BLZ/USDT', 'IRIS/USDT', 'KMD/USDT', 'BTC/DAI', 'ETH/DAI', 'BNB/DAI', 'USDT/DAI', 'BUSD/DAI', 'JST/BNB', 'JST/BTC', 'JST/BUSD', 'JST/USDT', 'SRM/BNB', 'SRM/BTC', 'SRM/BUSD', 'SRM/USDT', 'ANT/BNB', 'ANT/BTC', 'ANT/BUSD', 'ANT/USDT', 'CRV/BNB', 'CRV/BTC', 'CRV/BUSD', 'CRV/USDT', 'SAND/BNB', 'SAND/BTC', 'SAND/USDT', 'SAND/BUSD', 'OCEAN/BNB', 'OCEAN/BTC', 'OCEAN/BUSD', 'OCEAN/USDT', 'NMR/BTC', 'NMR/BUSD', 'NMR/USDT', 'DOT/BNB', 'DOT/BTC', 'DOT/BUSD', 'DOT/USDT', 'LUNA/BNB', 'LUNA/BTC', 'LUNA/BUSD', 'LUNA/USDT', 'IDEX/BTC', 'IDEX/BUSD', 'RSR/BNB', 'RSR/BTC', 'RSR/BUSD', 'RSR/USDT', 'PAXG/BNB', 'PAXG/BTC', 'PAXG/BUSD', 'PAXG/USDT', 'WNXM/BNB', 'WNXM/BTC', 'WNXM/BUSD', 'WNXM/USDT', 'TRB/BNB', 'TRB/BTC', 'TRB/BUSD', 'TRB/USDT', 'ETH/NGN', 'DOT/BIDR', 'LINK/AUD', 'SXP/AUD', 'BZRX/BNB', 'BZRX/BTC', 'BZRX/BUSD', 'BZRX/USDT', 'WBTC/BTC', 'WBTC/ETH', 'SUSHI/BNB', 'SUSHI/BTC', 'SUSHI/BUSD', 'SUSHI/USDT', 'YFII/BNB', 'YFII/BTC', 'YFII/BUSD', 'YFII/USDT', 'KSM/BNB', 'KSM/BTC', 'KSM/BUSD', 'KSM/USDT', 'EGLD/BNB', 'EGLD/BTC', 'EGLD/BUSD', 'EGLD/USDT', 'DIA/BNB', 'DIA/BTC', 'DIA/BUSD', 'DIA/USDT', 'RUNE/USDT', 'FIO/USDT', 'UMA/BTC', 'UMA/USDT', 'EOSUP/USDT', 'EOSDOWN/USDT', 'TRXUP/USDT', 'TRXDOWN/USDT', 'XRPUP/USDT', 'XRPDOWN/USDT', 'DOTUP/USDT', 'DOTDOWN/USDT', 'SRM/BIDR', 'ONE/BIDR', 'LINK/TRY', 'USDT/NGN', 'BEL/BNB', 'BEL/BTC', 'BEL/BUSD', 'BEL/USDT', 'WING/BNB', 'WING/BTC', 'SWRV/BNB', 'SWRV/BUSD', 'WING/BUSD', 'WING/USDT', 'LTCUP/USDT', 'LTCDOWN/USDT', 'LEND/BKRW', 'SXP/EUR', 'CREAM/BNB', 'CREAM/BUSD', 'UNI/BNB', 'UNI/BTC', 'UNI/BUSD', 'UNI/USDT', 'NBS/BTC', 'NBS/USDT', 'OXT/BTC', 'OXT/USDT', 'SUN/BTC', 'SUN/USDT', 'AVAX/BNB', 'AVAX/BTC', 'AVAX/BUSD', 'AVAX/USDT', 'HNT/BTC', 'HNT/USDT', 'BAKE/BNB', 'BURGER/BNB', 'SXP/BIDR', 'LINK/BKRW', 'FLM/BNB', 'FLM/BTC', 'FLM/BUSD', 'FLM/USDT', 'SCRT/BTC', 'SCRT/ETH', 'CAKE/BNB', 'CAKE/BUSD', 'SPARTA/BNB', 'UNIUP/USDT', 'UNIDOWN/USDT', 'ORN/BTC', 'ORN/USDT', 'TRX/NGN', 'SXP/TRY', 'UTK/BTC', 'UTK/USDT', 'XVS/BNB', 'XVS/BTC', 'XVS/BUSD', 'XVS/USDT', 'ALPHA/BNB', 'ALPHA/BTC', 'ALPHA/BUSD', 'ALPHA/USDT', 'VIDT/BTC', 'VIDT/BUSD', 'AAVE/BNB', 'BTC/BRL', 'USDT/BRL', 'AAVE/BTC', 'AAVE/ETH', 'AAVE/BUSD', 'AAVE/USDT', 'AAVE/BKRW', 'NEAR/BNB', 'NEAR/BTC', 'NEAR/BUSD', 'NEAR/USDT', 'SXPUP/USDT', 'SXPDOWN/USDT', 'DOT/BKRW', 'SXP/GBP', 'FIL/BNB', 'FIL/BTC', 'FIL/BUSD', 'FIL/USDT', 'FILUP/USDT', 'FILDOWN/USDT', 'YFIUP/USDT', 'YFIDOWN/USDT', 'INJ/BNB', 'INJ/BTC', 'INJ/BUSD', 'INJ/USDT', 'AERGO/BTC', 'AERGO/BUSD', 'LINK/EUR', 'ONE/BUSD', 'EASY/ETH', 'AUDIO/BTC', 'AUDIO/BUSD', 'AUDIO/USDT', 'CTK/BNB', 'CTK/BTC', 'CTK/BUSD', 'CTK/USDT', 'BCHUP/USDT', 'BCHDOWN/USDT', 'BOT/BTC', 'BOT/BUSD', 'ETH/BRL', 'DOT/EUR', 'AKRO/BTC', 'AKRO/USDT', 'KP3R/BNB', 'KP3R/BUSD', 'AXS/BNB', 'AXS/BTC', 'AXS/BUSD', 'AXS/USDT', 'HARD/BNB', 'HARD/BTC', 'HARD/BUSD', 'HARD/USDT', 'BNB/BRL', 'LTC/EUR', 'RENBTC/BTC', 'RENBTC/ETH', 'DNT/BUSD', 'DNT/USDT', 'SLP/ETH', 'ADA/EUR', 'LTC/NGN', 'CVP/ETH', 'CVP/BUSD', 'STRAX/BTC', 'STRAX/ETH', 'STRAX/BUSD', 'STRAX/USDT', 'FOR/BTC', 'FOR/BUSD', 'UNFI/BNB', 'UNFI/BTC', 'UNFI/BUSD', 'UNFI/USDT', 'FRONT/ETH', 'FRONT/BUSD', 'BCHA/BUSD', 'ROSE/BTC', 'ROSE/BUSD', 'ROSE/USDT', 'AVAX/TRY', 'BUSD/BRL', 'AVA/USDT', 'SYS/BUSD', 'XEM/USDT', 'HEGIC/ETH', 'HEGIC/BUSD', 'AAVEUP/USDT', 'AAVEDOWN/USDT', 'PROM/BNB', 'PROM/BUSD', 'XRP/BRL', 'XRP/NGN', 'SKL/BTC', 'SKL/BUSD', 'SKL/USDT', 'BCH/EUR', 'YFI/EUR', 'ZIL/BIDR', 'SUSD/BTC', 'SUSD/ETH', 'SUSD/USDT', 'COVER/ETH', 'COVER/BUSD', 'GLM/BTC', 'GLM/ETH', 'GHST/ETH', 'GHST/BUSD', 'SUSHIUP/USDT', 'SUSHIDOWN/USDT', 'XLMUP/USDT', 'XLMDOWN/USDT', 'LINK/BRL', 'LINK/NGN', 'LTC/RUB', 'TRX/TRY', 'XLM/EUR', 'DF/ETH', 'DF/BUSD', 'GRT/BTC', 'GRT/ETH', 'GRT/USDT', 'JUV/BTC', 'JUV/BUSD', 'JUV/USDT', 'PSG/BTC', 'PSG/BUSD', 'PSG/USDT', 'BUSD/BVND', 'USDT/BVND', '1INCH/BTC', '1INCH/USDT', 'REEF/BTC', 'REEF/USDT', 'OG/BTC', 'OG/USDT', 'ATM/BTC', 'ATM/USDT', 'ASR/BTC', 'ASR/USDT', 'CELO/BTC', 'CELO/USDT', 'RIF/BTC', 'RIF/USDT', 'CHZ/TRY', 'XLM/TRY', 'LINK/GBP', 'GRT/EUR', 'BTCST/BTC', 'BTCST/BUSD', 'BTCST/USDT', 'TRU/BTC', 'TRU/BUSD', 'TRU/USDT', 'DEXE/ETH', 'DEXE/BUSD', 'EOS/EUR', 'LTC/BRL', 'USDC/BUSD', 'TUSD/BUSD', 'PAX/BUSD', 'CKB/BTC', 'CKB/BUSD', 'CKB/USDT', 'TWT/BTC', 'TWT/BUSD', 'TWT/USDT', 'FIRO/BTC', 'FIRO/ETH', 'FIRO/USDT', 'BETH/ETH', 'DOGE/EUR', 'DOGE/TRY', 'DOGE/AUD', 'DOGE/BRL', 'DOT/NGN', 'PROS/ETH', 'LIT/BTC', 'LIT/BUSD', 'LIT/USDT', 'BTC/VAI', 'BUSD/VAI', 'SFP/BTC', 'SFP/BUSD', 'SFP/USDT', 'DOGE/GBP', 'DOT/TRY', 'FXS/BTC', 'FXS/BUSD', 'DODO/BTC', 'DODO/BUSD', 'DODO/USDT', 'FRONT/BTC', 'EASY/BTC', 'CAKE/BTC', 'CAKE/USDT', 'BAKE/BUSD', 'UFT/ETH', 'UFT/BUSD', '1INCH/BUSD', 'BAND/BUSD', 'GRT/BUSD', 'IOST/BUSD', 'OMG/BUSD', 'REEF/BUSD', 'ACM/BTC', 'ACM/BUSD', 'ACM/USDT', 'AUCTION/BTC', 'AUCTION/BUSD', 'PHA/BTC', 'PHA/BUSD', 'DOT/GBP', 'ADA/TRY', 'ADA/BRL', 'ADA/GBP', 'TVK/BTC', 'TVK/BUSD', 'BADGER/BTC', 'BADGER/BUSD', 'BADGER/USDT', 'FIS/BTC', 'FIS/BUSD', 'FIS/USDT', 'DOT/BRL', 'ADA/AUD', 'HOT/TRY', 'EGLD/EUR', 'OM/BTC', 'OM/BUSD', 'OM/USDT', 'POND/BTC', 'POND/BUSD', 'POND/USDT', 'DEGO/BTC', 'DEGO/BUSD', 'DEGO/USDT', 'AVAX/EUR', 'BTT/TRY', 'CHZ/BRL', 'UNI/EUR', 'ALICE/BTC', 'ALICE/BUSD', 'ALICE/USDT', 'CHZ/BUSD', 'CHZ/EUR', 'CHZ/GBP', 'BIFI/BNB', 'BIFI/BUSD', 'LINA/BTC', 'LINA/BUSD', 'LINA/USDT', 'ADA/RUB', 'ENJ/BRL', 'ENJ/EUR', 'MATIC/EUR', 'NEO/TRY', 'PERP/BTC', 'PERP/BUSD', 'PERP/USDT', 'RAMP/BTC', 'RAMP/BUSD', 'RAMP/USDT', 'SUPER/BTC', 'SUPER/BUSD', 'SUPER/USDT', 'CFX/BTC', 'CFX/BUSD', 'CFX/USDT', 'ENJ/GBP', 'EOS/TRY', 'LTC/GBP', 'LUNA/EUR', 'RVN/TRY', 'THETA/EUR', 'XVG/BUSD', 'EPS/BTC', 'EPS/BUSD', 'EPS/USDT', 'AUTO/BTC', 'AUTO/BUSD', 'AUTO/USDT', 'TKO/BTC', 'TKO/BIDR', 'TKO/BUSD', 'TKO/USDT', 'PUNDIX/ETH', 'PUNDIX/USDT', 'BTT/BRL', 'BTT/EUR', 'HOT/EUR', 'WIN/EUR', 'TLM/BTC', 'TLM/BUSD', 'TLM/USDT', '1INCHUP/USDT', '1INCHDOWN/USDT', 'BTG/BUSD', 'BTG/USDT', 'HOT/BUSD', 'BNB/UAH', 'ONT/TRY', 'VET/EUR', 'VET/GBP', 'WIN/BRL', 'MIR/BTC', 'MIR/BUSD', 'MIR/USDT', 'BAR/BTC', 'BAR/BUSD', 'BAR/USDT', 'FORTH/BTC', 'FORTH/BUSD', 'FORTH/USDT', 'CAKE/GBP', 'DOGE/RUB', 'HOT/BRL', 'WRX/EUR', 'EZ/BTC', 'EZ/ETH', 'BAKE/USDT', 'BURGER/BUSD', 'BURGER/USDT', 'SLP/BUSD', 'SLP/USDT', 'TRX/AUD', 'TRX/EUR', 'VET/TRY', 'SHIB/USDT', 'SHIB/BUSD', 'ICP/BTC', 'ICP/BNB', 'ICP/BUSD', 'ICP/USDT', 'BTC/GYEN', 'USDT/GYEN', 'SHIB/EUR', 'SHIB/RUB', 'ETC/EUR', 'ETC/BRL', 'DOGE/BIDR', 'AR/BTC', 'AR/BNB', 'AR/BUSD', 'AR/USDT', 'POLS/BTC', 'POLS/BNB', 'POLS/BUSD', 'POLS/USDT', 'MDX/BTC', 'MDX/BNB', 'MDX/BUSD', 'MDX/USDT', 'MASK/BNB', 'MASK/BUSD', 'MASK/USDT', 'LPT/BTC', 'LPT/BNB', 'LPT/BUSD', 'LPT/USDT', 'ETH/UAH', 'MATIC/BRL', 'SOL/EUR', 'SHIB/BRL', 'AGIX/BTC', 'ICP/EUR', 'MATIC/GBP', 'SHIB/TRY', 'MATIC/BIDR', 'MATIC/RUB', 'NU/BTC', 'NU/BNB', 'NU/BUSD', 'NU/USDT', 'XVG/USDT', 'RLC/BUSD', 'CELR/BUSD', 'ATM/BUSD', 'ZEN/BUSD', 'FTM/BUSD', 'THETA/BUSD', 'WIN/BUSD', 'KAVA/BUSD', 'XEM/BUSD', 'ATA/BTC', 'ATA/BNB', 'ATA/BUSD', 'ATA/USDT', 'GTC/BTC', 'GTC/BNB', 'GTC/BUSD', 'GTC/USDT', 'TORN/BTC', 'TORN/BNB', 'TORN/BUSD', 'TORN/USDT', 'MATIC/TRY', 'ETC/GBP', 'SOL/GBP', 'BAKE/BTC', 'COTI/BUSD', 'KEEP/BTC', 'KEEP/BNB', 'KEEP/BUSD', 'KEEP/USDT', 'SOL/TRY', 'RUNE/GBP', 'SOL/BRL', 'SC/BUSD', 'CHR/BUSD', 'STMX/BUSD', 'HNT/BUSD', 'FTT/BUSD', 'DOCK/BUSD', 'ADA/BIDR', 'ERN/BNB', 'ERN/BUSD', 'ERN/USDT', 'KLAY/BTC', 'KLAY/BNB', 'KLAY/BUSD', 'KLAY/USDT', 'RUNE/EUR', 'MATIC/AUD', 'DOT/RUB', 'UTK/BUSD', 'IOTX/BUSD', 'PHA/USDT', 'SOL/RUB', 'RUNE/AUD', 'BUSD/UAH', 'BOND/BTC', 'BOND/BNB', 'BOND/BUSD', 'BOND/USDT', 'MLN/BTC', 'MLN/BNB', 'MLN/BUSD', 'MLN/USDT', 'GRT/TRY', 'CAKE/BRL', 'ICP/RUB', 'DOT/AUD', 'AAVE/BRL', 'EOS/AUD', 'DEXE/USDT', 'LTO/BUSD', 'ADX/BUSD', 'QUICK/BTC', 'QUICK/BNB', 'QUICK/BUSD', 'C98/USDT', 'C98/BUSD', 'C98/BNB', 'C98/BTC', 'CLV/BTC', 'CLV/BNB', 'CLV/BUSD', 'CLV/USDT', 'QNT/BTC', 'QNT/BNB', 'QNT/BUSD', 'QNT/USDT', 'FLOW/BTC', 'FLOW/BNB', 'FLOW/BUSD', 'FLOW/USDT', 'XEC/BUSD', 'AXS/BRL', 'AXS/AUD', 'TVK/USDT', 'MINA/BTC', 'MINA/BNB', 'MINA/BUSD', 'MINA/USDT', 'RAY/BNB', 'RAY/BUSD', 'RAY/USDT', 'FARM/BTC', 'FARM/BNB', 'FARM/BUSD', 'FARM/USDT', 'ALPACA/BTC', 'ALPACA/BNB', 'ALPACA/BUSD', 'ALPACA/USDT', 'TLM/TRY', 'QUICK/USDT', 'ORN/BUSD', 'MBOX/BTC', 'MBOX/BNB', 'MBOX/BUSD', 'MBOX/USDT', 'VGX/BTC', 'VGX/ETH', 'FOR/USDT', 'REQ/USDT', 'GHST/USDT', 'TRU/RUB', 'FIS/BRL', 'WAXP/USDT', 'WAXP/BUSD', 'WAXP/BNB', 'WAXP/BTC', 'TRIBE/BTC', 'TRIBE/BNB', 'TRIBE/BUSD', 'TRIBE/USDT', 'GNO/USDT', 'GNO/BUSD', 'GNO/BNB', 'GNO/BTC', 'ARPA/TRY', 'PROM/BTC', 'MTL/BUSD', 'OGN/BUSD', 'XEC/USDT', 'C98/BRL', 'SOL/AUD', 'XRP/BIDR', 'POLY/BUSD', 'ELF/USDT', 'DYDX/USDT', 'DYDX/BUSD', 'DYDX/BNB', 'DYDX/BTC', 'ELF/BUSD', 'POLY/USDT', 'IDEX/USDT', 'VIDT/USDT', 'SOL/BIDR', 'AXS/BIDR', 'BTC/USDP', 'ETH/USDP', 'BNB/USDP', 'USDP/BUSD', 'USDP/USDT', 'GALA/USDT', 'GALA/BUSD', 'GALA/BNB', 'GALA/BTC', 'FTM/BIDR', 'ALGO/BIDR', 'CAKE/AUD', 'KSM/AUD', 'WAVES/RUB', 'SUN/BUSD', 'ILV/USDT', 'ILV/BUSD', 'ILV/BNB', 'ILV/BTC', 'REN/BUSD', 'YGG/USDT', 'YGG/BUSD', 'YGG/BNB', 'YGG/BTC', 'STX/BUSD', 'SYS/USDT', 'DF/USDT', 'SOL/USDC', 'ARPA/RUB', 'LTC/UAH', 'FET/BUSD', 'ARPA/BUSD', 'LSK/BUSD', 'AVAX/BIDR', 'ALICE/BIDR', 'FIDA/USDT', 'FIDA/BUSD', 'FIDA/BNB', 'FIDA/BTC', 'DENT/BUSD', 'FRONT/USDT', 'CVP/USDT', 'AGLD/BTC', 'AGLD/BNB', 'AGLD/BUSD', 'AGLD/USDT', 'RAD/BTC', 'RAD/BNB', 'RAD/BUSD', 'RAD/USDT', 'UNI/AUD', 'HIVE/BUSD', 'STPT/BUSD', 'BETA/BTC', 'BETA/BNB', 'BETA/BUSD', 'BETA/USDT', 'SHIB/AUD', 'RARE/BTC', 'RARE/BNB', 'RARE/BUSD', 'RARE/USDT', 'AVAX/BRL', 'AVAX/AUD', 'LUNA/AUD', 'TROY/BUSD', 'AXS/ETH', 'FTM/ETH', 'SOL/ETH', 'SSV/BTC', 'SSV/ETH', 'LAZIO/TRY', 'LAZIO/EUR', 'LAZIO/BTC', 'LAZIO/USDT', 'CHESS/BTC', 'CHESS/BNB', 'CHESS/BUSD', 'CHESS/USDT', 'FTM/AUD', 'FTM/BRL', 'SCRT/BUSD', 'ADX/USDT', 'AUCTION/USDT', 'CELO/BUSD', 'FTM/RUB', 'NU/AUD', 'NU/RUB', 'REEF/TRY', 'REEF/BIDR', 'SHIB/DOGE', 'DAR/USDT', 'DAR/BUSD', 'DAR/BNB', 'DAR/BTC', 'BNX/BTC', 'BNX/BNB', 'BNX/BUSD', 'BNX/USDT', 'RGT/USDT', 'RGT/BTC', 'RGT/BUSD', 'RGT/BNB', 'LAZIO/BUSD', 'OXT/BUSD', 'MANA/TRY', 'ALGO/RUB', 'SHIB/UAH', 'LUNA/BIDR', 'AUD/USDC', 'MOVR/BTC', 'MOVR/BNB', 'MOVR/BUSD', 'MOVR/USDT', 'CITY/BTC', 'CITY/BNB', 'CITY/BUSD', 'CITY/USDT', 'ENS/BTC', 'ENS/BNB', 'ENS/BUSD', 'ENS/USDT', 'SAND/ETH', 'DOT/ETH', 'MATIC/ETH', 'ANKR/BUSD', 'SAND/TRY', 'MANA/BRL', 'KP3R/USDT', 'QI/USDT', 'QI/BUSD', 'QI/BNB', 'QI/BTC', 'PORTO/BTC', 'PORTO/USDT', 'PORTO/TRY', 'PORTO/EUR', 'POWR/USDT', 'POWR/BUSD', 'AVAX/ETH', 'SLP/TRY', 'FIS/TRY', 'LRC/TRY', 'CHR/ETH', 'FIS/BIDR', 'VGX/USDT', 'GALA/ETH', 'JASMY/USDT', 'JASMY/BUSD', 'JASMY/BNB', 'JASMY/BTC', 'AMP/BTC', 'AMP/BNB', 'AMP/BUSD', 'AMP/USDT', 'PLA/BTC', 'PLA/BNB', 'PLA/BUSD', 'PLA/USDT', 'PYR/BTC', 'PYR/BUSD', 'PYR/USDT', 'RNDR/BTC', 'RNDR/USDT', 'RNDR/BUSD', 'ALCX/BTC', 'ALCX/BUSD', 'ALCX/USDT', 'SANTOS/BTC', 'SANTOS/USDT', 'SANTOS/BRL', 'SANTOS/TRY', 'MC/BTC', 'MC/BUSD', 'MC/USDT', 'BEL/TRY', 'COCOS/BUSD', 'DENT/TRY', 'ENJ/TRY', 'NEO/RUB', 'SAND/AUD', 'SLP/BIDR', 'ANY/BTC', 'ANY/BUSD', 'ANY/USDT', 'BICO/BTC', 'BICO/BUSD', 'BICO/USDT', 'FLUX/BTC', 'FLUX/BUSD', 'FLUX/USDT', 'ALICE/TRY', 'FXS/USDT', 'GALA/BRL', 'GALA/TRY', 'LUNA/TRY', 'REQ/BUSD', 'SAND/BRL', 'MANA/BIDR', 'SAND/BIDR', 'VOXEL/BTC', 'VOXEL/BNB', 'VOXEL/BUSD', 'VOXEL/USDT', 'COS/BUSD', 'CTXC/BUSD', 'FTM/TRY', 'MANA/BNB', 'MINA/TRY', 'XTZ/TRY', 'HIGH/BTC', 'HIGH/BUSD', 'HIGH/USDT', 'CVX/BTC', 'CVX/BUSD', 'CVX/USDT', 'PEOPLE/BTC', 'PEOPLE/BUSD', 'PEOPLE/USDT', 'OOKI/BUSD', 'OOKI/USDT', 'COCOS/TRY', 'GXS/BNB', 'LINK/BNB', 'LUNA/ETH', 'MDT/BUSD', 'NULS/BUSD', 'SPELL/BTC', 'SPELL/USDT', 'SPELL/BUSD', 'UST/BTC', 'UST/BUSD', 'UST/USDT', 'JOE/BTC', 'JOE/BUSD', 'JOE/USDT', 'ATOM/ETH', 'DUSK/BUSD', 'EGLD/ETH', 'ICP/ETH', 'LUNA/BRL', 'LUNA/UST', 'NEAR/ETH', 'ROSE/BNB', 'VOXEL/ETH', 'ALICE/BNB', 'ATOM/TRY', 'ETH/UST', 'GALA/AUD', 'LRC/BNB', 'ONE/ETH', 'OOKI/BNB', 'ACH/BTC', 'ACH/BUSD', 'ACH/USDT', 'IMX/BTC', 'IMX/BUSD', 'IMX/USDT', 'GLMR/BTC', 'GLMR/BUSD', 'GLMR/USDT', 'ATOM/BIDR', 'DYDX/ETH', 'FARM/ETH', 'FOR/BNB', 'ICP/TRY', 'JASMY/ETH', 'LINA/BNB', 'OOKI/ETH', 'ROSE/ETH', 'UMA/BUSD', 'UNI/ETH', 'XTZ/ETH', 'LOKA/BTC', 'LOKA/BNB', 'LOKA/BUSD', 'LOKA/USDT', 'ATOM/BRL', 'BNB/UST', 'CRV/ETH', 'HIGH/BNB', 'NEAR/RUB', 'ROSE/TRY', 'SCRT/USDT', 'API3/BTC', 'API3/BUSD', 'API3/USDT', 'BTTC/USDT', 'BTTC/USDC', 'BTTC/TRY', 'ACA/BTC', 'ACA/BUSD', 'ACA/USDT', 'ANC/BTC', 'ANC/BUSD', 'ANC/USDT', 'BDOT/DOT', 'XNO/BTC', 'XNO/ETH', 'XNO/BUSD', 'XNO/USDT', 'COS/TRY', 'KAVA/ETH', 'MC/BNB', 'ONE/TRY', 'WOO/BTC', 'WOO/BNB', 'WOO/BUSD', 'WOO/USDT', 'CELR/ETH', 'PEOPLE/BNB', 'SLP/BNB', 'SPELL/BNB', 'SPELL/TRY', 'TFUEL/BUSD', 'AXS/TRY', 'DAR/TRY', 'NEAR/TRY', 'IDEX/BNB', 'ALPINE/EUR', 'ALPINE/TRY', 'ALPINE/USDT', 'ALPINE/BTC', 'T/USDT', 'T/BUSD', 'API3/BNB', 'BETA/ETH', 'INJ/TRY', 'TLM/BNB', 'ASTR/BUSD', 'ASTR/USDT', 'API3/TRY', 'GLMR/BNB', 'MBOX/TRY', 'NBT/BIDR', 'NBT/USDT', 'GMT/BTC', 'GMT/BNB', 'GMT/BUSD', 'GMT/USDT', 'ANC/BNB', 'ATOM/EUR', 'GALA/EUR', 'KSM/ETH', 'UMA/TRY', 'KDA/BTC', 'KDA/BUSD', 'KDA/USDT', 'APE/USDT', 'APE/BUSD', 'APE/BTC', 'ALPINE/BUSD', 'LUNA/GBP', 'NEAR/EUR', 'TWT/TRY', 'WAVES/EUR', 'APE/EUR', 'APE/GBP', 'APE/TRY'])
'''