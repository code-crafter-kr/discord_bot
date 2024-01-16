import os
import pandas as pd
import numpy as np


# 현재 작업 디렉토리 가져오기
current_folder = os.getcwd()

# 현재 폴더 내의 모든 CSV 파일 목록 가져오기
csv_files = [f for f in os.listdir(current_folder) if f.endswith('.csv')]
# 모든 CSV 파일을 DataFrame으로 읽고 하나의 리스트에 저장
dataframes = []
for file in csv_files:
    file_path = os.path.join(current_folder, file)
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
    # group 을 데이터프레임의 열 제목으로 사용
    for idx, participant in enumerate(participants):
        # group을 데이터프레임의 열 제목으로 사용하고, idx를 행 인덱스로 사용
        df.loc[idx, group] = participant
        df.loc[idx, "출석" + ":" + group] = combined_df[group].value_counts()[participant]
        idx += 1
        continue


df.to_csv('group_counts.csv', index=False, encoding='utf-8-sig')