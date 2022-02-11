import discord
import environ

env = environ.Env()
environ.Env.read_env()
DISCORD_BOT_TOKEN = env("DISCORD_BOT_TOKEN")


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'What is the price of bitcoin':
            await message.channel.send('Too much for yo broke ass!')


client = MyClient()
client.run(DISCORD_BOT_TOKEN)

# https://stackoverflow.com/questions/39003853/passing-arguments-when-scheduling-a-function-with-asyncio-aiocron/39005726#39005726
# https://stackoverflow.com/questions/60719186/how-do-i-make-my-discord-bot-run-a-function-every-sunday-at-000/60721216
# https://github.com/gawel/aiocron
