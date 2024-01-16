# Python code to save a list to a .txt file including the brackets
import re
import os
from datetime import datetime
from collections import defaultdict
import pandas as pd 


def get_attendance_message(param, today_date):
    today_date = datetime.today().strftime('%Y-%m-%d')
    messages = {
        "화요일공성": "화요일 공성 출석",
        "수요일공성": "수요일 공성 출석",
        "목요일공성": "목요일 공성 출석",
        "금요일공성": "금요일 공성 출석",
        "평일분쟁2000": "평일 분쟁 오후 8시 출석",
        "평일분쟁2300": "평일 분쟁 오후 11시 출석",
        "주말분쟁1430": "주말 분쟁 오후 2시 30분 출석",
        "주말분쟁1500": "주말 분쟁 오후 3시 00분 출석",
        "주말분쟁2000": "주말 분쟁 오후 8시 출석",
        "주말분쟁2300": "주말 분쟁 오후 11시 출석"
    }
    
    return messages.get(param, f"{today_date} : {param} 입니다")

def get_attendance_filemname_txt(param, today_date):
    messages = {
        "화요일공성": f"{today_date}_화요일공성.txt",
        "수요일공성": f"{today_date}_수요일공성.txt",
        "목요일공성": f"{today_date}_목요일공성.txt",
        "금요일공성": f"{today_date}_금요일공성.txt",
        "평일분쟁2000": f"{today_date}_평일분쟁2000.txt",
        "평일분쟁2300": f"{today_date}_평일분쟁2300.txt",
        "주말분쟁1430": f"{today_date}_주말분쟁1430.txt",
        "주말분쟁1500": f"{today_date}_주말분쟁1500.txt",
        "주말분쟁2000": f"{today_date}_주말분쟁2000.txt",
        "주말분쟁2300": f"{today_date}_주말분쟁2300.txt"
    }
    
    return messages.get(param, f"{today_date}_{param}.txt")

def get_attendance_filemname_csv(param, today_date):
    today_date = datetime.today().strftime('%Y-%m-%d')
    messages = {
        "화요일공성": f"{today_date}_화요일공성.csv",
        "수요일공성": f"{today_date}_수요일공성.csv",
        "목요일공성": f"{today_date}_목요일공성.csv",
        "금요일공성": f"{today_date}_금요일공성.csv",
        "평일분쟁2000": f"{today_date}_평일분쟁2000.csv",
        "평일분쟁2300": f"{today_date}_평일분쟁2300.csv",
        "주말분쟁1430": f"{today_date}_주말분쟁1430.csv",
        "주말분쟁1500": f"{today_date}_주말분쟁1500.csv",
        "주말분쟁2000": f"{today_date}_주말분쟁2000.csv",
        "주말분쟁2300": f"{today_date}_주말분쟁2300.csv"
    }
    
    return messages.get(param, f"{today_date}_{param}.csv")



# Function to save a list to a file in a directory named with today's date
def save_list_to_file(list_to_save, base_directory, param, today_date):
    
    file_txt = get_attendance_filemname_txt(param, today_date)
    file_csv = get_attendance_filemname_csv(param, today_date)

    # Create a new directory with today's date
    date_directory = f"{base_directory}/{today_date}"
    if not os.path.exists(date_directory):
        os.makedirs(date_directory)

    # Full path for the file
    full_file_path = f"{date_directory}/{file_txt}"

    # Convert the list to string including brackets
    list_as_string = str(list_to_save)
    
    # Write the string representation of the list to the file
    with open(full_file_path, 'w') as file:
        file.write(list_as_string)

    df = create_hashed_df(list_to_save)
    # save df
    df.to_csv(f"{date_directory}/{file_csv}", index=False, encoding='utf-8-sig')

# Function to save a list to a file in a directory named with today's date
def get_before_at(text):
    match = re.search(r'([^@]+)@(.+)', text)
    if match:
        before_at = match.group(1)
        cleaned_before_at = re.sub(r'[0-9]|[\W_]|\b[xX]\b', '', before_at)
        return cleaned_before_at
    else:
        return '기타'

# Function to save a list to a file in a directory named with today's date
def get_after_at(text):
    match = re.search(r'([^@]+)@(.+)', text)
    if match:
        after_at = match.group(2)
        cleaned_after_at = re.sub(r'[^\uAC00-\uD7A3]', '', after_at)
        return cleaned_after_at
    else:
        return None 

def list_to_hash(lst):
    original_list_len = len(lst)

    hash_members = defaultdict(list)
    for item in lst:
        key = get_before_at(item)
        value = get_after_at(item)
        hash_members[key].append(value)
    hash_members_len = sum(len(values) for values in hash_members.values())

    if original_list_len != hash_members_len:
        print(f'WARNING: original list length is not equal {original_list_len} != hash_members len {hash_members_len}')

    return hash_members


def create_hashed_df(lst):
    original_len = len(lst)  # 최초의 리스트 길이를 저장 (최초 데이터 개수)
    hash_members = list_to_hash(lst)

    # 각 키에 대한 최대 길이를 구함
    max_length = max(len(v) for v in hash_members.values())

    # 모든 리스트를 동일한 길이로 맞춤
    for key in hash_members:
        hash_members[key].extend([None] * (max_length - len(hash_members[key])))

    # 판다스 데이터프레임으로 변환
    df = pd.DataFrame(dict(hash_members))
    non_none_counts_per_column = df.notnull().sum()  # 각 컬럼별로 None이 아닌 데이터 개수를 구함
    total_non_none_count = non_none_counts_per_column.sum()  # 모든 컬럼의 None이 아닌 데이터 개수를 구함

    # 데이터 검증
    if original_len != total_non_none_count:
        warning_msg = f"WARNING: Data is not equal to original data, original data: {original_len}, current data: {total_non_none_count}, please check the data."
        print(warning_msg)
        return df  # 데이터가 일치하지 않아도 일단 반환
    else:
        success_msg = f"Data is equal to original data, original list: {original_len}, DataFrame: {total_non_none_count}"
        print(success_msg)

    return df  # 데이터가 일치하면 DataFrame 반환

def create_print_df(df, param):
    today_date = datetime.today().strftime('%Y-%m-%d')
    today_type = get_attendance_message(param, today_date)

    result = f"{today_date} : {today_type} 입니다\n"

    total_non_none_count = df.notnull().sum().sum()
    for column in df:
        non_null_rows = df[column].dropna()
        # 공백으로 구분된 문자열로 row들을 결합합니다.
        joined_rows = ' '.join(non_null_rows)
        result += f"{column} - 참여인원: {len(non_null_rows)}명\n"
        result += "-" + joined_rows + '\n\n'
    result += f"총 인원: {total_non_none_count}\n"
    return result
