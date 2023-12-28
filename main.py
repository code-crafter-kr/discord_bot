import discord
import global_def as gd
from datetime import datetime


CHANNEL_ID = 1071803555926790177 # server id
CLIENT_ID = 332468315895365632 # user id (client id)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Subscribe to the privileged members intent.
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    all_members = []  # list for all members in voice channels
    print(f'Logged in as {client.user}!')
    for guild in client.guilds:  # traverse all guilds that bot is in
        if guild.name != 'Discord Bot Project':
            print(f'Looking in guild: {guild.name}')
            for channel in guild.voice_channels:  # traverse all voice channels in the guild
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

    # # Save the list of members to a file
    gd.save_list_to_file(all_members, 'backup', 'members.txt')

    df = gd.create_hashed_df(all_members)
    printing_result = gd.create_print_df(df)

    # # Send the message to the channel
    channel = client.get_channel(CHANNEL_ID)    
    if channel:
        await channel.send(printing_result)
    else:
        print(f"Channel with ID {CHANNEL_ID} not found.")
    
    user = await client.fetch_user(CLIENT_ID)  # get the user object

    today_date = datetime.today().strftime('%Y-%m-%d')
    FILE_PATH = 'backup' + today_date + '/members.csv'
    with open(FILE_PATH, 'rb') as file:  # open the file
        await user.send(file=discord.File(file, 'filename.csv'))  # send it to the user
    

client.run('MTE4ODk1MjE0OTY1MzIwNTAzMg.Grz3Ed.aQ-pI_X8fq9M3mJbZV6zckLEX6lV-c1oegKXxE')