import discord
import global_def as gd

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # 멤버 목록을 가져오기 위해 필요
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    all_members = []  # 모든 멤버들을 저장할 리스트
    print(f'Logged in as {client.user}!')
    for guild in client.guilds:  # 연결된 모든 서버(길드)를 순회
        if guild.name != 'Discord Bot Project':
            print(f'Looking in guild: {guild.name}')
            for channel in guild.voice_channels:  # 해당 서버의 모든 음성 채널을 순회
                print(f'Checking voice channel: {channel.name}')
                members = channel.members
                if members:
                    member_list = ', '.join([member.display_name for member in members])
                    if members:
                        member_list = [member.display_name for member in members]
                        all_members.extend(member_list)
                    print(f'Members in {channel.name}: {member_list}')
                else:
                    print(f'No members in {channel.name}')

    print("All members in voice channels:", all_members)
    print("Total members:", len(all_members))

    for member in all_members:
        print(gd.get_before_at(member))
        print(gd.get_after_at(member))


client.run('MTE4ODk1MjE0OTY1MzIwNTAzMg.Grz3Ed.aQ-pI_X8fq9M3mJbZV6zckLEX6lV-c1oegKXxE')