import discord
 
TOKEN = 'MTE4ODk1MjE0OTY1MzIwNTAzMg.Grz3Ed.aQ-pI_X8fq9M3mJbZV6zckLEX6lV-c1oegKXxE'
CHANNEL_ID = '1188942267420000359'
 
 
class MyClient(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        # 텍스트 채널인지 확인
        if isinstance(channel, discord.TextChannel):
            await channel.send('Hello World')
        else:
            print(f"The channel with ID {CHANNEL_ID} is not a text channel.")
 
 
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)