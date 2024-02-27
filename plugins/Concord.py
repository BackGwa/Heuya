from ast import literal_eval

from discord import Embed, Color

from .Fjson import Fjson
from .Flog import Flog


class ConcordMessage:
    def __init__(self, verbose: bool = False):
        """
        # Concord Message Plug-in
        discord.py의 메시지와 관련 된 편의기능을 추가하는 플러그인 입니다.
        """
        self.log = Flog(verbose=verbose)

    def blur(self, text: str, range: int = 0, blur_str: str = "*") -> str:
        """
        # 텍스트 모자이크
        인자로 입력받은 텍스트를 모자이크하여, 반환합니다.
        표시할 문자의 갯수보다 입력 된 텍스트의 길이가 작으면,
        모든 텍스트를 모자이크하여, 반환합니다.

        Args:
            text (str): 모자이크할 텍스트를 설정합니다.
            range (int): 표시할 문자의 갯수를 설정합니다. 기본값은 0 입니다.
            blur_str (str): 모자이크 시 치환 할 문자를 설정합니다. 기본값은 * 입니다.

        Exception:
            텍스트 모자이크를 처리하던 중 오류가 발생하면, 모든 텍스트를 모자이크하여, 반환합니다.

        Returns:
            text (str): 모자이크 처리가 된 텍스트를 반환합니다.
        """
        try:
            if len(text) <= range or range == 0:
                return blur_str * len(text)
            else:
                return text[:range] + blur_str * (len(text) - range)
        except Exception as e:
            self.log.error("텍스트 모자이크를 처리하던 중 오류가 발생했습니다!", e)
            return blur_str * len(text)

    def spoiler(self, text: str) -> str:
        """
        # 텍스트 스포일러
        인자로 입력받은 텍스트를 스포일러 처리하여, 반환합니다.

        Args:
            text (str): 스포일러 처리를 할 텍스트를 설정합니다.

        Returns:
            text (str): 스포일러 된 텍스트를 반환합니다.
        """
        return f"||{text}||"

    def is_command(self, text: str, prefix: list = ["/", "!"]) -> bool:
        """
        # 명령어 확인
        인자로 입력받은 텍스트가 명령어라면, True를 반환하고,
        명령어가 아니라면, False를 반환합니다.

        Exception:
            명령어 여부 확인 중 오류가 발생한다면, False를 반환합니다.

        Args:
            text (str): 명령어 여부를 확인할 텍스트를 설정합니다.
            prefix (list): 명령어 접두사를 설정합니다. 기본값은 ["/", "!"] 입니다.
        """
        try:
            if text:
                return text[0] in prefix
        except Exception as e:
            self.log.error("명령어 여부를 확인하던 중 오류가 발생했습니다!", e)
            return False

    def which(self, text: str) -> str:
        """
        # 텍스트 형식 확인
        인자로 입력받은 텍스트가 어떤 형식인지 분석하여, 반환합니다.
        general, code, notice 총 3가지 타입으로 구분합니다.

        Args:
            text (str): 형식을 분석 할 텍스트를 설정합니다.

        Exception:
            텍스트의 형식을 분석하던 중 오류가 발생한다면, general을 반환합니다.

        Returns:
            text (str): 텍스트가 어떤 형식인지, 반환합니다.
        """
        try:
            if text[0] == "#":
                return "notice"
            elif "```" in text:
                return "code"
            else:
                return "general"
        except Exception as e:
            self.log.error("텍스트의 형식을 분석하던 중 오류가 발생했습니다!", e)
            return "general"


class ConcordEmbed:
    def __init__(self, verbose: bool = False):
        """
        # Concord Embed Plug-in
        discord.py의 임베드와 관련 된 편의기능을 추가하는 플러그인 입니다.
        """
        self.json = Fjson(verbose=verbose)
        self.log = Flog(verbose=verbose)

    def __error__(self, content: str):
        """
        # 오류 임베드
        오류 임베드를 반환합니다.

        Args:
            content (str): 오류 내용을 설정합니다.

        Returns:
            embed (Embed): 오류 임베드를 반환합니다.
        """
        embed = Embed(
            title="오류가 발생하였습니다.",
            description=str(content), 
            color=0xff5151)
        return embed

    def load(self, path: str, pre_value: dict = {}):
        """
        # 임베드 파일 불러오기
        JSON 형식의 임베드 사전 설정 파일의 경로를 인자에 입력하여,
        discord.py 임베드로 반환합니다.

        Args:
            path (str): 임베드 사전 설정 파일의 경로를 설정합니다.
            pre_value (dict): 임베드 사전 설정 파일에 대입할 값을 설정합니다. 기본값은 비어있습니다.

        Raises:
            ValueError: JSON 데이터에 오류가 발생한다면, 오류 임베드를 반환합니다.

        Exception:
            임베드를 불러오는 과정에서 오류가 발생했을때, 오류 임베드를 반환합니다.

        Returns:
            embed (Embed): 불러온 discord.py 형식의 임베드를 반환합니다.
        """
        try:
            embed_json = self.json.read(path)

            if not (self.json.valid(embed_json, "config")):
                raise ValueError("임베드 설정이 존재하지 않습니다.")
            elif not (self.json.valid(embed_json, "embed")):
                raise ValueError("임베드가 존재하지 않습니다.")

            config = embed_json["config"]
            data = embed_json["embed"]

            name = self.json.get(config, "name")
            color = self.json.get(config, "color")
            header = self.json.get(data, "header")
            author = self.json.get(data, "author")
            content = self.json.get(data, "content")
            footer = self.json.get(data, "footer")

            embed = Embed(
                title=self.json.get(header, "title"),
                description=self.json.get(header, "description"),
                url=self.json.get(header, "url"),
                color=Color.from_rgb(
                    color[0] if color[0] != "" else 255,
                    color[1] if color[1] != "" else 255,
                    color[2] if color[2] != "" else 255
                )
            )

            embed.set_author(
                name=self.json.get(author, "name"),
                url=self.json.get(author, "url"),
                icon_url=self.json.get(author, "icon")
            )

            embed.set_thumbnail(
                url=self.json.get(content, "image")
            )

            if self.json.valid(content, "field"):
                for item in content["field"]:
                    embed.add_field(
                        name=item["name"],
                        value=item["value"],
                        inline=item["inline"]
                    )

            embed.set_footer(
                text=self.json.get(footer, "text")
            )

            if pre_value:
                raw_embed = str(embed.to_dict())
                for key, value in pre_value.items():
                    raw_embed = raw_embed.replace(f"<{key}>", str(value))
                return embed.from_dict(literal_eval(raw_embed))

            return embed

        except ValueError as e:
            self.log.warn("임베드 JSON 데이터에 오류가 있습니다!", e)
            return self.__error__(e)
        except Exception as e:
            self.log.error("임베드를 불러오는 과정에서 오류가 발생했습니다.", e)
            return self.__error__(e)