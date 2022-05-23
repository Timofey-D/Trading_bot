import time

from kraken import Kraken
from preprocessing import Preprocessing



if __name__ == '__main__':

    exchange = Kraken("api.ini")

    #server_time = exchange.get_server_time()
    #exchange.get_system_status()
    respond = exchange.get_assets_info()
    respond = exchange.get_asset_info('UST')
    respond = exchange.get_tradable_assets()
    respond = exchange.get_tradable_asset('1INCHEUR')
    respond = exchange.get_pair_info('XBTUSD')
    #respond = exchange.get_ohlc_data('XBTUSD')
    #respond = exchange.get_order_book('XBTUSD')
    #respond = exchange.get_recent_trades('XBTUSD')
    #respond = exchange.get_recent_spreads('XBTUSD')
    #respond = exchange.get_account_balance()
    #respond = exchange.get_account_asset('STORJ')
    #respond = exchange.get_trade_balance('USD')
    #respond = exchange.get_open_orders()
    #respond = exchange.get_closed_orders()
    #respond = exchange.get_order_info('OYDUP3-WFXN6-W3DHJA')
    #respond = exchange.get_trades_info()
    #respond = exchange.get_trade_info('OYDUP3-WFXN6-W3DHJA')
    #respond = exchange.get_open_position()
    #respond = exchange.get_ledgers_info('USD')
    #respond = exchange.get_ledger_info('LRURID-SXTNH-5R6CJP')
    #respond = exchange.get_trade_volume('XBTUSD')

    data = Preprocessing(respond)




    '''
    start_time = time.time()

    pair = 'ETHUSDT'
    
    account = sm(100000)
    
    budget = account.get_budget()
    print('Primary budget', budget)

    previous_time = 0
    prev_slow_sma = 0
    prev_fast_sma = 0
    while True:
        # The method gets PAIR and INTERVAL
        ohlc = dp.get_ohlc('ETHUSDT', 1)

        #cache.creation_or_updation_table_file('ETH_price.csv', ohlc, ['time', 'open', 'high', 'low', 'close'])
    
        if ohlc['time'].values[-1] != previous_time:
            curr_slow_sma = ts.SMA(ohlc, 'close', 120)
            curr_fast_sma = ts.SMA(ohlc, 'close', 60)

            signal = ts.comparison_ma(prev_slow_sma, curr_slow_sma, prev_fast_sma, curr_fast_sma)

            if signal == -1 or signal == 1:
                sgnl = [dp.convert_unixtime(ohlc['time'].values[-1]), ohlc['open'].values[-1], ohlc['high'].values[-1], ohlc['low'].values[-1], ohlc['close'].values[-1]]
                print(sgnl, 'BUY' if signal == 1 else 'SELL')

                #order = ts.creation_of_order(budget, 5, signal, pair)
                #account.add_position(order)
                #cache.creation_or_updation_table_file('Orders.csv', order.get_position(), ['id', 'Pair', 'Price', 'Volume', 'Type', 'Ordertype', 'Time', 'Position_cost'])
                #order.info_order()
                print()

            prev_ssma = curr_slow_sma
            prev_fsma = curr_fast_sma
            #cache.creation_or_updation_table_file('ETH_SMA.csv', [[curr_slow_sma, curr_fast_sma]], ['SMA_120', 'SMA_60'])

        previous_time = ohlc['time'].values[-1]
        time.sleep(30)

    print("--- %s seconds ---" % (time.time() - start_time))

   #cache.create_file('ETH_sma_60m.csv')
   '''
