from discord import Interaction
from discord.app_commands import command
from discord.ext.commands import Cog, Bot

from plugins import Flog
from plugins import Ftime
from plugins import Fmath
from plugins import Fcsv
from plugins import Fjson
from plugins import ConcordMessage, ConcordEmbed


log = Flog(verbose=True)
time = Ftime(verbose=True)
math = Fmath(verbose=True)
json = Fjson(verbose=True)
msg = ConcordMessage(verbose=True)
embed = ConcordEmbed(verbose=True)

WORDLIST    = json.read("res/kilogwa/config/wordlist.json")
CONFIG_JSON = json.read("res/kilogwa/config/config.json")
METADATA    = CONFIG_JSON["metadata"]
CONFIG      = CONFIG_JSON["config"]

csv = Fcsv(
    name=METADATA["name"],
    path=CONFIG["savepath"],
    structure=CONFIG["structure"],
    verbose=True
)

total_used = {"positive" : 0, "neutrality" : 0, "negative" : 0}
recent_feel = 0
recent_change = 0


def analyze_text(content: str) -> float:
    """
    # 텍스트 분석
    인자에 입력 된 텍스트와 사전에 설정한 데이터와 비교하여, 
    긍정, 중립, 부정 단어 사용 횟수를 카운트하고, 점수를 매겨 반환합니다.

    Args:
        content (str): 분석과 점수를 매길 텍스트를 설정합니다.

    Returns:
        eval_score (float): 텍스트에 매겨진 점수를 반환합니다.
    """
    global total_used, recent_change

    count = {"positive" : 0, "negative" : 0}
    length = len(content.replace(",", ""))
    valid = "max" if length > CONFIG["valid_length"] else "min"

    for word in WORDLIST["positive"]:
        if word in content:
            count["positive"] += 1

    for word in WORDLIST["negative"]:
        if word in content:
            count["negative"] += 1

    eval_score = {
        "positive" : CONFIG["score"]["positive"][valid] * count["positive"],
        "negative" : -(CONFIG["score"]["negative"][valid] * count["negative"])
    }

    total_used["positive"] += count["positive"]
    total_used["negative"] += count["negative"]
    recent_change = eval_score['positive'] - eval_score['negative']

    if count["positive"] != count["negative"]:
        if count["positive"] > count["negative"]:
            return eval_score['positive']
        else:
            return eval_score['negative']
    else:
        total_used["neutrality"] += 1
        return eval_score['positive'] - eval_score['negative']


def feeling(content: str, association: float) -> int:
    """
    # 감정 점수 평가
    인자에 입력 된 콘텐츠와 연관성을 이용하여, 감정 점수를 평가합니다.

    Args:
        content (str): 감정 점수를 평가할 문장를 설정합니다.
        association (float): 감정 점수를 평가할 연관성 값을 설정합니다.

    Returns:
        eval (int): 평가 된 감정 점수를 반환합니다.
    """
    global recent_feel

    score = analyze_text(content)
    score_stat = "positive" if score > 0 else "negative"
    eval_score = 0

    if recent_feel:
        eval_score = recent_feel
        if association >= CONFIG["valid_percent"]:
            eval_score += score * CONFIG["penalty"][score_stat]
        elif association >= CONFIG["old_percent"]:
            eval_score += score
        elif association < CONFIG["old_percent"]:
            eval_score = 50 + score * (CONFIG["penalty"][score_stat] / 2)
    else:
        eval_score = 50 + score * CONFIG["penalty"][score_stat]

    recent_feel = eval_score
    return eval_score


def sort_feel(score: int) -> str:
    """
    # 감정 상태 구분
    인자 입력 된 감정 점수를 바탕으로 감정 상태를 구분합니다.

    Args:
        score (int): 구분 할 감정 점수를 설정합니다.

    Returns:
        feel (str): 구분 한 감정 상태를 반환합니다.
    """
    if score >= 60:
        return "positive"
    elif score <= 40:
        return "negative"
    else:
        return "neutrality"


class Kliogwa(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.recent_message = [time.now(), ""]

    @Cog.listener()
    async def on_ready(self):
        log.write("모듈이 활성화되었습니다!", f"{METADATA['name']} - (버전 정보 : {METADATA['version']})")

    @Cog.listener()
    async def on_message(self, message):
        author = message.author
        content = message.content

        if msg.is_command(content) and msg.which != "general":
            return

        if str(author) in CONFIG["username"]:
            now = time.now()
            asso = time.association(
                valid=CONFIG["valid_time"],
                before=self.recent_message[0],
                after=now
            )
            feel = feeling(content=content, association=asso)
            csv.write([
                now.strftime("%Y%m%d"), now.strftime("%H%M%S"),
                author, content.replace(",", ""),
                sort_feel(feel), math.to_percent(asso)
            ])
            self.recent_message = [now, content]

    @command(name="logs", description="천과 - 최근 로그를 출력합니다.")
    async def logs(self, ctx: Interaction):
        recent_data = csv.read_recent()
        data = recent_data

        if data == []:
            embed_data = embed.load(path="res/kilogwa/embed/nonedata_preset.json")
        else:
            embed_data = embed.load(
                path="res/kilogwa/embed/logs_preset.json",
                pre_value={
                    "write_time" : time.format(
                        timedata=f"{data[0]}{data[1]}",
                        format="%Y년 %m월 %d일 ( %H시 %M분 )",
                        raw=True
                    ),
                    "recent_message" : msg.spoiler(
                        msg.blur(
                            text=data[3],
                            blur_str="#"
                        )
                    ),
                    "association" : f"{data[5]}%",
                    "feel_value" : recent_feel,
                    "feel_name" : {
                        "positive" : "긍정",
                        "neutrality" : "중립",
                        "negative" : "부정"
                    }[sort_feel(recent_feel)],
                    "change_value" : recent_change,
                    "positive" : total_used["positive"],
                    "neutrality" : total_used["neutrality"],
                    "negative" : total_used["negative"],
                    "data_length" : csv.read()["length"] - 1
                }
            )

        await ctx.response.send_message(embed=embed_data)

    @command(name="asso", description="천과 - 이전 대화에 대한, 현재까지의 연관성을 수치로 보여줍니다.")
    async def asso(self, ctx: Interaction):
        now = time.now()
        asso = time.association(
            valid=CONFIG["valid_time"],
            before=self.recent_message[0],
            after=now
        )

        embed_data = embed.load(
            path="res/kilogwa/embed/asso_preset.json",
            pre_value={
                "recent_message" : time.format(
                    timedata=self.recent_message[0],
                    format="%Y년 %m월 %d일 ( %H시 %M분 )"
                ),
                "association" : math.to_percent(
                    value=asso,
                    symbol=True
                ),
                "valid_percent" : math.to_percent(
                    value=CONFIG["valid_percent"],
                    symbol=True
                )
            }
        )
        await ctx.response.send_message(embed=embed_data)


async def setup(bot: Bot):
    await bot.add_cog(Kliogwa(bot))