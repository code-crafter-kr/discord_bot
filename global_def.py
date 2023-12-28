# Python code to save a list to a .txt file including the brackets
import re
import os
from datetime import datetime
from collections import defaultdict
import pandas as pd 

# Function to save a list to a file in a directory named with today's date
def save_list_to_file(list_to_save, base_directory, file_name):
    # Get today's date in the format YYYYMMDD
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Create a new directory with today's date
    date_directory = f"{base_directory}/{today_date}"
    if not os.path.exists(date_directory):
        os.makedirs(date_directory)

    # Full path for the file
    full_file_path = f"{date_directory}/{file_name}"

    # Convert the list to string including brackets
    list_as_string = str(list_to_save)
    
    # Write the string representation of the list to the file
    with open(full_file_path, 'w') as file:
        file.write(list_as_string)

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
        return None  # 데이터가 일치하지 않으면 None 반환
    else:
        success_msg = f"Data is equal to original data, original list: {original_len}, DataFrame: {total_non_none_count}"
        print(success_msg)

    return df  # 데이터가 일치하면 DataFrame 반환

def create_print_df(df):
    result = ""
    total_non_none_count = df.notnull().sum().sum()
    for column in df:
        non_null_rows = df[column].dropna()
        # 공백으로 구분된 문자열로 row들을 결합합니다.
        joined_rows = ' '.join(non_null_rows)
        result += f"{column} - 참여인원: {len(non_null_rows)}\n"
        result += joined_rows + '\n\n'
    result += f"총 인원: {total_non_none_count}\n"
    return result


# Example usage
if __name__ == "__main__":
    lst = ['死1@반함', '유리@마강마도', '빛@기광 x', '유리@머머', '약속2@요거', '빛@해리포터', '시크릿@초보', '빛@광안리가자', '유리@찐따같은초보', '빛@추해', '로망@제압 X', '유리@반격', '의리2@강도차승준', '유리@유천우', '유리@라자바', '약속4@김가율(X)', '약속6@황썬우', '의리2@우드워드', '달빛@프릭커', '빛@무현', '의리2@보리', '약속6@극용랑', '약속3@제일궁다샙', '死@따구미 X', '달빛@살살', '유리@동탁', '의지@방깍', '死3@쥐센세', '약속6@승민지(X)', '로망@문안나', '달빛@미나', '빛@아린의', '死1@습관', '의지@냥이', '약속1@배출(X)', '死@김쭈닝3 X', '약속4@의뀨(X)', '死5@배구', '빛@앙지은', '死3@세겹', '약속6@깅경태', '약속3@가은', '약속@제빔', '死1@피치', '유리2@솔랭', '약속1@예리 X', '로망@귀문킬러', '약속1@나나토', '의리1@에스급', '빛@이브x', '인연@잠양', '극한@니트언니', '死3@주니', '빛@레리x', '극한@원거리초보', '약속4@포맨(x)', '死1@달링', '의리1@매쫑', '빛@칸포', '死1@초급', '로망@휴지심', '의지@순궁', '의리2@듀님', '약속@비책(듣기용)', '의지@헤이', '빛@으둥', '死1@어멍네', '약속1@어제', '死3@소금3', '의리1@성용몬', '달빛@떡래', '빛@설라X', '약속3@급박', '유리@방어해제', '약속1@상담', '유리@첼채', '약속3@로빈달래', '약속4@타라수', '死1@하히', '시크릿@단요한', '死4@해찬갓', '유리@나비', '死3@풋볼2 X', '로망@휴디', '死2@화니버프(듣기)', '약속2@에디앙(X)', '시크릿@호두맥주', '유리@콩치', '약속2@섬연', '유리@도둑김용수', '死5@후지토라', '약속4@뚱붕(X)', '약속4@노숙', '약속@시하', '의리2@아가유나', '의리2@파트하', '인연@재원', '약속2@호로', '약속6@킴럼마', '약속1@팍쿠니', '의리1@힐타치', '약속4@셔룩(x)', '빛@어도', '시크릿@연탈토', '빛@진도표', '약속2@아가호랑', '달빛@꿀꺽', '死1@사기', '약속3@뱀띠', '빛@명주르', '유리@랫쥐', '약속6@라임초', '로망@허효찌', '死5@구탁', '달빛@밤밤', '로망@카디타', '死5@아이', '死3@김삐냥', '극한@사냥개고수', '유리@사수이광민', '死5@김숙', '의리1@체람', '로망@홀릭X', '달빛@꼬꼬닦', '약속1@대학생', '약속2@화룡비보', '시크릿@꽃희', '유리@우웽', '유리@참젖', '달빛@고천득', '빛@카드', '달빛@할수없어', '유리1@제코', '약속1@유럽', '死3@신검', '의지@쁠레기X', '달빛@동화', '약속2@호랑', '유리@이슬상', '약속@신궁', '유리@사숱', '의지@붸츄X', '유리@보이면삼초캇', '빛@마기', '로망@배터지는콜라X', '의리1@방심', '달빛@이경진', '빛@둘레길', '유리@알바코어X', '의지@자몽리', '死4@미여누 X', '死3@렌쥬', '달빛@쩌리', '의지@넋니', '유리@빙구업', '00약속@비책', '의리2@고맡X', '로망@탐키x', '약속2@로우', '死5@낙현', '의지@황창영x', '의리1@정연X', '로망@싫어', '死5@서포터니까', '약속2@네이x', '로망@앗쉐', '로망@바니', '시크릿@응왜', '극한@모도', '약속2@군주', '의리2@영준', '달빛@빙글', '로망@애틋', '의지@돔황쳐X', '약속4@아잇츄', '약속1@석윤', '死4@치타X']
    df = create_hashed_df(lst)
    print(df)