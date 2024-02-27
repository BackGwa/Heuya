from .Flog import Flog


class Fmath:
    def __init__(self, verbose: bool = False):
        """
        # F-Math Plug-in
        수학적 계산을 쉽게 도와주는 플러그인 입니다.

        Args:
            verbose (bool): 콘솔에 로그를 표시할 지 설정합니다. 기본값은 False 입니다.
        """
        self.log = Flog(verbose=verbose)

    def to_percent(self, value: float, decimal: int = 0, symbol: bool = False):
        """
        # 백분율 변환
        인자에 입력 된 실수 수치를 백분율로 변환하여, 반환합니다.
        소숫점 자릿수 표기와 기호 표시를 설정할 수도 있습니다.

        Args:
            value (float): 백분율로 변환할 실수로 이루어진 수치입니다. 0.0 ~ 1.0의 값을 가집니다.
            decimal (int): 표시 할 소숫점 자리수를 설정합니다. 기본값은 0 입니다.
            symbol (bool): 퍼센트 기호를 출력 여부를 설정합니다. 기본값은 False 입니다.

        Exception:
            백분율 변환 과정에서 오류가 발생한다면, 0.0을 반환합니다.

        Returns:
            value (float, str): 백분율로 변환 된 값을 반환합니다.
        """
        try:
            value = round(value * 100, decimal)
            return f"{value}%" if symbol else value
        except Exception as e:
            self.log.error("백분율 변환 과정에서 오류가 발생했습니다!", e)
            return 0.0