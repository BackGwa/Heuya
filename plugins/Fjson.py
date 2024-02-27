import json

from .Flog import Flog


class Fjson:
    def __init__(self, verbose: bool = False):
        """
        # F-JSON Plug-in
        JSON 파일을 쉽게 관리할 수 있는 플러그인 입니다.

        Args: 
            verbose (bool): 콘솔에 로그를 표시할 지 설정합니다. 기본값은 False 입니다.
        """
        self.log = Flog(verbose=verbose)
    
    def read(self, path: str, key: str = ""):
        """
        # JSON 파일 가져오기
        인자에 입력 된 경로의 JSON 파일을 읽어 데이터를 반환합니다.
        key 인자 값이 존재한다면, 해당 key 값의 데이터를 반환합니다.

        Args:
            path (str): 데이터를 가져올 JSON 파일의 경로입니다.
            key (str): JSON 데이터에서 가져올 값에 대한 키 값 입니다. 기본값은 비어있습니다.

        Raises:
            ValueError: JSON 데이터에 오류가 있거나, 읽을 수 없다면, 빈 데이터를 반환합니다.

        Exception:
            JSON 데이터를 읽는데 오류가 발생했다면, 빈 데이터를 반환합니다.

        Returns:
            data: 가져온 JSON 데이터를 반환합니다.
        """
        try:
            with open(path, encoding="UTF-8", mode="r") as data:
                data = json.load(data)
            return data[key] if key else data
        except ValueError as e:
            self.log.warn(f"'{path}'의 JSON 데이터에 오류가 존재합니다.", e)
        except Exception as e:
            self.log.error(f"'{path}'의 JSON 데이터를 읽는데 실패하였습니다!", e)

    def valid(self, data: dict, key: str) -> bool:
        """
        # JSON 데이터 유효성 검사
        인자에 입력 된 JSON 데이터에 키 값이 존재한다면,
        True를 반환하고, 존재하지 않는다면, False를 반환합니다.

        Args:
            data (dict): 유효성 검사를 할 JSON 데이터를 설정합니다.
            key (str): 유효성 검사를 할 키 값을 설정합니다.
        
        Returns:
            valid (bool): 유효성 검사 결과를 반환합니다.
        """
        try:
            _ = data[key]
        except:
            return False
        return True

    def get(self, data: dict, key: str):
        """
        # 값 가져오기
        인자에 입력 된 키 값으로 JSON 데이터를 읽습니다.
        키 값으로 JSON 데이터를 가져오지 못했다면, 빈 값을 반환합니다.

        Args:
            data (dict): 가져올 JSON 데이터를 설정합니다.
            key (str): 가져올 데이터의 키 값을 설정합니다.

        Exception:
            JSON 데이터를 가져오는데 오류가 발생했다면, 빈 데이터를 반환합니다.

        Returns:
            data: 가져온 JSON 데이터를 반환합니다.
        """
        try:
            if self.valid(data, key):
                return data[key]
            else:
                return ""
        except Exception as e:
            self.log.error("데이터를 읽는 중 오류가 발생했습니다!", e)
            return ""