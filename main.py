from asyncio import run
from os import listdir

from discord import Intents, Game, Status
from discord.ext.commands import Bot, when_mentioned

from plugins import Flog
from plugins import Fjson


log = Flog(verbose=True)
json = Fjson(verbose=True)
TOKEN = json.read("res/default/config/secret.json", "token")

intents = Intents.default()
intents.message_content = True

bot = Bot(when_mentioned, intents=intents)


@bot.event
async def on_ready():
    activity = Game("테스트")
    await bot.change_presence(status=Status.online, activity=activity)
    await bot.tree.sync()


async def load_module():
    try:
        for filename in listdir('module'):
            if not filename.endswith('.py'):
                continue
            log.write("모듈을 성공적으로 불러왔습니다!", filename[:-3])
            await bot.load_extension(f'module.{filename[:-3]}')
    except Exception as e:
        log.error("모듈을 가져오는데 실패하였습니다.", e)


if __name__ == '__main__':
    run(load_module())
    bot.run(TOKEN)