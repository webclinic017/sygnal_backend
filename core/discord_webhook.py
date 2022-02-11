import environ
import os
import asyncio

from pathlib import Path
from discord import Webhook, RequestsWebhookAdapter


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

env = environ.Env()
environ.Env.read_env()
URL = env("WEBHOOK_URL")


async def cornjob1():
    print("SENDING WEBHOOK MESSAGE")
    webhook = Webhook.from_url(URL, adapter=RequestsWebhookAdapter())
    webhook.send('Webhook Test', username='s y g n a l')

asyncio.run(cornjob1)
