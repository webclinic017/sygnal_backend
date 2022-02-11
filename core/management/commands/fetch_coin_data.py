# import ccxt
# import datetime
# import pandas as pd
# import schedule
# import time

# from django.core.management.base import BaseCommand
# from zoneinfo import ZoneInfo

# from core.indicators import RSIMACDCrossIndicator, SupertrendIndicator
# from core.utilities import slack

# pd.set_option('display.max_rows', None)


# class Command(BaseCommand):
#     exchange = ccxt.binanceus()
#     coins = [
#         {'name': 'Bitcoin', 'ticker': 'BTC'},
#         # {'name': 'Ethereum', 'ticker': 'ETH'},
#         # {'name': 'Lightcoin', 'ticker': 'LTC'},
#         # {'name': 'Cardano', 'ticker': 'ADA'},
#         # {'name': 'Cosmos', 'ticker': 'ATOM'},
#     ]

#     def fetch_candles(self):
#         now = datetime.datetime.now(ZoneInfo("America/Los_Angeles"))
#         timestamp = now.strftime("%a, %d %b %Y %I:%M %p")
#         print(f'Fetching coin data [{timestamp}]....')


#         for coin in self.coins:
#             ticker = coin.get('ticker')
#             candle_data = self.exchange.fetch_ohlcv(f'{ticker}/USDT', timeframe='1h', limit=100)
#             df = pd.DataFrame(candle_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

#             df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
#             df['timestamp'] = df['timestamp'].dt.tz_convert('America/Los_Angeles')

#             supertrend_indicator = SupertrendIndicator(df)
#             df['in_uptrend'] = supertrend_indicator.supertrend()

#             macd_cross_indicator = RSIMACDCrossIndicator(df['close'])
#             df['rsi_macd_cross'] = macd_cross_indicator.crossover()

#             print(df)

#         # if coins_with_alerts:
#         #     slack(coins=coins_with_alerts)

#     def handle(self, *args, **options):
#         schedule.every(2).seconds.do(self.fetch_candles)
#         # schedule.every(20).minutes.do(self.fetch_candles)
#         # schedule.every().hour.at(":01").do(self.fetch_candles)

#         while True:
#             schedule.run_pending()
#             time.sleep(1)
