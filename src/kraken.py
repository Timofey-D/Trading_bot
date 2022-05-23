"""
The module contains a private data:
"""
import urllib.parse
import hashlib
import hmac
import base64

import time
import configparser
import requests

# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = ''
api_sec = ''




class Kraken:


    def __init__(self, api):

        parser = configparser.ConfigParser()
        parser.read(api)
        
        self.API_URL = parser['API']['API_URL']
        self.API_KEY = parser['API']['API_KEY']
        self.API_SEC = parser['API']['API_SEC']


    def __get_kraken_signature__(self, urlpath, data):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.API_SEC), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    # Attaches auth headers and returns results of a POST request
    def __kraken_request__(self, uri_path, data):
        headers = {'API-Key': self.API_KEY, 'API-Sign': self.__get_kraken_signature__(uri_path, data)}
        # get_kraken_signature() as defined in the 'Authentication' section
        req = requests.post((api_url + uri_path), headers=headers, data=data)
        return req


    def __get_response__(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


    def __extract_respond__(self, resp, value=None):

        if value != None:
            result = resp.json()['result'][value]
        else:
            result = resp.json()['result']

        return result


    def __get_respond__(self, source, payload=dict()):
        url = self.API_URL + source 

        payload.update( {'nonce' : str(int(1000*time.time()))} )

        respond = None
        if source.find('public') == 1:
            respond = requests.get(url)
        else:
            respond = self.__kraken_request__(source, payload)

        return respond


    def get_server_time(self):
        source = '/0/public/Time'
        respond = self.__get_respond__(source)
        unixtime = self.__extract_respond__(respond, 'unixtime')
        return unixtime


    def get_system_status(self):
        source = '/0/public/SystemStatus'
        respond = self.__get_respond__(source)
        status = self.__extract_respond__(respond, 'status')
        return status

    
    def get_assets_info(self):
        source = '/0/public/Assets'
        respond = self.__get_respond__(source)
        assets = self.__extract_respond__(respond)
        return assets


    def get_asset_info(self, asset):
        source = '/0/public/Assets'
        respond = self.__get_respond__(source)
        asset = self.__extract_respond__(respond, asset)
        return asset


    def get_tradable_assets(self):
        source = '/0/public/AssetPairs'
        respond = self.__get_respond__(source)
        print(respond.json())
        tradable_assets = self.__extract_respond__(respond)
        return tradable_assets


    def get_tradable_asset(self, asset):
        source = '/0/public/AssetPairs?pair=%s' % asset
        respond = self.__get_respond__(source)
        tradable_asset = self.__extract_respond__(respond)
        return tradable_asset


    '''
        Array of strings
        a   Ask [<price>, <whole lot volume>, <lot volume>]
        b   Bid [<price>, <whole lot volume>, <lot volume>]
        c   Last trade closed [<price>, <lot volume>]
        v   Volume [<today>, <last 24 hours>]
        p   Volume weighted average price [<today>, <last 24 hours>]
        t   Number of trades [<today>, <last 24 hours>]
        l   Low [<today>, <last 24 hours>]
        h   High [<today>, <last 24 hours>]
        o   Today's opening price
    '''
    def get_pair_info(self, pair):
        source = '/0/public/Ticker?pair=%s' % pair
        respond = self.__get_respond__(source)
        pair = self.__extract_respond__(respond)
        return pair

    
    def get_ohlc_data(self, pair):
        source = '/0/public/OHLC?pair=%s' % pair
        respond = self.__get_respond__(source)
        ohlc = self.__extract_respond__(respond)
        return ohlc

    '''
    asks    Ask side array of entries [<price>, <volume>, <timestamp>]
    bid     Bid side array of entries [<price>, <volume>, <timestamp>]
    '''
    def get_order_book(self, pair):
        source = '/0/public/Depth?pair=%s' % pair
        respond = self.__get_respond__(source)
        order_book = self.__extract_respond__(respond)
        return order_book

    '''
    [<price>, <volume>, <time>, <buy/sell>, <market/limit>, <miscellaneous>]
    '''
    def get_recent_trades(self, pair):
        source = '/0/public/Trades?pair=%s' % pair
        respond = self.__get_respond__(source)
        recent_trades = self.__extract_respond__(respond)
        return recent_trades


    def get_recent_spreads(self, pair):
        source = '/0/public/Spread?pair=%s' % pair
        respond = self.__get_respond__(source)
        rcent_spreads = self.__extract_respond__(respond)
        return recent_spreads


    def get_account_balance(self):
        source = '/0/private/Balance'
        respond = self.__get_respond__(source)
        balance = self.__extract_respond__(respond)
        return balance


    def get_account_asset(self, asset):
        source = '/0/private/Balance'
        respond = self.__get_respond__(source)
        balance_asset = self.__extract_respond__(respond, asset)
        return balance_asset

    '''
    eb  Equivalent balance (combined balance of all currencies)
    tb  Trade balance (combined balance of all equity currencies)
    m   Margin amount of open positions
    n   Unrealized net profit/loss of open positions
    c   Cost basis of open positions
    v   Current floating valuation of open positions
    e   Equity: trade balance + unrealized net profit/loss
    mf  Free margin: Equity - initial margin (maximum margin available to open new positions)
    ml  Margin level: (equity / initial margin) * 100
    '''
    def get_trade_balance(self, currency):
        source = '/0/private/TradeBalance'
        
        payload = {
            "asset" : currency
        }

        respond = self.__get_respond__(source, payload)
        trade_balance = self.__extract_respond__(respond)
        return trade_balance


    def get_open_orders(self):
        source = '/0/private/OpenOrders'

        payload = {
            "trades": True
        }

        respond = self.__get_respond__(source, payload)
        open_orders = self.__extract_respond__(respond)
        return open_orders
    
    
    def get_closed_orders(self):
        source = '/0/private/ClosedOrders'

        payload = {
            "userref": 36493663
        }

        respond = self.__get_respond__(source, payload)
        closed_orders = self.__extract_respond__(respond)
        return closed_orders


    def get_order_info(self, txid):
        source = '/0/private/QueryOrders'

        payload = {
            "txid": txid, 
            "trades": True
        }

        respond = self.__get_respond__(source, payload)
        order_info = self.__extract_respond__(respond)
        return order_info


    def get_trades_info(self):
        source = '/0/private/TradesHistory'

        payload = {
            "trades": True
        }

        respond = self.__get_respond__(source, payload)
        trades_info = self.__extract_respond__(respond)
        return trades_info

    
    def get_trade_info(self, txid):
        source = '/0/private/QueryTrades'

        payload = {
            "txid": txid, 
            "trades": True
        }

        respond = self.__get_respond__(source, payload)
        trade_info = self.__extract_respond__(respond)
        return trade_info


    def get_open_position(self):
        source = '/0/private/OpenPositions'

        payload = {
            "docalcs": True
        }

        respond = self.__get_respond__(source, payload)
        open_position = self.__extract_respond__(respond)
        return open_position


    def get_ledgers_info(self, currency):
        source = '/0/private/Ledgers'

        payload = {
            "asset": currency, 
            "start": 1610124514
        }

        respond = self.__get_respond__(source, payload)
        ledgers_info = self.__extract_respond__(respond)
        return ledgers_info


    def get_ledger_info(self, id):
        source = '/0/private/QueryLedgers'

        payload = {
            "id": id
        }

        respond = self.__get_respond__(source, payload)
        ledger_info = self.__extract_respond__(respond)
        return ledger_info


    def get_trade_volume(self, pair):
        source = '/0/private/TradeVolume'

        payload = {
            "fee-info": True, 
            "pair": pair
        }

        respond = self.__get_respond__(source, payload)
        trade_volume = self.__extract_respond__(respond)
        return trade_volume

    '''
    ordertype   "market" "limit" "stop-loss" "take-profit" "stop-loss-limit" "take-profit-limit" "settle-position"
    type        "buy" "sell"
    pair        Asset pair id or altname
    price       limit, stop-loss, stop-loss-limit, take-profit and take-profit-limit orders
    price2      Limit price for stop-loss-limit and take-profit-limit orders 
    '''
    def add_order(self, ordertype, type, volume, pair, price):
        source = '/0/private/AddOrder'

        payload = {
            "ordertype": ordertype,
            "type": type,
            "volume": volume,
            "pair": pair,
            "price": price
        }

        respond = self.__get_respond__(source, payload)
        result = self.__extract_respond__(respond)
        return result


    def edit_order(self, txid, volume, pair, price, price2):
        source = '/0/private/EditOrder'

        payload = {
            "txid": txid,
            "volume": volume,
            "pair": pair,
            "price": price,
            "price2": price2
        }

        respond = self.__get_respond__(source, payload)
        result = self.__extract_respond__(respond)
        return result

    
    def cancel_order(self, txid):
        source = '/0/private/CancelOrder'

        payload = {
            "txid": txid
        }

        respond = self.__get_respond__(source, payload)
        result = self.__extract_respond__(respond)
        return result


    def cancel_all_orders(self):
        source = '/0/private/CancelAll'
        respond = self.__get_respond__(source)
        result = self.__extract_respond__(respond)
        return result

