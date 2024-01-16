import discord
import sys
import global_def as gd
from datetime import datetime

CHANNEL_ID = 1071803555926790177
CLIENT_ID = 332468315895365632 # 둘레님
# CLIENT_ID = 356357918310006794 # 나

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)



def gather_voice_channel_members(client): #완성형
    all_members = []
    for guild in client.guilds:
        if guild.name != 'Discord Bot Project':
            for channel in guild.voice_channels:
                members = channel.members
                if members:
                    all_members.extend([member.display_name for member in members])
    return all_members #모든 멤버 리스트로 반환환

async def save_and_print_set(members, param):
    gd.save_list_to_file(members, 'backup', param, today_date) # txt 및 csv 파일로 변환
    df = gd.create_hashed_df(members) # 해시 df로 변환 출력용
    return gd.create_print_df(df, param) # 출력용 form 으로 변환


async def send_channel_message(client, message):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print(f"Channel with ID {CHANNEL_ID} not found.")

async def send_user_file(client, file_path, filename):
    user = await client.fetch_user(CLIENT_ID)
    with open(file_path, 'rb') as file:
        today_type = gd.get_attendance_message(param, today_date)
        await user.send(f"{today_type} 입니다.")
        await user.send(file=discord.File(file, filename))

@client.event
async def on_ready():
    global param, today_date
    file_name = gd.get_attendance_filemname_csv(param, today_date)
    print(f'Logged in as {client.user}!')
    members = gather_voice_channel_members(client)
    print("Total members:", len(members))
    message = await save_and_print_set(members, param)
    await send_channel_message(client, message)
    today_date = datetime.today().strftime('%Y-%m-%d')
    file_path = f'backup/{today_date}/{file_name}'
    await send_user_file(client, file_path, file_name)
    await client.close()
    sys.exit()  # 스크립트 실행을 종료합니다.

def run_file(param):
    with open('run.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # 빈 줄이 아닌 경우에만 처리
                key, value = line.split(':')
                if key.strip() == param and value.strip() == '0':
                    return False
    return True

def run_bot(token):
    client.run(token)



param = input() #cron 설정에서 넘겨받을 예정
today_date = datetime.today().strftime('%Y-%m-%d')

if not run_file(param): # run.txt 에서 해당 파라미터가 0이면 종료
    sys.exit()

run_bot('MTE4ODk1MjE0OTY1MzIwNTAzMg.Grz3Ed.aQ-pI_X8fq9M3mJbZV6zckLEX6lV-c1oegKXxE')