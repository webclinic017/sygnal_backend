import pandas as pd

from binance import Client
from core.indicators import RSIMACDCrossIndicator, SupertrendIndicator
from .discord_webhook import DiscordWebhook

from core.models import Coin

pd.set_option('display.max_rows', None)


def scan() -> None:
    print('[SCANNING...]')
    client = Client(tld='us')
    coins_with_alerts = []
    coins = Coin.objects.filter(scan=True)

    for coin in coins:
        candle_data = client.get_historical_klines(
            f'{coin.ticker}USDT',
            Client.KLINE_INTERVAL_1HOUR,
            "1 week ago UTC"
        )

        df = pd.DataFrame(
            candle_data,
            columns=[
                'open-time',
                'open',
                'high',
                'low',
                'close',
                'volume',
                'close-time',
                'quote-asset-volume',
                'number-of-trades',
                'taker-buy-base-asset-volume',
                'taker-buy-quote-asset-volume',
                'ignore',
            ],
        )

        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        df['open-time'] = pd.to_datetime(df['open-time'], unit='ms', utc=True)
        df['open-time'] = df['open-time'].dt.tz_convert('America/Los_Angeles')

        coin_alert = {}
        coin_alert['name'] = coin.name
        coin_alert['ticker'] = coin.ticker
        coin_alert['img_url'] = coin.img_url
        coin_alert['color'] = coin.color

        # apply indicators
        supertrend_indicator = SupertrendIndicator(df)
        trend_changed = supertrend_indicator.trend_has_changed()
        coin_alert['Supertrend'] = supertrend_indicator.get_latest_trend()

        macd_cross_indicator = RSIMACDCrossIndicator(df['close'])
        crossed = macd_cross_indicator.is_undersold_and_crossed()
        coin_alert['Crossover'] = macd_cross_indicator.get_cross_status()

        if any([crossed, trend_changed]):
            coins_with_alerts.append(coin_alert)

    send_discord_alerts(coins_with_alerts)


def send_discord_alerts(coins):
    discord = DiscordWebhook()
    for coin in coins:
        discord.send_coin_signal(coin)
