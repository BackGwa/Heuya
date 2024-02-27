from os import listdir

from discord import Interaction
from discord.app_commands import command
from discord.ext.commands import Cog, Bot

from plugins import Flog
from plugins import Fjson
from plugins import ConcordEmbed


log = Flog(verbose=True)
json = Fjson(verbose=True)
embed = ConcordEmbed(verbose=True)

CONFIG_JSON = json.read("res/default/config/config.json")
METADATA    = CONFIG_JSON["metadata"]
CONFIG      = CONFIG_JSON["config"]


class Default(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        log.write("모듈이 활성화되었습니다!", f"{METADATA['name']} - (버전 정보 : {METADATA['version']})")

    @command(name="info", description="흐야 - 봇의 정보를 출력합니다.")
    async def info(self, ctx: Interaction):
        modules = ""
        for filename in listdir('module'):
            if not filename.endswith('.py'):
                continue
            modules += f"`{filename[:-3]}` "
        embed_data = embed.load(
            path="res/default/embed/info_preset.json",
            pre_value={
                "ping" : f"{round(self.bot.latency, 1)}ms",
                "version" : METADATA['version'],
                "modules" : modules
            }
        )
        await ctx.response.send_message(embed=embed_data)


async def setup(bot: Bot):
    await bot.add_cog(Default(bot))