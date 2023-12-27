# Python code to save a list to a .txt file including the brackets
import re
import os
from datetime import datetime
from collections import defaultdict

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

def hash_members(list_to_hash):
    original_list_len = len(list_to_hash)

    hash_members = defaultdict(list)
    for item in list_to_hash:
        key = get_before_at(item)
        value = get_after_at(item)
        hash_members[key].append(value)
    hash_members_len = sum(len(values) for values in hash_members.values())

    if original_list_len != hash_members_len:
        print(f'WARNING: original list length is not equal {original_list_len} != hash_members len {hash_members_len}')

    return hash_members

# Example usage
if __name__ == "__main__":
    lst = ['死1@반함', '인연@수안', '유리@져햐', '유리@마강마도', '유리@머머', '의지@미백', '유리@대초니', '약속2@요거', '빛@해 리포터', '로망@농협', '시크릿@초보', '빛@광안리가자', '유리@찐따같은초보', '로망@제압 X', '유리@반격', '의리2@강도차승준', '유리@유천우', '유리@라자 바', '약속4@김가율(X)', '의지@뫼뇌 x', '달빛@패브', '약속6@황썬우', '의리2@우드워드', '빛@무현', '의리2@보리', '약속6@극용랑', '약속3@제일궁다샙', ' 死4@보덕국왕 X', '死@따구미 X', '死3@쥐센세', '로망@문안나', '유리@조꺄치', '달빛@미나', '死5@도도코', '死1@습관', '의지@냥이', '약속1@배출(X)', '死@김쭈닝3 X', '약속4@의뀨(X)', '약속3@하땀', '死5@배구', '인연@순각', '로망@분유', '死3@세겹', '약속2@민채', '약속@제빔', '死1@피치', '로망@쿠팡윙X', '유리2@솔랭', '死3@뚠서3 X', '약속1@예리 X', '로망@귀문킬러', '약속1@나나토', '의리1@에스급', '빛@이브x', '인연@잠양', '극한@니트언니', '死1@달래1', '약속6@노래활', '死3@주니', '로망@갓방포', '빛@레리x', '극한@원거리초보', '약속4@포맨(x)', '死1@달링', '의리1@매쫑', '빛@칸포', '死1@초급', '로망@휴지심', '의지@순궁', '의리2@듀님', '약속@비책(듣기용)', '의지@헤이', '빛@으둥', '死1@어멍네', '약속1@어제', '死3@소금3', '의리1@성용몬', '빛@설라X', '약속3@급박', '유리@방어해제', '약속1@상담', '유리@이유나', '빛@섹션', '유리@첼채', '인연@니유', '유리@클링', '약속3@로빈달래', '유리@식객', '약속4@타라수', '로망@원닢', '死1@하히', '시크릿@단요한', '死4@해찬갓4', '유리@나비', '死3@풋볼2 X', '빛@소울트리', '로망@휴디', '달빛@강가', '死2@화니버프(듣기)', '시크릿@호두맥주', '약속3@섬연', '유리@도둑김용수', '死5@후지토라', '약속3@러브힐', '약속4@노숙', '약속@시하', '의리1@파트하', '死4@도톨임', '시 크릿@천치', '인연@재원', '약속2@호로', '약속6@킴럼마', '약속3@팍쿠니', '로망@갈남순', '의리1@힐타치', '인연@슬랜드', '빛@어도', '시크릿@연탈토', '달 빛@지하', '약속2@아가호랑', '로망@재요', '달빛@꿀꺽', '死1@사기', '로망@허효찌', '死5@구탁', '달빛@밤밤', '로망@카디타', '약속2@벨로치', '死5@아이', '달빛@불만', '死3@김삐냥', '빛@극압', '극한@사냥개고수', '유리@사수이광민', '死5@김숙', '로망@홀릭X', '달빛@꼬꼬닦', '약속1@대학생', '약속1@우웅(x)', '약속2@화룡비보', '시크릿@꽃희', '유리@우웽', '로망@투시아', '유리@참젖', '달빛@고천득', '빛@카드', '의리1@나인', '의지@윤인진', 'Developer', '유리1@제코', '약속1@유럽', '死3@신검', '의지@쁠레기X', '달빛@동화', '약속2@호랑', '유리@방역소', '약속6@이수', '약속@신궁', '유리@사숱', '약속4@오프벨', '유리@보이면삼초캇', '로망@배터지는콜라X', '의리1@방심', '달빛@이경진', '달빛@미올', '빛@둘레길', '빛@별새우', '유리@알바코어X', '의지@자몽리', '死4@ 미여누 X', '死3@렌쥬', '의지@넋니', '유리@강지영', '유리@빙구업', '00약속@비책', '약속3@이디은', '약속3@아가도하', '로망@탐키x', '약속2@로우', '유리@종교전쟁X', '로망@싫어', '시크릿@락두', '死5@서포터니까', '약속2@네이x', '로망@앗쉐', '로망@바니', '빛@파도가머물던', '시크릿@응왜', '약속2@군주', ' 의리2@영준', '로망@사신리퍼X', '달빛@빙글', '로망@애틋', '의지@돔황쳐X', '약속1@석윤', '死4@치타X', '死2@화니버프2 ●', '死2@행적2', '死2@후시딘2', ' 死2@꽃서비2', '死2@탐욕의이빨', '死2@탄뎅2', '死2@마도문어2', '死2@자신2']
    print(hash_members(lst))