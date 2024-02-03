import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import discord
import sys
import global_def as gd


intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 1071803555926790177
CLIENT_ID = 332468315895365632 # 둘레님
# CLIENT_ID = 356357918310006794 # 나


def check_content_for_string(file_path, search_string):
    """파일 내용에서 특정 문자열이 있는지 확인합니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if search_string in line:
                    return True
            return False
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False  # 파일 읽기 에러 발생 시, 기본적으로 문자열이 없는 것으로 처리

today_date = datetime.today().strftime('%Y-%m-%d')


# # 오늘 날짜에서 하루를 빼기
# today_date = datetime.today() - timedelta(days=1)

# # 날짜를 'YYYY-MM-DD' 형식의 문자열로 포매팅
# formatted_date = today_date.strftime('%Y-%m-%d')# 특정 폴더 경로 설정

folder_path = f'/home/code_crafter/backup/{today_date}'

# 현재 폴더 내의 모든 CSV 파일 목록 가져오기
csv_files = []
for f in os.listdir(folder_path):
    if f.endswith('.csv'):
        file_path = os.path.join(folder_path, f)
        # 파일 내 '공성' 문자열이 없는 경우에만 리스트에 추가
        if not check_content_for_string(file_path, '공성'):
            csv_files.append(f)

# 모든 CSV 파일을 DataFrame으로 읽고 하나의 리스트에 저장
dataframes = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

group_columns = [col for col in combined_df.columns]
group_participants = {col: combined_df[col].dropna().unique() for col in group_columns}

lst = []
for i in group_columns:
    lst.append(i)
    lst.append("출석" + ":" + i)
data = np.nan * np.ones((100, len(lst)))

df = pd.DataFrame(data, columns=lst)

for group, participants in group_participants.items():
    idx = 0
    for idx, participant in enumerate(participants):
        df.loc[idx, group] = participant
        # 참여 횟수를 계산할 때 에러가 발생하지 않도록 예외 처리가 필요할 수 있음
        df.loc[idx, "출석" + ":" + group] = combined_df[group].value_counts().get(participant, 0)
        idx += 1
        continue
today_date = datetime.today().strftime('%Y-%m-%d')

filename = today_date + "-dispute.csv"

async def send_user_file(client, file_path, filename, today_date):
    user = await client.fetch_user(CLIENT_ID)
    with open(file_path, 'rb') as file:
        await user.send(f"{today_date} 분쟁 통계 입니다.")
        await user.send(file=discord.File(file, filename))

# 결과를 특정 폴더에 저장
output_file_path = os.path.join(folder_path, filename)
df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

@client.event
async def on_ready():

    await send_user_file(client, output_file_path, filename, today_date)
    await client.close()
    sys.exit()  # 스크립트 실행을 종료합니다.
    
def run_bot(token):
    client.run(token)

run_bot('MTE4ODk1MjE0OTY1MzIwNTAzMg.Grz3Ed.aQ-pI_X8fq9M3mJbZV6zckLEX6lV-c1oegKXxE')
