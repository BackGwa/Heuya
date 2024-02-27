import csv

from .Ftime import Ftime
from .Flog import Flog


class Fcsv:
    def __init__(self, name: str, path: str, structure: list, verbose: bool = False) -> str:
        """
        # F-csv Plug-in
        csv 데이터셋의 데이터를 관리할 수 있는 플러그인 입니다.

        Args:
            name (str): 데이터셋의 이름을 설정합니다.
            path (str): 데이터셋 폴더의 경로를 설정합니다.
            structure (str): 데이터셋의 구조를 설정합니다.
            verbose (bool): 콘솔에 로그를 표시할 지 설정합니다. 기본값은 False 입니다.

        Exception:
            데이터셋 생성 중 오류가 발생한다면, 데이터셋을 생성을 하지않습니다.
        """
        self.time = Ftime(verbose=verbose)
        self.log = Flog(verbose=verbose)
        self.path = f"{path}/{name}_{self.time.now(raw=True, raw_format='%Y%m%d_%H%M%S')}.csv"
        self.structure = structure

        try:
            file = open(self.path, encoding="UTF-8", mode="w")
            for i in range(len(self.structure)):
                file.write(self.structure[i] + "," if ((len(self.structure) - 1) != i) else self.structure[i])
            file.close()
        except Exception as e:
            self.log.error("데이터셋을 생성하던 중 오류가 발생했습니다!", e)

    def write(self, data: list):
        """
        # 데이터 쓰기
        인자에 입력 된 데이터를 데이터셋에 추가합니다.

        Args:
            data (list): 추가할 데이터를 설정합니다.

        Raises:
            ValueError: 데이터가 데이터 형식에 일정하지 않으면, 추가하지 않습니다.

        Exception:
            데이터셋에 데이터를 추가하던 중 오류가 발생한다면, 데이터를 추가하지 않습니다.
        """

        try:
            if len(self.structure) != len(data):
                raise ValueError(f"데이터가 데이터셋에 비하여, {len(self.structure) - len(data)}개 차이납니다.")

            file = open(self.path, encoding="UTF-8", mode="a")
            file.write("\n")
            for i in range(len(self.structure)):
                file.write(str(data[i]) + "," if ((len(self.structure) - 1) != i) else str(data[i]))
            file.close()
        except ValueError as e:
            self.log.warn("데이터가 데이터 형식에 일치하지 않습니다!", e)
        except Exception as e:
            self.log.error("데이터셋에 데이터를 추가하던 중 오류가 발생했습니다!", e)

    def read(self) -> list:
        """
        # 데이터셋 읽기
        데이터셋에 기록 된 모든 데이터를 반환합니다.

        Exception:
            데이터셋을 가져오는데 실패하였다면, 빈 데이터를 반환합니다.

        Returns:
            data (list): 데이터셋에 기록 된 모든 데이터를 반환합니다.
        """
        try:
            file = open(self.path, encoding="UTF-8", mode="r")
            dataset = csv.reader(file)
            data = [i for i in dataset]
            file.close()
        except Exception as e:
            self.log.error("데이터셋을 가져오는데 오류가 발생했습니다!", e)
            data = [""]

        return {"data" : data, "length" : len(data)}

    def read_recent(self) -> list:
        """
        # 최근 데이터 가져오기
        데이터셋에 기록 된 마지막 데이터를 반환합니다.

        Exception:
            데이터셋을 가져오는데 실패하였다면, 빈 데이터를 반환합니다.

        Returns:
            data (list): 데이터셋에 기록 된 마지막 데이터를 반환합니다.
        """
        try:
            data = self.read()
            if data["length"] > 1:
                return data["data"][data["length"] - 1]
            else:
                self.log.warn("데이터셋의 마지막을 가져왔지만, 데이터가 존재하지 않습니다.", "빈 데이터를 반환합니다.")
                return []
        except Exception as e:
            self.log.error("데이터셋을 가져오는데 오류가 발생했습니다!", e)
            return [""]