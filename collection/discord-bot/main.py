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
USER        = config["bot_setting"]["user"]

# DoDB 설정 적용
NAME        = config["dodb_setting"]["name"]
PATH        = config["dodb_setting"]["path"]
DATA_FORMAT = config["dodb_setting"]["format"]

# 기본 상수 설정
CHAT_RECENT = config["data_setting"]["recent"]
CHAT_OLD    = config["data_setting"]["old"]
P_PENALTY   = config["data_setting"]["positive_penalty"]
N_PENALTY   = config["data_setting"]["negative_penalty"]
P_WORD      = config["wordlist"]["positive_word"]
N_WORD      = config["wordlist"]["negative_word"]

# 기본값 설정
recent_time = None
recent_feel = None
path        = None

# 클래스 초기화
db = Dodb(NAME, PATH, DATA_FORMAT)
client = discord.Client(intents=intents)


# 봇 작동 시작 시
@client.event
async def on_ready():
    global recent_time, recent_feel, path
    recent_time = db.gen_now()[0]
    recent_feel = 0
    db.log(f"KILOGWA", "Ready!")
    path = db.file_register()

    activity = discord.Game("데이터 수집")
    await client.change_presence(status=discord.Status.online, activity=activity)


# 메세지 입력 감지 시
@client.event
async def on_message(message):
    global recent_time

    # 봇 또는, 자기 자신에 관한 대화는 무시
    if message.author == client.user or message.author.bot:
        return

    # 보낸 사람의 ID가 backgwa인 경우 기록
    if (f"{message.author}" == USER):
        author  = f"{message.author}"           # 메세지 보낸 사람 저장
        content = f"{message.content}"          # 메세지 내용 저장

        db.log(f"===================\n새로운 메세지\n===================", f"{content}")

        if message_type(content) != "normal":      # 메세지 타입이 일반이 아닌 경우 무시
            return

        # 현재 채팅과 이전 채팅 연관성 계산
        now = db.gen_now()[0]
        diff = difference(recent_time, now)

        # 현재 채팅의 감정 계산
        feel = feeling(diff, content)
        feel_data = {
            "p" : "positive",
            "n" : "negative",
            "x" : "neutrality"
        }

        # 데이터셋에 데이터 등록
        db.register(path, [
            now.strftime("%Y%m%d"), now.strftime("%H%M%S"),
            author, content,
            feel_data[feel], diff
        ])

        # 이전 채팅 시간을 현재 시간으로 설정
        recent_time = now


# 감정 요소 계산
def feeling(diff, text):
    global recent_feel

    feel_value = detect_feel(text)                              # 현재 문장 내 감정 감지
    feel_score = 0                                              # 함수 내 감정 점수를 0으로 초기화

    if recent_feel != 0:                                        # 최근 감정 점수가 존재한다면,
        db.log(f"최근 감정 점수", f"{recent_feel}")
        feel_score = recent_feel                                # 현재 점수를 최근 감정 점수로 설정하고

        if diff >= CHAT_RECENT:                                 # 비교적 최근의 대화라면,
            if feel_value[0] == "p":                            # 감정 점수가 긍정을 가르키고 있을 때 감정 점수를 긍정 패널티 점수로 곱한 후 반영
                feel_score += int(feel_value[1:]) * P_PENALTY 
            elif feel_value[0] == "n":                          # 감정 점수가 부정을 가르키고 있을 때 감정 점수를 부정 패널티 점수로 곱한 후 반영
                feel_score -= int(feel_value[1:]) * N_PENALTY

            recent_feel = feel_score                            # 최근 감정 점수를 현재 감정 점수로 설정

        elif recent_feel != 0 and diff >= CHAT_OLD:             # 비교적 경과가 지난 채팅이라면,
            if sort_feel(recent_feel) == "p":                   # 감정 점수 긍정을 그대로 반영
                feel_score += int(feel_value[1:])   
            elif sort_feel(recent_feel) == "n":                 # 감정 점수 부정을 그대로 반영
                feel_score -= int(feel_value[1:])

            recent_feel = feel_score                            # 최근 감정 점수를 현재 감정 점수로 설정

        elif recent_feel != 0 and diff < CHAT_OLD:              # 연관성이 없다고 판단되는 채팅이라면,
            if sort_feel(recent_feel) == "p":                   # 감정 점수가 긍정을 가르키고 있을 때 감정 점수를 긍정 패널티 점수로 나눈 후 반영
                feel_score += int(feel_value[1:]) / P_PENALTY   
            elif sort_feel(recent_feel) == "n":                 # 감정 점수가 부정을 가르키고 있을 때 감정 점수를 부정 패널티 점수로 나눈 후 반영
                feel_score -= int(feel_value[1:]) / N_PENALTY
            
            recent_feel = 0                                     # 최근 감정 점수를 0으로 초기화

    else:                                                       # 최근 감정 점수가 존재하지 않는다면,
        if feel_value[0] == "p":                                # 감정 상태가 긍정이라면, 현재 (50 + 감정 점수 * 긍정 패널티)로 반영
            feel_score = 50 + int(feel_value[1:]) * P_PENALTY
        elif feel_value[0] == "n":                              # 감정 상태가 부정이라면, 현재 (50 - 감정 점수 * 부정 패널티)로 반영
            feel_score = 50 - int(feel_value[1:]) * N_PENALTY
        elif feel_value[0] == "x":                              # 감정 상태가 중립이라면, 50으로 반영
            feel_score = 50
        
        recent_feel = feel_score                                # 최근 감정 점수를 현재 감정 점수로 설정
    
    db.log(f"현재 감정 점수", feel_score)
    return sort_feel(feel_score)                                # 점수에 따른 감정 구분 후 반환


# 문장의 감정 상태 구분
def detect_feel(text):
    score = 0                                               # 0점으로 평가 시작
    p_count = 0                                             # 긍정 횟수 카운트
    n_count = 0                                             # 부정 횟수 카운트

    text = text.replace(" ", "")                            # 텍스트의 공백 제거
    text_len = len(text)                                    # 텍스트 길이 계산

    if text_len > 200:                                      # 한 메세지가 200자를 초과하면, 점수 감점 (10)
        score -= 10
        n_count += 1
        db.log(f"글자 수 초과", f"{text_len}")
    elif text_len > 100:                                    # 한 메세지가 100자를 초과하면, 점수 감점 (5)
        score -= 5
        n_count += 1
        db.log(f"글자 수 초과", f"{text_len}")
    elif text_len > 50:                                     # 한 메세지가 50자를 초과하면, 점수 감점 (1)
        score -= 1
        n_count += 1
        db.log(f"글자 수 초과", f"{text_len}")

    for i in P_WORD:                                        # 긍정 단어가 포함되어있고 유효하다면, 점수 증가 (6)
        if i in text and text_len > 4:
            score += 5
            db.log(f"긍정 단어 포함", f"{text} <= ({i})")
            p_count += 1
        elif i in text:                                     # 길이가 유효하지않다면, 점수 증가 (3)
            score += 2
            db.log(f"긍정 단어 포함", f"{text} <= ({i})")
            p_count += 1

    for i in N_WORD:                                        # 부정 단어가 포함되어있고 유효하다면, 점수 감점 (6)
        if i in text and text_len > 4:
            score -= 6
            db.log(f"부정 단어 포함", f"{text} <= ({i})")
            n_count += 1
        elif i in text:                                     # 길이가 유효하지않다면, 점수 감점 (3)
            score -= 3
            db.log(f"부정 단어 포함", f"{text} <= ({i})")
            n_count += 1

    db.log(f"긍정 반영 카운터", f"{p_count}")
    db.log(f"부정 반영 카운터", f"{n_count}")

    if p_count == n_count:                                  # 긍정 / 부정 비중 계산 후 결과에 반영
        db.log(f"반영 된 감정 수치", f"neutrality : {score}")
        return f"x{abs(score)}"
    elif p_count > n_count:
        db.log(f"반영 된 감정 수치", f"positive : {score}")
        return f"p{abs(score)}"
    else:
        db.log(f"반영 된 감정 수치 ", f"negative : {score}")
        return f"n{abs(score)}"


# 메세지 형식 구분
def message_type(text):
    if "```" in text:
        db.log(f"메세지 형식", "code")
        return "code"
    elif "#" in text or "##" in text:
        db.log(f"메세지 형식", "notice")
        return "notice"
    else:
        db.log(f"메세지 형식", "normal")
        return "normal"


# 현재 감정 점수에 따른 긍정 부정 구분
def sort_feel(score):
    if score >= 60:
        return "p"
    elif score <= 40:
        return "n"
    else:
        return "x"


# 연관성 계산
def difference(dt1, dt2):
    diff = abs(dt1.timestamp() - dt2.timestamp())   # 시간 값 차이 계산
    db.log(f"이전 메세지와 차이 값", diff)
    normal = 1.0 - diff / 180.0                     # 3분을 기준으로 0~1 범위 설정
    db.log(f"메세지 연관성 값", normal)
    return round(normal, 5)                         # 소숫점 5자리까지만, 반환


# 봇 작동 시작
client.run(TOKEN)