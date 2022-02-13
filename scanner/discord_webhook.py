import datetime
import environ
import os

from discord import Embed, RequestsWebhookAdapter, Webhook
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class DiscordWebhook():
    def __init__(self) -> None:
        now = datetime.datetime.now(ZoneInfo("America/Los_Angeles"))
        self.timestamp = now.strftime("%a, %d %b %Y %I:%M %p")

    def send_coin_signal(self, coin) -> None:
        ticker = coin.pop('ticker')
        name = coin.pop('name')
        img_url = coin.pop('img_url')
        color = coin.pop('color')


        # https://stackoverflow.com/questions/64799340/discord-js-embed-width-is-unreliable
        embed = Embed(color=color)
        embed.set_image(url='https://i.stack.imgur.com/Fzh0w.png')
        embed.set_author(name=f'{name} ({ticker})', icon_url=img_url)
        embed.set_footer(text=self.timestamp)

        for k, v in coin.items():
            embed.add_field(name=k, value=v)

        webhook = Webhook.from_url(env("WEBHOOK_URL"), adapter=RequestsWebhookAdapter())
        webhook.send(embed=embed)
