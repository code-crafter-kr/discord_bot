import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


async def response_message(message):
    filepath = '/home/code_crafter/Desktop/Project/run.txt'
    content = message.content

    if content == "설정":
        response = '현재 출석 설정 입니다\n'
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                key, value = line.strip().split(':')
                if value == '1':
                    response += f'{key} 출석 activated\n'
                elif value == '0':
                    response += f'{key} 출석 deactivated\n'
        await message.channel.send(response)

    elif content == "화요일공성 on":
        update_event_status('화요일공성', '1')
        await message.channel.send('화요일공성 출석이 활성화되었습니다.')
    elif content == "수요일공성 on":
        update_event_status('수요일공성', '1')
        await message.channel.send('수요일공성 출석이 활성화되었습니다.')
    elif content == "목요일공성 on":
        update_event_status('목요일공성', '1')
        await message.channel.send('목요일공성 출석이 활성화되었습니다.')
    elif content == "금요일공성 on":
        update_event_status('금요일공성', '1')
        await message.channel.send('금요일공성 출석이 활성화되었습니다.')
    elif content == "평일분쟁2000 on":
        update_event_status('평일분쟁2000', '1')
        await message.channel.send('평일분쟁 8시 출석이 활성화되었습니다.')
    elif content == "평일분쟁2300 on":
        update_event_status('평일분쟁2300', '1')
        await message.channel.send('평일분쟁 11시 출석이 활성화되었습니다.')
    elif content == "주말분쟁1430 on":
        update_event_status('주말분쟁1430', '1')
        await message.channel.send('주말분쟁 2시 30분 출석이 활성화되었습니다.')
    elif content == "주말분쟁1500 on":
        update_event_status('주말분쟁1500', '1')
        await message.channel.send('주말분쟁 3시 00분 출석이 활성화되었습니다.')
    elif content == "주말분쟁2000 on":
        update_event_status('주말분쟁2000', '1')
        await message.channel.send('주말분쟁 8시 출석이 활성화되었습니다.')
    elif content == "주말분쟁2300 on":
        update_event_status('주말분쟁2300', '1')
        await message.channel.send('주말분쟁 11시 출석이 활성화되었습니다.')
    
    elif content == "화요일공성 off":
        update_event_status('화요일공성', '0')
        await message.channel.send('화요일공성 출석이 비활성화되었습니다.')
    elif content == "수요일공성 off":
        update_event_status('수요일공성', '0')
        await message.channel.send('수요일공성 출석이 비활성화되었습니다.')
    elif content == "목요일공성 off":
        update_event_status('목요일공성', '0')
        await message.channel.send('목요일공성 출석이 비활성화되었습니다.')
    elif content == "금요일공성 off":
        update_event_status('금요일공성', '0')
        await message.channel.send('금요일공성 출석이 비활성화되었습니다.')
    elif content == "평일분쟁2000 off":
        update_event_status('평일분쟁2000', '0')
        await message.channel.send('평일분쟁 8시 출석이 비활성화되었습니다.')
    elif content == "평일분쟁2300 off":
        update_event_status('평일분쟁2300', '0')
        await message.channel.send('평일분쟁 11시 출석이 비활성화되었습니다.')
    elif content == "주말분쟁1430 off":
        update_event_status('주말분쟁1430', '0')
        await message.channel.send('주말분쟁 2시 30분 출석이 비활성화되었습니다.')
    elif content == "주말분쟁1500 off":
        update_event_status('주말분쟁1500', '0')
        await message.channel.send('주말분쟁 3시 00분 출석이 비활성화되었습니다.')
    elif content == "주말분쟁2000 off":
        update_event_status('주말분쟁2000', '0')
        await message.channel.send('주말분쟁 8시 출석이 비활성화되었습니다.')
    elif content == "주말분쟁2300 off":
        update_event_status('주말분쟁2300', '0')
        await message.channel.send('주말분쟁 11시 출석이 비활성화되었습니다.')
    else:
        print('xx')

def update_event_status(event_name, status):
    filepath = '/home/code_crafter/Desktop/Project/run.txt'

    # 파일 읽기
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 상태 업데이트
    updated_lines = []
    for line in lines:
        if line.startswith(event_name):
            key, _ = line.strip().split(':')
            updated_line = f'{key}:{status}\n'
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    # 파일 다시 쓰기
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)


@bot.event
async def on_message(message):
    # 특정 사용자들의 ID 목록
    specific_user_ids = [332468315895365632, 356357918310006794]

    # 특정 채널의 ID
    specific_channel_id = 1071803555926790177
    print(message.content)
    
    # 메시지가 봇에 의한 것이거나 특정 사용자들 중 하나가 아니거나 특정 채널이 아닌 경우 무시
    if message.author == bot.user or message.author.id not in specific_user_ids or message.channel.id != specific_channel_id:
        return

    await response_message(message)


# 봇 토큰
TOKEN = 'MTE4ODk1MjE0OTY1MzIwNTAzMg.Grz3Ed.aQ-pI_X8fq9M3mJbZV6zckLEX6lV-c1oegKXxE'

bot.run(TOKEN)
