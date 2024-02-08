import os
import pandas as pd
import numpy as np
from collections import defaultdict


def organize_and_sum_data_by_group(df):
    result = defaultdict(lambda: defaultdict(float))  # 소속을 키로, 멤버 이름과 점수의 합을 저장하는 내부 딕셔너리를 가짐
    columns = df.columns

    for i in range(0, len(columns), 2):
        group_name = columns[i]  # 소속 정보
        member_col = columns[i]  # 멤버 이름 컬럼
        attendance_col = columns[i+1]  # 출석 점수 컬럼
        
        for _, row in df.iterrows():
            member = row[member_col]
            attendance = row[attendance_col]
            #member가 nan이면 pass
            if pd.isna(member):
                continue
            
            if pd.notna(attendance):  # 점수가 NaN이 아닌 경우에만 합산
                result[group_name][member] += attendance
    
    # 결과를 보다 직관적으로 이해하기 위해 구조 조정
    final_result = {group: [{"이름": member, "횟수": score} for member, score in members.items()] for group, members in result.items()}
    
    return final_result

def create_df_from_organized_dict(organized_data):
    # 모든 멤버 이름을 저장할 세트
    all_members = set()
    
    # 각 그룹별 멤버와 횟수를 저장할 딕셔너리
    group_data = defaultdict(dict)
    
    for group, members in organized_data.items():
        for member_info in members:
            member = member_info['이름']
            count = member_info['횟수']
            all_members.add(member)
            group_data[group][member] = count
            
    # 데이터프레임 생성을 위한 준비
    columns = []
    data = []
    
    # 컬럼명 준비
    for group in group_data.keys():
        columns.append(group)
        columns.append(f'출석:{group}')
    
    # 데이터 준비
    for member in all_members:
        row = []
        for group in group_data.keys():
            row.append(member if member in group_data[group] else None)  # 멤버 이름 추가
            row.append(group_data[group].get(member, None))  # 해당 그룹에서 멤버의 횟수 추가
        data.append(row)
        
    # 데이터프레임 생성
    df = pd.DataFrame(data, columns=columns)
    
    return df

def sum_all_numeric_values(df):
    # 숫자형 데이터를 포함하는 컬럼만 선택
    numeric_df = df.select_dtypes(include=['number'])
    # 선택된 컬럼의 모든 값들을 합산
    total_sum = numeric_df.sum().sum()  # 첫 번째 sum()은 컬럼별 합, 두 번째 sum()은 그 결과의 합
    return total_sum

def multiply_all_numeric_values(df, multiplier):
    # 숫자형 데이터를 포함하는 컬럼만 선택하여 곱셈 수행
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].apply(lambda x: x * multiplier)
    return df

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

df_concat = pd.concat([dataframes[i] for i in range(len(dataframes))], ignore_index=True) # 모든 데이터프레임을 하나로 합치기

result = organize_and_sum_data_by_group(df_concat) # 데이터 정리 및 합산 함수 호출
final_df = create_df_from_organized_dict(result)  # 데이터프레임 생성 함수 호출

total_sum = sum_all_numeric_values(final_df)  # 모든 숫자항의 합을 계산하는 함수 호출
final_df.to_csv("final_df.csv", index=False, encoding="utf-8-sig")  # 결과를 CSV 파일로 저장

print(final_df)
print("총 참여횟수: ", total_sum)