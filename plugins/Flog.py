class Flog:
    def __init__(self, verbose: bool = False):
        """
        # F-Log Plug-in
        로그를 기록하는 플러그인 입니다.

        Args:
            verbose (bool): 콘솔에 로그를 표시할 지 설정합니다. 기본값은 False 입니다.
        """
        self.BOLD    = "\033[1m"
        self.RED     = "\033[31m"
        self.GREEN   = "\033[32m"
        self.YELLOW  = "\033[33m"
        self.CYAN    = "\033[36m"
        self.RESET   = "\033[0m" 
        
        self.verbose = verbose

    def __title__(self, text: str):
        """
        # 제목 출력
        로그의 제목을 출력합니다.

        Args:
            text (str): 로그의 제목을 입력합니다.
        """
        print(f"\n{self.BOLD}{text}{self.RESET}")

    def __content__(self, text: str):
        """
        # 콘텐츠 출력
        로그의 콘텐츠를 출력합니다.

        Args:
            text (str): 로그의 콘텐츠를 입력합니다.
        """
        print(f"> {text}")

    def __write__(self, title: str, content: str):
        """
        # 로그 출력
        verbose가 True일 때, 인자에 입력 된 제목과 콘텐츠를 기반으로 로그를 출력합니다.

        Args:
            title (str): 로그의 제목을 입력합니다.
            content (str): 로그의 콘텐츠를 입력합니다.
        """
        if self.verbose:
            self.__title__(title)
            self.__content__(content)

    def write(self, title: str, content: str):
        """
        # 로그 출력
        verbose가 True일 때, 인자에 입력 된 제목과 콘텐츠를 기반으로 일반 로그를 출력합니다.

        Args:
            title (str): 로그의 제목을 입력합니다.
            content (str): 로그의 콘텐츠를 입력합니다.
        """
        self.__write__(self.CYAN + title + self.RESET, content)

    def warn(self, title: str, content: str):
        """
        # 경고 출력
        verbose가 True일 때, 인자에 입력 된 제목과 콘텐츠를 기반으로 경고 로그를 출력합니다.

        Args:
            title (str): 로그의 제목을 입력합니다.
            content (str): 로그의 콘텐츠를 입력합니다.
        """
        self.__write__(self.YELLOW + title + self.RESET, content)

    def error(self, title: str, content: str):
        """
        # 에러 출력
        verbose가 True일 때, 인자에 입력 된 제목과 콘텐츠를 기반으로 에러 로그를 출력합니다.

        Args:
            title (str): 로그의 제목을 입력합니다.
            content (str): 로그의 콘텐츠를 입력합니다.
        """
        self.__write__(self.RED + title + self.RESET, content)