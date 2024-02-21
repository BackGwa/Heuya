import json
import discord

from dodb import Dodb

# 설정 파일 불러오기
with open('./config.json', 'r') as data:
    config = json.load(data)

# 봇 설정 적용
intents = discord.Intents.default()
intents.message_content = True

TOKEN       = config["bot_setting"]["token"]
USERID      = config["bot_setting"]["userid"]

# DoDB 설정 적용
NAME        = config["dodb_setting"]["name"]
PATH        = config["dodb_setting"]["path"]
DATA_FORMAT = config["dodb_setting"]["format"]

# 기본값 설정
recent_time = None
path        = None

# 클래스 초기화
db = Dodb(NAME, PATH, DATA_FORMAT)
client = discord.Client(intents=intents)


# 봇 작동 시작 시
@client.event
async def on_ready():
    global recent_time, path
    recent_time = db.gen_now()[0]
    print("KILOGWA - Ready!")
    path = db.file_register()

    activity = discord.Game("백과 따라")
    await client.change_presence(status=discord.Status.online, activity=activity)


# 메세지 입력 감지 시
@client.event
async def on_message(message):
    global recent_time

    # 봇 또는, 자기 자신에 관한 대화는 무시
    if message.author == client.user or message.author.bot:
        return

    # 보낸 사람의 ID가 backgwa인 경우 기록
    if (f"{message.author}" == "backgwa"):
        # 현재 채팅과 이전 채팅 연관성 계산
        now = db.gen_now()[0]
        diff = difference(recent_time, now)

        # 데이터셋에 데이터 등록
        db.register(path, [
            now.strftime("%Y%m%d"), now.strftime("%H%M%S"),
            f"{message.author}", f"{message.content}",
            diff])

        recent_time = now


# 연관성 계산
def difference(dt1, dt2):
    diff = abs(dt1.timestamp() - dt2.timestamp())   # 시간 값 차이 계산
    normal = 1.0 - diff / 600.0                     # 10분을 기준으로 0~1 범위 설정
    return round(normal, 5)                         # 소숫점 5자리까지만, 반환


# 봇 작동 시작
client.run(TOKEN)