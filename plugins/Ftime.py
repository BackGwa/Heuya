from datetime import datetime

from .Flog import Flog


class Ftime:
    def __init__(self, verbose: bool = False):
        """
        # F-Time Plug-in
        날짜 및 시간을 관리할 수 있는 플러그인 입니다.

        Args:
            verbose (bool): 콘솔에 로그를 표시할 지 설정합니다. 기본값은 False 입니다.
        """
        self.log = Flog(verbose=verbose)

    def now(self, raw: bool = False, raw_format: str = "%Y%m%d%H%M%S"):
        """
        # 현재 시각 반환
        현재 시각을 반환합니다.

        Args:
            raw (bool): 현재 시각을 RAW 형식으로 반환할 지 설정합니다.
            raw_format (str): RAW 데이터의 형식을 설정합니다. 기본값은 '%Y%m%d%H%M%S' 입니다.

        Exception:
            현재 시각을 반환하는 중 오류가 발생한다면, 빈 데이터를 반환합니다.

        Returns:
            now (datetime, str): 현재 시각을 반환합니다.
        """
        now = datetime.now()
        try:
            return now if not raw else now.strftime(raw_format)
        except Exception as e:
            self.log.warn("현재 시각을 반환하는데 오류가 발생했습니다.", e)
            return now if not raw else ""

    def format(self, timedata, format: str = "%Y년 %m월 %d일 %H시 %M분 %S초", raw: bool = False, raw_format: str = "%Y%m%d%H%M%S") -> str:
        """
        # 포맷 형식 출력
        인자에 입력 된 날짜를 포맷 형식으로 반환합니다.
        
        Args:
            timedata (datetime, str): 포맷팅할 날짜를 입력합니다. RAW가 True이라면, 문자열로 입력합니다.
            format (str): 출력 할 포맷의 형식입니다. 기본값은 '%Y년 %m월 %d일 %H시 %M분 %S초'입니다.
            raw (bool): timedata 인자에 입력한 데이터가 RAW 형식인지, 아닌지 나타냅니다. 기본값은 False 입니다.
            raw_format (str): RAW 데이터의 형식을 설정합니다. 기본값은 '%Y%m%d%H%M%S' 입니다.

        Exception:
            변환 중 오류가 발생한다면, 빈 데이터를 반환합니다.

        Returns:
            strftime (str): 포맷 형식으로 반환 된 날짜입니다.
        """
        try:
            if raw:
                dt = datetime.strptime(timedata, raw_format)
                data = dt.strftime(format)
            else:
                data = timedata.strftime(format)
        except Exception as e:
            self.log.warn("포맷 형식으로 변환하는데 오류가 발생했습니다.", e)
            data = ""

        return data

    def association(self, valid: float, before: datetime, after: datetime) -> float:
        """
        # 시간대 차이 계산
        인자에 입력 된 유효 시간 값을 기준으로 2개의 시간 데이터를 비교하여,
        차이를 계산하고 두 시간대의 연관이 얼마나 있는지 백분율(실수)로 반환합니다.

        Args:
            valid (float): 유효 시간 값으로 해당 시간을 기준으로 백분율을 나눕니다.
            before (datetime): 차이를 비교하기 위한, 이전 시간대 입니다.
            after (datetime): 이전 시간대와 차이를 비교할 시간대 입니다.
        
        Raises:
            ValueError: 유효 시간 값이 0보다 작다면, 0.0을 반환합니다.
            ValueError: 이전 시간대가 비교할 시간대보다 크다면, 0.0을 반환합니다.

        Exception:
            시간대 차이 계산 중 오류가 발생한다면, 0.0을 반환합니다.

        Returns:
            percent (float): 두 시간대의 차이에 대한, 백분율을 실수로 반환합니다.
        """
        try:
            if valid <= 0:
                raise ValueError("유효 시간 값이 0보다 커야합니다!")

            if before.timestamp() > after.timestamp():
                raise ValueError("이전 시간대가 비교할 시간대보다 큽니다!")
            
            diff = after.timestamp() - before.timestamp()
            return 1.0 - diff / valid
        except ValueError as e:
            self.log.warn("입력 된 값에 오류가 있습니다!", e)
            return 0.0
        except Exception as e:
            self.log.error("시간대 차이 계산 중 오류가 발생했습니다!", e)
            return 0.0