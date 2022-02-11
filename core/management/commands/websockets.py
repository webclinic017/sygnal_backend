# import pprint
# import json
# import websocket
# from datetime import datetime
# from django.core.management.base import BaseCommand

# pp = pprint.PrettyPrinter(indent=4)


# class Command(BaseCommand):
#     """ https://github.com/binance-us/binance-official-api-docs/blob/master/web-socket-streams.md """
#     help = 'Creates connection to Binanace.US Websocket'

#     def handle(self, *args, **options):
#         SOCKET = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'

#         def on_open(ws):
#             self.stdout.write(self.style.SUCCESS('WebSocket connection opened'))

#         def on_close(ws):
#             self.stdout.write(self.style.ERROR('WebSocket connection closed'))

#         def on_message(ws, message):
#             message_dict = json.loads(message)
#             candle = message_dict['k']
#             candle_closed = candle['x']

#             if candle_closed:
#                 print('CLOSED')
#                 timestamp = message_dict['E'] / 1000
#                 print(message_dict)
#                 print(datetime.fromtimestamp(timestamp/100))

#         ws = websocket.WebSocketApp(
#             SOCKET,
#             on_open=on_open,
#             on_close=on_close,
#             on_message=on_message,
#         )

#         ws.run_forever()
